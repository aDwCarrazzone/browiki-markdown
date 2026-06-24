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

## Estrutura

```
*.md              Artigos (namespace principal), 1 arquivo por página
Ajuda/            Páginas de Ajuda
Categoria/        Páginas de Categoria
dump/             browiki-current.xml — dump restaurável de TODOS os namespaces
state.json        Metadados de revisão (pageid → revid) para sync incremental
export_browiki.py Script de extração/sincronização
```

> **Imagens:** os arquivos `.md` referenciam `images/...`, mas as ~6.700 imagens (~1,2 GB)
> **não estão versionadas neste repositório** por enquanto (para mantê-lo leve). Para
> baixá-las localmente, rode `python export_browiki.py markdown` — elas vão para `images/`.
> (Futuramente podem ir para um Release, Git LFS ou repositório próprio.)

Cada `.md` tem um cabeçalho YAML com `title`, `source` (URL original), `revision`,
`retrieved` (data da coleta) e `categories`.

## Atualizar (sincronizar com a bROWiki)

```bash
pip install -r requirements.txt

python export_browiki.py markdown   # rebaixa só as páginas alteradas + novas imagens
python export_browiki.py dump       # regenera o dump XML completo
python export_browiki.py all        # os dois
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
