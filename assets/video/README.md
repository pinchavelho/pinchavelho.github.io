# assets/video

Os vídeos curtos (Shorts) de cada app aparecem nas páginas /pinchaplay/ e /pinchahide/.

- `pinchaplay-short.mp4` e `pinchahide-short.mp4`: versões leves para o site (720x1280, H.264, **sem som**), feitas a partir dos Shorts publicados no YouTube.
  - PinchaPlay: original c3aa921a…
  - PinchaHide: original 085ebcff…
  - O som foi tirado de propósito: as páginas são uma demonstração sem voz, e assim a música da Biblioteca de Áudio do YouTube não sai do YouTube.
- `*-short-poster.jpg`: a imagem que aparece antes de carregar em play.

Regras:
- O site serve os vídeos ele próprio, com `media-src 'self'` na CSP. Não se incorpora o leitor do YouTube, porque esse leitor faz pedidos e guarda dados da Google, e o site promete "No tracking". O YouTube aparece só como link de texto.
- `preload="none"`: o vídeo só se descarrega quando a pessoa carrega em play.
- Para pôr um vídeo novo, grava-se com outro nome (ex.: `-short-02`) e muda-se o `SHORTS` em `_ferramentas/gerar_site.py`.
