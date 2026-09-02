# Surface brief: strona główna MoVilla (index.html) + podstrony projektów

Scope: cała witryna (index + 5 podstron projektów), tryb Persuade.
Audience: rodziny szukające domu całorocznego oraz inwestorzy (wynajem, glamping); równorzędnie.
Job / action: zrozumieć w 10 s ofertę (5 modeli, metraż, standard, 30–60 dni) i wysłać zapytanie o wycenę.
Proof: katalogi PDF, wizualizacje (poglądowe), rzuty, przekroje, parametry U; brak realizacji, cen, opinii — nie wymyślać.
Constraints: język polski; treści i liczby z katalogów; nie za tanio/katalogowo, nie ciemno/ciężko, nie zimno/korporacyjnie; GSAP dostępny; strona statyczna generowana z _materials/build_site.py.
Memorable moment: scroll przesuwa kursor dnia po linijce 0–60; dom „buduje się” etapami razem z przewijaniem.

## Direction contract

THESIS: Strona jest harmonogramem budowy: oś 60 dni to kręgosłup, na którym wisi każdy etap, model i parametr. Odrzuca render na całą szerokość + siatkę kart projektów.

OWN-WORLD: biały arkusz harmonogramu, hairline’owa siatka dni, nasycony żółty pasek etapu (marker z tablicy w hali) niosący ok. 35 % powierzchni, niebieski „długopis” dla kursora dnia, linków i CTA, atramentowa czerń. Display i tekst: Bricolage Grotesque; skala dni, wymiary i liczby: Azeret Mono tabularny. Bez kart, ramek, eyebrow’ów; słupki metrażu jako wykres na tej samej siatce.

STORY: „Dom powstaje w 30–60 dni” → widzę etapy i co dostaję → porównuję pięć modeli po metrażu → rozumiem stal i warstwy → piszę po wycenę (dzień 0).

FIRST VIEWPORT: nav; pod nim pełnoszerokościowa linijka dni 0–60 (sticky); po lewej 60 % nagłówek „Dom w 30–60 dni.” w 8–9 rem; pod nim jedno zdanie i CTA „Poproś o wycenę”; przez całą szerokość żółty pasek 0→60 z czterema etapami; po prawej plansza domu z etykietą „fot. 01 · wizualizacja”; niebieski kursor dnia porusza się ze scrollem, a plansza przechodzi rysunek → stalowy szkielet → gotowy dom. Sygnatura: scroll = dni budowy; ruch tylko wzdłuż osi X (paski rosną od lewej, plansze wjeżdżają z prawej).

FORM: Harmonogram budowy (IMPECCABLE’S PICK, pozycja 1 mojej listy; wylosowana była 4 „Mapa działki”, użytkownik wybrał 1). Seed key bd2f9ac5.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance.
