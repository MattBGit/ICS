# Wettkampf-Dashboard

Ein interaktives Dashboard zur Auswertung von Matchdaten (Siege, Winrate, Trends).

## Live starten (Streamlit Cloud)
1. Lade dieses Repository auf deinen GitHub-Account hoch (als **öffentliches Repo**).
2. Lade deine Excel-Datei (`results.xlsx`) in Google Drive hoch und hole dir die **Datei-ID**.
3. Ersetze in `dashboard.py` den Platzhalter `DEINE_DATEI_ID` mit deiner Google-Drive-Datei-ID.
4. Gehe auf [https://share.streamlit.io](https://share.streamlit.io) und deploye das Repo.

## Lokal starten
```bash
pip install -r requirements.txt
streamlit run dashboard.py
```
