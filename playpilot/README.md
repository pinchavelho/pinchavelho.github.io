# playpilot/ — página da app PlayPilot (em inglês)

> Documentação interna para pessoas e para o bot Grok. Não é publicada no site.

**O que existe**

| Ficheiro | Endereço | Conteúdo |
|---|---|---|
| `index.html` | `/playpilot/` | página de produto: o que faz, capturas, Free vs Pro, preço, teste grátis, privacidade, botões de loja e compra |
| `privacy.html` | `/playpilot/privacy.html` | Política de Privacidade |
| `terms.html` | `/playpilot/terms.html` | Termos de Venda e Licença (EULA) |
| `refund.html` | `/playpilot/refund.html` | Política de Reembolso |

A versão portuguesa está em `/pt/playpilot/` com os mesmos nomes de ficheiro.

**Regras**

- Qualquer alteração aqui tem de ser feita também em `/pt/playpilot/`.
- Textos legais: só com a skill `pinchavelho-legal`. Regras do negócio que têm de bater certo em todos os textos: pagamento único, sem subscrição; teste grátis sem registo; sem reembolso por desistência depois da compra porque o cliente pede o acesso imediato e aceita perder o direito de livre resolução (caixa obrigatória no checkout); a garantia legal de conformidade (DL 84/2021) mantém-se sempre.
- Preços com IVA incluído e com a data de fim do preço de lançamento. Ao mudar preço, teste ou reembolso, procurar **todas** as ocorrências em EN e PT, incluindo a home e o aviso legal.
- O botão "Chrome Web Store — coming soon" (`.btn.pending`) fica até haver o link real da loja.
- O botão de compra aponta para o checkout da Polar (plataforma ainda por confirmar).
- Explicar cada permissão da extensão em linguagem simples.

**Pendente (decidido, ainda não aplicado)**

- A app chama-se agora **Ritmello by Pinchavelho**: esta pasta vai passar a `/ritmello/` (e `/pt/ritmello/`), com nome, título, menu, rodapé, sitemap e aviso legal atualizados.
- A função de **transferir vídeos é removida**: retirar dos textos ("downloads"), da tabela e das capturas.
- Teste grátis do Pro: **15 dias** (aqui ainda diz 7).
