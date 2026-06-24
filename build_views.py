#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_views.py — A partir do intermediario _flat/ (gerado por export_browiki.py),
constroi as visoes versionadas:

  1. Arvore organizada por categoria na RAIZ:  <Categoria>/<Pagina>.md
     - paginas de conteudo (ns 0) vao para a pasta da sua categoria PRIMARIA
     - paginas de Categoria/Ajuda mantem suas pastas de namespace
     - links internos e caminhos de imagem sao reescritos (relativos, corretos)
  2. INDEX.md  — indice navegavel por categoria (links para a arvore organizada)
  3. wiki/     — conteudo para o Wiki do GitHub (Home/_Sidebar/links/imagens proprios)

Uso:  python build_views.py
"""
from __future__ import annotations
import os, re, glob, collections, posixpath
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
FLAT = os.path.join(ROOT, "_flat")
# Imagens servidas pelo CDN jsDelivr a partir do repo browiki-images (content-type correto;
# o browiki serve como octet-stream e nao renderiza inline). Raiz do repo = a/ ab/ ...
IMG_CDN = "https://cdn.jsdelivr.net/gh/aDwCarrazzone/browiki-images@main/"


def img_url(rest: str) -> str:
    """rest = caminho apos 'images/' (ex.: 'a/ab/Foo.png') -> URL no CDN."""
    return IMG_CDN + quote(rest, safe="/")

_ILLEGAL = re.compile(r'[<>:"\\|?*\x00-\x1f]')
_RESERVED = re.compile(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$', re.I)

# Categorias de manutencao (nao servem como categoria "primaria" de uma pagina).
_MAINT = ("Páginas com", "Páginas marcadas", "Categorias ocultas", "Desambiguação")

NS_FOLDER = {12: "Ajuda", 14: "Categoria"}
NOCAT = "Sem categoria"

# --------------------------------------------------------------------------- #
def sanitize(seg: str) -> str:
    seg = _ILLEGAL.sub("-", seg).strip().rstrip(".") or "_"
    if _RESERVED.match(seg):
        seg += "_"
    return seg


def gh_anchor(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.U)
    return s.replace(" ", "-")


def wiki_name(title: str) -> str:
    parts = []
    for seg in title.split("/"):
        seg = sanitize(seg).replace(" ", "-")
        seg = re.sub(r"-{2,}", "-", seg)
        if _RESERVED.match(seg):
            seg += "_"
        parts.append(seg)
    return "/".join(parts)


def parse_fm(text: str):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    fm = text[3:end]
    body = text[end + 4:].lstrip("\n")
    def g(pat):
        m = re.search(pat, fm, re.M)
        return m.group(1) if m else ""
    cats = []
    if "categories:" in fm:
        tail = fm[fm.find("categories:"):]
        cats = [c.replace("_", " ") for c in re.findall(r'^\s*-\s*"?(.*?)"?\s*$', tail, re.M)]
    return {
        "title": g(r'^title:\s*"?(.*?)"?\s*$'),
        "source": g(r'^source:\s*(\S+)'),
        "rev": g(r'^revision:\s*(\S+)'),
        "ns": g(r'^namespace:\s*(\d+)'),
        "cats": cats,
    }, body


def primary_category(cats):
    if not cats:
        return NOCAT
    for c in cats:
        if not any(c.startswith(m) or m in c for m in _MAINT):
            return c
    return cats[0]


# --------------------------------------------------------------------------- #
def collect():
    records = []
    for f in glob.glob(os.path.join(FLAT, "**", "*.md"), recursive=True):
        rel = os.path.relpath(f, FLAT).replace("\\", "/")
        meta, body = parse_fm(open(f, encoding="utf-8").read())
        if not meta.get("title"):
            continue
        ns = int(meta["ns"]) if meta.get("ns") else 0
        base = posixpath.basename(rel)                  # nome de arquivo seguro
        key = rel[:-3]                                  # alvo dos links (sem .md)
        # caminho organizado
        if ns in NS_FOLDER:
            org = f"{NS_FOLDER[ns]}/{base}"
        elif ns == 0:
            org = f"{sanitize(primary_category(meta['cats']))}/{base}"
        else:
            org = base
        records.append({"rel": rel, "key": key, "org": org, "body": body, **meta})
    return records


def _sanitize_path(p):
    return "/".join(sanitize(s) for s in p.split("/"))


def rewrite_for_tree(rec, linkmap, lowermap):
    """Reescreve links internos e imagens para a posicao organizada do arquivo."""
    src_dir = posixpath.dirname(rec["org"])
    body = rec["body"]

    body = re.sub(r'\]\(images/([^)\s]+)\)',
                  lambda m: "](" + img_url(m.group(1)) + ")", body)

    def link(m):
        target, frag = m.group(1), m.group(2) or ""
        tip = m.group(3) or ""
        # tenta exato, depois nome reservado (CON->CON_), depois case-insensitive
        r = (linkmap.get(target) or linkmap.get(_sanitize_path(target))
             or lowermap.get(target.lower()) or lowermap.get(_sanitize_path(target).lower()))
        if not r:
            return m.group(0)  # alvo nao exportado/desconhecido: mantem
        rel = posixpath.relpath(r["org"], src_dir or ".")
        return "](" + quote(rel, safe="/") + frag + (f' "{tip}"' if tip else "") + ")"
    body = re.sub(
        r'\]\((?!https?:|/|#)([^)#]+?)\.md(#[^)\s]*)?(?:\s+"([^"]*)")?\)', link, body)
    return body


def to_wiki_body(body: str, meta: dict) -> str:
    body = re.sub(r'\]\(images/([^)\s]+)\)',
                  lambda m: "](" + img_url(m.group(1)) + ")", body)
    def repl(m):
        return "](" + m.group(1).replace(" ", "-") + (m.group(2) or "") + ")"
    body = re.sub(r'\]\((?!https?:|/)([^)#]+?)\.md(#[^)\s]*)?(?:\s+"[^"]*")?\)', repl, body)
    footer = ""
    if meta.get("source"):
        footer = f"\n\n---\n*Importado da [bROWiki]({meta['source']})"
        footer += f" — revisão {meta['rev']}*\n" if meta.get("rev") else "*\n"
    return body.rstrip() + "\n" + footer


# --------------------------------------------------------------------------- #
def build_index(records, link_fn, title_h1, intro):
    bycat = collections.defaultdict(list)
    for r in records:
        for c in (r["cats"] or [NOCAT]):
            bycat[c].append(r)
    cats = sorted(bycat, key=lambda c: (c == NOCAT, c.lower()))
    out = [f"# {title_h1}\n", intro, "",
           f"**{len(records)} páginas** em **{len(cats)} categorias**.\n", "## Categorias\n"]
    for c in cats:
        out.append(f"- [{c}](#{gh_anchor(c)}) ({len(bycat[c])})")
    out.append("")
    for c in cats:
        out.append(f"\n## {c}\n")
        for r in sorted(bycat[c], key=lambda x: x["title"].lower()):
            out.append(f"- [{r['title']}]({link_fn(r)})")
    return "\n".join(out) + "\n"


def build_sidebar(records):
    bycat = collections.Counter()
    for r in records:
        for c in (r["cats"] or [NOCAT]):
            bycat[c] += 1
    cats = sorted(bycat, key=lambda c: (c == NOCAT, c.lower()))
    out = ["### [🏠 Início](Home)\n", "**Categorias**\n"]
    out += [f"- [{c}](Home#{gh_anchor(c)})" for c in cats]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- #
def clean_tree():
    """Remove pastas de categoria/namespace antigas da raiz (deixa infra intacta)."""
    keep = {"_flat", "wiki", "dump", "images", ".git", ".claude", "__pycache__"}
    for name in os.listdir(ROOT):
        p = os.path.join(ROOT, name)
        if os.path.isdir(p) and name not in keep:
            import shutil
            shutil.rmtree(p)


def main():
    os.chdir(ROOT)
    records = collect()
    print(f"{len(records)} paginas coletadas de _flat/.")
    linkmap = {r["key"]: r for r in records}
    lowermap = {r["key"].lower(): r for r in records}

    # ---- 1) arvore organizada na raiz ----
    clean_tree()
    for r in records:
        dest = os.path.join(ROOT, *r["org"].split("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        body = rewrite_for_tree(r, linkmap, lowermap)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write("# " + r["title"] + "\n\n" + body)
    print("arvore organizada gerada.")

    # ---- 2) INDEX.md ----
    intro = ("Índice navegável por categoria. Cada página de conteúdo está na pasta da sua "
             "categoria principal (e listada em todas as suas categorias abaixo).")
    open(os.path.join(ROOT, "INDEX.md"), "w", encoding="utf-8").write(
        build_index(records, lambda r: quote(r["org"], safe="/"), "Índice da bROWiki", intro))
    print("INDEX.md gerado.")

    # ---- 3) wiki/ ----
    import shutil
    wdir = os.path.join(ROOT, "wiki")
    if os.path.isdir(wdir):
        for n in os.listdir(wdir):
            if n == ".git":
                continue
            pp = os.path.join(wdir, n)
            shutil.rmtree(pp) if os.path.isdir(pp) else os.remove(pp)
    os.makedirs(wdir, exist_ok=True)
    for r in records:
        dest = os.path.join(wdir, *(wiki_name(r["title"]) + ".md").split("/"))
        os.makedirs(os.path.dirname(dest) or wdir, exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write("# " + r["title"] + "\n\n" + to_wiki_body(r["body"], r))
    wi = ("Espelho navegável da [bROWiki](https://browiki.org) — wiki brasileira de "
          "Ragnarök Online. Use a barra lateral ou as categorias abaixo.")
    open(os.path.join(wdir, "Home.md"), "w", encoding="utf-8").write(
        build_index(records, lambda r: wiki_name(r["title"]), "bROWiki — Índice", wi))
    open(os.path.join(wdir, "_Sidebar.md"), "w", encoding="utf-8").write(build_sidebar(records))
    print(f"wiki/: {len(records)} paginas + Home.md + _Sidebar.md")


if __name__ == "__main__":
    main()
