<!-- Origem: /mnt/project-files/vedello/loja/transparencia/PAGINA-TRANSPARENCIA-EN-PT.md (11/11/2026). EN, depois --- , depois PT. -->
# PinchaHide transparency report

**In short:** PinchaHide answers cookie banners and blocks trackers inside your browser, with rules bundled in the extension. Your settings, counts and history stay on your computer. The only connection PinchaHide makes by itself is checking your Pro key with Polar, and only after you enter a key.

## Permissions and why

| Permission | Why |
|---|---|
| `storage` | Keeps your settings, counts, history (Pro), the trial start date and your Pro key only on this computer (not synced). |
| `declarativeNetRequest` | Lets Chrome itself apply the rules bundled in PinchaHide: send the Global Privacy Control signal and, with Pro, block trackers and strip tracking parameters from addresses. PinchaHide does not see the requests. |
| `activeTab` | Shows in the popup what PinchaHide did on the current tab and lets "Copy clean link" work on the tab where you click. |
| `scripting` | Adds the package's own scripts to pages to answer banners through the site's consent tool and send the GPC signal. No remote code. |
| `alarms` | Ends a timed pause and re-checks the Pro key about once a day. |
| `contextMenus` | Adds "Copy clean link" to the right-click menu on a link (Pro). |
| `privacy` (optional) | Asked only when you turn on a Chrome setting in Options: turn off third-party cookies, ad APIs and WebRTC leaks, and send Do Not Track (Pro). |
| `cookies` (optional) | Asked only when you turn on "Clear a site's cookies when its last tab closes" (Pro). It only deletes cookies; it never reads them for anything else. |
| All sites (`<all_urls>`) | Cookie banners appear on any site, so PinchaHide runs on every page to find the banner and press Reject. It only looks at the banner (and, with Pro, at newsletter boxes and at the address you copy). Nothing leaves your browser. |

## Network connections (version 1.0.0, tested 11 November 2026)

| Address | When |
|---|---|
| `api.polar.sh` | Only after you enter a Pro key: activation, then a check about once a day. No browsing data is sent. |
| `buy.polar.sh` | Only when you tick the box and click Continue on the Pro screen: the checkout opens in a new tab. |
| `pinchavelho.github.io` | Only if you click a link to our site. |

We opened local test pages with cookie banners from several consent platforms, a newsletter pop-up, a paywall and links with tracking parameters, copied an address, opened every PinchaHide page, clicked Continue on the Pro screen and entered a test key, and recorded every request with the internet blocked. Nothing else was contacted. The tracker lists bundled in PinchaHide name many tracking services; those names are what PinchaHide blocks, not addresses it contacts.

## Where your data is

On your computer only: settings, per-site exceptions, counts, history (Pro), trial date and Pro key in Chrome's extension storage; what was done on each open tab in memory until the tab closes; and the interface language you picked. Delete the history in Options, remove the key with "Remove key", or uninstall PinchaHide to delete everything.

## Chrome Web Store

The privacy practices on the store listing are our own declaration, filled in to match this report. The link to the listing will be added here once the store approves PinchaHide.

## Check it yourself

1. Open `chrome://extensions`, find PinchaHide and click **Details** to see the exact permissions Chrome granted.
2. Turn on **Developer mode**, click **Inspect views: service worker**, open the **Network** tab and use PinchaHide: only the addresses above can appear.
3. For a full log, open `chrome://net-export`, record while you browse with PinchaHide and open the file in the NetLog viewer.

## History

| Version | Date | SHA-256 of the package sent to the store | Result |
|---|---|---|---|
| 1.0.0 | 11 November 2026 | `64188cf14ea3feab885b964bb8b200a8dc00a22f0ed11e3c46f4bc48580f40ff` | Automatic checks passed |

The Chrome Web Store repackages and signs each upload, so the file you get from the store has a different checksum; the files inside are the same.

These are checks we ran ourselves. They are not an independent audit or a certification.

## Report a problem

Found something that doesn't match this page? Write to opinchavelho@gmail.com. We answer, fix it and note it here.

---

# Relatório de transparência do PinchaHide

**Em resumo:** o PinchaHide responde aos banners de cookies e bloqueia rastreadores dentro do seu navegador, com regras incluídas na extensão. As suas definições, contagens e histórico ficam no seu computador. A única ligação que o PinchaHide faz sozinho é verificar a sua chave Pro com a Polar, e só depois de introduzir uma chave.

## Permissões e porquê

| Permissão | Porquê |
|---|---|
| `storage` | Guarda as suas definições, as contagens, o histórico (Pro), a data de início do teste e a sua chave Pro só neste computador (sem sincronizar). |
| `declarativeNetRequest` | Deixa o próprio Chrome aplicar as regras incluídas no PinchaHide: enviar o sinal Global Privacy Control e, no Pro, bloquear rastreadores e tirar parâmetros de rastreio dos endereços. O PinchaHide não vê os pedidos. |
| `activeTab` | Mostra no popup o que o PinchaHide fez no separador atual e deixa "Copiar link limpo" funcionar no separador onde clica. |
| `scripting` | Põe os scripts do próprio pacote nas páginas para responder aos banners pela ferramenta de consentimento do site e enviar o sinal GPC. Sem código remoto. |
| `alarms` | Termina uma pausa com hora marcada e volta a verificar a chave Pro cerca de uma vez por dia. |
| `contextMenus` | Acrescenta "Copiar link limpo" ao menu do botão direito sobre um link (Pro). |
| `privacy` (opcional) | Só pedida quando liga uma definição do Chrome nas Opções: desligar cookies de terceiros, APIs de publicidade e fugas de WebRTC, e enviar Do Not Track (Pro). |
| `cookies` (opcional) | Só pedida quando liga "Limpar os cookies de um site ao fechar o último separador" (Pro). Só apaga cookies; não os lê para mais nada. |
| Todos os sites (`<all_urls>`) | Os banners de cookies aparecem em qualquer site, por isso o PinchaHide corre em todas as páginas para encontrar o banner e carregar em Rejeitar. Olha só para o banner (e, no Pro, para caixas de newsletter e para o endereço que copia). Nada sai do navegador. |

## Ligações de rede (versão 1.0.0, testada a 11 de novembro de 2026)

| Endereço | Quando |
|---|---|
| `api.polar.sh` | Só depois de introduzir uma chave Pro: ativação e, depois, uma verificação cerca de uma vez por dia. Não envia dados de navegação. |
| `buy.polar.sh` | Só quando marca a caixa e carrega em Continuar no ecrã do Pro: o checkout abre num separador novo. |
| `pinchavelho.github.io` | Só se clicar num link para o nosso site. |

Abrimos páginas de teste locais com banners de várias plataformas de consentimento, uma caixa de newsletter, um paywall e links com parâmetros de rastreio, copiámos um endereço, abrimos todas as páginas do PinchaHide, carregámos em Continuar no ecrã do Pro, introduzimos uma chave de teste e registámos todos os pedidos, com a internet bloqueada. Não houve mais nenhum endereço. As listas de rastreadores incluídas no PinchaHide nomeiam muitos serviços de rastreio: são o que o PinchaHide bloqueia, não endereços que contacta.

## Onde ficam os seus dados

Só no seu computador: definições, exceções por site, contagens, histórico (Pro), data do teste e chave Pro, no armazenamento da extensão no Chrome; o que foi feito em cada separador aberto, em memória até o separador fechar; e o idioma da interface que escolheu. Apague o histórico nas Opções, retire a chave com "Remover chave", ou desinstale o PinchaHide para apagar tudo.

## Chrome Web Store

As práticas de privacidade na ficha da loja são uma declaração nossa, preenchida de acordo com este relatório. O link para a ficha é acrescentado aqui quando a loja aprovar o PinchaHide.

## Verifique por si

1. Abra `chrome://extensions`, procure o PinchaHide e clique em **Detalhes** para ver as permissões exatas que o Chrome deu.
2. Ligue o **Modo de programador**, clique em **Inspecionar vistas: service worker**, abra o separador **Network** e use o PinchaHide: só podem aparecer os endereços acima.
3. Para um registo completo, abra `chrome://net-export`, grave enquanto navega com o PinchaHide e abra o ficheiro no visualizador NetLog.

## Histórico

| Versão | Data | SHA-256 do pacote enviado à loja | Resultado |
|---|---|---|---|
| 1.0.0 | 11 de novembro de 2026 | `64188cf14ea3feab885b964bb8b200a8dc00a22f0ed11e3c46f4bc48580f40ff` | Verificações automáticas aprovadas |

A Chrome Web Store volta a empacotar e assina cada envio, por isso o ficheiro que recebe da loja tem outra soma de verificação; os ficheiros lá dentro são os mesmos.

São verificações feitas por nós. Não são uma auditoria independente nem uma certificação.

## Comunicar um problema

Encontrou algo que não bate certo com esta página? Escreva para opinchavelho@gmail.com. Respondemos, corrigimos e registamos aqui.
