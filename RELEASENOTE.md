# Release Note – Miljødataanalyse v1.0

Dato: 2025-05-26
Versjon: 1.0
Prosjekt: TDT4114 – Anvendt Programmering

## Introduksjon

Dette er første offisielle versjon v prosjektet *Miljødataanalyse*, utviklet som en del av emnet TDT4114. Appliksjonen henter, renser, analyserer og visualiserer væredata fra ulike byer ved bruk av offentlige APIer og datasett. Prediksjonsmodeller er implementert for å forutse fremtidige temperaturutviklinger de neste 5 år. 

---

## Høydepunkter i denne versjonen

### Datainnhenting
* Støtte for Frost API (`Blindern`) med bruk av `.env`-fil for sikker håndtering av API- nøkler.
* Import av data fra Kaggle (`Boston`) og konvertering fra CSV til JSON (`London`).

### Datavask og kvalitet
* Robust behandling av manglende verdier (`mean`, `median`, `ffill`, `bfill`) i `FeilOgMangler.py`).
* Automatisk deteksjon og håndtering av uteliggere med definert kvantil- eller grensebasert logikk.
* Fjernet duplikater og ugyldige datoer. 

### Enhetstester
* Full testdekning på datarensing, uteliggeridentifisering og API- håndtering. 
* Tester følger *Arrange-Act-Assert* strukturen og kjøres isolert. 
* Bruk av mocking for API-kall for stabil og rask testing. 

### Visualisering og analyse
* Interaktive grafer (Plotly) for temperatur, nedbør og vind. 
* XGBoost og LightGBM- modeller for temperaturprediksjon 5 år frem i tid. 
* Lineær regresjon med evaluringsmetoder (MSE og R2). 
* Notebook fremstilling (`main.ipynb`) som samler hele prosjektet. 

### Struktur og organisering
* Tydelig mappestruktur: `src/`, `tester/`, `data/`, `visualisering/`
* Alle funksjoner og analyser kan kjøres via `main.ipynb` og kaller på `.py`-filer.
* README- filer per mappe for oversikt og dokumentasjon

---

## Forbedringer fra tidligere iterasjoner
* Fjernet .py- filer fra `data/`.
* Bedre modulnavn og paramterverifisering i funksjoner. 
* Endringer dokumentert og versjonskontrollert i separate brancher. 

---

## Neste steg (forslag til videreutvikling)
*  Legge til flere geografiske omrpder og datakilder. 
*  Utvide prediksjonsmodellen med sesong- og klimavariabler 
*  Bedre forntend for ikke- tekniske brukere 
*  CI/CD for automatisk testkjøring ved nye commits. 

---

## Bidragsytere

* Ingrid Amalie Lien
* Evine H. Fagerhaug
* Amalie Sofie Fredriksen

---


**API-kilde:** [frost.met.no](https://frost.met.no), Kaggle
**Oppgave:** Anvendt Porgrammering TDT4114 - Mappeinnlevering
**Kontakt:** via GitHub repository eller epost registrert i emnet.
