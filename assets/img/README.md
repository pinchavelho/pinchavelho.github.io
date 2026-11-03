# assets/img/ — imagens do site

> Documentação interna para pessoas e para o bot Grok. Não é publicada no site.

**O que existe (marca v1)**

| Ficheiro | Uso |
|---|---|
| `pinchavelho_horizontal_claro.svg` | logótipo no cabeçalho, modo claro (173×44) |
| `pinchavelho_horizontal_escuro.svg` | logótipo no cabeçalho, modo escuro (via `<picture>`) |
| `pinchavelho_horizontal_claro_1200.png` | imagem de partilha (`og:image`) |
| `pinchavelho_simbolo.svg` | favicon SVG |
| `pinchavelho_simbolo_512.png` | `apple-touch-icon` |
| `favicon.ico` | cópia do favicon (o que as páginas usam é `/favicon.ico` na raiz) |
| `playpilot-icon-128.png` | ícone da app PlayPilot (mostrado a 72 px na home e na página da app) |
| `pinchavelho_cws_32.png` | símbolo de 32 px; não é usado por nenhuma página |
| `screens/` | capturas das apps → `screens/README.md` |

**Regras**

- Só PNG ou SVG locais. SVG sem scripts nem ligações externas.
- Em cada `<img>`: `width`, `height` e `alt` (vazio `alt=""` só para imagens decorativas, como o ícone ao lado do nome da app).
- O logótipo tem versões claro e escuro: usar sempre as duas com `<picture>`.
- Logótipo, símbolo e ícones são da marca v1. A v2 "Manípulo" (Ritmello e Vedello) existe nas pastas do projeto, mas só entra aqui depois da aprovação do Jose. Para criar ou alterar ícones usar a skill `pinchavelho-logo`.

**Pendente:** com a mudança de nome, `playpilot-icon-128.png` vai dar lugar ao ícone do Ritmello, e o Vedello vai precisar do seu.
