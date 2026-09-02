# -*- coding: utf-8 -*-
"""Generuje index.html i podstrony projektów (wersja „Nestora”: minimalizm, duże zdjęcia).
Uruchom:  python3 _materials/build_site.py
"""
import os, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import PROJECTS, BY_SLUG, STD_ARC, title_of  # noqa: E402

# ---------------------------------------------------------------- ikony (jeden zestaw: kreska 1.6, siatka 24)
def ic(path, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{path}</svg>'
I_ARROW = ic('<path d="M4 12h16M14 6l6 6-6 6"/>')
I_PREV = ic('<path d="M20 12H4M10 6l-6 6 6 6"/>')
I_CLOSE = ic('<path d="M6 6l12 12M18 6L6 18"/>')
I_PLUS = ic('<path d="M12 5v14M5 12h14"/>')
I_CHECK = ic('<path d="M5 12.5l4.5 4.5L19 7"/>')
I_DOWN = ic('<path d="M12 4v16M6 14l6 6 6-6"/>')
I_ZOOM = ic('<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>')

def pic(src, alt, lazy=True, sizes="100vw", w960=True, extra=""):
    base = src.rsplit('.', 1)[0]
    srcset = f' srcset="{base}-960.webp 960w, {src} 1920w" sizes="{sizes}"' if w960 else ''
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    return f'<img src="{src}"{srcset} alt="{html.escape(alt)}"{load} {extra}>'

def area_txt(p):
    return f"{p['area']:.1f}".replace(".", ",").replace(",0", "")

# ---------------------------------------------------------------- shared
def head(title, desc, rel="", og=""):
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{rel}img/{og or 'forest/hero.webp'}">
<meta name="theme-color" content="#F6F4EF">
<link rel="icon" href="{rel}img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{rel}img/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}css/style.css">
</head>
<body>
<a class="skip" href="#main">Przejdź do treści</a>
'''

def nav(rel="", light=False):
    return f'''<header class="nav{' nav--light' if light else ''}" id="nav">
  <div class="nav__in">
    <a class="nav__logo" href="{rel}index.html" aria-label="MoVilla, strona główna"><img src="{rel}img/logo.webp" alt="MoVilla" width="132" height="38"></a>
    <nav class="nav__links" aria-label="Menu główne">
      <a href="{rel}index.html#projekty">Projekty</a>
      <a href="{rel}index.html#technologia">Technologia</a>
      <a href="{rel}index.html#proces">Proces</a>
      <a href="{rel}index.html#standard">Standard</a>
      <a href="{rel}index.html#kontakt">Kontakt</a>
    </nav>
    <a class="btn btn--sm nav__cta" href="{rel}index.html#kontakt">Zapytaj o wycenę</a>
    <button class="nav__burger" type="button" aria-label="Otwórz menu" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="menu" id="menu" aria-hidden="true">
  <nav class="menu__links" aria-label="Menu mobilne">
    <a href="{rel}index.html#projekty">Projekty</a>
    <a href="{rel}index.html#technologia">Technologia</a>
    <a href="{rel}index.html#proces">Proces</a>
    <a href="{rel}index.html#standard">Standard</a>
    <a href="{rel}index.html#kontakt">Kontakt</a>
  </nav>
  <div class="menu__models">
    <span class="label">Projekty domów</span>
    <a href="{rel}projekty/archouse-70.html">ArcHouse 70 <span>69,5 m²</span></a>
    <a href="{rel}projekty/mysa-120.html">MYSA 120 <span>120,2 m²</span></a>
    <a href="{rel}projekty/barnhouse-85.html">BarnHouse 85 <span>85 m²</span></a>
    <a href="{rel}projekty/barnhouse-130.html">BarnHouse 130 <span>130 m²</span></a>
    <a href="{rel}projekty/foresthouse.html">ForestHouse <span>90 m²</span></a>
  </div>
  <p class="menu__foot"><a href="mailto:hello@movilla.pl">hello@movilla.pl</a><span>Jesionowa 22, 40‑158 Katowice</span></p>
</div>
'''

def footer(rel=""):
    return f'''<footer class="footer">
  <div class="footer__in">
    <div class="footer__brand">
      <img src="{rel}img/logo.webp" alt="MoVilla" width="150" height="43">
      <p>Nowoczesne domy całoroczne w stalowej konstrukcji szkieletowej. Standard deweloperski podwyższony, realizacja w 30–60 dni.</p>
    </div>
    <div class="footer__col"><span class="label">Projekty</span>
      <a href="{rel}projekty/archouse-70.html">ArcHouse 70</a><a href="{rel}projekty/mysa-120.html">MYSA 120</a>
      <a href="{rel}projekty/barnhouse-85.html">BarnHouse 85</a><a href="{rel}projekty/barnhouse-130.html">BarnHouse 130</a>
      <a href="{rel}projekty/foresthouse.html">ForestHouse</a></div>
    <div class="footer__col"><span class="label">Firma</span>
      <a href="{rel}index.html#technologia">Technologia</a><a href="{rel}index.html#proces">Proces</a>
      <a href="{rel}index.html#standard">Standard</a><a href="{rel}index.html#kontakt">Kontakt</a></div>
    <div class="footer__col"><span class="label">Kontakt</span>
      <a href="mailto:hello@movilla.pl">hello@movilla.pl</a><a href="https://www.movilla.pl" target="_blank" rel="noopener">www.movilla.pl</a>
      <span>ADA Group Sp. z o.o.<br>Jesionowa 22, 40‑158 Katowice<br>NIP 9542897994</span></div>
  </div>
  <div class="footer__bottom"><span>© 2026 MoVilla · ADA Group Sp. z o.o.</span><span>Wizualizacje mają charakter poglądowy. Parametry doprecyzowujemy przy adaptacji projektu do działki.</span></div>
</footer>
<div class="mobile-cta"><a class="btn" href="{rel}index.html#kontakt">Zapytaj o wycenę {I_ARROW}</a></div>
'''

def lightbox():
    return f'''<div class="lightbox" role="dialog" aria-modal="true" aria-label="Podgląd zdjęcia" hidden>
  <button class="lightbox__close" type="button" aria-label="Zamknij podgląd">{I_CLOSE}</button>
  <button class="lightbox__nav lightbox__nav--prev" type="button" aria-label="Poprzednie zdjęcie">{I_PREV}</button>
  <figure><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt=""><figcaption></figcaption></figure>
  <button class="lightbox__nav lightbox__nav--next" type="button" aria-label="Następne zdjęcie">{I_ARROW}</button>
</div>
'''

def scripts(rel=""):
    return f'''<script src="{rel}js/vendor/gsap.min.js"></script>
<script src="{rel}js/vendor/ScrollTrigger.min.js"></script>
<script src="{rel}js/main.js"></script>
</body>
</html>
'''

def checklist(items):
    return "".join(f'<li><span class="chk">{I_CHECK}</span><span><b>{k}</b><small>{v}</small></span></li>' for k, v in items)

# ---------------------------------------------------------------- index
def index_html():
    rel = ""
    cards = ""
    for i, p in enumerate(PROJECTS):
        wide = i in (0, 3)
        cards += f'''
      <a class="pj{' pj--wide' if wide else ''}" href="projekty/{p['slug']}.html" data-reveal>
        <span class="pj__media"><span class="pj__img">{pic("img/" + p['hero'], f"{title_of(p)}, wizualizacja domu", sizes="(max-width:760px) 100vw, " + ("100vw" if wide else "50vw"))}</span><span class="pj__tag">{p['family']}</span></span>
        <span class="pj__body">
          <span class="pj__head"><span class="pj__name">{title_of(p)}</span><span class="pj__area">{area_txt(p)} m²</span></span>
          <span class="pj__desc">{p['card_desc']}</span>
          <span class="pj__meta"><span>{p['dims']}</span><span>{p['layout']}</span></span>
          <span class="pj__link">Zobacz projekt {I_ARROW}</span>
        </span>
      </a>'''
    gallery = "".join(f'<figure class="strip__item"><span class="strip__img">{pic("img/" + s, "Wizualizacja: " + c, sizes="(max-width:760px) 85vw, 40vw")}</span><figcaption>{c}</figcaption></figure>'
                      for s, c in [("arc70/lake-1.webp", "ArcHouse 70"), ("forest/int-7.webp", "ForestHouse, wnętrze"), ("barn130/night.webp", "BarnHouse 130"), ("mysa120/int-3.webp", "MYSA 120, antresola"), ("forest/vertical.webp", "Zespół ForestHouse"), ("mysa120/balcony-1.webp", "MYSA 120, balkon"), ("arc70/int-1.webp", "ArcHouse 70, kuchnia")])
    std = checklist(STD_ARC)
    return head("MoVilla: nowoczesne domy całoroczne w 30–60 dni", "Pięć projektów domów całorocznych w stalowej konstrukcji szkieletowej: ArcHouse 70, MYSA 120, BarnHouse 85 i 130, ForestHouse. Standard deweloperski podwyższony, realizacja w 30–60 dni.", rel) + nav(rel, light=True) + f'''
<main id="main">

<section class="hero" id="hero">
  <div class="hero__media">{pic("img/forest/hero.webp", "Dom A-frame MoVilla ForestHouse w górskim krajobrazie o zmierzchu", lazy=False, sizes="100vw")}</div>
  <div class="hero__content">
    <h1 class="hero__title"><span class="line">Nowoczesne domy</span><span class="line">całoroczne.</span><span class="line hero__accent">Gotowe w 30–60 dni.</span></h1>
    <div class="hero__aside">
      <p>Stalowa konstrukcja szkieletowa, standard deweloperski podwyższony i pięć projektów od 69 do 130 m². Dla rodzin i dla inwestorów.</p>
      <div class="hero__actions"><a class="btn btn--light" href="#projekty">Zobacz projekty {I_ARROW}</a><a class="btn btn--ghost" href="#kontakt">Zapytaj o wycenę</a></div>
    </div>
  </div>
  <a class="hero__scroll" href="#intro" aria-label="Przewiń w dół">{I_DOWN}</a>
</section>

<section class="intro" id="intro">
  <div class="wrap">
    <p class="statement" data-split>Projektujemy domy, które łączą architekturę z precyzją stalowej konstrukcji. Zamiast miesięcy budowy: kilka tygodni montażu. Zamiast kompromisów: dom całoroczny, ciepły i gotowy do wykończenia.</p>
    <dl class="facts" data-stagger>
      <div><dt>Projekty domów</dt><dd><span data-count="5">5</span></dd></div>
      <div><dt>Współczynnik U dachu i ścian</dt><dd>≤ <span data-count="0.15" data-decimals="2">0,15</span> <small>W/m²K</small></dd></div>
      <div><dt>Czas realizacji</dt><dd>30–<span data-count="60">60</span> <small>dni</small></dd></div>
      <div><dt>Grubość przegrody głównej</dt><dd><span data-count="425">425</span> <small>mm</small></dd></div>
    </dl>
  </div>
</section>

<section class="projects" id="projekty">
  <div class="wrap">
    <div class="sec-head" data-reveal>
      <h2 class="h2">Pięć projektów.<br>Jedna technologia.</h2>
      <p class="lead">Od kompaktowego domu z łukowym dachem po 130‑metrową stodołę. Każdy w stalowej konstrukcji, każdy całoroczny.</p>
    </div>
    <div class="pj-grid">{cards}</div>
  </div>
</section>

<section class="forms" id="formy">
  <div class="wrap">
    <div class="sec-head" data-reveal>
      <h2 class="h2">Trzy bryły do wyboru.</h2>
      <p class="lead">Ta sama konstrukcja i ten sam standard. Różni je forma dachu i charakter wnętrza.</p>
    </div>
    <div class="forms__grid">
      <a class="form" href="projekty/archouse-70.html" data-reveal>
        <span class="form__img">{pic("img/arc70/lake-2.webp", "Dom z łukowym dachem ArcHouse", sizes="(max-width:760px) 100vw, 33vw")}</span>
        <span class="form__body"><h3>Łuk</h3><p>Krążyny stalowe tworzą łukowy dach przechodzący w ścianę. Przeszklony szczyt, antresola, wnętrze bez ostrych kątów.</p><span class="form__models">ArcHouse 70 · MYSA 120</span></span>
      </a>
      <a class="form" href="projekty/barnhouse-85.html" data-reveal>
        <span class="form__img">{pic("img/barn85/ext-2.webp", "Nowoczesna stodoła BarnHouse", sizes="(max-width:760px) 100vw, 33vw")}</span>
        <span class="form__body"><h3>Stodoła</h3><p>Dwuspadowy dach z blachy na rąbek, ciemna elewacja, przeszklona ściana szczytowa i taras.</p><span class="form__models">BarnHouse 85 · BarnHouse 130</span></span>
      </a>
      <a class="form" href="projekty/foresthouse.html" data-reveal>
        <span class="form__img">{pic("img/forest/ext-2.webp", "Dom A-frame ForestHouse w lesie", sizes="(max-width:760px) 100vw, 33vw")}</span>
        <span class="form__body"><h3>A‑frame</h3><p>Trójkątna bryła z wysokim przeszkleniem frontu i tarasem na piętrze. Gotowa do zamieszkania, także jako produkt inwestycyjny.</p><span class="form__models">ForestHouse</span></span>
      </a>
    </div>
  </div>
</section>

<section class="tech" id="technologia">
  <div class="wrap tech__grid">
    <div class="tech__text" data-reveal>
      <h2 class="h2">Stalowy szkielet.<br>Ciepłe wnętrze.</h2>
      <p class="lead">Domy MoVilla to konstrukcje szkieletowe ze stali: ramy nośne i krążyny posadowione na płycie fundamentowej. Dach i ściany główne tworzą jedną, ciągłą przegrodę o grubości 425 mm z trzema warstwami wełny mineralnej.</p>
      <ul class="tech__list">
        <li><b>U ≤ 0,15 W/m²K</b><span>dach i ściany główne</span></li>
        <li><b>U ≤ 0,20 W/m²K</b><span>ściany szczytowe</span></li>
        <li><b>Uw od 0,5 W/m²K</b><span>szklenie potrójne, fasada Aliplast RAL 7016</span></li>
        <li><b>Ogrzewanie podłogowe</b><span>maty grzewcze w standardzie</span></li>
      </ul>
      <a class="lnk" href="projekty/archouse-70.html#technologia">Pełna specyfikacja przegród {I_ARROW}</a>
    </div>
    <div class="tech__media">
      <figure class="reveal" data-reveal><span class="reveal__img">{pic("img/common/tech-2.webp", "Montaż stalowej konstrukcji szkieletowej domu łukowego", sizes="(max-width:760px) 100vw, 50vw")}</span><figcaption>Montaż stalowej konstrukcji</figcaption></figure>
      <figure class="reveal reveal--sm" data-reveal><span class="reveal__img">{pic("img/common/detail-wall.webp", "Detal warstw dachu, ściany i fundamentu", sizes="(max-width:760px) 60vw, 25vw", w960=False)}</span><figcaption>Detal D‑01: warstwy przegrody</figcaption></figure>
    </div>
  </div>
</section>

<section class="process" id="proces">
  <div class="wrap">
    <div class="sec-head" data-reveal>
      <h2 class="h2">Od rozmowy do kluczy.</h2>
      <p class="lead">Cztery etapy. Większość pracy dzieje się w hali, nie na Twojej działce.</p>
    </div>
    <ol class="steps" data-stagger>
      <li><span class="steps__num">1</span><h3>Wybór i konfiguracja</h3><p>Wybierasz model i wariant: antresola otwarta lub zamknięta, pełny strop, garaż. Ustalamy zakres i standard.</p></li>
      <li><span class="steps__num">2</span><h3>Adaptacja do działki</h3><p>Dopasowujemy projekt do warunków lokalnych i strefy wiatrowej, przygotowujemy dokumentację techniczną i wycenę.</p></li>
      <li class="steps__key"><span class="steps__num">3</span><h3>Produkcja i montaż</h3><p>Płyta fundamentowa, stalowa konstrukcja, przegrody, dach z blachy na rąbek, stolarka i instalacje.</p><span class="steps__time">30–60 dni</span></li>
      <li><span class="steps__num">4</span><h3>Przekazanie</h3><p>Odbierasz dom w standardzie deweloperskim podwyższonym, gotowy do wykończenia wnętrz według własnego pomysłu.</p></li>
    </ol>
  </div>
</section>

<section class="standard" id="standard">
  <div class="wrap standard__grid">
    <div class="standard__text" data-reveal>
      <h2 class="h2">Co dostajesz w standardzie.</h2>
      <p class="lead">Dom przekazujemy w standardzie deweloperskim podwyższonym, przygotowany do dalszych prac wykończeniowych. Ogrzewanie podłogowe, instalacje i stolarka są w cenie.</p>
      <p class="note">Wizualizacje wnętrz mają charakter poglądowy. Wyposażenie ruchome, zabudowa meblowa i finalne wykończenie wnętrz nie są częścią standardu, o ile indywidualna oferta nie stanowi inaczej. ForestHouse jest przekazywany z wykończeniem wnętrza i wyposażeniem łazienek.</p>
    </div>
    <ul class="checklist" data-stagger>{std}</ul>
  </div>
</section>

<section class="gallery" aria-label="Wizualizacje">
  <div class="strip" tabindex="0">{gallery}</div>
</section>

<section class="contact" id="kontakt">
  <div class="wrap contact__grid">
    <div class="contact__text" data-reveal>
      <h2 class="h2">Porozmawiajmy o Twoim domu.</h2>
      <p class="lead">Napisz, który projekt Cię interesuje i gdzie jest działka. Przygotujemy indywidualną konfigurację, zakres realizacji i wycenę.</p>
      <address class="contact__info"><a class="contact__mail" href="mailto:hello@movilla.pl">hello@movilla.pl</a><span>ADA Group Sp. z o.o.<br>Jesionowa 22, 40‑158 Katowice<br>NIP 9542897994</span></address>
    </div>
    <form class="form-grid" novalidate data-reveal>
      <div class="field"><label for="f-name">Imię i nazwisko</label><input id="f-name" name="name" required autocomplete="name"></div>
      <div class="field"><label for="f-email">E‑mail</label><input id="f-email" name="email" type="email" required autocomplete="email" inputmode="email"></div>
      <div class="field"><label for="f-phone">Telefon</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
      <div class="field"><label for="f-proj">Projekt</label><select id="f-proj" name="projekt"><option>Nie wiem jeszcze</option><option>ArcHouse 70</option><option>MYSA 120</option><option>BarnHouse 85</option><option>BarnHouse 130</option><option>ForestHouse</option></select></div>
      <div class="field field--full"><label for="f-place">Lokalizacja działki</label><input id="f-place" name="place" placeholder="miejscowość, województwo"></div>
      <div class="field field--full"><label for="f-msg">Wiadomość</label><textarea id="f-msg" name="msg" rows="4" placeholder="Dom dla siebie czy inwestycja? Kiedy chcesz zacząć?"></textarea></div>
      <p class="field--full form-grid__err" role="alert" hidden>Uzupełnij imię i poprawny adres e‑mail, żebyśmy mogli odpowiedzieć.</p>
      <div class="field--full form-grid__foot"><small>Wysyłając formularz, otworzysz gotową wiadomość w swoim programie pocztowym.</small><button class="btn" type="submit">Wyślij zapytanie {I_ARROW}</button></div>
    </form>
  </div>
</section>

</main>
''' + footer(rel) + lightbox() + scripts(rel)

# ---------------------------------------------------------------- project page
def project_html(p):
    rel = "../"
    nxt = BY_SLUG[p["next"]]
    title = title_of(p)
    params = "".join(f'<div><b>{v} <small>{u}</small></b><span>{l}</span></div>' for v, u, l in p["params"])
    facts = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in p["facts"])
    gallery = "".join(f'<figure class="pg__item" data-lightbox="{rel}img/{s}" data-cap="{c} · wizualizacja"><span class="pg__img">{pic(rel + "img/" + s, f"{title}, {c}, wizualizacja", sizes="(max-width:760px) 100vw, 50vw")}</span><figcaption>{c}</figcaption><span class="pg__zoom" aria-hidden="true">{I_ZOOM}</span></figure>' for s, c in p["gallery"])
    interiors = "".join(f'<figure class="strip__item{" strip__item--tall" if tall else ""}" data-lightbox="{rel}img/{s}" data-cap="Wnętrze, aranżacja przykładowa"><span class="strip__img">{pic(rel + "img/" + s, f"{title}, wnętrze, aranżacja przykładowa", sizes="(max-width:760px) 85vw, 40vw")}</span></figure>' for s, tall in p["interiors"])
    tabs = "".join(f'<button class="tab{" is-active" if i == 0 else ""}" type="button" role="tab" id="tab-{i}" aria-selected="{"true" if i == 0 else "false"}" aria-controls="panel-{i}"><span class="tab__title">{t}</span><span class="tab__chip">{chip}</span></button>' for i, (t, d, chip, img, lab) in enumerate(p["variants"]))
    panels = "".join(f'<div class="tabpanel{" is-active" if i == 0 else ""}" role="tabpanel" id="panel-{i}" aria-labelledby="tab-{i}"{"" if i == 0 else " hidden"}><figure class="tabpanel__img"><img src="{img or (rel + "img/" + p["plans"][0][0])}" alt="{lab}" loading="lazy" decoding="async"><figcaption>{lab}</figcaption></figure><p>{d}</p></div>' for i, (t, d, chip, img, lab) in enumerate(p["variants"]))
    plans = "".join(f'<figure class="plan" data-lightbox="{rel}img/{s}" data-cap="{t}"><span class="plan__img"><img src="{rel}img/{s}" alt="{title}, {t}" loading="lazy" decoding="async"></span><figcaption><b>{t}</b><span>{n}</span></figcaption></figure>' for s, t, n in p["plans"])
    acc = ""
    for i, (t, u, th, desc, layers) in enumerate(p["spec"]):
        lay = "".join(f'<li><span>{n}</span><span class="num">{x}</span></li>' for n, x in layers)
        acc += f'''<div class="acc__item"><h3><button class="acc__btn" type="button" aria-expanded="false" aria-controls="acc-{i}" id="accb-{i}"><span class="acc__t">{t}</span><span class="acc__u">{u}{(" · " + th) if th else ""}</span><span class="acc__plus">{I_PLUS}</span></button></h3>
        <div class="acc__panel" id="acc-{i}" role="region" aria-labelledby="accb-{i}"><div class="acc__in">{f"<p>{desc}</p>" if desc else ""}{f"<ol class=layers>{lay}</ol>" if lay else ""}</div></div></div>'''
    is_forest = p["family_key"] == "forest"
    std_note = ("ForestHouse przekazujemy jako kompletne rozwiązanie: konstrukcja, stolarka, instalacje, wykończenie wnętrza i sanitariaty. Zakres dopasowujemy do inwestycji prywatnej, rekreacyjnej lub komercyjnej."
                if is_forest else "Wizualizacje wnętrz mają charakter poglądowy. Wyposażenie ruchome, zabudowa meblowa i finalne wykończenie wnętrz nie są częścią standardu, o ile indywidualna oferta nie stanowi inaczej.")
    spec_lead = ("Lekka rama stalowa i system warstwowych przegród, zaprojektowane pod stabilność, szybki montaż i estetykę wykończenia."
                 if is_forest else "Główne przegrody zewnętrzne osiągają U ≤ 0,15 W/m²K: wełna mineralna w trzech warstwach, paroizolacja aktywna, fasada aluminiowa z potrójnym szkleniem.")
    side_img = {"arc": "common/frame.webp", "barn": "common/tech-1.webp", "forest": "forest/ext-5.webp"}[p["family_key"]]

    return head(f"{title}: {p['family']} · MoVilla", p["tagline"], rel, p["hero"]) + nav(rel, light=True) + f'''
<main id="main">

<section class="phero">
  <div class="phero__media">{pic(rel + "img/" + p["hero"], f"{title}, wizualizacja domu", lazy=False, sizes="100vw")}</div>
  <div class="phero__content">
    <nav class="crumb" aria-label="Okruszki"><a href="{rel}index.html">MoVilla</a><span>/</span><a href="{rel}index.html#projekty">Projekty</a><span>/</span><span aria-current="page">{title}</span></nav>
    <h1 class="phero__title">{title}</h1>
    <p class="phero__sub">{p['tagline']}</p>
  </div>
</section>
<div class="params"><div class="wrap params__grid">{params}</div></div>

<section class="pintro">
  <div class="wrap pintro__grid">
    <div class="pintro__text" data-reveal>
      <h2 class="h2">{p['intro_title']}</h2>
      {"".join(f"<p>{t}</p>" for t in p["intro"])}
      <div class="pintro__actions"><a class="btn" href="{rel}index.html#kontakt">Zapytaj o ten projekt {I_ARROW}</a><a class="lnk" href="#rzuty">Zobacz rzuty {I_DOWN}</a></div>
    </div>
    <dl class="ptable" data-reveal>{facts}</dl>
  </div>
</section>

<section class="pg" aria-label="Galeria">
  <div class="wrap pg__grid">{gallery}</div>
</section>

<section class="pint">
  <div class="wrap sec-head" data-reveal><h2 class="h2">Przykładowa aranżacja wnętrz.</h2><p class="lead">Przewiń w bok. Dotknij zdjęcia, aby je powiększyć.</p></div>
  <div class="strip" tabindex="0">{interiors}</div>
  <p class="wrap note">Wizualizacje wnętrz mają charakter poglądowy i przedstawiają przykładową aranżację.</p>
</section>

<section class="variants" id="warianty">
  <div class="wrap">
    <div class="sec-head" data-reveal><h2 class="h2">Warianty i konfiguracje.</h2><p class="lead">Dopasuj układ do siebie: wybierz wariant, aby zobaczyć rzut lub wizualizację.</p></div>
    <div class="tabs" role="tablist" aria-label="Warianty">{tabs}</div>
    <div class="tabpanels">{panels}</div>
  </div>
</section>

<section class="plans" id="rzuty">
  <div class="wrap">
    <div class="sec-head" data-reveal><h2 class="h2">Rzuty i przekroje.</h2><p class="lead">Dotknij arkusz, aby zobaczyć go w powiększeniu.</p></div>
    <div class="plans__grid">{plans}</div>
    <p class="note">Parametry mogą zostać doprecyzowane na etapie adaptacji projektu do działki i warunków lokalnych. Rzuty poglądowe; układ pomieszczeń ustalamy indywidualnie.</p>
  </div>
</section>

<section class="spec" id="technologia">
  <div class="wrap spec__grid">
    <div class="spec__side" data-reveal>
      <h2 class="h2">Warstwa po warstwie.</h2>
      <p class="lead">{spec_lead}</p>
      <figure class="reveal"><span class="reveal__img">{pic(rel + "img/" + side_img, "Konstrukcja stalowa MoVilla", sizes="(max-width:760px) 100vw, 40vw")}</span><figcaption>{"Konstrukcja stalowa, wizualizacja" if p["family_key"] != "barn" else "Ramy stalowe na placu montażu"}</figcaption></figure>
    </div>
    <div class="acc" data-reveal>{acc}</div>
  </div>
</section>

<section class="standard" id="standard">
  <div class="wrap standard__grid">
    <div class="standard__text" data-reveal>
      <h2 class="h2">{"Kompletny dom w standardzie." if is_forest else "Standard deweloperski podwyższony."}</h2>
      <p class="lead">{std_note}</p>
      <a class="btn" href="{rel}index.html#kontakt">Poproś o wycenę {I_ARROW}</a>
    </div>
    <ul class="checklist" data-stagger>{checklist(p["standard"])}</ul>
  </div>
</section>

<a class="pnext" href="{rel}projekty/{nxt['slug']}.html">
  <span class="pnext__media">{pic(rel + "img/" + nxt["hero"], f"{title_of(nxt)}, wizualizacja", sizes="100vw")}</span>
  <span class="pnext__content wrap"><span class="label label--light">Następny projekt · {nxt['family']}</span><span class="pnext__title">{title_of(nxt)} {I_ARROW}</span><span class="pnext__meta">{area_txt(nxt)} m² · {nxt['layout']}</span></span>
</a>

</main>
''' + footer(rel) + lightbox() + scripts(rel)

# ---------------------------------------------------------------- write
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html())
os.makedirs(os.path.join(ROOT, "projekty"), exist_ok=True)
for p in PROJECTS:
    with open(os.path.join(ROOT, "projekty", p["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(project_html(p))
print("OK:", "index.html", *[p["slug"] + ".html" for p in PROJECTS])
