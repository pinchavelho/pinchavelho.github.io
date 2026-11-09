# _ferramentas/ — gerador do site (não é publicado)

> Documentação interna para pessoas e para o bot Grok. As pastas começadas por `_` não são publicadas pelo GitHub Pages.

**O que existe**

| Ficheiro | Para quê |
|---|---|
| `gerar_site.py` | Escreve **todas** as páginas `.html` (EN e PT), o `404.html`, os redirecionamentos dos endereços antigos e o `sitemap.xml` |
| `textos/TERMOS-1.8-EN-PT.md` | Termos de Venda e EULA do Ritmello 1.8 (a extensão tem de levar o mesmo texto na próxima 0.0.x) |
| `textos/PRIVACIDADE-1.6-EN-PT.md` | Política de Privacidade do Ritmello 1.6 (a extensão tem de levar o mesmo texto na próxima 0.0.x) |
| `textos/TRANSPARENCIA-EN-PT.md` | Relatório de transparência do Ritmello (origem: `ritmello/loja/transparencia/` nos ficheiros do projeto). Atualizar o histórico em cada versão |

**Como usar:** na raiz do repositório, `python3 -I _ferramentas/gerar_site.py .` e depois o `check_site.py` da skill `pinchavelho-site`.

**Valores num só sítio** (bloco `CONFIG` no topo do script):
- `RITMELLO_CHECKOUT`: link do checkout da Polar do produto "Ritmello Pro". `None` = botões "brevemente". **Nunca** acrescentar `custom_field_data` (pré-marcaria a caixa de renúncia). Os botões levam só `?amount=`.
- `RITMELLO_VALORES`, `MIN_ATUAL`, `MIN_DEPOIS`, `FIM_MIN`, `INICIO_DEPOIS`: preço à escolha. A 1/02/2027 mudar para `(299, 399, 599)` e os mínimos, e gerar de novo.
- `VENDEDOR_*`: dados do vendedor, iguais aos Termos e à Política.

**Regras**
- Os textos legais em `textos/` só mudam quando mudam dentro da extensão (mesma versão e data). Usar a skill `pinchavelho-legal`.
- O gerador não pode escrever JavaScript nem recursos de outro domínio (a CSP bloqueia e viola os valores da marca).
- Nunca usar "donativo"/"donation" nos textos do preço.
