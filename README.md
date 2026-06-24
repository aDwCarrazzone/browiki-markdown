# bROWiki — Espelho em Markdown

Backup completo e legível por humanos e IA da [**bROWiki**](https://browiki.org/wiki/) —
a wiki brasileira de Ragnarök Online.

O objetivo é triplo:

1. **Preservação / backup distribuído** — que o conhecimento da bROWiki não dependa de
   um servidor só. Clone este repositório e você tem uma cópia completa.
2. **Legibilidade por IA** — Markdown limpo (templates/infoboxes já expandidos), fácil de
   uma IA ler e raciocinar em cima.
3. **Versionamento** — cada sincronização vira um commit; dá para ver o que mudou e quando.

> Espelho **não oficial**, mantido para fins de arquivo. O conteúdo pertence à bROWiki e
> seus colaboradores. Este repositório só lê a wiki — nunca escreve de volta.

## Navegação

- **[📑 Índice por categoria (INDEX.md)](INDEX.md)** — todas as páginas agrupadas por categoria.
- **[📖 Wiki navegável](../../wiki)** — versão para leitura humana, com imagens, na aba *Wiki*.

## Estrutura

```
<Categoria>/      Artigos organizados em pastas por categoria principal
Categoria/        Páginas do namespace Categoria
Ajuda/            Páginas de Ajuda
INDEX.md          Índice navegável por categoria
dump/             browiki-current.xml — dump restaurável de TODOS os namespaces
export_browiki.py Extração/sincronização (baixa para _flat/)
build_views.py    Gera a árvore organizada + INDEX.md + wiki/ a partir de _flat/
_flat/            Markdown cru intermediário (não versionado)
```

Cada artigo de conteúdo fica na pasta da sua **categoria principal**; o `INDEX.md` lista
cada página em **todas** as suas categorias. Links internos e imagens são relativos e
corrigidos automaticamente.

> **Imagens:** os arquivos `.md` referenciam `images/...`, mas as ~6.700 imagens (~1,2 GB)
> **não ficam na árvore do repositório** (para mantê-lo leve). Elas estão num **.zip anexado
> ao [Release](../../releases)**, com a mesma estrutura de pastas.
>
> Para ter a wiki completa com as imagens no lugar (renderizando em cada página em leitores
> locais como VS Code/Obsidian):
>
> ```bash
> git clone https://github.com/aDwCarrazzone/browiki-markdown.git
> cd browiki-markdown
> # baixe browiki-images.zip do Release e extraia AQUI (na raiz):
> unzip browiki-images.zip          # cria a pasta images/ no lugar certo
> ```
>
> Observação: no preview web do github.com as imagens não aparecem (o site não extrai o zip);
> elas renderizam após a extração local. Alternativamente, `python export_browiki.py markdown`
> rebaixa as imagens direto da wiki para `images/`.

Cada `.md` tem um cabeçalho YAML com `title`, `source` (URL original), `revision`,
`retrieved` (data da coleta) e `categories`.

## Atualizar (sincronizar com a bROWiki)

```bash
pip install -r requirements.txt

python export_browiki.py markdown   # rebaixa só as páginas alteradas (para _flat/) + imagens
python build_views.py               # regenera a árvore organizada + INDEX.md + wiki/
python export_browiki.py dump       # regenera o dump XML completo
```

O modo Markdown é **incremental**: usa `state.json` para comparar a revisão local com a
da wiki e só rebaixa o que mudou. Para refazer tudo do zero, use `--full`.

Opções: `--limit N` (testes), `--no-images`, `--out DIR`, `--full`.

## Restaurar a wiki a partir do dump

`dump/browiki-current.xml` está no formato de exportação do MediaWiki e pode ser importado
em qualquer instalação MediaWiki via `Special:Import` ou `maintenance/importDump.php`.

## Como é gerado

`export_browiki.py` usa a API pública do MediaWiki (`action=parse`) para obter o HTML já
renderizado de cada página e o converte para Markdown com `markdownify`, reescrevendo
links internos e localizando as imagens. O dump usa `action=query&export`.

---
*Gerado automaticamente. Fonte: https://browiki.org*
