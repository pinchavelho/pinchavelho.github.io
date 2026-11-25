# assets/video

Os vídeos curtos (Shorts) de cada app aparecem nas páginas /pinchaplay/ e /pinchahide/.

- `pinchaplay-short.mp4` e `pinchahide-short.mp4`: versões leves para o site (720x1280, H.264, **sem som**), feitas a partir dos Shorts publicados no YouTube.
  - PinchaPlay: original `pinchaplay-short-01-velocidade_v4.mp4`, SHA-256 c3aa921a9138e634b6a869b3b777c30f465b0f987ebdc78a73039cbfd2e56169
  - PinchaHide: original `pinchahide-short-01-recusa-cookies_v4.mp4`, SHA-256 085ebcfff215dcf9a7b4f5bf6fb62e4852779f131fc1c8df31871d2d6fb8cc9d
  - O som foi tirado de propósito: as páginas são uma demonstração sem voz, e assim a música da Biblioteca de Áudio do YouTube não sai do YouTube.
- SHA-256 dos ficheiros do site: `pinchaplay-short.mp4` c045ca0cd23b70084c6f117618c29b23d413fa38b0771093e166ad523a679fd0; `pinchahide-short.mp4` d85448958d5f8174229aec5237f2f66141153bd2d6d05bb5c83fcbd3ee3072cb
- `*-short-poster.jpg`: a imagem que aparece antes de carregar em play.

Regras:
- O site serve os vídeos ele próprio, com `media-src 'self'` na CSP. Não se incorpora o leitor do YouTube, porque esse leitor faz pedidos e guarda dados da Google, e o site promete "No tracking". O YouTube aparece só como link de texto.
- `preload="none"`: o vídeo só se descarrega quando a pessoa carrega em play.
- Para pôr um vídeo novo, grava-se com outro nome (ex.: `-short-02`) e muda-se o `SHORTS` em `_ferramentas/gerar_site.py`.
