# -*- coding: utf-8 -*-
"""Generuje index.html oraz podstrony projektów (świat: harmonogram budowy).
Uruchom:  python3 _materials/build_site.py
"""
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- ikony (jeden zestaw, jedna kreska)
I_ARROW = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
I_CHECK = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'
I_PLUS = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'
I_CLOSE = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
I_PREV = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12H4M10 6l-6 6 6 6"/></svg>'
I_ZOOM = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5M11 8v6M8 11h6"/></svg>'
# sylwetki brył (kreska 1.75, siatka 48)
I_ARC = '<svg class="ic ic--form" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round" aria-hidden="true"><path d="M8 40V26C8 15 15 8 24 8s16 7 16 18v14H8z"/><path d="M8 40h32"/><path d="M18 40V28h12v12"/></svg>'
I_BARN = '<svg class="ic ic--form" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round" aria-hidden="true"><path d="M8 40V20L24 8l16 12v20H8z"/><path d="M8 40h32"/><path d="M19 40V28h10v12"/></svg>'
I_AFRAME = '<svg class="ic ic--form" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linejoin="round" aria-hidden="true"><path d="M6 40L24 8l18 32H6z"/><path d="M6 40h36"/><path d="M19 40V29h10v11"/></svg>'
FORM_ICON = {"arc": I_ARC, "barn": I_BARN, "forest": I_AFRAME}

def pic(src, alt, lazy=True, sizes="100vw", w960=True, extra=""):
    base = src.rsplit('.', 1)[0]
    srcset = f' srcset="{base}-960.webp 960w, {src} 1920w" sizes="{sizes}"' if w960 else ''
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img src="{src}"{srcset} alt="{html.escape(alt)}"{load} {extra}>'

def ruler(unit="dni", maxv=60, step=10, cursor=True):
    labels = "".join(f'<span style="left:{v / maxv * 100:.3f}%"><b>{v}</b></span>' for v in range(0, maxv + 1, step))
    cur = '<div class="ruler__cursor" aria-hidden="true"><em>Dzień <span data-day>0</span></em></div>' if cursor else ''
    cls = "ruler ruler--top" if cursor else "ruler"
    return f'<div class="{cls}" data-max="{maxv}" aria-hidden="true"><div class="ruler__scale">{labels}<i class="ruler__unit">{unit}</i></div>{cur}</div>'

# ---------------------------------------------------------------- shared
def head(title, desc, rel="", og=""):
    return f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{rel}img/{og or 'forest/hero.webp'}">
<meta name="theme-color" content="#F2B92E">
<link rel="icon" href="{rel}img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="{rel}img/favicon-180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300..800&family=Azeret+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}css/style.css">
</head>
<body>
<div class="veil" aria-hidden="true"></div>
'''

def topbar(rel=""):
    return f'''<header class="topbar">
  <a class="topbar__logo" href="{rel}index.html" aria-label="MoVilla, strona główna"><img src="{rel}img/logo.webp" alt="MoVilla"></a>
  <nav class="topbar__nav" aria-label="Menu główne">
    <a href="{rel}index.html#projekty">Modele</a>
    <a href="{rel}index.html#proces">60 dni</a>
    <a href="{rel}index.html#technologia">Warstwy</a>
    <a href="{rel}index.html#standard">Standard</a>
    <a href="{rel}index.html#kontakt">Kontakt</a>
  </nav>
  <a class="btn btn--sm topbar__cta" href="{rel}index.html#kontakt">Poproś o wycenę {I_ARROW}</a>
  <button class="topbar__burger" aria-label="Otwórz menu" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
</header>
<div class="menu" id="menu" aria-hidden="true">
  <nav class="menu__links" aria-label="Menu mobilne">
    <a href="{rel}index.html#projekty">Modele</a>
    <a href="{rel}projekty/archouse-70.html" class="menu__sub">ArcHouse 70</a>
    <a href="{rel}projekty/mysa-120.html" class="menu__sub">MYSA 120</a>
    <a href="{rel}projekty/barnhouse-85.html" class="menu__sub">BarnHouse 85</a>
    <a href="{rel}projekty/barnhouse-130.html" class="menu__sub">BarnHouse 130</a>
    <a href="{rel}projekty/foresthouse.html" class="menu__sub">ForestHouse</a>
    <a href="{rel}index.html#proces">60 dni</a>
    <a href="{rel}index.html#technologia">Warstwy</a>
    <a href="{rel}index.html#standard">Standard</a>
    <a href="{rel}index.html#kontakt">Kontakt</a>
  </nav>
  <p class="menu__foot"><a href="mailto:hello@movilla.pl">hello@movilla.pl</a><span>Jesionowa 22, 40‑158 Katowice</span></p>
</div>
'''

def titleblock(rel=""):
    return f'''<footer class="titleblock" aria-label="Stopka">
  <div class="titleblock__cell titleblock__cell--brand">
    <img src="{rel}img/logo.webp" alt="MoVilla" class="titleblock__logo">
    <p>Domy całoroczne w stalowej konstrukcji szkieletowej. Standard deweloperski podwyższony, realizacja 30–60 dni.</p>
  </div>
  <dl class="titleblock__cell"><dt>Modele</dt>
    <dd><a href="{rel}projekty/archouse-70.html">ArcHouse 70</a></dd><dd><a href="{rel}projekty/mysa-120.html">MYSA 120</a></dd>
    <dd><a href="{rel}projekty/barnhouse-85.html">BarnHouse 85</a></dd><dd><a href="{rel}projekty/barnhouse-130.html">BarnHouse 130</a></dd>
    <dd><a href="{rel}projekty/foresthouse.html">ForestHouse</a></dd></dl>
  <dl class="titleblock__cell"><dt>Arkusz</dt>
    <dd><a href="{rel}index.html#proces">60 dni</a></dd><dd><a href="{rel}index.html#technologia">Warstwy</a></dd>
    <dd><a href="{rel}index.html#standard">Standard</a></dd><dd><a href="{rel}index.html#kontakt">Kontakt</a></dd></dl>
  <dl class="titleblock__cell"><dt>Wykonawca</dt>
    <dd>ADA Group Sp. z o.o.</dd><dd>Jesionowa 22, 40‑158 Katowice</dd><dd>NIP 9542897994</dd>
    <dd><a href="mailto:hello@movilla.pl">hello@movilla.pl</a></dd><dd><a href="https://www.movilla.pl" target="_blank" rel="noopener">www.movilla.pl</a></dd></dl>
  <div class="titleblock__cell titleblock__cell--meta">
    <span><b>Rewizja</b> 2026‑09</span><span><b>Skala</b> 1 : 60 dni</span><span><b>Uwagi</b> Wizualizacje mają charakter poglądowy; parametry doprecyzowujemy przy adaptacji do działki.</span>
  </div>
</footer>
'''

def lightbox():
    return f'''<div class="lightbox" role="dialog" aria-modal="true" aria-label="Podgląd">
  <button class="lightbox__close" aria-label="Zamknij podgląd">Zamknij {I_CLOSE}</button>
  <button class="lightbox__nav prev" aria-label="Poprzednie">{I_PREV}</button>
  <figure><img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt=""><figcaption></figcaption></figure>
  <button class="lightbox__nav next" aria-label="Następne">{I_ARROW}</button>
</div>
'''

def scripts(rel=""):
    return f'''<script src="{rel}js/vendor/gsap.min.js"></script>
<script src="{rel}js/vendor/ScrollTrigger.min.js"></script>
<script src="{rel}js/main.js"></script>
</body>
</html>
'''

# ---------------------------------------------------------------- data
STD_ARC = [
    ("Fundament", "płyta fundamentowa"),
    ("Konstrukcja", "stalowa konstrukcja szkieletowa"),
    ("Dach", "konstrukcja, izolacja, blacha na rąbek"),
    ("Ściany zewnętrzne", "warstwy zgodnie z przekrojem DSZ / SZ"),
    ("Ścianki działowe", "zgodnie z projektem"),
    ("Instalacja wod‑kan", "rozprowadzenie instalacji"),
    ("Instalacja elektryczna", "rozprowadzenie instalacji"),
    ("Ogrzewanie", "podłogowe, maty grzewcze"),
    ("Stolarka", "okna, drzwi zewnętrzne, drzwi tarasowe"),
    ("Wnętrze", "przygotowane do prac wykończeniowych"),
]
STD_BARN = STD_ARC[:4] + [("Fasada i ściany szczytowe", "elewacja, ocieplenie"), ("Schody na antresolę", "w zakresie")] + STD_ARC[4:]
STD_FOREST = [
    ("Konstrukcja stalowa", "ocynkowana rama + łączniki"),
    ("Ściany zewnętrzne i wewnętrzne", "system warstwowych przegród"),
    ("Stolarka", "okna i drzwi aluminiowe"),
    ("Warstwy podłogowe", "z wykończeniem SPC lub drewnianym"),
    ("Instalacja wod‑kan", "podstawowa, rury PPR / PVC"),
    ("Instalacja elektryczna", "oprawy, gniazda, rozdzielnica"),
    ("Wyposażenie łazienek", "umywalka, lustro, prysznic, WC, armatura"),
    ("Wykończenie wnętrza", "panele dekoracyjne, płytki w łazienkach"),
    ("Taras użytkowy", "na drugiej kondygnacji"),
    ("Dokumentacja techniczna", "przygotowanie pod realizację"),
]
SPEC_ARC = [
    ("DSZ1 · Dach / ściana główna", "U ≤ 0,15 W/m²K", "425 mm",
     "Główna przegroda domu: łukowa (ArcHouse, MYSA) lub dwuspadowa (BarnHouse). Warstwy od zewnątrz.",
     [("Blacha na rąbek stojący", ""), ("Ekran włóknisty paroprzepuszczalny", ""), ("Pełne deskowanie z płyty OSB", "20 mm"),
      ("Szczelina wentylacyjna, listwy 40×40", "40 mm"), ("Membrana wstępnego krycia", ""), ("Wełna mineralna między łatami", "80 mm"),
      ("Wełna mineralna między krokwiami stalowymi IPE 180", "180 mm"), ("Ruszt stalowy wypełniony wełną", "80 mm"),
      ("Paroizolacja aktywna", ""), ("Płyta GK 2 × 12,5", "25 mm")]),
    ("DSZ2 · Dach wiatrołapu", "U ≤ 0,15 W/m²K", "335–370 mm", "",
     [("Blacha na rąbek stojący", ""), ("Ekran włóknisty paroprzepuszczalny", ""), ("Pełne deskowanie z płyty OSB", "20 mm"),
      ("Szczelina wentylacyjna, listwy 40×40", "40 mm"), ("Membrana wstępnego krycia", ""), ("Wełna mineralna między łatami", "90–130 mm"),
      ("Wełna mineralna między krokwiami stalowymi", "160 mm"), ("Paroizolacja aktywna", ""), ("Płyta GK 2 × 12,5", "25 mm")]),
    ("SZ1 · Ściana szczytowa", "U ≤ 0,20 W/m²K", "365 mm", "Przeszklona lub pełna ściana szczytowa z drewnianą elewacją.",
     [("Deski elewacyjne", "20 mm"), ("Łaty, szczelina wentylacyjna 40×40", "40 mm"), ("Płyta drzewna otwarta dyfuzyjnie", "20 mm"),
      ("Konstrukcja stalowa 90 + kontrłaty 80, wełna mineralna", "170 mm"), ("Profile stalowe 90, wełna mineralna", "90 mm"),
      ("Paroizolacja aktywna", ""), ("Płyta GK 2 × 12,5", "25 mm")]),
    ("SZ2 · Ściana wiatrołapu", "U ≤ 0,20 W/m²K", "325 mm", "",
     [("Panele lub deski elewacyjne", "20 mm"), ("Łaty, szczelina wentylacyjna 40×40", "40 mm"), ("Płyta drzewna otwarta dyfuzyjnie", "20 mm"),
      ("Kontrłaty drewniane 60, wełna mineralna", "60 mm"), ("Łaty drewniane 80, wełna mineralna", "80 mm"),
      ("Konstrukcja stalowa 80, wełna mineralna", "80 mm"), ("Paroizolacja aktywna", ""), ("Płyta GK 2 × 12,5", "25 mm")]),
    ("PP · Podłoga parteru", "U ≤ 0,30 W/m²K", "", "Warstwa wykończeniowa (parkiet, terakota) po stronie inwestora, o ile oferta nie stanowi inaczej.",
     [("Warstwa wykończeniowa inwestora", "ok. 20 mm"), ("Wylewka cementowa, jastrych", "60 mm"), ("Ogrzewanie podłogowe", ""),
      ("Folia izolacyjna", ""), ("Styropian podłogowy EPS", "120 mm"), ("Izolacja przeciwwilgociowa, folia budowlana", ""),
      ("Płyta fundamentowa wg projektu", "250 mm"), ("2 × folia budowlana na zakład", ""), ("Styrodur 4000 CS", "200 mm"),
      ("Chudy beton B10", "100 mm"), ("Podbudowa: tłuczeń, pospółka", "300–400 mm")]),
    ("Stolarka i szklenie", "Uw od 0,5 W/m²K", "", "Fasada słupowo‑ryglowa RAL 7016 w systemie MC WALL ALIPLAST, okna GENESIS ALIPLAST. Szklenie potrójne; grubość i typ szkła dobierane do strefy wiatrowej (powłoki Antisol, Cool Light, Sun Guard). Statyka wg PN‑EN 1991‑1‑3 i 1991‑1‑4.", []),
]
SPEC_FOREST = [
    ("Konstrukcja", "rama stalowa", "ocynk", "Lekka rama stalowa z ocynkowanych profili zamkniętych z kompletem łączników, kątowników i śrub kotwiących.",
     [("Profile 140 × 80 mm", "słupy, rygle"), ("Profile 80 × 80 mm", ""), ("Profile 40 × 60 i 40 × 80 mm", ""), ("Łączniki, kątowniki, śruby kotwiące", "")]),
    ("Ściany zewnętrzne", "system prefabrykowany", "155 mm", "",
     [("Panel izolacyjny ze stopu cynku i aluminium", "16 mm"), ("Płyta XPS", "50 mm"), ("Płyta OSB", "9 mm"), ("Izolacja ścienna", "80 mm")]),
    ("Ściany wewnętrzne i łazienki", "", "47 mm", "",
     [("Płyta OSB", "9 mm"), ("Izolacja XPS", "30 mm"), ("Panel dekoracyjny", "8 mm"), ("Łazienki: płyty kompozytowe odporne na wilgoć", "")]),
    ("Podłoga", "", "", "",
     [("Płyta cementowo‑włóknowa", "18 mm"), ("Podłoga SPC 6 mm lub drewniana 12 mm", ""), ("Folia przeciwwilgociowa", "0,3–0,5 mm"), ("Łazienka: płytki antypoślizgowe", "9 mm")]),
    ("Stolarka", "aluminium, argon, Low‑E", "", "",
     [("Drzwi wejściowe: aluminiowe, przesuwne, szklane", "1600 × 2100 mm"), ("Drzwi łazienkowe: szkło prywatności", "700 × 2050 mm"), ("Okna: profile aluminiowe z przekładką termiczną, szyby z argonem i powłoką Low‑E", "")]),
    ("Instalacje i wyposażenie", "w standardzie", "", "",
     [("Instalacja wodna z rur PPR", ""), ("Kanalizacja PVC", "110 / 50 mm"), ("Instalacja elektryczna: oprawy downlight, przełączniki, gniazda, rozdzielnica", ""), ("Łazienki: umywalka, lustro, zestaw prysznicowy, toaleta, armatura", "")]),
]

def VAR_ARC(pre, full):
    return [
        ("Antresola otwarta", "Otwarta antresola połączona wizualnie z salonem: lekkość, optyczne powiększenie i lepsze doświetlenie. Sypialnia, gabinet lub strefa relaksu.", "w standardzie", f"{pre}/plan-open.webp", "Rzut parteru i antresoli otwartej"),
        ("Pełny strop + balkon", f"Pełnowymiarowe piętro jako prywatna strefa z sypialniami, garderobą, łazienką lub gabinetem. Opcja z balkonem lub bez.{full}", "opcja", None, "Rzut piętra, pełny strop"),
        ("Antresola zamknięta", "Wydzielona przestrzeń na piętrze, więcej prywatności i komfortu. Sypialnia, gabinet, pokój dziecięcy.", "opcja", None, "Rzut antresoli zamkniętej"),
        ("Garaż lub garaż z tarasem", "Do każdego modelu można dodać garaż albo garaż z tarasem na dachu.", "opcja dodatkowa", f"{pre}/garage.webp", "Wizualizacja z garażem"),
    ]

PROJECTS = [
    dict(slug="archouse-70", name="ArcHouse", num="70", family="Łukowy dach", family_key="arc", area=69.5,
        tagline="Kompaktowy dom całoroczny o łukowej bryle. Parter z antresolą, przeszklony szczyt, standard deweloperski podwyższony.",
        card_desc="Łuk, antresola i przeszklony szczyt. Start dla pary lub małej rodziny.", hero="arc70/hero.webp",
        dims="7,28 × 7,60 m", layout="parter + antresola", height="6,9 m", people="",
        params=[("69,50", "m²", "powierzchnia razem"), ("7,28 × 7,60", "m", "wymiary w osiach"), ("6,9", "m", "wysokość kalenicy"), ("30–60", "dni", "czas realizacji")],
        intro_title="Łuk, który otwiera przestrzeń.",
        intro=["ArcHouse 70 to całoroczny dom w technologii stalowej konstrukcji szkieletowej, zaprojektowany w charakterystycznej formie łukowego dachu. Bryła oparta na rzucie prostokąta, z przylegającym wiatrołapem w połowie ściany podłużnej.",
               "Parter mieści otwartą strefę dzienną z kuchnią, łazienkę i wiatrołap. Antresola, przewidziana na około 2/3 długości budynku, to sypialnia, gabinet albo strefa relaksu, w wersji otwartej lub zamkniętej.",
               "Propozycja dla osób, które szukają komfortowego, nowoczesnego domu w atrakcyjnej cenie: solidnie wykonanego i gotowego do wykończenia według własnych potrzeb."],
        facts=[("Powierzchnia parteru", "54,12 m²"), ("Powierzchnia antresoli", "15,38 m²"), ("Wysokość w kalenicy", "ok. 6,9 m"), ("Poziom parteru", "+40 cm nad terenem"), ("Podpiwniczenie", "brak"), ("Posadowienie", "płyta fundamentowa")],
        gallery=[("arc70/ext-2.webp", "Elewacja frontowa"), ("arc70/vertical.webp", "Przeszklony szczyt o zmierzchu"), ("arc70/ext-4.webp", "Bryła w zabudowie"), ("arc70/lake-1.webp", "Nad wodą"), ("arc70/lake-2.webp", "Strefa wejściowa i taras")],
        stats=[("Powierzchnia razem", "69.5", 1, "m²", "parter i antresola"), ("Parter", "54.12", 2, "m²", "strefa dzienna, kuchnia, łazienka, wiatrołap"), ("Antresola", "15.38", 2, "m²", "na ok. 2/3 długości budynku"),
               ("Wysokość", "6.9", 1, "m", "od terenu do kalenicy"), ("U dachu i ścian", "0.15", 2, "W/m²K", "główne przegrody zewnętrzne"), ("Realizacja", "60", 0, "dni", "orientacyjnie 30–60 dni")],
        interiors=[("arc70/int-1.webp", False), ("arc70/int-3.webp", False), ("arc70/int-2.webp", False), ("arc70/int-4.webp", False)],
        variants=VAR_ARC("../img/arc70", " Wariant ok. 80 m²."),
        plans=[("arc70/plan-open.webp", "Antresola otwarta", "rzut parteru + antresoli"), ("arc70/plan-full.webp", "Pełny strop + balkon", "rzut piętra, wariant ok. 80 m²"), ("arc70/section.webp", "Przekrój", "wysokości i poziomy")],
        spec=SPEC_ARC, standard=STD_ARC, next="mysa-120"),
    dict(slug="mysa-120", name="MYSA", num="120", family="Łukowy dach", family_key="arc", area=120.2,
        tagline="Większy z domów łukowych: przestronny parter, pełne piętro lub antresola i ponad 120 m² dla całej rodziny.",
        card_desc="Wydłużony łuk: 90 m² parteru i pełnowymiarowe piętro.", hero="mysa120/hero.webp",
        dims="7,28 × 12,90 m", layout="parter + piętro", height="6,9 m", people="",
        params=[("120,20", "m²", "powierzchnia razem"), ("7,28 × 12,90", "m", "wymiary w osiach"), ("6,9", "m", "wysokość kalenicy"), ("30–60", "dni", "czas realizacji")],
        intro_title="Więcej domu pod tym samym łukiem.",
        intro=["MYSA 120 to wydłużona wersja domu łukowego: 90 m² parteru i blisko 30 m² piętra. Ta sama technologia krążyn stalowych, ta sama forma, ale przestrzeń dla rodziny, która potrzebuje kilku sypialni i osobnej strefy nocnej.",
               "Parter to duża strefa dzienna z kuchnią i jadalnią, sypialnia, łazienka oraz wiatrołap. Piętro można zrealizować jako otwartą lub zamkniętą antresolę albo pełny strop z balkonem.",
               "Dom całoroczny w standardzie deweloperskim podwyższonym, przekazywany z instalacjami, stolarką i ogrzewaniem podłogowym."],
        facts=[("Powierzchnia parteru", "90,33 m²"), ("Powierzchnia piętra", "29,87 m²"), ("Wysokość w kalenicy", "ok. 6,9 m"), ("Poziom parteru", "+40 cm nad terenem"), ("Podpiwniczenie", "brak"), ("Posadowienie", "płyta fundamentowa")],
        gallery=[("mysa120/ext-2.webp", "Elewacja frontowa"), ("mysa120/vertical.webp", "Szczyt o zmierzchu"), ("mysa120/balcony-1.webp", "Wariant z balkonem"), ("mysa120/family.webp", "Dom dla rodziny"), ("mysa120/lake-4.webp", "Nad wodą")],
        stats=[("Powierzchnia razem", "120.2", 1, "m²", "parter i piętro"), ("Parter", "90.33", 2, "m²", "strefa dzienna, sypialnia, łazienka, wiatrołap"), ("Piętro", "29.87", 2, "m²", "antresola lub pełny strop"),
               ("Wysokość", "6.9", 1, "m", "od terenu do kalenicy"), ("U dachu i ścian", "0.15", 2, "W/m²K", "główne przegrody zewnętrzne"), ("Realizacja", "60", 0, "dni", "orientacyjnie 30–60 dni")],
        interiors=[("mysa120/int-1.webp", False), ("mysa120/int-3.webp", False), ("mysa120/int-2.webp", False), ("mysa120/int-4.webp", False), ("mysa120/int-5.webp", False)],
        variants=[("Antresola otwarta", "Otwarta antresola połączona wizualnie z salonem: lekkość, optyczne powiększenie i lepsze doświetlenie.", "w standardzie", "../img/mysa120/plan-open.webp", "Rzut parteru i antresoli"),
                  ("Pełny strop + balkon", "Pełnowymiarowe piętro jako prywatna strefa z sypialniami, garderobą, łazienką lub gabinetem. Opcja z balkonem lub bez.", "opcja", "../img/mysa120/balcony-2.webp", "Wizualizacja z balkonem"),
                  ("Antresola zamknięta", "Wydzielona przestrzeń na piętrze: więcej prywatności i komfortu.", "opcja", None, "Rzut antresoli zamkniętej"),
                  ("Garaż lub garaż z tarasem", "Do każdego modelu można dodać garaż lub garaż z tarasem na dachu.", "opcja dodatkowa", "../img/mysa120/garage-terrace.webp", "Wizualizacja z garażem i tarasem")],
        plans=[("mysa120/plan-open.webp", "Rzut parteru i antresoli", "wariant z antresolą otwartą"), ("mysa120/section.webp", "Przekrój", "wysokości i poziomy, bryła łukowa")],
        spec=SPEC_ARC, standard=STD_ARC, next="barnhouse-85"),
    dict(slug="barnhouse-85", name="BarnHouse", num="85", family="Nowoczesna stodoła", family_key="barn", area=85,
        tagline="Klasyczna forma współczesnej stodoły w technologii stalowej. 85 m² z antresolą, przeszklonym szczytem i dachem z blachy na rąbek.",
        card_desc="Współczesna stodoła w stali. Zwarta, z antresolą.", hero="barn85/hero.webp",
        dims="7,28 × 7,60 m", layout="parter + antresola", height="7,9 m", people="",
        params=[("85", "m²", "powierzchnia razem"), ("7,28 × 7,60", "m", "wymiary w osiach"), ("7,9", "m", "wysokość kalenicy"), ("30–60", "dni", "czas realizacji")],
        intro_title="Stodoła, którą znasz. Nowa technologia.",
        intro=["BarnHouse łączy technologię MoVilla z klasyczną formą inspirowaną współczesną stodołą. Dwuspadowy dach, przeszklona ściana szczytowa i prosta, elegancka bryła na rzucie prostokąta.",
               "Parter mieści otwartą strefę dzienną z kuchnią, łazienkę oraz wiatrołap przylegający do ściany podłużnej. Antresola, na około 2/3 długości budynku, pełni rolę sypialni lub gabinetu. Schody na antresolę są w standardzie.",
               "Budynek opracowano na sprawdzonych parametrach modelu MoVilla BarnHouse, z gwarancją solidności wszystkich zastosowanych elementów."],
        facts=[("Powierzchnia", "85 m²"), ("Układ", "parter + antresola"), ("Wysokość w kalenicy", "ok. 7,9 m"), ("Poziom parteru", "+40 cm nad terenem"), ("Podpiwniczenie", "brak"), ("Posadowienie", "płyta fundamentowa")],
        gallery=[("barn85/ext-2.webp", "Elewacja z tarasem"), ("barn130/vertical.webp", "Wieczorem"), ("barn85/ext-3.webp", "Widok boczny"), ("barn85/aerial.webp", "Bryła w otoczeniu"), ("barn130/night.webp", "Nocą")],
        stats=[("Powierzchnia razem", "85", 0, "m²", "parter i antresola"), ("Szerokość", "7.28", 2, "m", "w osiach konstrukcyjnych"), ("Długość", "7.6", 1, "m", "w osiach konstrukcyjnych"),
               ("Wysokość", "7.9", 1, "m", "od terenu do kalenicy"), ("U dachu i ścian", "0.15", 2, "W/m²K", "główne przegrody zewnętrzne"), ("Realizacja", "60", 0, "dni", "orientacyjnie 30–60 dni")],
        interiors=[("barn85/int-1.webp", False), ("barn85/int-2.webp", False), ("arc70/int-3.webp", False), ("mysa120/int-5.webp", False)],
        variants=[("Antresola", "Sypialnia lub gabinet nad strefą dzienną, otwarta na salon lub wydzielona ścianką.", "w standardzie", "../img/barn85/plan-antresola.webp", "Rzut antresoli"),
                  ("BarnHouse 130", "Ta sama forma w większym metrażu: 130 m² z pełnowymiarowym piętrem.", "większy model", "../img/barn130/hero.webp", "BarnHouse 130"),
                  ("Garaż lub garaż z tarasem", "Do każdego modelu można dodać garaż albo garaż z tarasem na dachu.", "opcja dodatkowa", None, "Opcja dodatkowa")],
        plans=[("barn85/plan-parter.webp", "Rzut parteru", "strefa dzienna, kuchnia, łazienka, wiatrołap"), ("barn85/plan-antresola.webp", "Rzut antresoli", "sypialnia lub gabinet"), ("barn85/section.webp", "Przekrój", "wysokości i poziomy")],
        spec=SPEC_ARC, standard=STD_BARN, next="barnhouse-130"),
    dict(slug="barnhouse-130", name="BarnHouse", num="130", family="Nowoczesna stodoła", family_key="barn", area=130,
        tagline="Największy dom w ofercie: 130 m² w formie współczesnej stodoły. Pełna strefa dzienna na parterze i prywatna część nocna na piętrze.",
        card_desc="130 m² dla dużej rodziny. Pełne piętro, przeszklony szczyt.", hero="barn130/hero.webp",
        dims="szer. 7,28 m", layout="parter + piętro", height="7,9 m", people="",
        params=[("130", "m²", "powierzchnia razem"), ("7,28", "m", "szerokość w osiach"), ("7,9", "m", "wysokość kalenicy"), ("30–60", "dni", "czas realizacji")],
        intro_title="Dom dla całej rodziny. Bez kompromisów.",
        intro=["BarnHouse 130 to rozwinięcie modelu 85: wydłużona bryła współczesnej stodoły, która daje pełną strefę dzienną na parterze i wydzieloną część nocną na piętrze.",
               "Parter: przestronny salon z kuchnią i jadalnią, sypialnia lub gabinet, łazienka, wiatrołap i pomieszczenie gospodarcze. Piętro: sypialnie z łazienką i miejsce na garderobę.",
               "Dom całoroczny w stalowej konstrukcji szkieletowej, przekazywany w standardzie deweloperskim podwyższonym: z fasadą, ociepleniem, instalacjami, schodami i ogrzewaniem podłogowym."],
        facts=[("Powierzchnia", "130 m²"), ("Układ", "parter + piętro"), ("Wysokość w kalenicy", "ok. 7,9 m"), ("Poziom parteru", "+40 cm nad terenem"), ("Podpiwniczenie", "brak"), ("Posadowienie", "płyta fundamentowa")],
        gallery=[("barn130/night.webp", "Wieczorne oświetlenie"), ("barn130/vertical.webp", "Nad jeziorem"), ("barn130/ext-2.webp", "Elewacja boczna"), ("barn130/aerial.webp", "Z lotu ptaka"), ("barn85/ext-2.webp", "Taras i przeszklenia")],
        stats=[("Powierzchnia razem", "130", 0, "m²", "parter i piętro"), ("Szerokość", "7.28", 2, "m", "w osiach konstrukcyjnych"), ("Kondygnacje", "2", 0, "", "parter + pełne piętro"),
               ("Wysokość", "7.9", 1, "m", "od terenu do kalenicy"), ("U dachu i ścian", "0.15", 2, "W/m²K", "główne przegrody zewnętrzne"), ("Realizacja", "60", 0, "dni", "orientacyjnie 30–60 dni")],
        interiors=[("barn130/int-2.webp", False), ("barn130/int-1.webp", False), ("mysa120/int-3.webp", False), ("mysa120/int-4.webp", False)],
        variants=[("Pełne piętro", "Piętro jako prywatna strefa nocna: sypialnie, łazienka, garderoba. Schody w standardzie.", "w standardzie", "../img/barn130/plan-antresola.webp", "Rzut piętra"),
                  ("BarnHouse 85", "Ta sama forma w kompaktowym metrażu: 85 m² z antresolą.", "mniejszy model", "../img/barn85/hero.webp", "BarnHouse 85"),
                  ("Garaż lub garaż z tarasem", "Do każdego modelu można dodać garaż albo garaż z tarasem na dachu.", "opcja dodatkowa", None, "Opcja dodatkowa")],
        plans=[("barn130/plan-parter.webp", "Rzut parteru", "salon, kuchnia, sypialnia, łazienka, wiatrołap"), ("barn130/plan-antresola.webp", "Rzut piętra", "sypialnie, łazienka"), ("barn130/section.webp", "Przekrój", "wysokości i poziomy")],
        spec=SPEC_ARC, standard=STD_BARN, next="foresthouse"),
    dict(slug="foresthouse", name="ForestHouse", num="", family="A‑frame", family_key="forest", area=90,
        tagline="Kompaktowy dom A‑frame na 4 osoby: całoroczny, rekreacyjny albo inwestycyjny. W standardzie z wykończeniem wnętrza i wyposażeniem łazienek.",
        card_desc="A‑frame z tarasem. Gotowy produkt pod wynajem lub glamping.", hero="forest/hero.webp",
        dims="8,30 × 8,00 m", layout="2 sypialnie · 2 łazienki", height="7,0 m", people="4 osoby",
        params=[("90", "m²", "powierzchnia budynku"), ("8,30 × 8,00", "m", "wymiary zewnętrzne"), ("7,0", "m", "wysokość"), ("4", "osoby", "układ dla")],
        intro_title="Bliżej natury. Gotowy do zamieszkania.",
        intro=["ForestHouse to kompaktowy dom w stylistyce A‑frame, zaprojektowany z myślą o nowoczesnym wypoczynku, inwestycjach pod wynajem i całorocznym użytkowaniu. Trójkątna bryła, wysokie przeszklenia frontowe i taras łączą komfort domu z bliskością natury.",
               "Parter to otwarta strefa dzienna z salonem, kuchnią, łazienką i sypialnią. Na drugiej kondygnacji jest prywatna część z sypialnią pod połacią dachu, łazienką i wyjściem na taras.",
               "W odróżnieniu od pozostałych modeli ForestHouse przekazujemy jako kompletne rozwiązanie: z wykończeniem wnętrza, panelami dekoracyjnymi i podstawowym wyposażeniem sanitarnym łazienek."],
        facts=[("Powierzchnia", "90 m²"), ("Wymiary zewnętrzne", "8,30 × 8,00 m"), ("Wysokość", "ok. 7,00 m"), ("Sypialnie", "2"), ("Łazienki", "2"), ("Technologia", "stal + ściany prefabrykowane")],
        gallery=[("forest/ext-2.webp", "W lesie"), ("forest/vertical.webp", "Osiedle A‑frame"), ("forest/ext-3.webp", "Na słupach, nad wodą"), ("forest/glamping.webp", "Zespół pięciu domów"), ("forest/ext-4.webp", "Przeszklony front")],
        stats=[("Powierzchnia", "90", 0, "m²", "powierzchnia budynku"), ("Szerokość", "8.3", 1, "m", "wymiar zewnętrzny"), ("Głębokość", "8", 1, "m", "wymiar zewnętrzny"),
               ("Wysokość", "7", 1, "m", "w szczycie"), ("Użytkownicy", "4", 0, "osoby", "2 sypialnie, 2 łazienki"), ("Kondygnacje", "2", 0, "", "parter + poddasze z tarasem")],
        interiors=[("forest/int-7.webp", False), ("forest/int-1.webp", False), ("forest/int-3.webp", True), ("forest/int-10.webp", False), ("forest/int-4.webp", True), ("forest/int-11.webp", False), ("forest/int-5.webp", True), ("forest/int-8.webp", True), ("forest/int-6.webp", True), ("forest/int-9.webp", True)],
        variants=[("Dom całoroczny", "Prywatny dom na działce: izolowane przegrody, ogrzewanie i pełne wykończenie wnętrza.", "zastosowanie", "../img/forest/ext-2.webp", "Dom całoroczny"),
                  ("Inwestycja pod wynajem", "Produkt gotowy do wykorzystania: układ dla 4 osób, dwie łazienki, taras.", "zastosowanie", "../img/forest/ext-3.webp", "Wynajem krótkoterminowy"),
                  ("Resort lub glamping", "Zespół kilku domów na działce rekreacyjnej lub w resorcie: powtarzalny moduł, krótki montaż.", "zastosowanie", "../img/forest/glamping.webp", "Zespół domów"),
                  ("Indywidualny standard", "Zakres wykończenia dopasowujemy do inwestycji prywatnej, rekreacyjnej lub komercyjnej.", "konfiguracja", None, "Konfiguracja")],
        plans=[("forest/plan-parter.webp", "Rzut parteru", "salon, kuchnia, łazienka, sypialnia"), ("forest/plan-pietro.webp", "Rzut drugiej kondygnacji", "sypialnia, łazienka, taras"), ("forest/elev-1.webp", "Elewacja boczna", ""), ("forest/elev-2.webp", "Elewacja frontowa", "")],
        spec=SPEC_FOREST, standard=STD_FOREST, next="archouse-70"),
]
BY_SLUG = {p["slug"]: p for p in PROJECTS}
AREA_MAX = 130
def title_of(p): return f"{p['name']} {p['num']}".strip()

# ---------------------------------------------------------------- wspólne bloki
def bars(rel, active=None):
    """Wykres metrażu pięciu modeli na siatce 0–130 m²."""
    out = ""
    for p in PROJECTS:
        w = p["area"] / AREA_MAX * 100
        act = " is-active" if p["slug"] == active else ""
        area = f"{p['area']:.1f}".replace(".", ",").replace(",0", "")
        out += f'''<a class="mrow{act}" href="{rel}projekty/{p['slug']}.html" data-model="{p['slug']}">
      <span class="mrow__name">{FORM_ICON[p['family_key']]}<b>{title_of(p)}</b><small>{p['family']}</small></span>
      <span class="mrow__track" style="--w:{w:.2f}%"><i class="mrow__bar"></i><em class="mrow__val"><span data-count="{p['area']}" data-decimals="{1 if p['area'] % 1 else 0}">{area}</span> m²</em></span>
      <span class="mrow__meta"><span>{p['dims']}</span><span>{p['layout']}</span>{f"<span>{p['people']}</span>" if p['people'] else ""}</span>
    </a>'''
    return out

def checklist(items):
    return "".join(f'<li><span class="chk">{I_CHECK}</span><span><b>{k}</b><small>{v}</small></span></li>' for k, v in items)

# ---------------------------------------------------------------- index
def index_html():
    rel = ""
    plates = "".join(f'<figure class="plate" data-cap="{c}">{pic(f"img/{s}", f"Wizualizacja, {c}", sizes="40vw")}<figcaption>{c}</figcaption></figure>'
                     for s, c in [("arc70/lake-1.webp", "fot. 04 · ArcHouse 70"), ("forest/int-7.webp", "fot. 05 · ForestHouse, wnętrze"), ("barn130/night.webp", "fot. 06 · BarnHouse 130"), ("mysa120/int-3.webp", "fot. 07 · MYSA 120, antresola"), ("forest/vertical.webp", "fot. 08 · zespół ForestHouse")])
    layers_list = "".join(f'<li><span>{n}</span><span class="mono">{t or "·"}</span></li>' for n, t in SPEC_ARC[0][4])
    seq = ["płyta fundamentowa", "konstrukcja stalowa", "przegrody i dach", "stolarka", "instalacje", "przekazanie"]
    seq_html = "".join(f'<li>{s}</li>' for s in seq)
    models_stage = "".join(f'<img src="img/{p["hero"]}" alt="{title_of(p)}" data-model="{p["slug"]}" loading="lazy">' for p in PROJECTS)

    return head("MoVilla: dom całoroczny w 30–60 dni", "Pięć domów całorocznych w stalowej konstrukcji szkieletowej: ArcHouse 70, MYSA 120, BarnHouse 85 i 130, ForestHouse. Standard deweloperski podwyższony, realizacja w 30–60 dni.", rel) + topbar(rel) + ruler() + f'''
<main id="top">

<section class="hero" id="hero">
  <div class="hero__text">
    <h1 class="hero__title">Dom w <span class="hl">30–60</span> dni.</h1>
    <p class="hero__lead">Całoroczne domy w stalowej konstrukcji szkieletowej. Pięć modeli od 69 do 130 m², przekazywanych w standardzie deweloperskim podwyższonym.</p>
    <div class="hero__actions"><a class="btn" href="#kontakt">Poproś o wycenę {I_ARROW}</a><a class="lnk" href="#projekty">Porównaj modele</a></div>
  </div>
  <figure class="plate plate--hero">
    <img src="img/common/frame.webp" alt="Stalowy szkielet domu łukowego, model konstrukcyjny" data-stage="0" fetchpriority="high">
    {pic("img/common/tech-2.webp", "Montaż stalowej konstrukcji szkieletowej domu łukowego", lazy=False, sizes="55vw", extra='data-stage="1"')}
    {pic("img/arc70/lake-2.webp", "Gotowy dom ArcHouse 70 nad wodą", lazy=False, sizes="55vw", extra='data-stage="2"')}
    <figcaption><span class="mono">fot. 01</span><span data-stage-cap>rysunek konstrukcji · dzień 0 · wizualizacja</span></figcaption>
  </figure>
  <div class="stagebar" aria-label="Orientacyjny czas realizacji">
    <div class="stagebar__bar"><i class="stagebar__fill"></i><i class="stagebar__range" style="--from:50%;--to:100%"></i><b class="stagebar__l" style="left:50%">30 dni</b><b class="stagebar__l stagebar__l--end" style="left:100%">60 dni</b></div>
    <ol class="stagebar__seq">{seq_html}</ol>
    <p class="stagebar__note">Produkcja i montaż trwają 30–60 dni zależnie od zakresu prac, dostępności materiałów i warunków na działce. Kolejność prac powyżej; terminy ustalamy indywidualnie.</p>
  </div>
</section>

<section class="models" id="projekty">
  <h2 class="h2">Pięć modeli.<br>Jedna konstrukcja.</h2>
  <div class="models__grid">
    <div class="models__chart">
      {ruler("m²", 130, 10, cursor=False)}
      <div class="mrows">{bars(rel)}</div>
      <p class="models__note">Długość słupka to powierzchnia razem wg katalogu. Metraże BarnHouse 85 i 130 podane bez rozbicia na kondygnacje.</p>
    </div>
    <figure class="plate plate--sticky models__stage">{models_stage}<figcaption><span class="mono">fot. 02</span><span data-model-cap>ArcHouse 70</span><span>· wizualizacja</span></figcaption></figure>
  </div>
</section>

<section class="stages" id="proces">
  <h2 class="h2">Co dzieje się między dniem 0 a 60.</h2>
  <ol class="stages__list">
    <li><span class="mono stages__day">dzień 0</span><h3>Wybór i konfiguracja</h3><p>Wybierasz model i wariant: antresola otwarta lub zamknięta, pełny strop, garaż. Ustalamy zakres i standard.</p></li>
    <li><span class="mono stages__day">przed produkcją</span><h3>Adaptacja do działki</h3><p>Dopasowujemy projekt do warunków lokalnych i strefy wiatrowej, przygotowujemy dokumentację techniczną i wycenę.</p></li>
    <li class="is-key"><span class="mono stages__day">30–60 dni</span><h3>Produkcja i montaż</h3><p>Płyta fundamentowa, stalowa konstrukcja, przegrody, dach z blachy na rąbek, stolarka i instalacje. Większość pracy dzieje się w hali, nie na Twojej działce.</p></li>
    <li><span class="mono stages__day">odbiór</span><h3>Przekazanie</h3><p>Odbierasz dom w standardzie deweloperskim podwyższonym, z ogrzewaniem podłogowym, gotowy do wykończenia wnętrz.</p></li>
  </ol>
  <div class="stages__plates">
    <figure class="plate">{pic("img/common/tech-1.webp", "Stalowe ramy nośne domu MoVilla na placu montażu", sizes="45vw")}<figcaption><span class="mono">fot. 03</span><span>montaż ram stalowych</span></figcaption></figure>
    <figure class="plate">{pic("img/common/builder.webp", "Wykonawca MoVilla przed gotowym domem BarnHouse", sizes="30vw", w960=False)}<figcaption><span class="mono">fot. 03a</span><span>odbiór domu</span></figcaption></figure>
  </div>
</section>

<section class="layers" id="technologia">
  <div class="layers__head">
    <h2 class="h2">Warstwa po warstwie.</h2>
    <p class="lead">Dach i ściana główna to jedna ciągła przegroda o grubości 425 mm z trzema warstwami wełny mineralnej. Poniżej lista materiałów przegrody DSZ1 od zewnątrz do wnętrza.</p>
  </div>
  <figure class="plate plate--sticky layers__plate">
    <img src="img/common/detail-wall.webp" alt="Detal D‑01: przekrój przez warstwy dachu, ściany i fundamentu" loading="lazy">
    <figcaption><span class="mono">det. D‑01</span><span>warstwy poziome i pionowe</span></figcaption>
  </figure>
  <div class="layers__body">
    <dl class="kpi">
      <div><dt>U dachu i ścian głównych</dt><dd><span data-count="0.15" data-decimals="2">0,15</span><small>W/m²K</small></dd></div>
      <div><dt>grubość przegrody DSZ1</dt><dd><span data-count="425">425</span><small>mm</small></dd></div>
      <div><dt>szklenie potrójne, Uw od</dt><dd><span data-count="0.5" data-decimals="1">0,5</span><small>W/m²K</small></dd></div>
      <div><dt>wełna mineralna razem</dt><dd><span data-count="340">340</span><small>mm</small></dd></div>
    </dl>
    <ol class="bom">{layers_list}</ol>
    <p class="layers__note">Pełne specyfikacje ścian szczytowych, wiatrołapu i podłogi parteru są na podstronach modeli. ForestHouse ma osobny system przegród prefabrykowanych.</p>
    <a class="lnk" href="projekty/archouse-70.html#technologia">Zobacz pełną specyfikację {I_ARROW}</a>
  </div>
</section>

<section class="forms" id="formy">
  <h2 class="h2">Trzy bryły do wyboru.</h2>
  <div class="forms__rows">
    <div class="form">{I_ARC}<h3>Łuk</h3><p>Krążyny stalowe tworzą łukowy dach przechodzący w ścianę. Przeszklony szczyt, antresola, wnętrze bez ostrych kątów.</p><p class="form__models"><a href="projekty/archouse-70.html">ArcHouse 70</a><a href="projekty/mysa-120.html">MYSA 120</a></p></div>
    <div class="form">{I_BARN}<h3>Stodoła</h3><p>Dwuspadowy dach z blachy na rąbek, ciemna elewacja, przeszklona ściana szczytowa i taras.</p><p class="form__models"><a href="projekty/barnhouse-85.html">BarnHouse 85</a><a href="projekty/barnhouse-130.html">BarnHouse 130</a></p></div>
    <div class="form">{I_AFRAME}<h3>A‑frame</h3><p>Trójkątna bryła z wysokim przeszkleniem frontu i tarasem na piętrze. Gotowa do zamieszkania, także jako produkt inwestycyjny.</p><p class="form__models"><a href="projekty/foresthouse.html">ForestHouse</a></p></div>
  </div>
</section>

<section class="standard" id="standard">
  <div class="standard__head">
    <h2 class="h2">Odebrane w standardzie.</h2>
    <p class="lead">Dom przekazujemy w standardzie deweloperskim podwyższonym, przygotowany do dalszych prac wykończeniowych. Ogrzewanie podłogowe, instalacje i stolarka są w cenie.</p>
  </div>
  <ul class="checklist">{checklist(STD_ARC)}</ul>
  <p class="standard__note">Wizualizacje wnętrz mają charakter poglądowy. Wyposażenie ruchome, zabudowa meblowa i finalne wykończenie wnętrz nie są częścią standardu, o ile indywidualna oferta nie stanowi inaczej. ForestHouse jest przekazywany z wykończeniem wnętrza i wyposażeniem łazienek.</p>
</section>

<section class="strip" aria-label="Wizualizacje">
  <div class="strip__track">{plates}</div>
</section>

<section class="contact" id="kontakt">
  <div class="contact__head">
    <h2 class="h2">Dzień 0 zaczyna się od wiadomości.</h2>
    <p class="lead">Napisz, który model Cię interesuje i gdzie jest działka. Na kolejnym etapie przygotowujemy konfigurację domu, zakres realizacji oraz wycenę.</p>
    <address class="contact__info"><a class="contact__mail" href="mailto:hello@movilla.pl">hello@movilla.pl</a><span>ADA Group Sp. z o.o.<br>Jesionowa 22, 40‑158 Katowice</span></address>
  </div>
  <form class="form-grid" novalidate>
    <div class="field"><label for="f-name">Imię i nazwisko</label><input id="f-name" name="name" required autocomplete="name"></div>
    <div class="field"><label for="f-email">E‑mail</label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
    <div class="field"><label for="f-phone">Telefon</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="f-proj">Model</label><select id="f-proj" name="projekt"><option>Nie wiem jeszcze</option><option>ArcHouse 70</option><option>MYSA 120</option><option>BarnHouse 85</option><option>BarnHouse 130</option><option>ForestHouse</option></select></div>
    <div class="field field--full"><label for="f-place">Lokalizacja działki</label><input id="f-place" name="place" placeholder="miejscowość, województwo"></div>
    <div class="field field--full"><label for="f-msg">Wiadomość</label><textarea id="f-msg" name="msg" rows="4" placeholder="Kiedy chcesz zacząć? Dom dla siebie czy inwestycja?"></textarea></div>
    <p class="field--full form-grid__err" role="alert" hidden>Uzupełnij imię i poprawny adres e‑mail, żebyśmy mogli odpowiedzieć.</p>
    <div class="field--full form-grid__foot"><small>Wysyłając formularz, otworzysz gotową wiadomość w swoim programie pocztowym.</small><button class="btn" type="submit">Wyślij zapytanie {I_ARROW}</button></div>
  </form>
</section>

</main>
''' + titleblock(rel) + lightbox() + scripts(rel)

# ---------------------------------------------------------------- project page
def project_html(p):
    rel = "../"
    nxt = BY_SLUG[p["next"]]
    title = title_of(p)
    params = "".join(f'<div><b>{v}<small>{u}</small></b><span>{l}</span></div>' for v, u, l in p["params"])
    facts = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in p["facts"])
    gallery = "".join(f'<figure class="plate" data-lightbox="{rel}img/{s}" data-cap="fot. {i+2:02d} · {c}">{pic(rel + "img/" + s, f"{title}, {c}", sizes="(max-width:800px) 100vw, 50vw")}<figcaption><span class="mono">fot. {i+2:02d}</span><span>{c} · wizualizacja</span></figcaption></figure>' for i, (s, c) in enumerate(p["gallery"]))
    stats = "".join(f'<div><dt>{l}</dt><dd><span data-count="{v}" data-decimals="{d}">{v.replace(".", ",")}</span><small>{u}</small></dd><p>{desc}</p></div>' for l, v, d, u, desc in p["stats"])
    interiors = "".join(f'<figure class="plate{" plate--tall" if tall else ""}" data-lightbox="{rel}img/{s}" data-cap="wnętrze {i+1:02d} · aranżacja przykładowa">{pic(rel + "img/" + s, f"{title}, wnętrze, aranżacja przykładowa", sizes="45vw")}<figcaption><span class="mono">wn. {i+1:02d}</span></figcaption></figure>' for i, (s, tall) in enumerate(p["interiors"]))
    vrows = "".join(f'<button class="orow{" is-active" if i == 0 else ""}" data-label="{lab}" role="tab" aria-selected="{"true" if i == 0 else "false"}"><span class="chk">{I_CHECK}</span><span class="orow__body"><b>{t}</b><small>{chip}</small><p>{d}</p></span></button>' for i, (t, d, chip, img, lab) in enumerate(p["variants"]))
    vimgs = "".join(f'<img src="{img or (rel + "img/" + p["plans"][0][0])}" alt="{lab}" class="{"is-active" if i == 0 else ""}" loading="lazy">' for i, (t, d, chip, img, lab) in enumerate(p["variants"]))
    plans = "".join(f'<figure class="sheet" data-lightbox="{rel}img/{s}" data-cap="{t}"><img src="{rel}img/{s}" alt="{title}, {t}" loading="lazy"><figcaption><b>{t}</b><span>{n}</span></figcaption></figure>' for s, t, n in p["plans"])
    acc = ""
    for i, (t, u, th, desc, layers) in enumerate(p["spec"]):
        lay = "".join(f'<li><span>{n}</span><span class="mono">{x or "·"}</span></li>' for n, x in layers)
        acc += f'''<div class="acc__item"><button class="acc__btn" aria-expanded="false"><span class="acc__t">{t}</span><span class="mono acc__u">{u}</span><span class="mono acc__th">{th}</span><span class="acc__plus">{I_PLUS}</span></button>
        <div class="acc__panel"><div class="acc__in">{f"<p>{desc}</p>" if desc else ""}{f"<ol class=bom>{lay}</ol>" if lay else ""}</div></div></div>'''
    std_note = ("ForestHouse przekazujemy jako kompletne rozwiązanie: konstrukcja, stolarka, instalacje, wykończenie wnętrza i sanitariaty. Zakres dopasowujemy do inwestycji prywatnej, rekreacyjnej lub komercyjnej."
                if p["family_key"] == "forest" else
                "Wizualizacje wnętrz mają charakter poglądowy. Wyposażenie ruchome, zabudowa meblowa i finalne wykończenie wnętrz nie są częścią standardu, o ile indywidualna oferta nie stanowi inaczej.")
    spec_lead = ("Lekka rama stalowa i system warstwowych przegród, zaprojektowane pod stabilność, szybki montaż i estetykę wykończenia."
                 if p["family_key"] == "forest" else
                 "Główne przegrody zewnętrzne osiągają U ≤ 0,15 W/m²K: wełna mineralna w trzech warstwach, paroizolacja aktywna, fasada aluminiowa z potrójnym szkleniem.")
    side_img = {"arc": "common/frame.webp", "barn": "common/tech-1.webp", "forest": "forest/ext-5.webp"}[p["family_key"]]

    return head(f"{title}, {p['family']} · MoVilla", p["tagline"], rel, p["hero"]) + topbar(rel) + ruler() + f'''
<main id="top">

<section class="phero">
  <div class="phero__text">
    <nav class="crumb" aria-label="Okruszki"><a href="{rel}index.html">MoVilla</a> / <a href="{rel}index.html#projekty">Modele</a></nav>
    <h1 class="phero__title">{p['name']}{f' <span class="hl">{p["num"]}</span>' if p['num'] else ''}</h1>
    <p class="hero__lead"><b>{p['family']}.</b> {p['tagline']}</p>
    <div class="hero__actions"><a class="btn" href="{rel}index.html#kontakt">Zapytaj o ten model {I_ARROW}</a><a class="lnk" href="#rzuty">Zobacz rzuty</a></div>
  </div>
  <figure class="plate plate--hero">{pic(rel + "img/" + p["hero"], f"{title}, wizualizacja", lazy=False, sizes="55vw")}<figcaption><span class="mono">fot. 01</span><span>wizualizacja poglądowa</span></figcaption></figure>
  <div class="phero__params">{params}</div>
</section>

<section class="models models--compact">
  <h2 class="h2">{title} na tle oferty.</h2>
  <div class="models__chart">{ruler("m²", 130, 10, cursor=False)}<div class="mrows">{bars(rel, active=p['slug'])}</div></div>
</section>

<section class="pintro">
  <div class="pintro__text">
    <h2 class="h2">{p['intro_title']}</h2>
    {"".join(f"<p>{t}</p>" for t in p["intro"])}
  </div>
  <dl class="facts">{facts}</dl>
</section>

<section class="pgallery">{gallery}</section>


<section class="pint">
  <div class="pint__head"><h2 class="h2">Przykładowa aranżacja.</h2><p class="lead">Przeciągnij pasek lub przewiń w bok. Kliknij, aby powiększyć.</p></div>
  <div class="strip__track strip__track--drag">{interiors}</div>
  <p class="note">Wizualizacje wnętrz mają charakter poglądowy i przedstawiają przykładową aranżację.</p>
</section>

<section class="variants" id="warianty">
  <h2 class="h2">Opcje w zamówieniu.</h2>
  <div class="variants__grid">
    <div class="orows" role="tablist">{vrows}</div>
    <figure class="plate plate--sheet variants__stage"><span class="mono variants__label">{p['variants'][0][4]}</span>{vimgs}</figure>
  </div>
</section>

<section class="plans" id="rzuty">
  <div class="plans__head"><h2 class="h2">Rzuty i przekroje.</h2><p class="lead">Kliknij arkusz, aby zobaczyć go w powiększeniu.</p></div>
  <div class="plans__grid">{plans}</div>
  <p class="note">Parametry mogą zostać doprecyzowane na etapie adaptacji projektu do działki i warunków lokalnych. Rzuty poglądowe; układ pomieszczeń ustalamy indywidualnie.</p>
</section>

<section class="spec" id="technologia">
  <div class="spec__side">
    <h2 class="h2">Warstwa po warstwie.</h2>
    <p class="lead">{spec_lead}</p>
    <figure class="plate">{pic(rel + "img/" + side_img, "Konstrukcja stalowa MoVilla", sizes="35vw")}<figcaption><span class="mono">fot. 09</span><span>{"konstrukcja · wizualizacja" if p["family_key"] != "barn" else "konstrukcja"}</span></figcaption></figure>
  </div>
  <div class="acc">{acc}</div>
</section>

<section class="standard" id="standard">
  <div class="standard__head">
    <h2 class="h2">{"Kompletny dom w standardzie." if p["family_key"] == "forest" else "Odebrane w standardzie."}</h2>
    <p class="lead">{std_note}</p>
    <a class="btn" href="{rel}index.html#kontakt">Poproś o wycenę {I_ARROW}</a>
  </div>
  <ul class="checklist">{checklist(p["standard"])}</ul>
</section>

<a class="pnext" href="{rel}projekty/{nxt['slug']}.html">
  <span class="pnext__text"><span class="mono">następny wiersz harmonogramu</span><span class="pnext__title">{title_of(nxt)} {I_ARROW}</span><span class="pnext__meta">{nxt['family']} · {f"{nxt['area']:.1f}".replace('.', ',').replace(',0', '')} m² · {nxt['layout']}</span></span>
  <span class="plate pnext__plate">{pic(rel + "img/" + nxt["hero"], title_of(nxt), sizes="50vw")}</span>
</a>

</main>
''' + titleblock(rel) + lightbox() + scripts(rel)

# ---------------------------------------------------------------- write
with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html())
os.makedirs(os.path.join(ROOT, "projekty"), exist_ok=True)
for p in PROJECTS:
    with open(os.path.join(ROOT, "projekty", p["slug"] + ".html"), "w", encoding="utf-8") as f:
        f.write(project_html(p))
print("OK:", "index.html", *[p["slug"] + ".html" for p in PROJECTS])
