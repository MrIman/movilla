# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Dwie równorzędne grupy (potwierdzone przez właściciela):

- **Rodziny i osoby prywatne** szukające całorocznego domu na własnej działce, w rozsądnej cenie i krótkim czasie budowy. Porównują oferty domów prefabrykowanych, chcą szybko zrozumieć metraż, układ, standard i czas realizacji, a potem zapytać o wycenę.
- **Inwestorzy** kupujący jeden lub kilka domów jako produkt: wynajem krótkoterminowy, resort, glamping. Interesuje ich powtarzalność modułu, gotowość „pod klucz” (ForestHouse), czas montażu i efekt wizualny obiektu.

Strona nie faworyzuje żadnej grupy; każdy projekt ma być czytelny dla obu.

## Product Purpose

MoVilla (ADA Group Sp. z o.o., Katowice) projektuje i buduje nowoczesne domy całoroczne w stalowej konstrukcji szkieletowej. Strona prezentuje pięć projektów (ArcHouse 70, MYSA 120, BarnHouse 85, BarnHouse 130, ForestHouse), tłumaczy technologię i standard przekazania oraz prowadzi do kontaktu i indywidualnej wyceny. Sukces: zapytanie ofertowe (e‑mail / formularz) z wybranym modelem i lokalizacją działki.

## Positioning

Potwierdzone wyróżniki:

- **Stalowy szkielet i realizacja w 30–60 dni** — trwałość stali plus bardzo krótki czas montażu na działce.
- **Stosunek jakości do ceny** — atrakcyjna cena przy standardzie deweloperskim podwyższonym (fundament, konstrukcja, dach z blachy na rąbek, stolarka aluminiowa, instalacje, ogrzewanie podłogowe).
- **Własna produkcja i zespół** — kompleksowa obsługa od konfiguracji i adaptacji do działki po montaż i przekazanie.

Architektura (łuk, stodoła, A‑frame) jest rozpoznawalna, ale właściciel nie wskazał jej jako głównego wyróżnika.

## Operating Context

- Katalogi techniczne PDF dla każdego modelu (`_materials/Movilla str/*.pdf`) są źródłem wszystkich parametrów i opisów.
- Proces: wybór modelu i wariantu → adaptacja projektu do działki i strefy wiatrowej, dokumentacja i wycena → produkcja i montaż (30–60 dni) → przekazanie w standardzie deweloperskim podwyższonym.
- Kontakt: hello@movilla.pl, www.movilla.pl, ADA Group Sp. z o.o., Jesionowa 22, 40‑158 Katowice, NIP 9542897994. Katalog ForestHouse podaje inny podmiot (ARPA Group, Myszków) — do wyjaśnienia przed publikacją.

## Capabilities and Constraints

- Pięć modeli: ArcHouse 70 (69,50 m², 7,28 × 7,60 m), MYSA 120 (120,20 m²), BarnHouse 85, BarnHouse 130, ForestHouse (90 m², 8,30 × 8,00 m, 4 osoby, 2 sypialnie, 2 łazienki).
- Warianty domów łukowych i stodół: antresola otwarta / zamknięta, pełny strop z balkonem lub bez, garaż lub garaż z tarasem.
- Parametry cieplne: U ≤ 0,15 W/m²K dach i ściana główna, U ≤ 0,20 ściany szczytowe, U ≤ 0,30 podłoga; okna Uw od 0,5; fasada Aliplast RAL 7016.
- ForestHouse jako jedyny jest przekazywany z wykończeniem wnętrza i wyposażeniem łazienek; pozostałe modele w standardzie deweloperskim podwyższonym (wykończenie po stronie inwestora).
- Niepewne dane z katalogów: wymiary BarnHouse 130 (skopiowane z 85) oraz długość MYSA 120 (przyjęto 7,28 × 12,90 m z opisu technologii). Ceny nie są publikowane.
- Terminologia: „standard deweloperski podwyższony”, „antresola”, „krążyny stalowe”, „blacha na rąbek”, „wiatrołap”.
- Strona statyczna (HTML/CSS/GSAP) generowana z `_materials/build_site.py`; formularz działa przez mailto (brak backendu).

## Brand Commitments

- Nazwa i logo MoVilla (`img/logo.webp`, favicon `img/favicon-*.png`).
- Kolorystyka katalogów: ciepłe beże/taupe, ciemny grafit, limonkowy akcent — używana na stronie jako kontynuacja identyfikacji.
- Głos: rzeczowy, techniczny, bez marketingowych przesady; wszystkie liczby muszą pochodzić z katalogów.

## Evidence on Hand

- Wizualizacje zewnętrzne i wnętrz, rzuty, przekroje, detale warstw i zdjęcia konstrukcji stalowej (`img/`, `_materials/`).
- **Brak** prawdziwych zdjęć zrealizowanych domów, opinii klientów, referencji, cen i nagród. Strona nie może ich tworzyć ani sugerować; wizualizacje mają być opisane jako poglądowe.

## Product Principles

1. Liczby z katalogu, nigdy z domysłu; niepewne dane są oznaczane, nie uzupełniane.
2. Każdy model jest czytelny w 10 sekund: metraż, wymiary, układ, standard, czas.
3. Dwie ścieżki odbiorcy (dom dla siebie / produkt inwestycyjny) prowadzą do tej samej akcji: zapytania o wycenę.
4. Technologia jest argumentem sprzedażowym, więc pokazujemy ją, a nie tylko wspominamy (przekroje, warstwy, U).
5. Prezentacja ma robić wrażenie, ale nie kosztem szybkości i działania na telefonie.

## Accessibility & Inclusion

Brak wymagań formalnych od właściciela. Utrzymujemy: kontrast tekstu, klawiaturową obsługę menu, lightboxa i akordeonów oraz tryb bez animacji dla `prefers-reduced-motion`.
