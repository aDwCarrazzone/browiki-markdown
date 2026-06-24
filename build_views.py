#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_views.py — Gera duas camadas de NAVEGACAO a partir dos .md ja exportados:

  1. wiki/        -> conteudo no formato do Wiki do GitHub (sem frontmatter, links e
                     imagens ajustados) + Home.md + _Sidebar.md + indices por categoria.
                     Esse diretorio e' empurrado para o repo browiki-markdown.wiki.git.
  2. INDEX.md     -> indice navegavel por categoria, dentro do proprio repositorio
                     (os arquivos .md continuam onde estao; nada e' movido).

Uso:
  python build_views.py           # gera wiki/ e INDEX.md
"""
from __future__ import annotations
import os, re, glob, collections
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
BROWIKI_IMG = "https://browiki.org/images/"

_ILLEGAL = re.compile(r'[<>:"\\|?*\x00-\x1f]')
SKIP = {"README.md", "INDEX.md"}

# --------------------------------------------------------------------------- #
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
    title = g(r'^title:\s*"?(.*?)"?\s*$')
    source = g(r'^source:\s*(\S+)')
    rev = g(r'^revision:\s*(\S+)')
    cats = []
    if "categories:" in fm:
        tail = fm[fm.find("categories:"):]
        cats = [c.replace("_", " ") for c in re.findall(r'^\s*-\s*"?(.*?)"?\s*$', tail, re.M)]
    return {"title": title, "source": source, "rev": rev, "cats": cats}, body


def gh_anchor(s: str) -> str:
    """Reproduz o slug de cabecalho do GitHub (mantem letras acentuadas)."""
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.U)  # remove pontuacao, mantem acentos
    return s.replace(" ", "-")


def wiki_name(title: str) -> str:
    """Nome de pagina no Wiki do GitHub: chars ilegais -> '-', espacos -> '-'."""
    parts = []
    for seg in title.split("/"):
        seg = _ILLEGAL.sub("-", seg).strip().rstrip(".") or "_"
        seg = seg.replace(" ", "-")
        seg = re.sub(r"-{2,}", "-", seg)
        parts.append(seg)
    return "/".join(parts)


def to_wiki_body(body: str, meta: dict) -> str:
    # imagens -> URL absoluta do browiki (renderiza no Wiki web)
    body = body.replace("](images/", "](" + BROWIKI_IMG)
    # links internos [..](Alvo.md#frag "tip") -> [..](Alvo-com-hifen#frag)
    def repl(m):
        target, frag = m.group(1), m.group(2) or ""
        return "](" + target.replace(" ", "-") + frag + ")"
    body = re.sub(r'\]\((?!https?:|/)([^)#]+?)\.md(#[^)\s]*)?(?:\s+"[^"]*")?\)', repl, body)
    footer = ""
    if meta.get("source"):
        footer = f"\n\n---\n*Importado da [bROWiki]({meta['source']})"
        footer += f" — revisão {meta['rev']}*\n" if meta.get("rev") else "*\n"
    return body.rstrip() + "\n" + footer


# --------------------------------------------------------------------------- #
def collect():
    records = []
    for f in glob.glob("**/*.md", recursive=True):
        if f.startswith("wiki" + os.sep) or os.path.basename(f) in SKIP:
            continue
        text = open(f, encoding="utf-8").read()
        meta, body = parse_fm(text)
        if not meta.get("title"):
            continue
        records.append({"path": f.replace("\\", "/"), "body": body, **meta})
    return records


def build_index(records, link_fn, title_h1: str, intro: str) -> str:
    """Gera um indice por categoria. link_fn(rec) -> URL do alvo."""
    bycat = collections.defaultdict(list)
    for r in records:
        if r["cats"]:
            for c in r["cats"]:
                bycat[c].append(r)
        else:
            bycat["(sem categoria)"].append(r)
    cats = sorted(bycat, key=lambda c: (c == "(sem categoria)", c.lower()))

    out = [f"# {title_h1}\n", intro, ""]
    out.append(f"**{len(records)} páginas** em **{len(cats)} categorias**.\n")
    out.append("## Categorias\n")
    for c in cats:
        anchor = gh_anchor(c)
        out.append(f"- [{c}](#{anchor}) ({len(bycat[c])})")
    out.append("")
    for c in cats:
        out.append(f"\n## {c}\n")
        for r in sorted(bycat[c], key=lambda x: x["title"].lower()):
            out.append(f"- [{r['title']}]({link_fn(r)})")
    return "\n".join(out) + "\n"


def build_sidebar(records) -> str:
    bycat = collections.defaultdict(int)
    for r in records:
        for c in (r["cats"] or ["(sem categoria)"]):
            bycat[c] += 1
    cats = sorted(bycat, key=lambda c: (c == "(sem categoria)", c.lower()))
    out = ["### [🏠 Início](Home)\n", "**Categorias**\n"]
    for c in cats:
        anchor = gh_anchor(c)
        out.append(f"- [{c}](Home#{anchor})")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- #
def main():
    os.chdir(ROOT)
    records = collect()
    print(f"{len(records)} paginas coletadas.")

    # ---- 1) WIKI ----
    wdir = os.path.join(ROOT, "wiki")
    os.makedirs(wdir, exist_ok=True)
    for r in records:
        name = wiki_name(r["title"])
        dest = os.path.join(wdir, name + ".md")
        os.makedirs(os.path.dirname(dest) or wdir, exist_ok=True)
        content = "# " + r["title"] + "\n\n" + to_wiki_body(r["body"], r)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(content)

    intro = ("Espelho navegável da [bROWiki](https://browiki.org) — wiki brasileira de "
             "Ragnarök Online. Use a barra lateral ou as categorias abaixo.")
    home = build_index(records, lambda r: wiki_name(r["title"]),
                       "bROWiki — Índice", intro)
    open(os.path.join(wdir, "Home.md"), "w", encoding="utf-8").write(home)
    open(os.path.join(wdir, "_Sidebar.md"), "w", encoding="utf-8").write(build_sidebar(records))
    print(f"wiki/: {len(records)} paginas + Home.md + _Sidebar.md")

    # ---- 2) INDEX.md do repo ----
    intro_repo = ("Índice navegável por categoria. Os arquivos `.md` ficam na raiz "
                  "(e em `Categoria/`); este índice apenas os organiza.")
    idx = build_index(records, lambda r: quote(r["path"]),
                      "Índice da bROWiki", intro_repo)
    open(os.path.join(ROOT, "INDEX.md"), "w", encoding="utf-8").write(idx)
    print("INDEX.md gerado.")


if __name__ == "__main__":
    main()
