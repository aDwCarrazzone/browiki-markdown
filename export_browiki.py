#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_browiki.py — Espelha a bROWiki (https://browiki.org) para Markdown + imagens + dump XML.

Objetivos:
  * Backup distribuido (Git/GitHub) a prova da queda do site.
  * Markdown limpo, legivel por IA (HTML renderizado -> Markdown, templates expandidos).
  * Sincronizacao incremental: re-roda e so rebaixa o que mudou (via state.json).

Subcomandos:
  python export_browiki.py markdown      # renderiza Markdown + baixa imagens (incremental)
  python export_browiki.py markdown --full   # ignora o estado, refaz tudo
  python export_browiki.py dump          # dump XML completo de TODOS os namespaces
  python export_browiki.py all           # markdown + dump

Opcoes uteis:
  --limit N        processa no maximo N paginas (para testes)
  --no-images      nao baixa imagens
  --out DIR        diretorio de saida (default: diretorio do script)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from urllib.parse import quote, unquote

import requests
from bs4 import BeautifulSoup, NavigableString
from markdownify import markdownify as md_convert

API = "https://browiki.org/api.php"
WIKI = "https://browiki.org/wiki/"
BASE = "https://browiki.org"
UA = "browiki-markdown/1.0 (backup; https://github.com/aDwCarrazzone/browiki-markdown)"

# Namespaces que viram Markdown (conteudo legivel). O dump XML pega TODOS de qualquer forma.
#   0 = (principal/artigos)  12 = Ajuda  14 = Categoria
MD_NAMESPACES = [0, 12, 14]
NS_PREFIX = {12: "Ajuda", 14: "Categoria"}  # prefixo de pasta por namespace

session = requests.Session()
session.headers["User-Agent"] = UA


# --------------------------------------------------------------------------- #
# API helpers
# --------------------------------------------------------------------------- #
def api_get(params: dict, retries: int = 4) -> dict:
    params = {**params, "format": "json", "formatversion": "1"}
    last = None
    for attempt in range(retries):
        try:
            r = session.get(API, params=params, timeout=60)
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"API falhou apos {retries} tentativas: {last}")


def api_query_all(params: dict, root_key: str):
    """Itera sobre todos os resultados paginados de uma query (action=query)."""
    params = {**params, "action": "query"}
    while True:
        data = api_get(params)
        q = data.get("query", {})
        if root_key in q:
            yield from q[root_key]
        if "continue" in data:
            params.update(data["continue"])
        else:
            break


def list_pages(namespace: int):
    """Todos os titulos+pageid+revid de um namespace."""
    yield from api_query_all(
        {"list": "allpages", "apnamespace": namespace, "aplimit": "max"},
        "allpages",
    )


# --------------------------------------------------------------------------- #
# Filenames
# --------------------------------------------------------------------------- #
_ILLEGAL = re.compile(r'[<>:"\\|?*\x00-\x1f]')
# Nomes de dispositivo reservados no Windows (CON, PRN, COM1...): recebem sufixo "_".
_RESERVED = re.compile(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$', re.I)


def safe_name(title: str) -> str:
    """Converte um titulo de pagina num caminho de arquivo seguro e legivel."""
    # Subpaginas (A/B) viram subpastas; demais chars ilegais no Windows viram '-'.
    out = []
    for p in title.split("/"):
        p = _ILLEGAL.sub("-", p).strip().rstrip(".") or "_"
        if _RESERVED.match(p):
            p += "_"
        out.append(p)
    return "/".join(out)


def md_path_for(title: str, ns: int) -> str:
    name = safe_name(title)
    prefix = NS_PREFIX.get(ns)
    return f"{prefix}/{name}.md" if prefix else f"{name}.md"


# --------------------------------------------------------------------------- #
# HTML -> Markdown
# --------------------------------------------------------------------------- #
def _local_image_path(src: str) -> str | None:
    """
    Normaliza uma URL de imagem do MediaWiki para o ARQUIVO ORIGINAL e devolve
    o caminho local relativo (images/<a>/<ab>/<nome>). Ignora thumbs.
    Ex.: /images/thumb/d/db/Foo.jpg/350px-Foo.jpg -> images/d/db/Foo.jpg
         /images/c/c5/Bar.png                     -> images/c/c5/Bar.png
    """
    if not src:
        return None
    src = src.split("?")[0]
    m = re.search(r"/images/(?:thumb/)?([0-9a-f]/[0-9a-f]{2}/[^/]+)", src)
    if not m:
        return None
    return "images/" + unquote(m.group(1))


def _image_url_from_local(local: str) -> str:
    return BASE + "/" + quote(local.replace("images/", "images/", 1))


def clean_and_collect(html: str, exported_titles: set[str]):
    """
    Limpa o HTML renderizado, reescreve links/imagens e devolve (html_limpo, imagens).
    `imagens` = set de caminhos locais (images/...) a baixar.
    """
    soup = BeautifulSoup(html, "lxml")
    images: set[str] = set()

    # Remove cromo que nao agrega para leitura/IA.
    for sel in [
        ".mw-editsection", "style", "script", ".mw-empty-elt",
        ".noprint", ".mw-jump-link", "link",
    ]:
        for el in soup.select(sel):
            el.decompose()

    # Coordenadas de mapa (.navi-copy: <span>mapa</span><span>x</span><span>y</span>)
    # viram texto legivel "mapa x,y" (ex.: localizacao de NPC).
    for nav in soup.select(".navi-copy"):
        vals = [s.get_text(strip=True) for s in nav.find_all("span")]
        vals = [v for v in vals if v]
        if len(vals) >= 3:
            txt = f" ({vals[0]} {vals[1]},{vals[2]})"
        elif vals:
            txt = " (" + " ".join(vals) + ")"
        else:
            txt = ""
        nav.replace_with(NavigableString(txt))

    # Links internos -> .md relativo (se exportado) ou URL absoluta do browiki.
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/wiki/"):
            target = unquote(href[len("/wiki/"):]).split("#")[0].replace("_", " ")
            frag = href.split("#", 1)[1] if "#" in href else ""
            if target in exported_titles:
                rel = safe_name(target) + ".md" + (f"#{frag}" if frag else "")
                a["href"] = rel
            else:
                a["href"] = WIKI + quote(target.replace(" ", "_")) + (f"#{frag}" if frag else "")
        elif href.startswith("/"):
            a["href"] = BASE + href

    # Imagens -> caminho local + coleta.
    for img in soup.find_all("img"):
        local = _local_image_path(img.get("src", ""))
        if local:
            images.add(local)
            img["src"] = local
            if not img.get("alt"):
                img["alt"] = unquote(os.path.splitext(os.path.basename(local))[0]).replace("_", " ")
            for attr in ("srcset", "decoding", "loading", "width", "height", "class"):
                img.attrs.pop(attr, None)
        else:
            # imagem externa (ex.: divine-pride) — mantem absoluta
            s = img.get("src", "")
            if s.startswith("//"):
                img["src"] = "https:" + s

    return str(soup), images


def html_to_markdown(html: str) -> str:
    text = md_convert(
        html,
        heading_style="ATX",
        bullets="-",
        strip=["span"],
    )
    # Normaliza excesso de linhas em branco.
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text + "\n"


# --------------------------------------------------------------------------- #
# Markdown export
# --------------------------------------------------------------------------- #
def load_state(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"pages": {}, "images": {}}


def save_state(path: str, state: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1, sort_keys=True)


def frontmatter(title: str, ns: int, revid, categories, retrieved: str) -> str:
    def esc(s):
        return '"' + str(s).replace('"', '\\"') + '"'
    cats = "\n".join(f"  - {esc(c.replace('_', ' '))}" for c in categories)
    url = WIKI + quote(title.replace(" ", "_"))
    lines = [
        "---",
        f"title: {esc(title)}",
        f"source: {url}",
        f"namespace: {ns}",
        f"revision: {revid}",
        f"retrieved: {retrieved}",
    ]
    if categories:
        lines.append("categories:")
        lines.append(cats)
    lines.append("---\n")
    return "\n".join(lines)


def export_markdown(out: str, limit=None, do_images=True, full=False):
    state_path = os.path.join(out, "state.json")
    state = {"pages": {}, "images": {}} if full else load_state(state_path)
    retrieved = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1) enumera todas as paginas-alvo (precisamos do conjunto p/ resolver links)
    print("Enumerando paginas...", flush=True)
    pages = []  # (ns, title, pageid)
    for ns in MD_NAMESPACES:
        for p in list_pages(ns):
            pages.append((ns, p["title"], p["pageid"]))
    exported_titles = {t for _, t, _ in pages}
    print(f"  {len(pages)} paginas em {MD_NAMESPACES}", flush=True)

    if limit:
        pages = pages[:limit]

    md_dir = out
    new_images: set[str] = set()
    changed = unchanged = 0

    for i, (ns, title, pageid) in enumerate(pages, 1):
        try:
            data = api_get({
                "action": "parse", "pageid": pageid,
                "prop": "text|categories|revid",
                "disableeditsection": "true", "disabletoc": "false",
            })
            parse = data.get("parse")
            if not parse:
                print(f"  [skip] {title}: sem parse", flush=True)
                continue
            revid = parse.get("revid")
            key = str(pageid)
            if not full and state["pages"].get(key, {}).get("revid") == revid \
                    and os.path.exists(os.path.join(md_dir, md_path_for(title, ns))):
                unchanged += 1
                continue

            html = parse["text"]["*"] if isinstance(parse["text"], dict) else parse["text"]
            cats = [c["*"] if isinstance(c, dict) else c for c in parse.get("categories", [])]
            clean_html, imgs = clean_and_collect(html, exported_titles)
            new_images |= imgs

            body = html_to_markdown(clean_html)
            fm = frontmatter(title, ns, revid, cats, retrieved)
            rel = md_path_for(title, ns)
            dest = os.path.join(md_dir, rel)
            os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
            with open(dest, "w", encoding="utf-8") as f:
                f.write(fm + "\n# " + title + "\n\n" + body)

            state["pages"][key] = {"title": title, "ns": ns, "revid": revid, "path": rel}
            changed += 1
            if i % 50 == 0 or changed <= 5:
                print(f"  [{i}/{len(pages)}] {title} (rev {revid})", flush=True)
            time.sleep(0.05)
        except Exception as e:  # noqa: BLE001
            print(f"  [ERRO] {title}: {e}", flush=True)

    print(f"Markdown: {changed} gravadas, {unchanged} inalteradas.", flush=True)

    if do_images:
        download_images(out, state, new_images, full=full)

    save_state(state_path, state)
    print("state.json salvo.", flush=True)


def download_images(out: str, state: dict, images: set[str], full=False):
    todo = sorted(images)
    print(f"Imagens referenciadas nesta rodada: {len(todo)}", flush=True)
    got = skipped = failed = 0
    for j, local in enumerate(todo, 1):
        dest = os.path.join(out, local)
        if not full and os.path.exists(dest) and local in state["images"]:
            skipped += 1
            continue
        url = _image_url_from_local(local)
        try:
            r = session.get(url, timeout=90)
            if r.status_code != 200 or not r.content:
                failed += 1
                continue
            os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
            with open(dest, "wb") as f:
                f.write(r.content)
            state["images"][local] = {"bytes": len(r.content)}
            got += 1
            if j % 100 == 0:
                print(f"  imagens [{j}/{len(todo)}]", flush=True)
            time.sleep(0.03)
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  [img ERRO] {local}: {e}", flush=True)
    print(f"Imagens: {got} baixadas, {skipped} ja existentes, {failed} falhas.", flush=True)


# --------------------------------------------------------------------------- #
# XML dump (TODOS os namespaces) — backup fiel/restauravel
# --------------------------------------------------------------------------- #
def export_dump(out: str):
    dump_dir = os.path.join(out, "dump")
    os.makedirs(dump_dir, exist_ok=True)
    dest = os.path.join(dump_dir, "browiki-current.xml")
    print("Coletando titulos de TODOS os namespaces para o dump...", flush=True)

    # TODOS os namespaces nao-negativos (inclui Discussao) — backup realmente completo.
    #  0 principal, 1 Discussao, 2 Usuario, 3 Usuario Disc., 4 Projeto, 5 Projeto Disc.,
    #  6 Arquivo, 7 Arquivo Disc., 8 MediaWiki, 9 MediaWiki Disc., 10 Predef., 11 Predef. Disc.,
    # 12 Ajuda, 13 Ajuda Disc., 14 Categoria, 15 Categoria Disc.
    content_ns = list(range(0, 16))
    titles = []
    for ns in content_ns:
        n = 0
        for p in list_pages(ns):
            titles.append(p["title"])
            n += 1
        print(f"  ns {ns}: {n} paginas", flush=True)
    print(f"Total p/ dump: {len(titles)} paginas. Exportando XML...", flush=True)

    # action=query&export em lotes de 50 titulos, concatenando paginas <page>.
    header = ('<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/" '
              'xml:lang="pt-br">\n')
    with open(dest, "w", encoding="utf-8") as out_f:
        out_f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        out_f.write(header)
        for k in range(0, len(titles), 50):
            batch = titles[k:k + 50]
            data = session.get(API, params={
                "action": "query", "export": "1", "exportnowrap": "1",
                "titles": "|".join(batch), "format": "json", "formatversion": "1",
            }, timeout=120)
            xml = data.text
            # extrai apenas os <page>...</page>
            for m in re.finditer(r"<page>.*?</page>", xml, re.S):
                out_f.write(m.group(0) + "\n")
            if (k // 50) % 10 == 0:
                print(f"  dump [{k}/{len(titles)}]", flush=True)
            time.sleep(0.05)
        out_f.write("</mediawiki>\n")
    size = os.path.getsize(dest)
    print(f"Dump XML salvo: {dest} ({size/1e6:.1f} MB)", flush=True)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Espelha a bROWiki para Markdown/XML.")
    ap.add_argument("cmd", choices=["markdown", "dump", "all"])
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--no-images", action="store_true")
    ap.add_argument("--full", action="store_true", help="ignora o estado e refaz tudo")
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    if args.cmd in ("markdown", "all"):
        export_markdown(args.out, limit=args.limit,
                        do_images=not args.no_images, full=args.full)
    if args.cmd in ("dump", "all"):
        export_dump(args.out)


if __name__ == "__main__":
    main()
