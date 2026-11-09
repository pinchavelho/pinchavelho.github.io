# assets/css/ — estilos do site

> Documentação interna para pessoas e para o bot Grok. Não é publicada no site.

**O que existe:** `site.css`, o **único** ficheiro de estilos de todas as páginas (`<link rel="stylesheet" href="/assets/css/site.css">`).

## Regras

- Não criar outros CSS nem usar `style=""` ou `<style>` nas páginas: a CSP (`style-src 'self'`) bloqueia-os.
- Cores sempre por variáveis (tokens) definidas em `:root`. Para mudar a marca, muda-se aqui e em mais nenhum sítio.
- Modo escuro com `@media (prefers-color-scheme:dark)`, que redefine os mesmos tokens.
- Âmbar e verde nunca como cor de texto sobre fundo claro (contraste insuficiente).
- Manter acessibilidade: foco visível, link "saltar para o conteúdo" (`.skip`), `prefers-reduced-motion`.

## Tokens (marca v2 «Manípulo»; iguais aos da v1)

| Token | Claro | Escuro |
|---|---|---|
| `--bg` | `#F5F7FA` | `#0F1B2D` |
| `--surface` | `#FFFFFF` | `#132238` |
| `--surface2` | `#EEF1F6` | `#0B1422` |
| `--text` | `#0F1B2D` | `#F5F7FA` |
| `--muted` | `#45556B` | `#B4C2D6` |
| `--border` | `#D3DAE5` | `#2E4466` |
| `--link` | `#1756AD` | `#8DBBFF` |
| `--ok` | `#15703A` | `#6EE7A0` |
| `--btn-bg` / `--btn-fg` / `--btn-line` | `#0F1B2D` / `#FFFFFF` / `#FFB020` | `#FFB020` / `#0F1B2D` / `#0F1B2D` |

Cores fixas da marca: `--noite #0F1B2D`, `--ambar #FFB020`, `--azul #1E6FD9`, `--nevoa #F5F7FA`, `--verde #22A06B`.

## Classes disponíveis (reutilizar antes de criar novas)

| Classe | Para quê |
|---|---|
| `.wrap`, `.narrow` | largura máxima 68rem; texto corrido 46rem |
| `.hero`, `.eyebrow`, `.lead` | topo da página: etiqueta, título, frase de abertura |
| `.card`, `.card.product`, `.card.bare`, `.grid` | cartões (cantos assimétricos 14/4, assinatura da marca); cartão de produto com ícone de 72 px |
| `.btn`, `.btn.ghost`, `.btn.pending` | botão principal, secundário, e "brevemente" (sem link) |
| `.pill` | etiqueta pequena (ex.: "Chrome") |
| `.shots`, `figure`, `figcaption` | galeria de capturas |
| `table`, `td.c`, `.yes` | tabela Free vs Pro com ✓ |
| `.pricing`, `.price` | bloco de preço (números tabulares) |
| `.callout`, `.note` | caixa de destaque; nota pequena |
| `.doc`, `.meta` | páginas legais |
| `dl.trader` | dados do vendedor no aviso legal |
| `.skip`, `.visually-hidden`, `.lang`, `.nopad` | acessibilidade, seletor de idioma, ajustes |

## Como usar

Editar `site.css`, depois ver todas as páginas em claro, escuro e a 375 px de largura. A identidade v2 "Manípulo" foi aprovada a 4/11/2026; mudanças de identidade só com aprovação do Jose e depois de atualizar a skill `pinchavelho-brand`.
