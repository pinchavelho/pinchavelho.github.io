# assets/ — recursos partilhados do site

> Documentação interna para pessoas e para o bot Grok. Não é publicada no site.

**O que existe**

| Pasta | Conteúdo | Guia |
|---|---|---|
| `css/` | o único ficheiro de estilos, `site.css` | `css/README.md` |
| `fonts/` | Inter e Space Grotesk em woff2, com as licenças | `fonts/README.md` |
| `img/` | logótipos, símbolo, ícones de app, imagem de partilha | `img/README.md` |
| `img/screens/` | capturas de ecrã das apps (1280×800) | `img/screens/README.md` |

**Regras**

- Tudo o que o site usa tem de estar aqui (ou na raiz). A CSP só permite recursos do próprio site (`'self'`): uma fonte, imagem ou CSS de outro domínio **não carrega** e viola os valores da marca.
- Sem ficheiros JavaScript.
- Caminhos absolutos a partir da raiz nas páginas: `/assets/css/site.css`, `/assets/img/...`.
- Antes de apagar ou renomear um ficheiro, procurar onde é usado: `grep -rn "nome-do-ficheiro" --include=*.html .`
