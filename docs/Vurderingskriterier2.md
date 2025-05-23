# Vurderingskriterier – Oppgave 2: Datainnsamling

## 1. Hvilke åpne datakilder er identifisert som relevante for miljødata, og hva er kriteriene (f.eks. kildeautoritet, datakvalitet, tilgjengelighet, brukervennlighet osv.) for å vurdere deres pålitelighet og kvalitet?

Frost API, Copernicus Climate Data Store, OpenAQ og EEA Air Quality Data er alle relevante kilder for miljødata.  
Frost API er en kilde fra Meteorologisk institutt som gir historiske samt sanntidsmålinger av værdata. Dette er en kilde med høy kildeautoritet, da den er statlig.

Copernicus tilbyr data hentet fra satellitter og bakkemålinger av høy kvalitet, drevet av det europeiske jordobservasjonsprogrammet – også en pålitelig aktør.

Andre eksempler:
- **NOAA** - hydrologiske data om havnivå og værmønstre
- **NVE** - vannføringsdata fra norske innsjøer og elver
- **GBIF** - global miljødata

### Kriterier for pålitelighet:
- **Kildeautoritet**: Er det en statlig eller forskningsbasert institusjon?
- **Datakvalitet**: Hvor nøyaktige og komplette er dataene?
- **Oppdateringshyppighet**: Er dataene oppdaterte, spesielt ved sanntidsbruk?
- **Brukervennlighet**: Er dataene godt dokumentert og strukturert?
- **Tilgjengelighet**: Er dataene åpne og lisensiert for gjenbruk?

---

## 2. Hvilke teknikker (f.eks. håndtering av CSV-filer, JSON-data) er valgt å bruke for å lese inn dataene, og hvordan påvirker disse valgene datakvaliteten og prosessen videre?

- **observations_data.json (Frost API)**: Data hentes direkte fra kilden via API – alltid oppdatert med siste målinger. Krever internett og nøkkel.
- **bostonData2.csv (Kaggle via API)**: CSV lastes ned og analyseres lokalt. Gir kontroll og enkel distribusjon, men kan bli utdaterte eller tunge filer.
- **london_weather.json (Kaggle CSV → JSON)**: Lokal CSV konverteres til strukturert JSON for bedre manipulering og testing. JSON er bedre egnet for datarensing og simulering av feil.

Valgene våre sikrer fleksibilitet og gjør det enklere å jobbe både med sanntid og lokal filbehandling.

---

## 3. Dersom det er brukt API-er, hvilke spesifikke API-er er valgt å bruke, og hva er de viktigste dataene som kan hentes fra disse kildene?

API-er brukt og hva slags data de tilbyr:

- **Frost API (observations_data.json)**  
  Tjeneste fra Meteorologisk institutt for værdata. Kodesnutten `requests.get(endpoint, parameters, auth=...)` sender HTTP GET-forespørsel med API-nøkkel for autentisering.

- **Meteostat API (bostonData2.csv)**  
  Python-modul for værdata. Koden bruker `Daily('72509', start, end)` for å hente værhistorikk fra gitt stasjon.

- **Kaggle CSV (london_weather.json)**  
  Data lastes manuelt ned, og en konverteringskode lagrer det som JSON. Dette gir oss et kontrollerbart testmiljø hvor vi selv kunne tilføre feil og mangler.

---
