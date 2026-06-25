#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_views.py — A partir do intermediario _flat/ (gerado por export_browiki.py),
constroi as visoes versionadas usando uma TAXONOMIA CURADA de 2 niveis:

  1. Arvore organizada na RAIZ:  <Tipo>/<Subtipo>/<Pagina>.md
     (Habilidades/Ofensiva, Quests/Experiencia, Classes/Guias, Lugares, etc.)
     - links internos e caminhos de imagem reescritos (relativos / CDN)
  2. INDEX.md  — indice navegavel pela mesma taxonomia
  3. wiki/     — Wiki do GitHub (Home + _Sidebar pela taxonomia; imagens via CDN)

Uso:  python build_views.py
"""
from __future__ import annotations
import os, re, glob, collections, posixpath
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
FLAT = os.path.join(ROOT, "_flat")
# Imagens via CDN jsDelivr a partir do repo browiki-images (content-type correto).
IMG_CDN = "https://cdn.jsdelivr.net/gh/aDwCarrazzone/browiki-images@main/"

_ILLEGAL = re.compile(r'[<>:"\\|?*\x00-\x1f]')
_RESERVED = re.compile(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$', re.I)

# --- taxonomia ------------------------------------------------------------- #
WEAPONS = {"Chicote", "Instrumento musical", "Arco", "Lança", "Espada",
"Espada de Duas Mãos", "Adaga", "Katar", "Machado", "Maça", "Pistola", "Espingarda",
"Rifle", "Livro", "Lança-Granadas", "Metralhadora Gatling", "Shuriken Huuma",
"Soqueira", "Escudo"}
SKILL_FLAVOR = {"Ofensiva", "Ativa", "Passiva", "Suporte", "Rápidos no Gatilho",
"O Tiro Certeiro da Natureza", "O Poder dos Elementos", "O Poder Divino",
"A Justiça em Ação", "A Luz das Trevas", "O Poder Interior", "O Segredo das Sombras",
"A Arte da Alquimia e da Forja", "Duetos"}


def is_skill_cat(c):
    return c.startswith("Habilidades") or c in SKILL_FLAVOR


def classify(cats, is_redirect, ns):
    """Mapeia (categorias cruas, redirect?, namespace) -> pasta da taxonomia."""
    if ns == 14:
        return "Referência/Categorias"
    if ns == 12:
        return "Referência/Ajuda"
    if is_redirect:
        return "Redirecionamentos"
    s = set(cats)
    if "Homunculus" in s:
        return "Homúnculos"
    if "Guias de Classe" in s:
        return "Classes/Guias"
    if "Classes" in s:
        return "Classes"
    if any(is_skill_cat(c) for c in cats):
        if "Habilidades de monstros" in s:
            return "Habilidades/De monstros"
        if "Ofensiva" in s:
            return "Habilidades/Ofensiva"
        if "Suporte" in s:
            return "Habilidades/Suporte"
        if "Passiva" in s:
            return "Habilidades/Passiva"
        if any(c.startswith("Habilidades com ") and c[16:] in WEAPONS for c in cats):
            return "Habilidades/Por arma"
        return "Habilidades/Especiais"
    if "Instâncias" in s or "Acesso a Calabouços" in s:
        return "Calabouços e Instâncias"
    if "Quests de experiência" in s:
        return "Quests/Experiência"
    if "Quests de caça" in s:
        return "Quests/Caça"
    if "Quests repetíveis" in s:
        return "Quests/Repetíveis"
    if "Quests diárias" in s:
        return "Quests/Diárias"
    if "Quest" in s:
        return "Quests/Gerais"
    if "Lugares em Ragnarök" in s:
        return "Lugares"
    if "Itens" in s:
        return "Itens"
    if "Evento" in s or "Colaborações" in s:
        return "Eventos"
    if "Informações básicas" in s or "PvP" in s:
        return "Sistema e Mecânicas"
    return "Referência"


# --- helpers --------------------------------------------------------------- #
def sanitize(seg: str) -> str:
    seg = _ILLEGAL.sub("-", seg).strip().rstrip(".") or "_"
    if _RESERVED.match(seg):
        seg += "_"
    return seg


def _sanitize_path(p):
    return "/".join(sanitize(s) for s in p.split("/"))


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


def img_url(rest: str) -> str:
    return IMG_CDN + quote(rest, safe="/")


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
        "ns": int(g(r'^namespace:\s*(\d+)') or 0),
        "cats": cats,
    }, body


# --- coleta ---------------------------------------------------------------- #
def collect():
    records = []
    for f in glob.glob(os.path.join(FLAT, "**", "*.md"), recursive=True):
        rel = os.path.relpath(f, FLAT).replace("\\", "/")
        meta, body = parse_fm(open(f, encoding="utf-8").read())
        if not meta.get("title"):
            continue
        is_red = bool(re.search(r'(?m)^Redirecionar para:', body))
        base = posixpath.basename(rel)
        folder = classify(meta["cats"], is_red, meta["ns"])
        records.append({
            "rel": rel, "key": rel[:-3], "base": base, "body": body,
            "folder": folder, "org": f"{folder}/{base}", **meta,
        })
    return records


# --- reescrita de corpo ---------------------------------------------------- #
def rewrite_for_tree(rec, linkmap, lowermap):
    src_dir = posixpath.dirname(rec["org"])
    body = rec["body"]
    body = re.sub(r'\]\(images/([^)\s]+)\)',
                  lambda m: "](" + img_url(m.group(1)) + ")", body)

    def link(m):
        target, frag = m.group(1), m.group(2) or ""
        tip = m.group(3) or ""
        r = (linkmap.get(target) or linkmap.get(_sanitize_path(target))
             or lowermap.get(target.lower()) or lowermap.get(_sanitize_path(target).lower()))
        if not r:
            return m.group(0)
        rel = posixpath.relpath(r["org"], src_dir or ".")
        return "](" + quote(rel, safe="/") + frag + (f' "{tip}"' if tip else "") + ")"
    body = re.sub(
        r'\]\((?!https?:|/|#)([^)#]+?)\.md(#[^)\s]*)?(?:\s+"([^"]*)")?\)', link, body)
    return body


def tree_footer(r):
    cats = ", ".join(r["cats"]) if r["cats"] else "—"
    src = f"[bROWiki]({r['source']})" if r.get("source") else "bROWiki"
    rev = f" — revisão {r['rev']}" if r.get("rev") else ""
    return f"\n\n---\n*Categorias: {cats}*  \n*Importado da {src}{rev}*\n"


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


# --- indices --------------------------------------------------------------- #
def build_index(records, link_fn, title_h1, intro):
    bysub = collections.defaultdict(list)
    for r in records:
        bysub[r["folder"]].append(r)
    tops = collections.defaultdict(list)
    for folder in sorted(bysub):
        tops[folder.split("/")[0]].append(folder)
    out = [f"# {title_h1}\n", intro, "", f"**{len(records)} páginas**.\n", "## Conteúdo\n"]
    for top in sorted(tops):
        out.append(f"- [{top}](#{gh_anchor(top)}) ({sum(len(bysub[f]) for f in tops[top])})")
    for top in sorted(tops):
        out.append(f"\n## {top}\n")
        for folder in tops[top]:
            sub = folder.split("/", 1)[1] if "/" in folder else None
            if sub:
                out.append(f"\n### {sub}\n")
            for r in sorted(bysub[folder], key=lambda x: x["title"].lower()):
                out.append(f"- [{r['title']}]({link_fn(r)})")
    return "\n".join(out) + "\n"


def build_sidebar(records):
    tops = collections.defaultdict(set)
    for r in records:
        parts = r["folder"].split("/")
        tops[parts[0]].add(parts[1] if len(parts) > 1 else "")
    out = ["### [🏠 Início](Home)\n"]
    for top in sorted(tops):
        out.append(f"\n**[{top}](Home#{gh_anchor(top)})**")
        for sub in sorted(s for s in tops[top] if s):
            out.append(f"- [{sub}](Home#{gh_anchor(sub)})")
    return "\n".join(out) + "\n"


# --- main ------------------------------------------------------------------ #
def clean_tree():
    keep = {"_flat", "wiki", "dump", "images", ".git", ".claude", "__pycache__"}
    import shutil
    for name in os.listdir(ROOT):
        p = os.path.join(ROOT, name)
        if os.path.isdir(p) and name not in keep:
            shutil.rmtree(p)


def main():
    os.chdir(ROOT)
    records = collect()
    print(f"{len(records)} paginas coletadas de _flat/.")
    linkmap = {r["key"]: r for r in records}
    lowermap = {r["key"].lower(): r for r in records}

    # 1) arvore organizada
    clean_tree()
    for r in records:
        dest = os.path.join(ROOT, *r["org"].split("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        body = rewrite_for_tree(r, linkmap, lowermap)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write("# " + r["title"] + "\n\n" + body.rstrip() + tree_footer(r))
    print("arvore organizada gerada.")

    # 2) INDEX.md
    intro = ("Índice navegável pela taxonomia do acervo. Cada página aparece na sua pasta; "
             "as categorias originais da wiki ficam no rodapé de cada página.")
    open(os.path.join(ROOT, "INDEX.md"), "w", encoding="utf-8").write(
        build_index(records, lambda r: quote(r["org"], safe="/"), "Índice da bROWiki", intro))
    print("INDEX.md gerado.")

    # 3) wiki/
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
          "Ragnarök Online. Use a barra lateral ou as seções abaixo.")
    open(os.path.join(wdir, "Home.md"), "w", encoding="utf-8").write(
        build_index(records, lambda r: wiki_name(r["title"]), "bROWiki — Índice", wi))
    open(os.path.join(wdir, "_Sidebar.md"), "w", encoding="utf-8").write(build_sidebar(records))
    print(f"wiki/: {len(records)} paginas + Home.md + _Sidebar.md")


if __name__ == "__main__":
    main()
