# MoVilla — strona internetowa

Statyczna strona (HTML + CSS + GSAP), bez frameworka i bez procesu budowania w przeglądarce.

## Gałęzie

- `nestora` — wersja główna: minimalizm inspirowany projektem Nestora, duże zdjęcia, mobile-first.
- `imp` — alternatywna wersja zbudowana pluginem impeccable (świat „harmonogram budowy”).

## Struktura

```
index.html                 strona główna
projekty/*.html            5 podstron projektów (generowane)
css/style.css              style
js/main.js                 animacje GSAP i interakcje
js/vendor/                 GSAP 3.14 (gsap, ScrollTrigger, ScrollSmoother, SplitText)
img/<projekt>/*.webp       zdjęcia (1920 px + wersja -960 px), rzuty, przekroje
video/hero.mp4             film w tle hero (pętla 20 s, 1080p) + hero-720.mp4 dla telefonów; hero-alt*.mp4 to wariant zapasowy
_materials/                materiały źródłowe (katalogi PDF, oryginalne zdjęcia) i skrypty
```

## Podgląd lokalny

```bash
node _materials/serve.js 8765
```

Następnie otwórz http://localhost:8765. Strona wymaga serwera HTTP (nie działa z `file://`).

## Edycja treści projektów

Treści podstron (parametry, opisy, warianty, rzuty, specyfikacja) są w jednym miejscu:
`_materials/data.py` → lista `PROJECTS`. Szablony HTML są w `_materials/build_site.py`. Po zmianie uruchom:

```bash
python3 _materials/build_site.py
```

Skrypt nadpisuje `index.html` i wszystkie pliki w `projekty/`.

## Zdjęcia

`_materials/build_images.py` konwertuje oryginały (PNG z folderu `Movilla str` i obrazy
wyciągnięte z katalogów PDF) do WebP. Wymaga Pillow (`pip install pillow`).

## Tryby

- `?static` w adresie (albo systemowe „ogranicz ruch”) wyłącza animacje — przydatne do testów.
- Preloader z licznikiem pokazuje się raz na sesję; kolejne podstrony mają krótkie przejście.

## Formularz kontaktowy

Formularz otwiera gotową wiadomość e‑mail (`mailto:hello@movilla.pl`). Aby wysyłać
bez klienta pocztowego, podłącz np. Formspree / Netlify Forms w `js/main.js` (sekcja *contact form*).
