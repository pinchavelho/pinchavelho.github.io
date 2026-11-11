# assets/img/ — imagens do site

> Documentação interna para pessoas e para o bot Grok. Não é publicada no site.

**O que existe (identidade v2 «Manípulo», de `identidade-visual/fase5-final/`)**

| Ficheiro | Uso |
|---|---|
| `pinchavelho-horizontal-claro.svg` | logótipo no cabeçalho, modo claro (216×44) |
| `pinchavelho-horizontal-escuro.svg` | logótipo no cabeçalho, modo escuro (via `<picture>`) |
| `pinchavelho-simbolo.svg` | manípulo livre (só fundos escuros); de reserva |
| `pinchavelho-simbolo-placa.svg` | manípulo com placa Noite (fundos claros); de reserva |
| `favicon.svg`, `favicon.ico` | favicon (o `.ico` também está na raiz) |
| `apple-touch-icon.png` | 180×180, sem transparência |
| `og-image-1200x630.png` | imagem de partilha (`og:image`, `twitter:card`) |
| `pinchaplay-icon-128.png`, `pinchaplay-icone.svg` | ícone do PinchaPlay (mostrado a 72 px) |
| `pinchahide-icon-128.png`, `pinchahide-icone.svg` | ícone do PinchaHide (estado ativo) |
| `screens/` | capturas das apps → `screens/README.md` |

**Regras**
- Só PNG ou SVG locais. SVG sem scripts nem ligações externas (os SVG da v2 têm só metadados C2PA).
- Em cada `<img>`: `width`, `height` e `alt` (vazio só para imagens decorativas, como o ícone ao lado do nome da app).
- O manípulo livre nunca vai sobre fundo claro. Logótipo horizontal com pelo menos 140 px de largura.
- Ficheiros da v1 apagados a 9/11/2026 (histórico do git e `identidade-visual/v1-backup`). Ícones novos: skill `pinchavelho-logo`.
