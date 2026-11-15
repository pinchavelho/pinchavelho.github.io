#!/usr/bin/env python3
"""Gera todas as páginas .html do site Pinchavelho (EN e pt-PT) a partir deste ficheiro.

Uso (na raiz do repositório):  python3 -I _ferramentas/gerar_site.py .

- Pastas e ficheiros começados por "_" não são publicados pelo GitHub Pages, por isso
  esta pasta fica só no repositório. Ver _ferramentas/README.md.
- O site continua a ser HTML + CSS estático: este script só escreve os ficheiros.
- Valores que mudam (link do checkout, preços, datas) estão no bloco CONFIG, num só sítio.
"""
import html
import os
import re
import sys

# ---------------------------------------------------------------- CONFIG
SITE = "https://pinchavelho.github.io"
EMAIL = "opinchavelho@gmail.com"
LASTMOD = "2026-11-15"

# Link do checkout da Polar para o produto "PinchaPlay Pro" (Pay what you want).
# None = botões de compra aparecem como "brevemente" (sem ligação). Produto atual criado a 9/11/2026.
# Quando o Jose criar o produto novo, pôr aqui o link (ex.: "https://buy.polar.sh/polar_cl_...")
# e voltar a correr o script. NUNCA acrescentar custom_field_data ao link: pré-marcaria a caixa de renúncia.
# Ficha do PinchaPlay na Chrome Web Store (publicado a 10-11/11/2026).
PINCHAPLAY_CWS = "https://chromewebstore.google.com/detail/lcbdnpliajnokjhmlbgdcaeggbpjpahn"
PINCHAPLAY_CHECKOUT = "https://buy.polar.sh/polar_cl_ysg4lrAleNzT1fhy9MqU7tUREqkss0piC9yqe0KMSBI"  # produto 263e1114-4e1f-451c-8597-481c663d9d75
# PinchaHide (publicado na Chrome Web Store a 15/11/2026) e checkout de produção do PinchaHide Pro
# (produto f30ab9b4-f351-451d-ae23-4075663ed8df). Os mesmos valores rápidos e o mesmo mínimo do PinchaPlay.
PINCHAHIDE_CWS = "https://chromewebstore.google.com/detail/fceapkacofhlmcmojhbkkmlnaofmdlcd"
PINCHAHIDE_CHECKOUT = "https://buy.polar.sh/polar_cl_hFIUGaZVHQu1owWgaa4F7qrd0yRbqNaMbKFA90KrLeo"
# Valores rápidos (cêntimos) das duas apps até 31/01/2027. A 1/02/2027: (299, 399, 599) e MIN_* abaixo.
PINCHAPLAY_VALORES = (199, 299, 499)
MIN_ATUAL = {"en": "€1.99", "pt": "1,99 €"}
MIN_DEPOIS = {"en": "€2.99", "pt": "2,99 €"}
FIM_MIN = {"en": "31 January 2027", "pt": "31 de janeiro de 2027"}
INICIO_DEPOIS = {"en": "1 February 2027", "pt": "1 de fevereiro de 2027"}

# Dados do vendedor: completos (com NIF) só no Aviso legal (regra do Jose, 9/11/2026). Termos e Privacidade têm nome e morada, sem NIF.
VENDEDOR_NOME = "José Augusto Alves Pinhão"
VENDEDOR_MORADA = "Estrada V Centenario Vila Sol I, Bloco B 3CE, 9360-500 Ponta do Sol, Portugal"
VENDEDOR_NIF = "218449283"

CSP = "default-src 'none'; img-src 'self'; style-src 'self'; font-src 'self'; base-uri 'none'; form-action 'none'"
OG_IMG = SITE + "/assets/img/og-image-1200x630.png"

# ---------------------------------------------------------------- helpers
e = html.escape


def euro(cents, lang):
    v = "%d.%02d" % (cents // 100, cents % 100)
    return "€" + v if lang == "en" else v.replace(".", ",") + " €"


def url(lang, path):
    """path EN ('/', '/pinchaplay/', '/about.html') -> path na língua pedida."""
    return path if lang == "en" else "/pt" + path


def linkify(text):
    t = e(text)
    t = re.sub(r"(https?://[^\s<)]+[^\s<).,;:])", r'<a href="\1">\1</a>', t)
    t = re.sub(r"(?<![/\w.])(www\.[a-z0-9.-]+\.[a-z]{2,})(?![\w/])", r'<a href="https://\1">\1</a>', t)
    t = re.sub(r"([\w.+-]+@[\w-]+\.[\w.]+[a-z])", r'<a href="mailto:\1">\1</a>', t)
    return t


T = {
    "en": dict(
        lang="en", skip="Skip to content", home="Home", about="About", nav="Main",
        brand_alt="Pinchavelho, home page", other="PT", other_label="PT – Português", other_lang="pt-PT",
        foot_tag="Small, honest tools. No tracking, no ads. This website uses no cookies, no analytics and no third-party resources.",
        rights="All rights reserved.", privacy="Privacy", terms="Terms & EULA", refunds="Refunds",
        legal="Legal notice", soon="coming soon", cws_soon="Chrome Web Store: coming soon",
        buy_soon="PinchaPlay Pro: purchase opens soon",
    ),
    "pt": dict(
        lang="pt-PT", skip="Saltar para o conteúdo", home="Início", about="Sobre", nav="Principal",
        brand_alt="Pinchavelho, página inicial", other="EN", other_label="EN – English", other_lang="en",
        foot_tag="Ferramentas pequenas e honestas. Sem rastreio, sem publicidade. Este site não usa cookies, analytics nem recursos de terceiros.",
        rights="Todos os direitos reservados.", privacy="Privacidade", terms="Termos e EULA", refunds="Reembolsos",
        legal="Aviso legal", soon="brevemente", cws_soon="Chrome Web Store: brevemente",
        buy_soon="PinchaPlay Pro: compra disponível brevemente",
    ),
}


def page(lang, path, title, desc, body, current=None, noindex=False, alt_path=None, redirect=None):
    t = T[lang]
    alt_path = alt_path or path
    en_url, pt_url = SITE + alt_path, SITE + "/pt" + alt_path
    canon = SITE + url(lang, path)
    other_href = url("pt" if lang == "en" else "en", alt_path)

    def nav_item(label, p, key):
        cur = ' aria-current="page"' if current == key else ""
        return '<li><a href="%s"%s>%s</a></li>' % (url(lang, p), cur, label)

    nav = "".join([
        nav_item(t["home"], "/", "home"),
        nav_item("PinchaPlay", "/pinchaplay/", "pinchaplay"),
        nav_item("PinchaHide", "/pinchahide/", "pinchahide"),
        nav_item(t["about"], "/about.html", "about"),
        '<li><a class="lang" href="%s" hreflang="%s" lang="%s" aria-label="%s">%s</a></li>'
        % (other_href, t["other_lang"], t["other_lang"], t["other_label"], t["other"]),
    ])
    head_extra = ""
    if redirect:
        head_extra += '<meta http-equiv="refresh" content="0; url=%s">\n' % redirect
    if noindex:
        head_extra += '<meta name="robots" content="noindex">\n'
    alts = "" if noindex else (
        '<link rel="alternate" hreflang="en" href="%s">\n<link rel="alternate" hreflang="pt-PT" href="%s">\n'
        '<link rel="alternate" hreflang="x-default" href="%s">\n' % (en_url, pt_url, en_url))
    # Nas páginas do PinchaHide o rodapé liga aos textos do PinchaHide; nas restantes, aos do PinchaPlay.
    fapp, fslug = ("PinchaHide", "pinchahide") if current == "pinchahide" else ("PinchaPlay", "pinchaplay")
    foot_links = [
        (fapp + ": " + t["privacy"], "/%s/privacy.html" % fslug),
        (fapp + ": " + t["terms"], "/%s/terms.html" % fslug),
        (fapp + ": " + t["refunds"], "/%s/refund.html" % fslug),
        (t["legal"], "/legal-notice.html"),
        (t["about"], "/about.html"),
    ]
    foot = " ".join('<li><a href="%s">%s</a></li>' % (url(lang, p), e(l)) for l, p in foot_links)
    return """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="referrer" content="strict-origin-when-cross-origin">
{head_extra}<title>{title}</title>
<meta name="description" content="{desc}">
{alts}<link rel="canonical" href="{canon}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/inter-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/site.css">
<meta name="theme-color" content="#F5F7FA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F1B2D" media="(prefers-color-scheme: dark)">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="Pinchavelho">
<meta property="og:locale" content="{oglocale}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Pinchavelho">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<header class="site"><div class="wrap">
<a class="brand" href="{homeurl}"><picture><source srcset="/assets/img/pinchavelho-horizontal-escuro.svg" media="(prefers-color-scheme: dark)"><img src="/assets/img/pinchavelho-horizontal-claro.svg" alt="{brand_alt}" width="216" height="44"></picture></a>
<nav class="main" aria-label="{navl}"><ul>{nav}</ul></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site"><div class="wrap">
<ul>{foot}</ul>
<p>{tag}</p>
<p>© 2026 Pinchavelho. {rights} · <a href="mailto:{email}">{email}</a></p>
</div></footer>
</body>
</html>
""".format(lang=t["lang"], csp=CSP, head_extra=head_extra, title=e(title), desc=e(desc), alts=alts, canon=canon,
           oglocale="en_GB" if lang == "en" else "pt_PT", og=OG_IMG, skip=t["skip"], homeurl=url(lang, "/"),
           brand_alt=t["brand_alt"], navl=t["nav"], nav=nav, body=body.strip(), foot=foot, tag=e(t["foot_tag"]),
           rights=t["rights"], email=EMAIL)


# ---------------------------------------------------------------- shared blocks
VALUES = {
    "en": [
        ("Privacy first", "We do not collect, sell or share personal data. No tracking, no analytics, no ads, no remote code. Your data stays on your device."),
        ("Minimal permissions", "We ask only for what a feature needs, when you use it, and explain every permission in plain words."),
        ("Respect for creators and websites", "Our tools never get around copy protection (DRM), encryption, paywalls or other protection measures."),
        ("Freedom with responsibility", "You decide how to use your tools, within the law. We tell you the limits without lecturing."),
        ("Fair price", "The essentials are free. Pro is a one-time payment, with a 15-day free trial and no account."),
    ],
    "pt": [
        ("Privacidade primeiro", "Não recolhemos, vendemos nem partilhamos dados pessoais. Sem rastreio, analytics, anúncios nem código remoto. Os seus dados ficam no seu dispositivo."),
        ("Permissões mínimas", "Pedimos só o que cada funcionalidade precisa, quando a usa, e explicamos cada permissão em linguagem simples."),
        ("Respeito pelos criadores e pelos sites", "As nossas ferramentas nunca contornam proteções contra cópia (DRM), cifragem, paywalls ou outras medidas de proteção."),
        ("Liberdade com responsabilidade", "Decide como usa as suas ferramentas, dentro da lei. Dizemos-lhe os limites sem dar sermões."),
        ("Preço justo", "O essencial é grátis. O Pro é um pagamento único, com 15 dias de teste grátis e sem conta."),
    ],
}


def values_grid(lang):
    return '<div class="grid">' + "".join(
        '<div class="card"><h3>%s</h3><p>%s</p></div>' % (e(h), e(p)) for h, p in VALUES[lang]) + "</div>"


def product_card(lang, app):
    if app == "pinchaplay":
        name, icon, href = "PinchaPlay", "/assets/img/pinchaplay-icon-128.png", url(lang, "/pinchaplay/")
        txt = {"en": "Speed, skips and clearer sound for the video and audio you learn from. Works on any site after one click. Free core features; Pro: pay what you think is fair, from %s." % MIN_ATUAL["en"],
               "pt": "Velocidade, saltos e som mais claro para os vídeos e áudios com que aprende. Funciona em qualquer site depois de um clique. O essencial é grátis; Pro: pague o que achar justo, a partir de %s." % MIN_ATUAL["pt"]}[lang]
        pill = {"en": "Chrome · available", "pt": "Chrome · disponível"}[lang]
    else:
        name, icon, href = "PinchaHide", "/assets/img/pinchahide-icon-128.png", url(lang, "/pinchahide/")
        txt = {"en": "Answers cookie banners with “reject” for you and sends a do-not-track signal. Everything runs on your computer. Free core features; Pro: pay what you think is fair, from %s." % MIN_ATUAL["en"],
               "pt": "Responde aos banners de cookies com “rejeitar” por si e envia um sinal para não ser rastreado. Tudo corre no seu computador. O essencial é grátis; Pro: pague o que achar justo, a partir de %s." % MIN_ATUAL["pt"]}[lang]
        pill = {"en": "Chrome · available", "pt": "Chrome · disponível"}[lang]
    return ('<div class="card product"><img src="%s" alt="" width="72" height="72"><div><h3><a href="%s">%s</a> '
            '<span class="pill">%s</span></h3><p>%s</p></div></div>' % (icon, href, name, pill, e(txt)))


# ---------------------------------------------------------------- home
def home(lang):
    if lang == "en":
        body = """
<section class="hero wrap"><p class="eyebrow">Software by Pinchavelho · Portugal</p>
<h1>Small mechanisms that make things work.</h1>
<p class="lead"><i lang="pt">Pinchavelho</i> is a Portuguese word for the small part that makes a machine work. We build small, simple browser tools that do one job well, with no tracking and no ads.</p>
<div class="actions"><a class="btn" href="/pinchaplay/">Meet PinchaPlay</a><a class="btn ghost" href="/about.html">About us</a></div></section>
<section class="wrap" aria-labelledby="prod"><h2 id="prod">Our tools</h2><div class="products">%s%s</div></section>
<section class="wrap" aria-labelledby="val"><h2 id="val">What we stand for</h2>%s</section>
<section class="wrap" aria-labelledby="deal"><h2 id="deal">A fair deal</h2><div class="grid">
<div class="card"><h3>Free stays free</h3><p>The core of each tool is free, with no time limit and no ads.</p></div>
<div class="card"><h3>Pro, once</h3><p>Pay what you think is fair, from a small minimum. One payment, no subscription. Paying more doesn’t add features.</p></div>
<div class="card"><h3>Try first</h3><p>15 days of Pro for free, from installation. No sign-up, no card.</p></div>
<div class="card"><h3>Limits, before you buy</h3><p>Each tool says what it can’t do in a “They’ll always win.” note, next to the price.</p></div>
</div></section>
""" % (product_card(lang, "pinchaplay"), product_card(lang, "pinchahide"), values_grid(lang))
        return page(lang, "/", "Pinchavelho: small, honest browser tools",
                    "Pinchavelho makes small, privacy-first tools for Chrome, with no tracking and no ads: PinchaPlay (video speed and sound) and PinchaHide (cookie banners).",
                    body, current="home")
    body = """
<section class="hero wrap"><p class="eyebrow">Software da Pinchavelho · Portugal</p>
<h1>Pequenos mecanismos que fazem as coisas funcionar.</h1>
<p class="lead">Um pinchavelho é a pequena peça que faz uma máquina funcionar. Fazemos ferramentas pequenas e simples para o navegador, que fazem bem uma coisa, sem rastreio e sem publicidade.</p>
<div class="actions"><a class="btn" href="/pt/pinchaplay/">Conhecer o PinchaPlay</a><a class="btn ghost" href="/pt/about.html">Sobre nós</a></div></section>
<section class="wrap" aria-labelledby="prod"><h2 id="prod">As nossas ferramentas</h2><div class="products">%s%s</div></section>
<section class="wrap" aria-labelledby="val"><h2 id="val">O que defendemos</h2>%s</section>
<section class="wrap" aria-labelledby="deal"><h2 id="deal">Um negócio justo</h2><div class="grid">
<div class="card"><h3>O grátis é grátis</h3><p>O essencial de cada ferramenta é grátis, sem prazo e sem anúncios.</p></div>
<div class="card"><h3>Pro, uma vez</h3><p>Pague o que achar justo, a partir de um mínimo pequeno. Um só pagamento, sem subscrição. Pagar mais não acrescenta funcionalidades.</p></div>
<div class="card"><h3>Experimente primeiro</h3><p>15 dias de Pro grátis, a contar da instalação. Sem registo e sem cartão.</p></div>
<div class="card"><h3>Limites antes de comprar</h3><p>Cada ferramenta diz o que não consegue fazer num aviso “Eles vão ganhar sempre.”, ao lado do preço.</p></div>
</div></section>
""" % (product_card(lang, "pinchaplay"), product_card(lang, "pinchahide"), values_grid(lang))
    return page(lang, "/", "Pinchavelho: ferramentas pequenas e honestas para o navegador",
                "A Pinchavelho faz ferramentas pequenas para o Chrome, com a privacidade em primeiro lugar, sem rastreio nem publicidade: PinchaPlay (velocidade e som de vídeos) e PinchaHide (banners de cookies).",
                body, current="home")


# ---------------------------------------------------------------- pinchaplay
R = {
    "en": dict(
        free=["Speed from 0.1x to 16x, with presets", "Skip back or forward 10 seconds", "Keyboard shortcuts",
              "Shift + mouse wheel over a video changes speed", "On-screen speed indicator", "Picture-in-picture",
              "Works on any site after one click on the icon", "Turn it off on chosen sites"],
        pro=["Always on for the sites you choose", "Panel with every video and audio on the page",
             "Skip silences in lessons and talks", "A-B loop and bookmarks", "Frame by frame",
             "Time left at your speed, and time saved", "Focus mode", "Volume boost up to 600%",
             "10-band equalizer with presets", "Clear voice and Night modes, mono, stereo balance",
             "Per-site memory (stored only on your computer)", "Custom shortcuts, including volume keys"],
        shots=[("pinchaplay_01_speed_en_1280x800.png", "PinchaPlay's speed panel next to a lesson video: 1.5x, with the time it ends at your speed and the on-screen indicator."),
               ("pinchaplay_02_study_en_1280x800.png", "Study tools (Pro): skip silences, focus mode, an A-B loop, bookmarks and time saved."),
               ("pinchaplay_03_focus_en_1280x800.png", "Focus mode (Pro): the rest of the page is dimmed around the video."),
               ("pinchaplay_04_panel_en_1280x800.png", "Every video on the page (Pro): one panel with its own controls for each video and audio.")],
        limits_title="They’ll always win.",
        limits_intro="Some things we wanted to build are not possible, or not allowed. Here they are, before you buy.",
        idea="We thought of:", reason="Why not:", instead="What it does instead:",
        limits=[
            ("Saving videos to your computer.", "We left it out on purpose, out of respect for creators. Sales platforms also do not accept this kind of product.", "It only changes how the video already playing is played."),
            ("Improving the sound of copy-protected videos, or of videos from another site that does not allow it.", "These videos do not let other apps read their sound. Getting around that would mean breaking the protection.", "Speed still works. Sound effects and skip silences turn off by themselves and PinchaPlay tells you."),
            ("Skipping the ads on video sites.", "It goes against those sites’ rules and against the creators who live from those ads.", "Nothing: ads stay as the site shows them."),
            ("Working on its own on every site from the moment you install it.", "That would need permission to read and change every site you visit. We prefer to ask you first.", "It works after one click on the icon. With Pro you choose the sites where it turns on by itself."),
            ("Working on Chrome’s own pages and on the Chrome Web Store.", "Chrome does not let any extension into those pages.", "It works on every other web page."),
            ("Syncing bookmarks and time saved between your computers.", "We would have to send your data to a server. We promised not to.", "They stay only on this computer, and you can delete them in Options."),
        ],
        limits_outro="Found another case? Write to %s. We review this list with every version." % EMAIL,
    ),
    "pt": dict(
        free=["Velocidade de 0,1x a 16x, com predefinições", "Saltar 10 segundos para trás ou para a frente",
              "Atalhos de teclado", "Shift + roda do rato sobre um vídeo muda a velocidade", "Indicador de velocidade no ecrã",
              "Imagem-na-imagem", "Funciona em qualquer site depois de um clique no ícone", "Desligar nos sites que escolher"],
        pro=["Sempre ativo nos sites que escolher", "Painel com todos os vídeos e áudios da página",
             "Saltar silêncios em aulas e palestras", "Loop A-B e marcadores", "Fotograma a fotograma",
             "Tempo restante ao seu ritmo e tempo poupado", "Modo foco", "Amplificação de volume até 600%",
             "Equalizador de 10 bandas com predefinições", "Modos Voz clara e Noite, mono, balanço estéreo",
             "Memória por site (guardada só no seu computador)", "Atalhos personalizados, incluindo teclas de volume"],
        shots=[("pinchaplay_01_speed_pt_1280x800.png", "O painel de velocidade do PinchaPlay ao lado de um vídeo de uma aula: 1,5x, com a hora a que acaba ao seu ritmo e o indicador no ecrã."),
               ("pinchaplay_02_study_pt_1280x800.png", "Ferramentas de estudo (Pro): saltar silêncios, modo foco, um loop A-B, marcadores e tempo poupado."),
               ("pinchaplay_03_focus_pt_1280x800.png", "Modo foco (Pro): o resto da página fica escurecido à volta do vídeo."),
               ("pinchaplay_04_panel_pt_1280x800.png", "Todos os vídeos da página (Pro): um painel com controlos próprios para cada vídeo e áudio.")],
        limits_title="Eles vão ganhar sempre.",
        limits_intro="Algumas coisas que quisemos fazer não são possíveis ou não são permitidas. Aqui estão, antes de comprar.",
        idea="Pensámos em:", reason="Porque não:", instead="O que faz em vez disso:",
        limits=[
            ("Guardar vídeos no computador.", "Ficou de fora de propósito, por respeito aos criadores. As plataformas de venda também não aceitam este tipo de produto.", "Só muda a forma como o vídeo que já está a tocar é reproduzido."),
            ("Melhorar o som de vídeos protegidos contra cópia, ou de vídeos de outro site que não o permite.", "Estes vídeos não deixam outras apps ler o som. Dar a volta a isso seria contornar a proteção.", "A velocidade continua a funcionar. Os efeitos de som e saltar silêncios desligam-se sozinhos e o PinchaPlay avisa."),
            ("Saltar os anúncios dos sites de vídeo.", "Vai contra as regras desses sites e contra os criadores que vivem desses anúncios.", "Nada: os anúncios ficam como o site os mostra."),
            ("Funcionar sozinho em todos os sites desde a instalação.", "Isso exigia autorização para ler e alterar todos os sites que visita. Preferimos perguntar-lhe primeiro.", "Funciona depois de um clique no ícone. Com o Pro escolhe os sites onde se liga sozinho."),
            ("Funcionar nas páginas do próprio Chrome e na Chrome Web Store.", "O Chrome não deixa nenhuma extensão entrar nessas páginas.", "Funciona em todas as outras páginas web."),
            ("Sincronizar os marcadores e o tempo poupado entre os seus computadores.", "Teríamos de enviar os seus dados para um servidor. Prometemos não o fazer.", "Ficam só neste computador e pode apagá-los nas opções."),
        ],
        limits_outro="Encontrou outro caso? Escreva para %s. Revemos esta lista em cada versão." % EMAIL,
    ),
}


def yes(lang):
    return '<span class="yes"></span><span class="visually-hidden">%s</span>' % ("Included" if lang == "en" else "Incluído")


def no(lang):
    return '<span aria-hidden="true">–</span><span class="visually-hidden">%s</span>' % ("Not included" if lang == "en" else "Não incluído")


def limits_block(lang):
    r = R[lang]
    items = "".join(
        '<li><p><strong>%s</strong> %s</p><p><strong>%s</strong> %s</p><p><strong>%s</strong> %s</p></li>'
        % (r["idea"], e(a), r["reason"], e(b), r["instead"], e(c)) for a, b, c in r["limits"])
    summ = "(i) What PinchaPlay can’t do" if lang == "en" else "(i) O que o PinchaPlay não faz"
    return ('<details class="limits" id="limits"><summary>%s</summary><h3>%s</h3><p>%s</p><ol>%s</ol><p class="note">%s</p></details>'
            % (summ, e(r["limits_title"]), e(r["limits_intro"]), items, linkify(r["limits_outro"])))


def buy_buttons(lang, checkout="pinchaplay"):
    # checkout: link do checkout da app; None = botões "brevemente" sem ligação.
    if checkout == "pinchaplay":
        checkout = PINCHAPLAY_CHECKOUT
    labels = {"en": ("minimum", "suggested", ""), "pt": ("mínimo", "sugerido", "")}[lang]
    other = {"en": "or another amount", "pt": "ou outro valor"}[lang]
    out = []
    for cents, lab in zip(PINCHAPLAY_VALORES, labels):
        inner = '<span class="amount">%s</span>' % euro(cents, lang)
        if lab:
            inner += '<span class="what">%s</span>' % lab
        if checkout:
            out.append('<a class="choice" href="%s?amount=%d" rel="noopener">%s</a>' % (e(checkout), cents, inner))
        else:
            out.append('<span class="choice pending">%s</span>' % inner)
    # "Outro valor": abre o checkout sem ?amount=, com o mínimo, e o cliente escreve o valor lá.
    if checkout:
        tail = '<p class="other"><a href="%s" rel="noopener">%s</a></p>' % (e(checkout), other)
    else:
        tail = '<p class="other">%s</p>' % other
    return '<div class="choices">%s</div>%s' % ("".join(out), tail)


def pinchaplay(lang):
    r = R[lang]
    en = lang == "en"
    # Ampliar sem JS: cada captura liga para #zoom-N; o CSS mostra esse bloco (:target) por cima da página.
    # Clicar na imagem ampliada (ou em "Fechar") volta a #see. A imagem ampliada só carrega quando aparece.
    zoom_l, close_l = ("Enlarge image", "Close") if en else ("Ampliar imagem", "Fechar")
    shots = "".join(
        '<figure><a class="zoomable" href="#zoom-%d" aria-label="%s: %s"><img src="/assets/img/screens/%s" alt="%s" width="1280" height="800" loading="lazy" decoding="async"></a><figcaption>%s</figcaption></figure>'
        % (i, zoom_l, e(a), f, e(a), e(a)) for i, (f, a) in enumerate(r["shots"], 1))
    shots_zoom = "".join(
        '<div class="lightbox" id="zoom-%d"><a href="#see" aria-label="%s"><img src="/assets/img/screens/%s" alt="%s" width="1280" height="800" loading="lazy" decoding="async"><span class="lb-close">%s ×</span></a></div>'
        % (i, close_l, f, e(a), close_l) for i, (f, a) in enumerate(r["shots"], 1))
    rows = "".join('<tr><th scope="row">%s</th><td class="c">%s</td><td class="c">%s</td></tr>' % (e(x), yes(lang), yes(lang)) for x in r["free"])
    rows += "".join('<tr><th scope="row">%s</th><td class="c">%s</td><td class="c">%s</td></tr>' % (e(x), no(lang), yes(lang)) for x in r["pro"])
    cws = '<a class="btn" href="%s" rel="noopener">%s</a>' % (PINCHAPLAY_CWS, "Add to Chrome, free" if en else "Adicionar ao Chrome, grátis")
    buy_top = ('<a class="btn ghost" href="#price">%s</a>' % ("PinchaPlay Pro: pay what you think is fair" if en else "PinchaPlay Pro: pague o que achar justo"))
    if en:
        perms = [("storage", "Remembers your choices, bookmarks and licence key on this computer only."),
                 ("activeTab", "PinchaPlay only enters a page when you click its icon or press Alt+Shift+R. The access ends when you leave the page."),
                 ("scripting", "Puts PinchaPlay’s controls into the page you chose. Only files inside the extension are used, never code from the internet."),
                 ("Sites you choose (optional, Pro)", "Only if you click “Always on for this site” and Chrome asks you to allow that one site. You can withdraw it at any time."),
                 ("api.polar.sh", "Checks your Pro licence key with Polar, the shop, about once a day. Only after you enter a key.")]
        body = """
<section class="hero wrap"><div class="card product bare"><img src="/assets/img/pinchaplay-icon-128.png" alt="" width="72" height="72"><div>
<p class="eyebrow">PinchaPlay · extension for Chrome</p>
<h1>Learn at your own pace.</h1>
<p class="lead">Speed, skips and clearer sound for the video and audio you learn from, on any website. PinchaPlay only enters a page when you click it. No tracking. No ads. No account.</p>
<div class="actions">{cws}{buy}</div>
<p class="note">For Google Chrome 124 or later. Every Pro feature can be tried free for 15 days.</p></div></div></section>
<section class="wrap" aria-labelledby="see"><h2 id="see">See it</h2><p class="note">Click an image to enlarge it.</p><div class="shots">{shots}</div>{shots_zoom}</section>
<section class="wrap" aria-labelledby="what"><h2 id="what">What it does</h2><div class="grid">
<div class="card"><h3>Your speed</h3><p>From 0.1x to 16x, in steps of 0.1 or with one-click presets. The speed you pick stays as you move through the video.</p></div>
<div class="card"><h3>Less waiting</h3><p>Skip 10 seconds with a key. With Pro, PinchaPlay speeds through the silences in lessons and talks, and tells you how much time you saved.</p></div>
<div class="card"><h3>Study tools</h3><p>With Pro: repeat a part with an A-B loop, bookmark moments, go frame by frame and dim the page with focus mode.</p></div>
<div class="card"><h3>Clearer sound</h3><p>With Pro: volume up to 600% with a limiter, a 10-band equalizer, Clear voice and Night modes, mono and balance.</p></div>
</div></section>
<section class="wrap" aria-labelledby="cmp"><h2 id="cmp">Free and Pro</h2>
<table><caption class="visually-hidden">Features in the free version and in Pro</caption><thead><tr><th scope="col">Feature</th><th scope="col" class="c">Free</th><th scope="col" class="c">Pro</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="wrap" aria-labelledby="price"><h2 id="price">Price</h2><div class="grid two">
<div class="card pricing"><h3>PinchaPlay Pro: pay what you think is fair</h3>
<p>Minimum <strong>{mn}</strong>, VAT included, until {fim}. From {ini} the minimum is {md}.</p>
{buttons}
<p>One-time payment. Lifetime personal licence. No subscription, no automatic renewal. Paying more doesn’t add features: everyone gets the same Pro. You can still change the amount on the checkout.</p>
<p class="note">{buynote}Secure checkout by Polar, our merchant of record, which handles payment, VAT and your invoice. The final amount is shown before you pay.</p>
{limits}</div>
<div class="card"><h3>Try first, decide later</h3><ul>
<li>15 days of every Pro feature, free, from installation. No sign-up, no card.</li>
<li>After the trial, PinchaPlay simply goes back to the free version. Free keeps working.</li>
<li>Before paying, the checkout asks you to tick: “I want immediate access and I accept that I lose my 14-day right of withdrawal.” So there is no refund for a change of mind.</li>
<li>If Pro doesn’t work as described, the legal guarantee applies: we fix it, reduce the price or refund what you paid. <a href="/pinchaplay/refund.html">Refund policy</a>.</li></ul></div>
</div></section>
<section class="wrap" aria-labelledby="perm"><h2 id="perm">Permissions, in plain words</h2>
<table><caption class="visually-hidden">Chrome permissions PinchaPlay asks for and why</caption><thead><tr><th scope="col">Permission</th><th scope="col">Why</th></tr></thead><tbody>{perms}</tbody></table>
<p class="note">PinchaPlay does not ask for access to all websites and has no access to your history, tabs or cookies.</p></section>
<section class="wrap" aria-labelledby="priv"><h2 id="priv">Privacy and respect</h2><div class="grid two">
<div class="card"><h3>Stays on your computer</h3><p>Settings, bookmarks and time saved are stored only in your browser. No analytics, no tracking, no remote code. The only network request PinchaPlay makes is the licence check with Polar, and only if you enter a key.</p></div>
<div class="card"><h3>Respects creators</h3><p>PinchaPlay only changes how media that is already playing is played. It does not save or record media, does not get around copy protection (DRM) and does not skip ads.</p></div>
</div></section>
<section class="wrap faq" aria-labelledby="faq"><h2 id="faq">Questions</h2>
<details><summary>Why do I have to click the icon?</summary><p>So PinchaPlay can only see the pages you choose. Click the icon or press Alt+Shift+R on a page with video, and it is ready. With Pro you can choose sites, such as your course platform, where it turns on by itself.</p></details>
<details><summary>Does it work on every video?</summary><p>It works with the standard video and audio of web pages. On copy-protected videos the speed still works, but sound effects and skip silences turn off by themselves. Chrome’s own pages and the Chrome Web Store are closed to every extension.</p></details>
<details><summary>What happens when the trial ends?</summary><p>The Pro features lock and PinchaPlay goes back to the free version. Your bookmarks stay on your computer. Nothing is charged: there is no card to charge.</p></details>
<details><summary>Can I use Pro on more than one computer?</summary><p>Yes, on your own browsers. The licence is personal: it is for you, not for sharing or reselling.</p></details>
<details><summary>Do I need an account?</summary><p>No. After payment your licence key is in the Polar customer portal: open it from the link in Polar's confirmation email or sign in with the email you used to buy; you paste it into PinchaPlay’s Options.</p></details>
</section>
<section class="wrap"><p><a href="/pinchaplay/transparency.html">Transparency report</a> · <a href="/pinchaplay/privacy.html">Privacy policy</a> · <a href="/pinchaplay/terms.html">Terms of sale &amp; EULA</a> · <a href="/pinchaplay/refund.html">Refund policy</a></p></section>
"""
        title = "PinchaPlay: video speed and sound control for online learning"
        desc = "PinchaPlay for Chrome: video speed from 0.1x to 16x, skips and shortcuts for free; Pro adds skip silences, A-B loop, bookmarks and clearer sound. No tracking. Pay what you think is fair, from %s." % MIN_ATUAL["en"]
        buynote = "" if PINCHAPLAY_CHECKOUT else "The purchase opens soon. "
    else:
        perms = [("storage", "Guarda as suas escolhas, marcadores e chave de licença só neste computador."),
                 ("activeTab", "O PinchaPlay só entra numa página quando clica no ícone ou carrega em Alt+Shift+R. O acesso termina quando sai da página."),
                 ("scripting", "Põe os controlos do PinchaPlay na página que escolheu. Usa só ficheiros que vêm dentro da extensão, nunca código da internet."),
                 ("Sites que escolher (opcional, Pro)", "Só se clicar em “Ativar sempre neste site” e o Chrome lhe pedir autorização para esse site. Pode retirá-la quando quiser."),
                 ("api.polar.sh", "Verifica a sua chave Pro junto da Polar, a loja, cerca de uma vez por dia. Só depois de introduzir uma chave.")]
        body = """
<section class="hero wrap"><div class="card product bare"><img src="/assets/img/pinchaplay-icon-128.png" alt="" width="72" height="72"><div>
<p class="eyebrow">PinchaPlay · extensão para o Chrome</p>
<h1>Aprenda ao seu ritmo.</h1>
<p class="lead">Velocidade, saltos e som mais claro para os vídeos e áudios com que aprende, em qualquer site. O PinchaPlay só entra numa página quando clica nele. Sem rastreio. Sem anúncios. Sem conta.</p>
<div class="actions">{cws}{buy}</div>
<p class="note">Para o Google Chrome 124 ou mais recente. Todas as funcionalidades Pro podem ser experimentadas grátis durante 15 dias.</p></div></div></section>
<section class="wrap" aria-labelledby="see"><h2 id="see">Veja</h2><p class="note">Clique numa imagem para a ampliar.</p><div class="shots">{shots}</div>{shots_zoom}</section>
<section class="wrap" aria-labelledby="what"><h2 id="what">O que faz</h2><div class="grid">
<div class="card"><h3>A sua velocidade</h3><p>De 0,1x a 16x, em passos de 0,1 ou com predefinições de um clique. A velocidade que escolhe mantém-se ao longo do vídeo.</p></div>
<div class="card"><h3>Menos espera</h3><p>Salte 10 segundos com uma tecla. Com o Pro, o PinchaPlay acelera nos silêncios das aulas e palestras e diz-lhe quanto tempo poupou.</p></div>
<div class="card"><h3>Ferramentas de estudo</h3><p>Com o Pro: repita uma parte com um loop A-B, marque momentos, avance fotograma a fotograma e escureça a página com o modo foco.</p></div>
<div class="card"><h3>Som mais claro</h3><p>Com o Pro: volume até 600% com limitador, equalizador de 10 bandas, modos Voz clara e Noite, mono e balanço.</p></div>
</div></section>
<section class="wrap" aria-labelledby="cmp"><h2 id="cmp">Grátis e Pro</h2>
<table><caption class="visually-hidden">Funcionalidades da versão gratuita e do Pro</caption><thead><tr><th scope="col">Funcionalidade</th><th scope="col" class="c">Grátis</th><th scope="col" class="c">Pro</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="wrap" aria-labelledby="price"><h2 id="price">Preço</h2><div class="grid two">
<div class="card pricing"><h3>PinchaPlay Pro: pague o que achar justo</h3>
<p>Mínimo de <strong>{mn}</strong>, IVA incluído, até {fim}. A partir de {ini}, o mínimo passa a {md}.</p>
{buttons}
<p>Pagamento único. Licença pessoal vitalícia. Sem subscrição nem renovação automática. Pagar mais não acrescenta funcionalidades: todos recebem o mesmo Pro. Ainda pode alterar o valor no checkout.</p>
<p class="note">{buynote}Pagamento seguro na Polar, o nosso revendedor (merchant of record), que trata do pagamento, do IVA e da sua fatura. O valor final é mostrado antes de pagar.</p>
{limits}</div>
<div class="card"><h3>Experimente primeiro, decida depois</h3><ul>
<li>15 dias de todas as funcionalidades Pro, grátis, a contar da instalação. Sem registo e sem cartão.</li>
<li>No fim do teste, o PinchaPlay volta simplesmente à versão gratuita. O grátis continua a funcionar.</li>
<li>Antes de pagar, o checkout pede-lhe que marque: “Quero acesso imediato e aceito perder o direito de livre resolução de 14 dias.” Por isso não há reembolso por desistência.</li>
<li>Se o Pro não funcionar como descrito, aplica-se a garantia legal: corrigimos, reduzimos o preço ou devolvemos o que pagou. <a href="/pt/pinchaplay/refund.html">Política de reembolso</a>.</li></ul></div>
</div></section>
<section class="wrap" aria-labelledby="perm"><h2 id="perm">Permissões, em linguagem simples</h2>
<table><caption class="visually-hidden">Permissões do Chrome que o PinchaPlay pede e porquê</caption><thead><tr><th scope="col">Permissão</th><th scope="col">Porquê</th></tr></thead><tbody>{perms}</tbody></table>
<p class="note">O PinchaPlay não pede acesso a todos os sites e não tem acesso ao seu histórico, aos separadores nem aos cookies.</p></section>
<section class="wrap" aria-labelledby="priv"><h2 id="priv">Privacidade e respeito</h2><div class="grid two">
<div class="card"><h3>Fica no seu computador</h3><p>As definições, os marcadores e o tempo poupado ficam só no seu navegador. Sem analytics, rastreio nem código remoto. O único pedido de rede do PinchaPlay é a verificação da licença na Polar, e só se introduzir uma chave.</p></div>
<div class="card"><h3>Respeita os criadores</h3><p>O PinchaPlay só muda a forma como o media que já está a tocar é reproduzido. Não guarda nem grava media, não contorna proteções contra cópia (DRM) e não salta anúncios.</p></div>
</div></section>
<section class="wrap faq" aria-labelledby="faq"><h2 id="faq">Perguntas</h2>
<details><summary>Porque tenho de clicar no ícone?</summary><p>Para o PinchaPlay só ver as páginas que escolher. Clique no ícone ou carregue em Alt+Shift+R numa página com vídeo e fica pronto. Com o Pro pode escolher sites, como a sua plataforma de cursos, onde se liga sozinho.</p></details>
<details><summary>Funciona em todos os vídeos?</summary><p>Funciona com o vídeo e o áudio normais das páginas web. Em vídeos protegidos contra cópia a velocidade continua a funcionar, mas os efeitos de som e saltar silêncios desligam-se sozinhos. As páginas do próprio Chrome e a Chrome Web Store estão fechadas a todas as extensões.</p></details>
<details><summary>O que acontece quando o teste acaba?</summary><p>As funcionalidades Pro ficam bloqueadas e o PinchaPlay volta à versão gratuita. Os seus marcadores ficam no seu computador. Não é cobrado nada: não há cartão para cobrar.</p></details>
<details><summary>Posso usar o Pro em mais do que um computador?</summary><p>Sim, nos seus navegadores. A licença é pessoal: é para si, não para partilhar nem revender.</p></details>
<details><summary>Preciso de uma conta?</summary><p>Não. Depois do pagamento, a chave de licença fica no portal de cliente da Polar: abra-o pelo link do email de confirmação ou entre com o email que usou na compra; cola-a nas Opções do PinchaPlay.</p></details>
</section>
<section class="wrap"><p><a href="/pt/pinchaplay/transparency.html">Relatório de transparência</a> · <a href="/pt/pinchaplay/privacy.html">Política de privacidade</a> · <a href="/pt/pinchaplay/terms.html">Termos de venda e EULA</a> · <a href="/pt/pinchaplay/refund.html">Política de reembolso</a></p></section>
"""
        title = "PinchaPlay: velocidade e som de vídeos para quem aprende online"
        desc = "PinchaPlay para o Chrome: velocidade de 0,1x a 16x, saltos e atalhos grátis; o Pro junta saltar silêncios, loop A-B, marcadores e som mais claro. Sem rastreio. Pague o que achar justo, a partir de %s." % MIN_ATUAL["pt"]
        buynote = "" if PINCHAPLAY_CHECKOUT else "A compra abre brevemente. "
    perm_rows = "".join('<tr><th scope="row"><code>%s</code></th><td>%s</td></tr>' % (e(a), e(b)) if not a.startswith(("Sites",)) else
                        '<tr><th scope="row">%s</th><td>%s</td></tr>' % (e(a), e(b)) for a, b in perms)
    body = body.format(cws=cws, buy=buy_top, shots=shots, shots_zoom=shots_zoom, rows=rows, mn=MIN_ATUAL[lang], fim=FIM_MIN[lang], ini=INICIO_DEPOIS[lang],
                       md=MIN_DEPOIS[lang], buttons=buy_buttons(lang), buynote=buynote, limits=limits_block(lang), perms=perm_rows)
    return page(lang, "/pinchaplay/", title, desc, body, current="pinchaplay")


# ---------------------------------------------------------------- pinchahide
PH = {
    "en": dict(
        shots=[("pinchahide_01_refuse_en_1280x800.png", "PinchaHide’s popup on a sample news page: the cookie banner was refused, trackers blocked and Global Privacy Control sent."),
               ("pinchahide_02_free_pro_en_1280x800.png", "What is free and what comes with Pro, side by side."),
               ("pinchahide_03_clean_links_en_1280x800.png", "Clean Links (Pro): addresses copied without tracking codes, and “Copy clean link” in the right-click menu."),
               ("pinchahide_04_control_en_1280x800.png", "Options (Pro): turn Pop-up Cleaner, Clean Links and the local history on or off.")],
        free=["Rejects cookie banners automatically (about 40 consent platforms and a careful generic check)",
              "Hides a banner that offers no way to refuse, without ever accepting it",
              "Sends the Global Privacy Control signal",
              "Pause, and “protection off on this site”",
              "What was done on the current page, and totals"],
        pro=["Blocks trackers: analytics, advertising and session recording",
             "Removes tracking parameters from addresses (utm_, fbclid, gclid…)",
             "Clean Links: copy addresses without tracking",
             "Objects to “legitimate interest” where the site’s consent tool allows it",
             "Pop-up Cleaner: newsletter, “allow notifications” and “install the app” boxes",
             "Blocks tracking pings and, if you want, social widgets",
             "Chrome privacy settings: third-party cookies, ad APIs, Do Not Track, WebRTC",
             "Clears a site’s cookies when you close its last tab",
             "Per-site exceptions and a local history of the last 30 days"],
        perms=[("storage", "Keeps your settings, counts, history (Pro), the trial start date and your Pro key on this computer only."),
               ("declarativeNetRequest", "Lets Chrome itself apply the rules that come inside PinchaHide: send Global Privacy Control and, with Pro, block trackers and tracking parameters. PinchaHide does not see your requests."),
               ("activeTab", "Shows in the popup what PinchaHide did on the current tab, and lets “Copy clean link” work where you click."),
               ("scripting", "Adds PinchaHide’s own scripts to pages to answer the banner. Only files inside the extension, never code from the internet."),
               ("alarms", "Ends a timed pause and re-checks the Pro key about once a day."),
               ("contextMenus", "Adds “Copy clean link” to the right-click menu on a link (Pro)."),
               ("privacy (optional)", "Asked only when you turn on a Chrome privacy setting in Options (Pro)."),
               ("cookies (optional)", "Asked only when you turn on “Clear a site’s cookies when its last tab closes” (Pro). It only deletes cookies."),
               ("All sites", "Cookie banners appear on any site, so PinchaHide runs on every page to find the banner and press Reject. Nothing leaves your browser.")],
    ),
    "pt": dict(
        shots=[("pinchahide_01_refuse_pt_1280x800.png", "A janela do PinchaHide numa página de notícias de exemplo: o banner de cookies foi recusado, os rastreadores bloqueados e o Global Privacy Control enviado."),
               ("pinchahide_02_free_pro_pt_1280x800.png", "O que é grátis e o que vem com o Pro, lado a lado."),
               ("pinchahide_03_clean_links_pt_1280x800.png", "Clean Links (Pro): endereços copiados sem códigos de rastreio e “Copiar link limpo” no menu do botão direito."),
               ("pinchahide_04_control_pt_1280x800.png", "Opções (Pro): ligue ou desligue o Pop-up Cleaner, o Clean Links e o histórico local.")],
        free=["Recusa banners de cookies automaticamente (cerca de 40 plataformas de consentimento e uma deteção genérica cuidadosa)",
              "Esconde o banner que não dá forma de recusar, sem nunca o aceitar",
              "Envia o sinal Global Privacy Control",
              "Pausa e “sem proteção neste site”",
              "O que foi feito na página atual e totais"],
        pro=["Bloqueia rastreadores: analítica, publicidade e gravação de sessões",
             "Remove parâmetros de rastreio dos endereços (utm_, fbclid, gclid…)",
             "Clean Links: copia endereços sem rastreio",
             "Opõe-se ao “interesse legítimo” quando a ferramenta de consentimento do site o permite",
             "Pop-up Cleaner: caixas de newsletter, “ativar notificações” e “instale a app”",
             "Bloqueia pings de rastreio e, se quiser, widgets sociais",
             "Definições de privacidade do Chrome: cookies de terceiros, APIs de publicidade, Do Not Track, WebRTC",
             "Apaga os cookies de um site ao fechar o último separador dele",
             "Exceções por site e histórico local dos últimos 30 dias"],
        perms=[("storage", "Guarda as definições, as contagens, o histórico (Pro), a data de início do teste e a chave Pro só neste computador."),
               ("declarativeNetRequest", "Deixa o próprio Chrome aplicar as regras que vêm dentro do PinchaHide: enviar o Global Privacy Control e, com o Pro, bloquear rastreadores e parâmetros de rastreio. O PinchaHide não vê os seus pedidos."),
               ("activeTab", "Mostra na janela o que o PinchaHide fez no separador atual e faz funcionar “Copiar link limpo” onde clica."),
               ("scripting", "Põe nas páginas os scripts do próprio PinchaHide para responder ao banner. Só ficheiros que vêm dentro da extensão, nunca código da internet."),
               ("alarms", "Termina uma pausa com hora marcada e volta a verificar a chave Pro cerca de uma vez por dia."),
               ("contextMenus", "Junta “Copiar link limpo” ao menu do botão direito sobre um link (Pro)."),
               ("privacy (opcional)", "Só é pedida quando liga uma definição de privacidade do Chrome nas Opções (Pro)."),
               ("cookies (opcional)", "Só é pedida quando liga “Apagar os cookies de um site ao fechar o último separador” (Pro). Só apaga cookies."),
               ("Todos os sites", "Os banners de cookies aparecem em qualquer site, por isso o PinchaHide corre em todas as páginas para encontrar o banner e carregar em Rejeitar. Nada sai do seu navegador.")],
    ),
}


def shots_html(lang, shots):
    """Capturas com ampliação sem JS (:target). Clicar na imagem ampliada volta a #see."""
    zoom_l, close_l = ("Enlarge image", "Close") if lang == "en" else ("Ampliar imagem", "Fechar")
    s = "".join(
        '<figure><a class="zoomable" href="#zoom-%d" aria-label="%s: %s"><img src="/assets/img/screens/%s" alt="%s" width="1280" height="800" loading="lazy" decoding="async"></a><figcaption>%s</figcaption></figure>'
        % (i, zoom_l, e(a), f, e(a), e(a)) for i, (f, a) in enumerate(shots, 1))
    z = "".join(
        '<div class="lightbox" id="zoom-%d"><a href="#see" aria-label="%s"><img src="/assets/img/screens/%s" alt="%s" width="1280" height="800" loading="lazy" decoding="async"><span class="lb-close">%s ×</span></a></div>'
        % (i, close_l, f, e(a), close_l) for i, (f, a) in enumerate(shots, 1))
    return s, z


def pinchahide(lang):
    p = PH[lang]
    en = lang == "en"
    shots, shots_zoom = shots_html(lang, p["shots"])
    rows = "".join('<tr><th scope="row">%s</th><td class="c">%s</td><td class="c">%s</td></tr>' % (e(x), yes(lang), yes(lang)) for x in p["free"])
    rows += "".join('<tr><th scope="row">%s</th><td class="c">%s</td><td class="c">%s</td></tr>' % (e(x), no(lang), yes(lang)) for x in p["pro"])
    perm_rows = "".join(('<tr><th scope="row"><code>%s</code></th><td>%s</td></tr>' if a[0].islower() else '<tr><th scope="row">%s</th><td>%s</td></tr>') % (e(a), e(b)) for a, b in p["perms"])
    cws = '<a class="btn" href="%s" rel="noopener">%s</a>' % (PINCHAHIDE_CWS, "Add to Chrome, free" if en else "Adicionar ao Chrome, grátis")
    buy_top = '<a class="btn ghost" href="#price">%s</a>' % ("PinchaHide Pro: pay what you think is fair" if en else "PinchaHide Pro: pague o que achar justo")
    if en:
        body = """
<section class="hero wrap"><div class="card product bare"><img src="/assets/img/pinchahide-icon-128.png" alt="" width="72" height="72"><div>
<p class="eyebrow">PinchaHide – Reject Cookie Banners · extension for Chrome</p>
<h1>Say no to cookies, once.</h1>
<p class="lead">PinchaHide answers cookie banners with “reject” on your behalf and tells websites you do not want to be tracked. It never presses Accept. It runs on your computer, collects nothing and sends nothing.</p>
<div class="actions">{cws}{buy}</div>
<p class="note">For Google Chrome. Nothing to set up: install it and browse as usual. Every Pro feature can be tried free for 15 days.</p></div></div></section>
<section class="wrap" aria-labelledby="see"><h2 id="see">See it</h2><p class="note">Click an image to enlarge it.</p><div class="shots">{shots}</div>{shots_zoom}</section>
<section class="wrap" aria-labelledby="what"><h2 id="what">What it does</h2><div class="grid">
<div class="card"><h3>Rejects cookie banners</h3><p>Presses “Reject all”, or unticks every optional purpose and saves, on the main consent platforms and on many sites with their own banner.</p></div>
<div class="card"><h3>Sends privacy signals</h3><p>Global Privacy Control tells every site you do not allow your data to be sold or shared.</p></div>
<div class="card"><h3>You stay in charge</h3><p>Click the icon to see what it did on the page. Pause it, or turn it off on a site that stops working. Counts stay on your computer.</p></div>
<div class="card"><h3>More with Pro</h3><p>Blocks known trackers in your own browser, cleans tracking codes from links, closes newsletter pop-ups and more.</p></div>
</div></section>
<section class="wrap" aria-labelledby="cmp"><h2 id="cmp">Free and Pro</h2>
<table><caption class="visually-hidden">Features in the free version and in Pro</caption><thead><tr><th scope="col">Feature</th><th scope="col" class="c">Free</th><th scope="col" class="c">Pro</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="wrap" aria-labelledby="not"><h2 id="not">What it won’t do</h2><div class="grid two">
<div class="card"><h3>Paywalls and “accept or pay”</h3><p>PinchaHide never hides or gets around paywalls, “accept or pay” pages, sign-in walls, prices or age checks. Those are the site’s choice.</p></div>
<div class="card"><h3>Its limits</h3><p>It can’t make a site respect your refusal, and it can’t refuse every banner on every site. The full list, and why, is in the app before you buy.</p></div>
</div></section>
<section class="wrap" aria-labelledby="price"><h2 id="price">Price</h2><div class="grid two">
<div class="card pricing"><h3>PinchaHide Pro: pay what you think is fair</h3>
<p>Minimum <strong>{mn}</strong>, VAT included, until {fim}. From {ini} the minimum is {md}.</p>
{buttons}
<p>One-time payment. Lifetime personal licence. No subscription, no automatic renewal. Paying more doesn’t add features: everyone gets the same Pro. You can still change the amount on the checkout. PinchaHide Pro is sold separately from PinchaPlay Pro.</p>
<p class="note">Secure checkout by Polar, our merchant of record, which handles payment, VAT and your invoice. The final amount is shown before you pay.</p></div>
<div class="card"><h3>Try first, decide later</h3><ul>
<li>15 days of every Pro feature, free, from installation. No sign-up, no card.</li>
<li>After the trial, PinchaHide simply goes back to the free version, which keeps refusing cookie banners.</li>
<li>Before paying, the checkout asks you to tick: “I want immediate access and I accept that I lose my 14-day right of withdrawal.” So there is no refund for a change of mind.</li>
<li>If Pro doesn’t work as described, the legal guarantee applies: we fix it, reduce the price or refund what you paid. <a href="/pinchahide/refund.html">Refund policy</a>.</li></ul></div>
</div></section>
<section class="wrap" aria-labelledby="perm"><h2 id="perm">Permissions, in plain words</h2>
<table><caption class="visually-hidden">Chrome permissions PinchaHide asks for and why</caption><thead><tr><th scope="col">Permission</th><th scope="col">Why</th></tr></thead><tbody>{perms}</tbody></table>
<p class="note">The blocking rules are our own and come inside the extension; nothing is fetched from the internet while it runs. The only connection PinchaHide makes by itself is checking your Pro key with Polar, and only after you enter a key.</p></section>
<section class="wrap faq" aria-labelledby="faq"><h2 id="faq">Questions</h2>
<details><summary>Does it accept cookies when it can’t refuse?</summary><p>No. PinchaHide never presses Accept. If a banner offers no way to refuse, it hides the banner without answering it.</p></details>
<details><summary>A site stopped working. What do I do?</summary><p>Click the PinchaHide icon and turn protection off for that site. You can also pause PinchaHide for an hour or until you resume it.</p></details>
<details><summary>What happens when the trial ends?</summary><p>The Pro features stop and PinchaHide goes back to the free version, which keeps refusing cookie banners. Your Pro settings stay saved. Nothing is charged: there is no card to charge.</p></details>
<details><summary>Do I need an account?</summary><p>No. After payment your licence key is in the Polar customer portal: open it from the link in Polar’s confirmation email or sign in with the email you used to buy; you paste it into PinchaHide’s Options.</p></details>
<details><summary>Does a PinchaPlay key work in PinchaHide?</summary><p>No. Each app has its own Pro and its own key.</p></details>
</section>
<section class="wrap"><p><a href="/pinchahide/transparency.html">Transparency report</a> · <a href="/pinchahide/privacy.html">Privacy policy</a> · <a href="/pinchahide/terms.html">Terms of sale &amp; EULA</a> · <a href="/pinchahide/refund.html">Refund policy</a></p></section>
"""
        title = "PinchaHide: reject cookie banners automatically, in Chrome"
        desc = "PinchaHide – Reject Cookie Banners for Chrome answers cookie banners with “reject” for you and sends Global Privacy Control. Free; Pro from %s. Runs on your computer and collects nothing." % MIN_ATUAL["en"]
    else:
        body = """
<section class="hero wrap"><div class="card product bare"><img src="/assets/img/pinchahide-icon-128.png" alt="" width="72" height="72"><div>
<p class="eyebrow">PinchaHide – Recusar banners de cookies · extensão para o Chrome</p>
<h1>Diga não aos cookies, uma vez.</h1>
<p class="lead">O PinchaHide responde aos banners de cookies com “rejeitar” por si e diz aos sites que não quer ser rastreado. Nunca carrega em Aceitar. Corre no seu computador, não recolhe nada e não envia nada.</p>
<div class="actions">{cws}{buy}</div>
<p class="note">Para o Google Chrome. Não há nada para configurar: instale e navegue como sempre. Todas as funcionalidades Pro podem ser experimentadas grátis durante 15 dias.</p></div></div></section>
<section class="wrap" aria-labelledby="see"><h2 id="see">Veja</h2><p class="note">Clique numa imagem para a ampliar.</p><div class="shots">{shots}</div>{shots_zoom}</section>
<section class="wrap" aria-labelledby="what"><h2 id="what">O que faz</h2><div class="grid">
<div class="card"><h3>Rejeita banners de cookies</h3><p>Carrega em “Rejeitar tudo”, ou desmarca todas as finalidades opcionais e guarda, nas principais plataformas de consentimento e em muitos sites com banner próprio.</p></div>
<div class="card"><h3>Envia sinais de privacidade</h3><p>O Global Privacy Control diz a cada site que não autoriza a venda nem a partilha dos seus dados.</p></div>
<div class="card"><h3>Quem manda é você</h3><p>Clique no ícone para ver o que fez na página. Pause-o, ou desligue-o num site que deixe de funcionar. As contagens ficam no seu computador.</p></div>
<div class="card"><h3>Mais com o Pro</h3><p>Bloqueia rastreadores conhecidos no seu próprio navegador, limpa códigos de rastreio dos links, fecha caixas de newsletter e mais.</p></div>
</div></section>
<section class="wrap" aria-labelledby="cmp"><h2 id="cmp">Grátis e Pro</h2>
<table><caption class="visually-hidden">Funcionalidades da versão gratuita e do Pro</caption><thead><tr><th scope="col">Funcionalidade</th><th scope="col" class="c">Grátis</th><th scope="col" class="c">Pro</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="wrap" aria-labelledby="not"><h2 id="not">O que não faz</h2><div class="grid two">
<div class="card"><h3>Paywalls e “aceitar ou pagar”</h3><p>O PinchaHide nunca esconde nem contorna paywalls, páginas “aceitar ou pagar”, muros de login, preços ou confirmações de idade. Essa escolha é do site.</p></div>
<div class="card"><h3>Os seus limites</h3><p>Não consegue obrigar um site a respeitar a recusa, nem recusar todos os banners em todos os sites. A lista completa, e porquê, está na app antes de comprar.</p></div>
</div></section>
<section class="wrap" aria-labelledby="price"><h2 id="price">Preço</h2><div class="grid two">
<div class="card pricing"><h3>PinchaHide Pro: pague o que achar justo</h3>
<p>Mínimo de <strong>{mn}</strong>, IVA incluído, até {fim}. A partir de {ini}, o mínimo passa a {md}.</p>
{buttons}
<p>Pagamento único. Licença pessoal vitalícia. Sem subscrição nem renovação automática. Pagar mais não acrescenta funcionalidades: todos recebem o mesmo Pro. Ainda pode alterar o valor no checkout. O PinchaHide Pro é vendido em separado do PinchaPlay Pro.</p>
<p class="note">Pagamento seguro na Polar, o nosso revendedor (merchant of record), que trata do pagamento, do IVA e da sua fatura. O valor final é mostrado antes de pagar.</p></div>
<div class="card"><h3>Experimente primeiro, decida depois</h3><ul>
<li>15 dias de todas as funcionalidades Pro, grátis, a contar da instalação. Sem registo e sem cartão.</li>
<li>No fim do teste, o PinchaHide volta simplesmente à versão gratuita, que continua a recusar banners de cookies.</li>
<li>Antes de pagar, o checkout pede-lhe que marque: “Quero acesso imediato e aceito perder o direito de livre resolução de 14 dias.” Por isso não há reembolso por desistência.</li>
<li>Se o Pro não funcionar como descrito, aplica-se a garantia legal: corrigimos, reduzimos o preço ou devolvemos o que pagou. <a href="/pt/pinchahide/refund.html">Política de reembolso</a>.</li></ul></div>
</div></section>
<section class="wrap" aria-labelledby="perm"><h2 id="perm">Permissões, em linguagem simples</h2>
<table><caption class="visually-hidden">Permissões do Chrome que o PinchaHide pede e porquê</caption><thead><tr><th scope="col">Permissão</th><th scope="col">Porquê</th></tr></thead><tbody>{perms}</tbody></table>
<p class="note">As regras de bloqueio são nossas e vêm dentro da extensão; nada é obtido da internet enquanto funciona. A única ligação que o PinchaHide faz sozinho é verificar a sua chave Pro na Polar, e só depois de introduzir uma chave.</p></section>
<section class="wrap faq" aria-labelledby="faq"><h2 id="faq">Perguntas</h2>
<details><summary>Aceita os cookies quando não consegue recusar?</summary><p>Não. O PinchaHide nunca carrega em Aceitar. Se um banner não der forma de recusar, esconde o banner sem lhe responder.</p></details>
<details><summary>Um site deixou de funcionar. O que faço?</summary><p>Clique no ícone do PinchaHide e desligue a proteção nesse site. Também pode pausar o PinchaHide durante uma hora ou até o retomar.</p></details>
<details><summary>O que acontece quando o teste acaba?</summary><p>As funcionalidades Pro deixam de ser aplicadas e o PinchaHide volta à versão gratuita, que continua a recusar banners de cookies. As suas definições Pro ficam guardadas. Não é cobrado nada: não há cartão para cobrar.</p></details>
<details><summary>Preciso de uma conta?</summary><p>Não. Depois do pagamento, a chave de licença fica no portal de cliente da Polar: abra-o pelo link do email de confirmação ou entre com o email que usou na compra; cola-a nas Opções do PinchaHide.</p></details>
<details><summary>Uma chave do PinchaPlay funciona no PinchaHide?</summary><p>Não. Cada app tem o seu Pro e a sua chave.</p></details>
</section>
<section class="wrap"><p><a href="/pt/pinchahide/transparency.html">Relatório de transparência</a> · <a href="/pt/pinchahide/privacy.html">Política de privacidade</a> · <a href="/pt/pinchahide/terms.html">Termos de venda e EULA</a> · <a href="/pt/pinchahide/refund.html">Política de reembolso</a></p></section>
"""
        title = "PinchaHide: rejeitar banners de cookies automaticamente, no Chrome"
        desc = "PinchaHide – Recusar banners de cookies, para o Chrome: responde aos banners com “rejeitar” por si e envia o Global Privacy Control. Grátis; Pro a partir de %s. Não recolhe nada." % MIN_ATUAL["pt"]
    body = body.format(cws=cws, buy=buy_top, shots=shots, shots_zoom=shots_zoom, rows=rows, mn=MIN_ATUAL[lang], fim=FIM_MIN[lang], ini=INICIO_DEPOIS[lang],
                       md=MIN_DEPOIS[lang], buttons=buy_buttons(lang, PINCHAHIDE_CHECKOUT), perms=perm_rows)
    return page(lang, "/pinchahide/", title, desc, body, current="pinchahide")


# ---------------------------------------------------------------- legal docs from the extension's own texts
def split_md(path):
    txt = open(path, encoding="utf-8").read()
    en, pt = txt.split("\n---\n", 1)
    return {"en": en.strip(), "pt": pt.strip()}


def terms(lang):
    src = split_md(os.path.join(HERE, "textos", "TERMOS-1.12-EN-PT.md"))[lang]
    lines = [l for l in src.splitlines() if l.strip()]
    h1, meta = lines[0].lstrip("# ").strip(), lines[1].strip()
    out = []
    for l in lines[2:]:
        m = re.match(r"(\d+)\. ([^:]+): (.*)", l)
        n, head, rest = m.group(1), m.group(2), m.group(3)
        rest = rest[0].upper() + rest[1:]
        out.append('<h2 id="s%s">%s. %s</h2>\n<p>%s</p>' % (n, n, e(head), linkify(rest)))
    refund = "/pinchaplay/refund.html" if lang == "en" else "/pt/pinchaplay/refund.html"
    privacy = "/pinchaplay/privacy.html" if lang == "en" else "/pt/pinchaplay/privacy.html"
    call = ({"en": 'These terms include the End-User Licence Agreement (EULA, clause 8). PinchaPlay is proprietary software. See also the <a href="%s">refund policy</a> and the <a href="%s">privacy policy</a>. If translations differ, the English text prevails, without prejudice to mandatory consumer rights. The extension will carry this same text from its next update.',
             "pt": 'Estes termos incluem o Contrato de Licença de Utilizador Final (EULA, cláusula 8). O PinchaPlay é software proprietário. Veja também a <a href="%s">política de reembolso</a> e a <a href="%s">política de privacidade</a>. Se as traduções divergirem, prevalece o texto inglês, sem prejuízo dos direitos imperativos do consumidor. A extensão passa a levar este mesmo texto na próxima atualização.'}[lang]) % (refund, privacy)
    body = '<div class="wrap narrow doc"><h1>%s</h1><p class="meta">%s</p><p class="callout">%s</p>\n%s\n</div>' % (e(h1), e(meta), call, "\n".join(out))
    title = h1
    desc = {"en": "Terms of sale and licence (EULA) for PinchaPlay Pro: pay what you think is fair from a minimum, 15-day free trial, right of withdrawal waiver, legal guarantee.",
            "pt": "Termos de venda e licença (EULA) do PinchaPlay Pro: pague o que achar justo a partir de um mínimo, 15 dias de teste, renúncia à livre resolução, garantia legal."}[lang]
    return page(lang, "/pinchaplay/terms.html", title, desc, body, current="pinchaplay")


def md_inline(t):
    """Markdown simples (só o que os textos usam): `código`, **negrito**, links e emails."""
    out = []
    for p in re.split(r"(`[^`]+`)", t):
        if len(p) > 1 and p.startswith("`") and p.endswith("`"):
            out.append("<code>%s</code>" % e(p[1:-1]))
        else:
            out.append(re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", linkify(p)))
    return "".join(out)


def md_block(src):
    """Títulos ##, parágrafos, tabelas | a | b | e listas 1. (o texto de origem não tem HTML)."""
    out, rows, items, bullets = [], [], [], []

    def flush():
        if rows:
            head = rows[0]
            body = [r for r in rows[1:] if not re.match(r"^[\s|:-]+$", "|".join(r))]
            th = "".join('<th scope="col">%s</th>' % md_inline(c) for c in head)
            tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % md_inline(c) for c in r) for r in body)
            out.append('<div class="tablewrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, tr))
            rows.clear()
        if items:
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % md_inline(i) for i in items))
            items.clear()
        if bullets:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % md_inline(i) for i in bullets))
            bullets.clear()

    for l in src.splitlines():
        l = l.strip()
        if not l or l.startswith("<!--"):
            flush()
            continue
        if l.startswith("|"):
            rows.append([c.strip() for c in l.strip("|").split("|")])
            continue
        m = re.match(r"^\d+\. (.*)", l)
        if m:
            if bullets:
                flush()
            items.append(m.group(1))
            continue
        if l.startswith("- "):
            if items:
                flush()
            bullets.append(l[2:])
            continue
        flush()
        if l.startswith("## "):
            out.append("<h2>%s</h2>" % md_inline(l[3:]))
        else:
            out.append("<p>%s</p>" % md_inline(l))
    flush()
    return "\n".join(out)


def transparency(lang, app="PinchaPlay", fname="TRANSPARENCIA-EN-PT.md"):
    src = split_md(os.path.join(HERE, "textos", fname))[lang]
    lines = [l for l in src.splitlines() if l.strip() and not l.startswith("<!--")]
    h1 = lines[0].lstrip("# ").strip()
    body = '<div class="wrap narrow doc"><h1>%s</h1>\n%s\n</div>' % (e(h1), md_block("\n".join(lines[1:])))
    desc = {"en": "What %s can access and why, every network connection it makes, where your data stays, and how to check it yourself." % app,
            "pt": "O que o %s pode aceder e porquê, todas as ligações de rede que faz, onde ficam os seus dados e como verificar por si." % app}[lang]
    slug = app.lower()
    return page(lang, "/%s/transparency.html" % slug, h1, desc, body, current=slug)


def pinchahide_transparency(lang):
    return transparency(lang, "PinchaHide", "PINCHAHIDE-TRANSPARENCIA-EN-PT.md")


def privacy(lang):
    src = split_md(os.path.join(HERE, "textos", "PRIVACIDADE-1.8-EN-PT.md"))[lang]
    lines = [l.strip() for l in src.splitlines() if l.strip()]
    h1, meta = lines[0].lstrip("# ").strip(), lines[1]
    out, in_list = [], False
    for l in lines[2:]:
        if l.startswith("Online:"):
            continue
        if re.match(r"^\d+\. ", l) and len(l) < 80:
            if in_list:
                out.append("</ul>"); in_list = False
            n = l.split(".")[0]
            out.append('<h2 id="s%s">%s</h2>' % (n, e(l)))
        elif l.startswith("- "):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append("<li>%s</li>" % linkify(l[2:]))
        else:
            if in_list:
                out.append("</ul>"); in_list = False
            out.append("<p>%s</p>" % linkify(l))
    if in_list:
        out.append("</ul>")
    note = {"en": "The extension will carry this same text from its next update.", "pt": "A extensão passa a levar este mesmo texto na próxima atualização."}[lang]
    tr = {"en": 'What PinchaPlay can access, every network connection it makes and how to check it yourself: <a href="/pinchaplay/transparency.html">transparency report</a>.',
          "pt": 'O que o PinchaPlay pode aceder, todas as ligações de rede que faz e como verificar por si: <a href="/pt/pinchaplay/transparency.html">relatório de transparência</a>.'}[lang]
    body = '<div class="wrap narrow doc"><h1>%s</h1><p class="meta">%s · %s</p><p class="callout">%s</p>\n%s\n</div>' % (e(h1), e(meta), note, tr, "\n".join(out))
    desc = {"en": "PinchaPlay's privacy policy: no tracking, no analytics, data stays on your device; the only network request is the licence check with Polar.",
            "pt": "Política de privacidade do PinchaPlay: sem rastreio nem analytics, os dados ficam no seu dispositivo; o único pedido de rede é a verificação da licença na Polar."}[lang]
    return page(lang, "/pinchaplay/privacy.html", h1, desc, body, current="pinchaplay")


def refund(lang, app="PinchaPlay", terms_v="1.9"):
    if lang == "en":
        body = """<div class="wrap narrow doc"><h1>PinchaPlay Pro – Refund policy</h1><p class="meta">Last updated: 11 November 2026 · Matches the Terms of sale, version 1.12</p>
<h2 id="s1">1. Try it first</h2>
<p>Every Pro feature can be tried free for 15 days from installation, without sign-up, payment or card. Please use the trial to check that PinchaPlay Pro works for you before you buy.</p>
<h2 id="s2">2. No refund for a change of mind</h2>
<p>PinchaPlay Pro is digital content delivered immediately (a licence key). Before paying, the checkout asks you to tick the box “I want immediate access and I accept that I lose my 14-day right of withdrawal.” By ticking it you ask for immediate access and accept that you lose the right of withdrawal once supply has begun. The same sentence is repeated in your confirmation email. For this reason we do not offer refunds for a change of mind (clause 6 of the <a href="/pinchaplay/terms.html">Terms</a>).</p>
<h2 id="s3">3. If Pro does not work as described</h2>
<p>Your legal guarantee always applies. If Pro does not work as described, you are entitled to have it fixed, a price reduction or a refund (Decree-Law 84/2021 / Directive (EU) 2019/770; clause 7 of the Terms). A refund returns the amount you actually paid.</p>
<h2 id="s4">4. How to ask</h2>
<ul><li>Email <a href="mailto:{email}">{email}</a>.</li>
<li>Write from, or mention, the email address you used at checkout, so we can find your order.</li>
<li>Tell us what does not work, on which site and in which Chrome version, if you can.</li></ul>
<p>We first try to fix the problem. If we cannot, we reduce the price or refund through Polar, our merchant of record. The money goes back to the original payment method; how long your bank takes to show it is outside our control. After a full refund the licence key is revoked and PinchaPlay returns to the free version, which keeps working.</p>
<h2 id="s5">5. Polar</h2>
<p>Polar, as the seller of record, may also decide refunds under its own buyer terms, for example to prevent chargebacks.</p>
</div>""".replace("{email}", EMAIL)
        h1, desc = "PinchaPlay Pro – Refund policy", "PinchaPlay Pro refund policy: 15-day free trial first; no refund for a change of mind after the withdrawal waiver; the legal guarantee always applies."
    else:
        body = """<div class="wrap narrow doc"><h1>PinchaPlay Pro – Política de reembolso</h1><p class="meta">Última atualização: 11 de novembro de 2026 · De acordo com os Termos de venda, versão 1.12</p>
<h2 id="s1">1. Experimente primeiro</h2>
<p>Todas as funcionalidades Pro podem ser experimentadas grátis durante 15 dias a contar da instalação, sem registo, sem pagamento e sem cartão. Use o teste para confirmar que o PinchaPlay Pro lhe serve antes de comprar.</p>
<h2 id="s2">2. Sem reembolso por desistência</h2>
<p>O PinchaPlay Pro é conteúdo digital fornecido de imediato (uma chave de licença). Antes de pagar, o checkout pede-lhe que marque a caixa “Quero acesso imediato e aceito perder o direito de livre resolução de 14 dias.” Ao marcá-la pede o acesso imediato e aceita perder o direito de livre resolução logo que o fornecimento se inicie. A mesma frase é repetida no email de confirmação. Por isso não fazemos reembolsos por desistência (cláusula 6 dos <a href="/pt/pinchaplay/terms.html">Termos</a>).</p>
<h2 id="s3">3. Se o Pro não funcionar como descrito</h2>
<p>A sua garantia legal aplica-se sempre. Se o Pro não funcionar como descrito, tem direito à reposição da conformidade, à redução do preço ou ao reembolso (DL 84/2021; cláusula 7 dos Termos). O reembolso devolve o valor que efetivamente pagou.</p>
<h2 id="s4">4. Como pedir</h2>
<ul><li>Escreva para <a href="mailto:{email}">{email}</a>.</li>
<li>Escreva a partir do email que usou no checkout, ou indique-o, para encontrarmos a encomenda.</li>
<li>Diga-nos o que não funciona, em que site e em que versão do Chrome, se puder.</li></ul>
<p>Primeiro tentamos resolver o problema. Se não conseguirmos, reduzimos o preço ou reembolsamos através da Polar, o nosso revendedor (merchant of record). O dinheiro volta ao meio de pagamento original; o tempo que o seu banco demora a mostrá-lo não depende de nós. Depois de um reembolso total, a chave de licença é revogada e o PinchaPlay volta à versão gratuita, que continua a funcionar.</p>
<h2 id="s5">5. Polar</h2>
<p>A Polar, enquanto vendedora registada, pode também decidir reembolsos ao abrigo dos seus próprios termos de comprador, por exemplo para evitar estornos.</p>
</div>""".replace("{email}", EMAIL)
        h1, desc = "PinchaPlay Pro – Política de reembolso", "Política de reembolso do PinchaPlay Pro: primeiro 15 dias de teste grátis; sem reembolso por desistência depois da renúncia; a garantia legal aplica-se sempre."
    if app != "PinchaPlay":
        body, h1, desc = (re.sub(r"(version|versão) 1\.\d+", r"\g<1> " + terms_v, x.replace("PinchaPlay", app).replace("/pinchaplay/", "/%s/" % app.lower()))
                          for x in (body, h1, desc))
    slug = app.lower()
    return page(lang, "/%s/refund.html" % slug, h1, desc, body, current=slug)


def pinchahide_legal(lang, fname, path, desc, callout=""):
    """Termos e Privacidade do PinchaHide: markdown com títulos ## (iguais aos do pacote do PinchaHide)."""
    src = split_md(os.path.join(HERE, "textos", fname))[lang]
    lines = [l for l in src.splitlines() if l.strip()]
    h1, meta = lines[0].lstrip("# ").strip(), lines[1].strip()
    call = '<p class="callout">%s</p>' % callout if callout else ""
    body = '<div class="wrap narrow doc"><h1>%s</h1><p class="meta">%s</p>%s\n%s\n</div>' % (e(h1), md_inline(meta), call, md_block("\n".join(lines[2:])))
    return page(lang, path, h1, desc[lang], body, current="pinchahide")


def pinchahide_terms(lang):
    return pinchahide_legal(lang, "PINCHAHIDE-TERMOS-1.1-EN-PT.md", "/pinchahide/terms.html", {
        "en": "Terms of sale and licence (EULA) for PinchaHide Pro: pay what you think is fair from a minimum, 15-day free trial, right of withdrawal waiver, legal guarantee.",
        "pt": "Termos de venda e licença (EULA) do PinchaHide Pro: pague o que achar justo a partir de um mínimo, 15 dias de teste, renúncia à livre resolução, garantia legal."})


def pinchahide_privacy(lang):
    return pinchahide_legal(lang, "PINCHAHIDE-PRIVACIDADE-1.0-EN-PT.md", "/pinchahide/privacy.html", {
        "en": "Privacy policy for PinchaHide: no analytics or tracking, data stays on your device; the only network connection is the licence check with Polar.",
        "pt": "Política de privacidade do PinchaHide: sem analítica nem rastreio, os dados ficam no seu dispositivo; a única ligação de rede é a verificação da licença na Polar."},
        {"en": 'What PinchaHide can access, every network connection it makes and how to check it yourself: <a href="/pinchahide/transparency.html">transparency report</a>.',
         "pt": 'O que o PinchaHide pode aceder, todas as ligações de rede que faz e como verificar por si: <a href="/pt/pinchahide/transparency.html">relatório de transparência</a>.'}[lang])


def pinchahide_refund(lang):
    return refund(lang, "PinchaHide", "1.1")


# ---------------------------------------------------------------- about, legal notice, 404, redirects
def about(lang):
    if lang == "en":
        body = """<div class="wrap narrow"><section class="hero nopad"><p class="eyebrow">About</p><h1>Tools you can trust</h1>
<p class="lead">A pinchavelho is the small part that makes a machine work. That is what we build: small, simple, useful tools for your browser.</p></section>
<p>We started from a real concern: many free extensions collect data, show ads or hide code that does more than it says. So we build our own tools, ones people can trust, and we say clearly what they do and what they don’t.</p>
<p>We are an independent, one-person studio in Portugal. Our software is proprietary (closed source); this website and our policies are public.</p>
<h2>Our principles</h2></div><div class="wrap">{values}</div>
<div class="wrap narrow"><h2>Contact</h2><p>Questions, bugs or ideas: <a href="mailto:{email}">{email}</a>. Trader details are in the <a href="/legal-notice.html">legal notice</a>.</p></div>"""
        title, desc = "About Pinchavelho", "Pinchavelho is an independent, one-person software studio in Portugal that makes small, privacy-first browser tools."
    else:
        body = """<div class="wrap narrow"><section class="hero nopad"><p class="eyebrow">Sobre</p><h1>Ferramentas em que pode confiar</h1>
<p class="lead">Um pinchavelho é a pequena peça que faz uma máquina funcionar. É isso que fazemos: ferramentas pequenas, simples e úteis para o seu navegador.</p></section>
<p>Partimos de uma preocupação real: muitas extensões gratuitas recolhem dados, mostram anúncios ou escondem código que faz mais do que diz. Por isso fazemos as nossas próprias ferramentas, em que as pessoas possam confiar, e dizemos com clareza o que fazem e o que não fazem.</p>
<p>Somos um estúdio independente de uma pessoa, em Portugal. O nosso software é proprietário (código fechado); este site e as nossas políticas são públicos.</p>
<h2>Os nossos princípios</h2></div><div class="wrap">{values}</div>
<div class="wrap narrow"><h2>Contacto</h2><p>Dúvidas, erros ou ideias: <a href="mailto:{email}">{email}</a>. Os dados do vendedor estão no <a href="/pt/legal-notice.html">aviso legal</a>.</p></div>"""
        title, desc = "Sobre a Pinchavelho", "A Pinchavelho é um estúdio de software independente, de uma pessoa, em Portugal, que faz ferramentas pequenas para o navegador com a privacidade em primeiro lugar."
    return page(lang, "/about.html", title, desc, body.format(values=values_grid(lang), email=EMAIL), current="about")


def legal_notice(lang):
    gh = "https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement"
    if lang == "en":
        body = """<div class="wrap narrow doc"><h1>Legal notice</h1><p class="meta">Last updated: 9 November 2026</p>
<h2>Who we are</h2><dl class="trader"><dt>Trader</dt><dd>{nome}, trading as “Pinchavelho” (sole trader)</dd><dt>Address</dt><dd>{morada}</dd><dt>NIF / Tax ID</dt><dd>{nif}</dd><dt>Email</dt><dd><a href="mailto:{email}">{email}</a></dd><dt>Website</dt><dd><a href="https://pinchavelho.github.io/">https://pinchavelho.github.io</a></dd></dl>
<h2>Products and sales</h2><p>Pinchavelho makes the browser extensions PinchaPlay and PinchaHide. Pro licences are sold by Polar Software Inc. (polar.sh) as our reseller and merchant of record; Polar handles payment, VAT/sales tax and invoices. Software, licences and support are provided by the trader above. Each product has its own privacy policy, terms of sale and refund policy, linked from its page.</p>
<h2>Disclaimer</h2><p>Our software is provided “as is” to the extent permitted by law. Nothing in this notice limits your mandatory consumer rights, including the legal guarantee of conformity for paid features. You are responsible for how you use our tools: respect copyright and each website’s terms. Our tools do not host or provide any content, and never get around copy protection (DRM), encryption, paywalls or other technical protection measures.</p>
<h2>Complaints and disputes</h2><p>Please contact us first at <a href="mailto:{email}">{email}</a>. Electronic complaints book: <a href="https://www.livroreclamacoes.pt">www.livroreclamacoes.pt</a>. Alternative dispute resolution: CNIACC – Centro Nacional de Informação e Arbitragem de Conflitos de Consumo (<a href="https://www.cniacc.pt">www.cniacc.pt</a>) or the competent ADR centre.</p>
<h2>This website and your privacy</h2><p>No cookies, no analytics, no trackers and no third-party resources; fonts are self-hosted. Hosted by GitHub Pages (GitHub, Inc., USA), which may log visitors’ IP addresses for security, under <a href="{gh}">GitHub’s privacy statement</a>. For PinchaPlay, see its <a href="/pinchaplay/privacy.html">privacy policy</a>.</p>
<h2>Intellectual property</h2><p>Pinchavelho, PinchaPlay, PinchaHide, the logos, icons and all site content are © 2026 {nome}, trading as Pinchavelho. All rights reserved. Chrome is a trademark of Google LLC. Fonts: Inter and Space Grotesk, used under the SIL Open Font License 1.1 (<a href="/assets/fonts/OFL-Inter.txt">Inter licence</a>, <a href="/assets/fonts/OFL-SpaceGrotesk.txt">Space Grotesk licence</a>).</p></div>"""
        title, desc = "Legal notice", "Trader details for Pinchavelho (José Pinhão, sole trader, Portugal), sales through Polar, complaints and intellectual property."
    else:
        body = """<div class="wrap narrow doc"><h1>Aviso legal</h1><p class="meta">Última atualização: 9 de novembro de 2026</p>
<h2>Quem somos</h2><dl class="trader"><dt>Comerciante</dt><dd>{nome}, que usa a designação “Pinchavelho” (empresário em nome individual)</dd><dt>Morada</dt><dd>{morada}</dd><dt>NIF</dt><dd>{nif}</dd><dt>Email</dt><dd><a href="mailto:{email}">{email}</a></dd><dt>Site</dt><dd><a href="https://pinchavelho.github.io/pt/">https://pinchavelho.github.io</a></dd></dl>
<h2>Produtos e vendas</h2><p>A Pinchavelho faz as extensões de navegador PinchaPlay e PinchaHide. As licenças Pro são vendidas pela Polar Software Inc. (polar.sh), o nosso revendedor e merchant of record; a Polar trata do pagamento, do IVA/impostos e das faturas. O software, as licenças e o suporte são fornecidos pelo comerciante acima. Cada produto tem a sua política de privacidade, termos de venda e política de reembolso, com ligação na sua página.</p>
<h2>Exclusão de responsabilidade</h2><p>O nosso software é fornecido “tal como está”, na medida permitida por lei. Nada neste aviso limita os seus direitos imperativos de consumidor, incluindo a garantia legal de conformidade das funcionalidades pagas. É responsável pela forma como usa as nossas ferramentas: respeite os direitos de autor e os termos de cada site. As nossas ferramentas não alojam nem fornecem conteúdos e nunca contornam proteções contra cópia (DRM), cifragem, paywalls ou outras medidas técnicas de proteção.</p>
<h2>Reclamações e litígios</h2><p>Contacte-nos primeiro em <a href="mailto:{email}">{email}</a>. Livro de Reclamações Eletrónico: <a href="https://www.livroreclamacoes.pt">www.livroreclamacoes.pt</a>. Resolução alternativa de litígios: CNIACC – Centro Nacional de Informação e Arbitragem de Conflitos de Consumo (<a href="https://www.cniacc.pt">www.cniacc.pt</a>) ou o centro de arbitragem competente.</p>
<h2>Este site e a sua privacidade</h2><p>Sem cookies, analytics, rastreadores nem recursos de terceiros; as fontes estão alojadas no próprio site. Alojado no GitHub Pages (GitHub, Inc., EUA), que pode registar o endereço IP dos visitantes por segurança, ao abrigo da <a href="{gh}">declaração de privacidade do GitHub</a>. Para o PinchaPlay, veja a sua <a href="/pt/pinchaplay/privacy.html">política de privacidade</a>.</p>
<h2>Propriedade intelectual</h2><p>Pinchavelho, PinchaPlay, PinchaHide, os logótipos, os ícones e todo o conteúdo do site são © 2026 {nome}, que usa a designação Pinchavelho. Todos os direitos reservados. Chrome é uma marca da Google LLC. Tipos de letra: Inter e Space Grotesk, usados ao abrigo da SIL Open Font License 1.1 (<a href="/assets/fonts/OFL-Inter.txt">licença da Inter</a>, <a href="/assets/fonts/OFL-SpaceGrotesk.txt">licença da Space Grotesk</a>).</p></div>"""
        title, desc = "Aviso legal", "Dados do comerciante Pinchavelho (José Pinhão, empresário em nome individual, Portugal), vendas através da Polar, reclamações e propriedade intelectual."
    body = body.format(nome=VENDEDOR_NOME, morada=VENDEDOR_MORADA, nif=VENDEDOR_NIF, email=EMAIL, gh=gh)
    return page(lang, "/legal-notice.html", title, desc, body)


def not_found():
    body = """<div class="wrap narrow hero"><p class="eyebrow">404</p><h1>Page not found</h1><p class="lead">This page does not exist or has moved.</p>
<div class="actions"><a class="btn" href="/">Home page</a><a class="btn ghost" href="/pinchaplay/">PinchaPlay</a><a class="btn ghost" href="/pinchahide/">PinchaHide</a></div>
<div lang="pt-PT"><h2>Página não encontrada</h2><p>Esta página não existe ou mudou de sítio. <a href="/pt/">Ir para a página inicial</a>.</p></div></div>"""
    return page("en", "/404.html", "Page not found · Pinchavelho", "This page does not exist or has moved.", body, noindex=True, alt_path="/")


def moved(lang, old, new):
    """Página antiga que redireciona (sem JavaScript) para o endereço novo."""
    target = url(lang, new)
    txt = {"en": ("This page has moved", 'This page is now at <a href="%s">%s</a>.'),
           "pt": ("Esta página mudou de sítio", 'Esta página está agora em <a href="%s">%s</a>.')}[lang]
    body = '<div class="wrap narrow hero"><h1>%s</h1><p class="lead">%s</p></div>' % (txt[0], txt[1] % (target, SITE + target))
    p = page(lang, old, txt[0], txt[0] + ".", body, noindex=True, redirect=target, alt_path=new)
    return p.replace('href="%s"' % (SITE + url(lang, old)), 'href="%s"' % (SITE + target)).replace(
        'content="%s"' % (SITE + url(lang, old)), 'content="%s"' % (SITE + target))


# ---------------------------------------------------------------- sitemap
PAGES = ["/", "/pinchaplay/", "/pinchaplay/transparency.html", "/pinchaplay/privacy.html", "/pinchaplay/terms.html", "/pinchaplay/refund.html",
         "/pinchahide/", "/pinchahide/transparency.html", "/pinchahide/privacy.html", "/pinchahide/terms.html", "/pinchahide/refund.html", "/about.html", "/legal-notice.html"]


def sitemap():
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p in PAGES:
        for lang in ("en", "pt"):
            out.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod>" % (SITE, url(lang, p), LASTMOD))
            out.append('    <xhtml:link rel="alternate" hreflang="en" href="%s%s"/>' % (SITE, p))
            out.append('    <xhtml:link rel="alternate" hreflang="pt-PT" href="%s/pt%s"/>' % (SITE, p))
            out.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/></url>' % (SITE, p))
    out.append("</urlset>")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- main
def write(root, rel, content):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    gens = {"index.html": home, "pinchaplay/index.html": pinchaplay, "pinchaplay/privacy.html": privacy,
            "pinchaplay/terms.html": terms, "pinchaplay/transparency.html": transparency, "pinchaplay/refund.html": refund, "pinchahide/index.html": pinchahide, "pinchahide/terms.html": pinchahide_terms, "pinchahide/privacy.html": pinchahide_privacy, "pinchahide/refund.html": pinchahide_refund, "pinchahide/transparency.html": pinchahide_transparency,
            "about.html": about, "legal-notice.html": legal_notice}
    for rel, fn in gens.items():
        write(root, rel, fn("en"))
        write(root, "pt/" + rel, fn("pt"))
    write(root, "404.html", not_found())
    # Endereços antigos da app de vídeo (antes do nome PinchaPlay): redirecionam para /pinchaplay/.
    for old in ("index.html", "privacy.html", "terms.html", "refund.html"):
        new = "/pinchaplay/" + ("" if old == "index.html" else old)
        oldp = "/playpilot/" + ("" if old == "index.html" else old)
        write(root, "playpilot/" + old, moved("en", oldp, new))
        write(root, "pt/playpilot/" + old, moved("pt", oldp, new))
    # Nomes anteriores (até 11/11/2026): /ritmello/ e /vedello/ redirecionam para os nomes novos.
    for oldslug, newslug in (("ritmello", "pinchaplay"), ("vedello", "pinchahide")):
        for old in ("index.html", "privacy.html", "terms.html", "refund.html", "transparency.html"):
            tail = "" if old == "index.html" else old
            write(root, oldslug + "/" + old, moved("en", "/%s/%s" % (oldslug, tail), "/%s/%s" % (newslug, tail)))
            write(root, "pt/" + oldslug + "/" + old, moved("pt", "/%s/%s" % (oldslug, tail), "/%s/%s" % (newslug, tail)))
    write(root, "sitemap.xml", sitemap())
    print("OK: páginas geradas em", os.path.abspath(root))
