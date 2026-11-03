# pt/ — o site em português de Portugal

> Documentação interna para pessoas e para o bot Grok. Não é publicada no site.

**O que existe:** o espelho em pt-PT do site em inglês. Cada ficheiro tem o **mesmo caminho** que a gémea EN, com `/pt` à frente.

| PT | EN |
|---|---|
| `pt/index.html` → `/pt/` | `index.html` → `/` |
| `pt/about.html` | `about.html` |
| `pt/legal-notice.html` | `legal-notice.html` |
| `pt/playpilot/` | `playpilot/` → `pt/playpilot/README.md` |

Não há `pt/404.html`: o GitHub Pages usa só o `404.html` da raiz.

**Regras**

- O inglês é o texto de referência; o português diz exatamente o mesmo (preços, prazos, promessas).
- Português de Portugal, nunca do Brasil: "navegador", "transferência", "ecrã", "reembolso", "utilizador", "aplicação".
- `<html lang="pt-PT">`, `hreflang` en / pt-PT / x-default (x-default aponta para EN) e `canonical` para o próprio endereço PT.
- Os links internos apontam para páginas PT (`/pt/...`); o seletor de idioma aponta para a gémea EN.
- Mesma CSP, mesmo CSS e mesmo rodapé (traduzido) que as páginas EN.

**Como usar:** ao criar ou alterar uma página EN, fazer o mesmo aqui no mesmo pull request e acrescentar as duas ao `sitemap.xml`.
