HUSK Å SKRIVE OPP BESKRIVELSE OM DATAENE.
Bl.a.:
HVOR er det hentet fra?
HVA handler  de om?
EVT. lenker?
HVILKE  kolonner sier hva, hvilke kolonner har vi fått lest osv...

I denne mappen finner du kildekoden som behandler datasettene fra data mappen. datasett2.py henter inn en .csv fil ved bruk av en API (bostonData2.csv, som du finner i datamappen). koden i dataSettApi.ipynb henter et datasett fra Frost ved hjelp av en API nøkkel(dataen er altså ikke lagret lokalt). Koden i find_parameters.py finner parametere som skal brukes i koden dataSettApi.ipynb. Disse parameterne representerer værstasjoner. 

Filen main.py skal inneholde funksjoner som refererer til alle tre datasettene. Dette kommer...