# Visualisering og prediktiv analyse

Denne mappen inneholder Python-skript som visualiserer miljødataene vi har hentet og renset i prosjektet. Visualiseringene er laget med Matplotlib og Seaborn, og hvert script er knyttet til ett av datasettene (Blindern, Boston og London).

I tillegg er det inkludert enkle prediktive analyser – som eksempelvis lineær regresjon – for å gi innsikt i hvordan variabler som temperatur kan utvikle seg over tid.

---

## Formål

* Forstå og kommunisere trender i miljødata
* Identifisere sammenhenger mellom variabler
* Forutsi fremtidige forhold (f.eks. temperatur) basert på historiske data
* Støtte datadrevne vurderinger i refleksjonsnotatet

---

## Filoversikt

### `BlindernWeather.py`

* Visualiserer værdata hentet fra Frost API for Blindern (Oslo)
* Viser f.eks. utviklingen i temperatur, fuktighet og nedbør
* Prediktiv modell: Enkel lineær regresjon på temperatur over tid

### `BostonWeather.py`

* Visualiserer Boston-dataene hentet fra Kaggle (gjennom API)
* Inkluderer f.eks. nedbørsmengde og vindhastighet
* Fokuserer på sesongvariasjoner og trender over tid

### `LondonWeather.py`

* Visualiserer London-dataene som først ble manipulert og deretter renset
* Sammenligner opprinnelig og oppdatert datasett
* Viser bl.a. solskinn, temperatur og trykk
* Kan inkludere prediksjon for fremtidig gjennomsnittstemperatur

---

## Bruk

Kjør filene individuelt for å vise grafer, f.eks.:

```bash
python Visualisering/LondonWeather.py
```

Eller bruk `main.ipynb` for å samle visualiseringene i ett sted.

---

## Vurderingsgrunnlag

Visualiseringene er valgt for å være:

* Forklarende (tidsserier, sammenligning, korrelasjoner)
* Lesbare (riktig skala, titler, farger, akser)
* Konsistente med analyse og refleksjonsnotat
* Bruker både statiske og prediktive teknikker

---

## Biblioteker brukt

* `matplotlib`
* `seaborn`
* `pandas`
* `numpy`
* `scikit-learn` (for lineær regresjon)
