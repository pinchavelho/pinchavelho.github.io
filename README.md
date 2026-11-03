# Site Pinchavelho — guia do repositório

> Este ficheiro é para pessoas e para assistentes (ex.: o bot Grok) que precisem de perceber o site antes de o alterar. **Não é publicado no site** (ver "Documentação interna" no fim).

**O que é:** o site público da Pinchavelho, estúdio independente de uma pessoa em Portugal (Jose Pinhao, empresário em nome individual). Fazemos ferramentas pequenas, simples e úteis, sem rastreio e sem publicidade.

- Endereço: https://pinchavelho.github.io
- Repositório: `pinchavelho/pinchavelho.github.io` (público), publicado pelo GitHub Pages a partir do ramo `main`.
- Contacto: opinchavelho@gmail.com · X: https://x.com/OPinchavelho

## Regras inegociáveis do site

1. **HTML + CSS estático. Sem JavaScript**, nem em linha nem em ficheiro.
2. **Sem cookies, sem analytics, sem pixels, sem recursos de terceiros** (fontes, imagens, iframes, CDNs, widgets). Tudo é servido do próprio site.
3. **CSP restritiva em todas as páginas**, exatamente esta:
   ```html
   <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; style-src 'self'; font-src 'self'; base-uri 'none'; form-action 'none'">
   <meta name="referrer" content="strict-origin-when-cross-origin">
   ```
4. **Um único CSS:** `/assets/css/site.css`. Sem `style=""` nem `<style>` nas páginas (a CSP bloqueia-os).
5. **Bilingue:** cada página em inglês (referência) tem uma gémea em português de Portugal em `/pt/` com o mesmo caminho. Ambas têm `hreflang` (`en`, `pt-PT`, `x-default` → EN) e `canonical`. Nunca português do Brasil.
6. **Rodapé igual em todas as páginas:** links legais da app, aviso legal, sobre, a frase "This website uses no cookies, no analytics and no third-party resources.", © e email.
7. **Imagens locais** (PNG/SVG) com `width`, `height` e `alt`.
8. **Sem** formulários, comentários, newsletter, chat, contadores, links de afiliados.
9. **Marketing sem dark patterns:** sem falsa urgência, contadores falsos ou opções pré-marcadas.
10. **Nada é publicado sem a confirmação do Jose.** Um push para `main` publica de imediato. Trabalhar sempre num ramo e abrir um pull request.

## Marca (versão atual v1)

O site usa a identidade visual v1. Uma nova identidade (v2, "Manípulo") está preparada mas **ainda não foi aprovada**; até lá não se muda nada visual.

| Nome | Hex | Uso |
|---|---|---|
| Noite | `#0F1B2D` | Texto no claro, fundo no escuro |
| Âmbar | `#FFB020` | Destaques (barra dos H2, linha dos botões). Nunca como texto sobre fundo claro |
| Azul | `#1E6FD9` | Centro do símbolo; base dos links |
| Névoa | `#F5F7FA` | Fundo claro; texto no escuro |
| Verde | `#22A06B` | Só decorativo |

- Tipos de letra: **Space Grotesk** (títulos) e **Inter** (texto), ficheiros locais em `/assets/fonts/`.
- Modo claro e escuro automático (`prefers-color-scheme`).
- Tom: curto, honesto, concreto. Dizer o que a app faz e o que não faz. Sem superlativos vazios.
- Detalhe das cores e componentes: `assets/css/README.md`.

## Estrutura

```
/                     páginas gerais em inglês
├── index.html        início (lista de produtos)
├── about.html        sobre
├── legal-notice.html aviso legal (dados do vendedor)
├── 404.html          página de erro
├── favicon.ico
├── robots.txt        permite tudo e aponta para o sitemap
├── sitemap.xml       todas as páginas EN e PT com alternates de idioma
├── _config.yml       só para não publicar os .md (ver abaixo)
├── assets/           CSS, fontes e imagens            → assets/README.md
├── playpilot/        página e textos legais da app    → playpilot/README.md
└── pt/               espelho em português de Portugal → pt/README.md
```

Cada pasta tem o seu `README.md` com o que lá existe, as regras e como usar.

## Estado atual e pendentes (3 nov 2026)

O site ainda mostra a situação antiga. Já foi decidido, mas **ainda não está no site**:

- **PlayPilot passa a chamar-se "Ritmello by Pinchavelho".** A pasta `/playpilot/` vai mudar para `/ritmello/` (com redirecionamento a decidir).
- No Ritmello a **função de transferir vídeos é removida**; a página ainda fala em "downloads" e tem a captura `playpilot_03_download`.
- **Teste grátis do Pro: 15 dias** (o site ainda diz 7 dias).
- Preço Pro: 1,49 € até 31/01/2027, depois 1,99 €, pagamento único (já está no site).
- **Nova app: "Vedello by Pinchavelho"** (recusa banners de cookies e bloqueia rastreadores). Ainda não tem página.
- Plataforma de vendas: o botão de compra usa a Polar (polar.sh); a escolha final ainda está por decidir.

Ao corrigir qualquer destes pontos, atualizar EN e PT, textos legais, home, aviso legal e `sitemap.xml` ao mesmo tempo.

## Como fazer alterações

1. Criar um ramo a partir de `main`.
2. Editar EN e PT juntos. Reutilizar classes do CSS antes de criar novas.
3. Ao criar uma pasta nova, criar também o `README.md` dela.
4. Verificar antes de pedir aprovação:
   - correr o verificador da skill `pinchavelho-site` (`check_site.py`): CSP, hreflang, canonical, gémeas EN/PT, `alt`, ausência de JavaScript;
   - abrir localmente (`python3 -m http.server`) e ver em claro, escuro e a 375 px de largura;
   - confirmar que nada vem de outro domínio além dos links normais.
5. Abrir um pull request e esperar pela aprovação do Jose. Não fazer merge sozinho.

### Adicionar uma app nova
Copiar `/playpilot/` e `/pt/playpilot/` para `/<app>/` e `/pt/<app>/`, reescrever tudo (não deixar texto da outra app), acrescentar o cartão na home EN e PT, o item no menu de **todas** as páginas, o produto no aviso legal e 8 entradas no `sitemap.xml` (4 páginas × 2 idiomas). Os textos legais seguem a skill `pinchavelho-legal`.

## Documentação interna (porque os .md não aparecem no site)

O GitHub Pages usa o Jekyll para construir o site. Sem configuração, os ficheiros `.md` seriam publicados: como texto simples, ou convertidos em páginas (ex.: `/README.html`) pelos plugins que o GitHub Pages ativa por defeito.

Para o evitar:

- o ficheiro `.nojekyll` foi removido, para o Jekyll ler o `_config.yml`;
- o `_config.yml` exclui `*.md` e `**/*.md`, por isso **nenhum `.md` chega ao site publicado**. Sem esta regra, os plugins do GitHub Pages transformariam cada `README.md` numa página (ex.: `/assets/` passaria a mostrar este guia);
- o `_config.yml` também tem `theme: null`, para o GitHub Pages não acrescentar o CSS do tema por defeito (`/assets/css/style.css`);
- as páginas `.html` não têm "front matter" (`---` no topo), por isso o Jekyll copia-as **sem alterações**. Nunca pôr `---` no início de um `.html`;
- ficheiros e pastas começados por `_` ou `.` também não são publicados.

Atenção: o repositório é público, por isso estes `.md` continuam visíveis em github.com. Não escrever aqui nada privado (chaves, senhas, dados pessoais além dos que já estão no aviso legal).
