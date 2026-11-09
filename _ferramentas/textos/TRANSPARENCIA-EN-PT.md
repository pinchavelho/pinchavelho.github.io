<!-- Origem: /mnt/project-files/ritmello/loja/transparencia/PAGINA-TRANSPARENCIA-EN-PT.md (9/11/2026). EN, depois --- , depois PT. -->
# Ritmello transparency report

**In short:** Ritmello only enters a page when you click its icon or press Alt+Shift+R. Your settings, bookmarks and time saved stay on your computer. The only connection Ritmello makes by itself is checking your Pro key with Polar, and only after you enter a key.

## Permissions and why

| Permission | Why |
|---|---|
| `storage` | Remembers your settings, shortcuts, bookmarks, time saved, the trial start date and your Pro key on this computer only (not synced). |
| `activeTab` | Lets Ritmello into the current tab only after you click its icon or press Alt+Shift+R; access ends when you leave the page. |
| `scripting` | Puts Ritmello's own packaged controls into the page you chose (and into sites you set to Always on, with Pro). No remote code. |
| `https://api.polar.sh/*` | Checks your Pro licence key with Polar, the shop, only after you enter a key, and again about once a day. |
| `https://*/*`, `http://*/*` (optional) | Never granted at install. Asked one site at a time, only when you choose "Always on for this site" (Pro) and accept Chrome's prompt. |

## Network connections (version 1.0.0, tested 9 November 2026)

| Address | When |
|---|---|
| `api.polar.sh` | Only after you enter a Pro key: activation, then a check about once a day. No browsing data is sent. |
| `buy.polar.sh` | Only when you click Buy: the checkout opens in a new tab. |
| `pinchavelho.github.io` | Only if you click the link to the privacy policy online. |

We opened test pages with video and audio, used the shortcuts, opened every Ritmello page, clicked Buy and entered a test key, and recorded every request. Nothing else was contacted.

## Where your data is

On your computer only: settings, shortcuts, bookmarks, time saved, trial date and Pro key in Chrome's extension storage, and the interface language you picked. Delete them in Ritmello's Options or by uninstalling Ritmello. Sites you set to "Always on" are kept by Chrome as a permission; remove them in Options or in Chrome.

## Chrome Web Store

The privacy practices on the store listing are our own declaration, filled in to match this report. The link to the listing will be added here once the store approves Ritmello.

## Check it yourself

1. Open `chrome://extensions`, find Ritmello and click **Details** to see the exact permissions Chrome granted.
2. Turn on **Developer mode**, click **Inspect views: service worker**, open the **Network** tab and use Ritmello: only the addresses above can appear.
3. For a full log, open `chrome://net-export`, record while you use Ritmello and open the file in the NetLog viewer.

## History

| Version | Date | SHA-256 of the package sent to the store | Result |
|---|---|---|---|
| 1.0.0 | 9 November 2026 | `e532065df56931c45234a50bb75b699cef0478b20c730c31395f7d48dc603664` | Automatic checks passed |

The Chrome Web Store repackages and signs each upload, so the file you download from the store has a different checksum; the files inside are the same.

These are checks we ran ourselves. They are not an independent audit or a certification.

## Report a problem

Found something that doesn't match this page? Write to opinchavelho@gmail.com. We answer, fix it and note it here.

---

# Relatório de transparência do Ritmello

**Em resumo:** o Ritmello só entra numa página quando clica no ícone ou carrega em Alt+Shift+R. As suas definições, marcadores e tempo poupado ficam no seu computador. A única ligação que o Ritmello faz sozinho é verificar a sua chave Pro com a Polar, e só depois de introduzir uma chave.

## Permissões e porquê

| Permissão | Porquê |
|---|---|
| `storage` | Guarda as suas definições, atalhos, marcadores, tempo poupado, a data de início do teste e a sua chave Pro só neste computador (sem sincronizar). |
| `activeTab` | Deixa o Ritmello entrar no separador atual só depois de clicar no ícone ou carregar em Alt+Shift+R; o acesso acaba quando sai da página. |
| `scripting` | Põe os controlos do próprio pacote do Ritmello na página que escolheu (e nos sites com "Ativar sempre", no Pro). Sem código remoto. |
| `https://api.polar.sh/*` | Verifica a sua chave Pro com a Polar, a loja, só depois de introduzir uma chave, e de novo cerca de uma vez por dia. |
| `https://*/*`, `http://*/*` (opcionais) | Nunca são dadas na instalação. São pedidas um site de cada vez, só quando escolhe "Ativar sempre neste site" (Pro) e aceita o pedido do Chrome. |

## Ligações de rede (versão 1.0.0, testada a 9 de novembro de 2026)

| Endereço | Quando |
|---|---|
| `api.polar.sh` | Só depois de introduzir uma chave Pro: ativação e, depois, uma verificação cerca de uma vez por dia. Não envia dados de navegação. |
| `buy.polar.sh` | Só quando clica em Comprar: o checkout abre num separador novo. |
| `pinchavelho.github.io` | Só se clicar no link da política de privacidade online. |

Abrimos páginas de teste com vídeo e áudio, usámos os atalhos, abrimos todas as páginas do Ritmello, clicámos em Comprar, introduzimos uma chave de teste e registámos todos os pedidos. Não houve mais nenhum endereço.

## Onde ficam os seus dados

Só no seu computador: definições, atalhos, marcadores, tempo poupado, data do teste e chave Pro, no armazenamento da extensão no Chrome, e o idioma da interface que escolheu. Apague-os nas opções do Ritmello ou desinstalando-o. Os sites com "Ativar sempre" ficam guardados pelo Chrome como uma autorização; retire-os nas opções ou no Chrome.

## Chrome Web Store

As práticas de privacidade na ficha da loja são uma declaração nossa, preenchida de acordo com este relatório. O link para a ficha é acrescentado aqui quando a loja aprovar o Ritmello.

## Verifique por si

1. Abra `chrome://extensions`, procure o Ritmello e clique em **Detalhes** para ver as permissões exatas que o Chrome deu.
2. Ligue o **Modo de programador**, clique em **Inspecionar vistas: service worker**, abra o separador **Network** e use o Ritmello: só podem aparecer os endereços acima.
3. Para um registo completo, abra `chrome://net-export`, grave enquanto usa o Ritmello e abra o ficheiro no visualizador NetLog.

## Histórico

| Versão | Data | SHA-256 do pacote enviado à loja | Resultado |
|---|---|---|---|
| 1.0.0 | 9 de novembro de 2026 | `e532065df56931c45234a50bb75b699cef0478b20c730c31395f7d48dc603664` | Verificações automáticas aprovadas |

A Chrome Web Store volta a empacotar e assina cada envio, por isso o ficheiro descarregado da loja tem outra soma de verificação; os ficheiros lá dentro são os mesmos.

São verificações feitas por nós. Não são uma auditoria independente nem uma certificação.

## Comunicar um problema

Encontrou algo que não bate certo com esta página? Escreva para opinchavelho@gmail.com. Respondemos, corrigimos e registamos aqui.
