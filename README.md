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

## Marca (identidade v2 «Manípulo», aprovada a 4/11/2026)

O site usa a identidade v2: o manípulo âmbar (símbolo), o logótipo horizontal claro/escuro e os ícones do PinchaPlay (play) e do PinchaHide (traço de "proibido"). Os ficheiros vêm de `identidade-visual/fase5-final/` (pasta do projeto) e as regras estão na skill `pinchavelho-brand` e no `LOGO-GUIA.md`. Os ficheiros da v1 foram apagados do site (ficam no histórico do git e em `identidade-visual/v1-backup`).

| Nome | Hex | Uso |
|---|---|---|
| Noite | `#0F1B2D` | Texto no claro, fundo no escuro, placa dos ícones |
| Âmbar | `#FFB020` | Manípulo e destaques (barra dos H2, linha dos botões). Nunca como texto sobre fundo claro |
| Azul | `#1E6FD9` | Só links (já não entra no símbolo) |
| Névoa | `#F5F7FA` | Fundo claro; texto no escuro |
| Verde | `#22A06B` | Só decorativo |

- Tipos de letra: **Space Grotesk** (títulos) e **Inter** (texto), ficheiros locais em `/assets/fonts/`.
- Modo claro e escuro automático (`prefers-color-scheme`).
- Tom: curto, honesto, concreto. Dizer o que a app faz e o que não faz. Sem superlativos vazios.
- Detalhe das cores e componentes: `assets/css/README.md`.

## Estrutura

```
/                     páginas gerais em inglês
├── index.html        início (as duas apps, valores, "um negócio justo")
├── about.html        sobre
├── legal-notice.html aviso legal (dados do vendedor, vendas pela Polar)
├── 404.html          página de erro (EN e PT na mesma página)
├── favicon.ico
├── robots.txt        permite tudo e aponta para o sitemap
├── sitemap.xml       todas as páginas EN e PT com alternates de idioma
├── _config.yml       só para não publicar os .md (ver abaixo)
├── _ferramentas/     gerador das páginas e textos legais de origem (não é publicado) → _ferramentas/README.md
├── assets/           CSS, fontes e imagens                        → assets/README.md
├── pinchaplay/       página e textos legais do PinchaPlay          → pinchaplay/README.md
├── pinchahide/       página e textos legais do PinchaHide          → pinchahide/README.md
├── playpilot/, ritmello/, vedello/  só redirecionamentos (nomes antigos) → README.md de cada uma
└── pt/               espelho em português de Portugal             → pt/README.md
```

Cada pasta tem o seu `README.md` com o que lá existe, as regras e como usar.

## Como as páginas são feitas

**Todas as páginas `.html` são geradas** por `_ferramentas/gerar_site.py` (EN e PT, cabeçalho, rodapé, sitemap). Para mudar um texto, um preço ou o link de compra: editar o script e correr, na raiz,

```
python3 -I _ferramentas/gerar_site.py .
```

Editar um `.html` à mão funciona, mas a próxima geração apaga a alteração. Os Termos, a Privacidade e a Transparência das duas apps vêm de `_ferramentas/textos/`.

## Estado (15 nov 2026)

- Apps: **PinchaPlay** (velocidade e som de vídeo) e **PinchaHide** (banners de cookies), as duas publicadas na Chrome Web Store. O nome antigo da app de vídeo foi retirado; os endereços antigos redirecionam para `/pinchaplay/`.
- O PinchaPlay **não transfere vídeos** (função removida). O site não a anuncia em lado nenhum.
- Preço Pro de cada app: **pague o que achar justo, mínimo 1,99 € até 31/01/2027 e 2,99 € depois**, IVA incluído, pagamento único. Nunca "donativo".
- Teste Pro: **15 dias**, sem registo.
- Compra pela **Polar**. Os links de checkout estão no gerador: `PINCHAPLAY_CHECKOUT` e `PINCHAHIDE_CHECKOUT` (com `None`, os botões aparecem como "brevemente", sem ligação). O link **nunca** leva `custom_field_data` (pré-marcaria a caixa de renúncia).
- **A 1/02/2027:** mudar no gerador `PINCHAPLAY_VALORES` (usado pelas duas apps) para `(299, 399, 599)` e os mínimos (`MIN_ATUAL`/`MIN_DEPOIS`) e gerar de novo.
- Textos legais em vigor (só no site): PinchaPlay Termos 1.12 e Privacidade 1.8; PinchaHide Termos 1.1 e Privacidade 1.0. As versões dentro dos pacotes (Termos 1.11 e 1.0) ficam em `_ferramentas/textos/` como histórico.
- As capturas das duas apps são as da loja (sem número de versão nem marcas de terceiros), em `assets/img/screens/`.

## Como fazer alterações

1. Criar um ramo a partir de `main`.
2. Editar o gerador (EN e PT juntos) e corrê-lo. Reutilizar classes do CSS antes de criar novas.
3. Ao criar uma pasta nova, criar também o `README.md` dela.
4. Verificar antes de pedir aprovação:
   - correr o verificador da skill `pinchavelho-site` (`check_site.py`): CSP, hreflang, canonical, gémeas EN/PT, `alt`, ausência de JavaScript;
   - abrir localmente (`python3 -m http.server`) e ver em claro, escuro e a 375 px de largura;
   - confirmar que nada vem de outro domínio além dos links normais.
5. Abrir um pull request e esperar pela aprovação do Jose. Não fazer merge sozinho.

### Adicionar uma app nova
No gerador: uma função de página nova (copiar `pinchaplay()` e reescrever tudo, sem deixar texto da outra app), o cartão em `product_card()`, o item no menu (`page()`), o produto no aviso legal e as páginas em `PAGES` (sitemap). Criar `/<app>/README.md` e `/pt/<app>/README.md`. Os textos legais seguem a skill `pinchavelho-legal`.

## Documentação interna (porque os .md não aparecem no site)

O GitHub Pages usa o Jekyll para construir o site. Sem configuração, os ficheiros `.md` seriam publicados: como texto simples, ou convertidos em páginas (ex.: `/README.html`) pelos plugins que o GitHub Pages ativa por defeito.

Para o evitar:

- o ficheiro `.nojekyll` foi removido, para o Jekyll ler o `_config.yml`;
- o `_config.yml` exclui `*.md` e `**/*.md`, por isso **nenhum `.md` chega ao site publicado**. Sem esta regra, os plugins do GitHub Pages transformariam cada `README.md` numa página (ex.: `/assets/` passaria a mostrar este guia);
- o `_config.yml` também tem `theme: null`, para o GitHub Pages não acrescentar o CSS do tema por defeito (`/assets/css/style.css`);
- as páginas `.html` não têm "front matter" (`---` no topo), por isso o Jekyll copia-as **sem alterações**. Nunca pôr `---` no início de um `.html`;
- ficheiros e pastas começados por `_` ou `.` também não são publicados.

Atenção: o repositório é público, por isso estes `.md` continuam visíveis em github.com. Não escrever aqui nada privado (chaves, senhas, dados pessoais além dos que já estão no aviso legal).
