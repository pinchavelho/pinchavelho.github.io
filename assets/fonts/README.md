# assets/fonts/ — tipos de letra

> Documentação interna para pessoas e para o bot Grok. Não é publicada no site.

**O que existe**

| Ficheiro | Uso |
|---|---|
| `space-grotesk-var-latin.woff2` | títulos (pesos 500–700) |
| `inter-var-latin.woff2` | texto (pesos 400–600) |
| `OFL-SpaceGrotesk.txt`, `OFL-Inter.txt` | licenças SIL Open Font License 1.1 |

**Regras**

- Fontes sempre locais. **Nunca** Google Fonts nem outro CDN (a CSP `font-src 'self'` bloqueia e seria um recurso de terceiros).
- As licenças OFL têm de acompanhar sempre os ficheiros das fontes. Não apagar.
- Só o subconjunto latino: cobre inglês e português.

**Como usar:** as fontes são declaradas com `@font-face` no topo de `/assets/css/site.css`. A Inter é pré-carregada no `<head>` de cada página com `<link rel="preload" ... crossorigin>`. Para trocar uma fonte, substituir o ficheiro, a licença e a declaração no CSS.
