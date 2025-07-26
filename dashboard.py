import streamlit as st
import pandas as pd
import requests
import tempfile
from pdf2image import convert_from_path
import os

# --- Deine Excel von Google Drive ---
EXCEL_URL = "https://drive.google.com/uc?export=download&id=12vDy52LsShWpMuEh0lFABFXXhjgtVTUS"

st.set_page_config(page_title="Intercontinental Championship – Hall of Fame", layout="wide")
st.markdown("<h1 style='text-align:center; color:gold;'>Intercontinental Championship – Hall of Fame</h1>", unsafe_allow_html=True)

try:
    # --- Schritt 1: Excel von Google Drive herunterladen ---
    excel_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    r = requests.get(EXCEL_URL)
    excel_temp.write(r.content)
    excel_temp.flush()

    # --- Schritt 2: Mit LibreOffice (sofern auf Server vorhanden) in PDF exportieren ---
    # Für Streamlit Cloud: LibreOffice ist oft nicht installiert, daher vereinfachen wir:
    # Stattdessen gehen wir davon aus, dass du das Dashboard-Blatt in Google Drive auch als PDF freigeben kannst.
    # -> Wenn du stattdessen direkt ein PDF-Dashboard bereitstellst (aus Excel exportiert), geht das einfacher.
    # Hier zeigen wir, wie man ein PDF (bereits hochgeladen) rendert.

    # Beispiel: Du exportierst dein Dashboard einmal manuell als PDF und lädst es hoch:
    DASHBOARD_PDF_URL = "https://drive.google.com/uc?export=download&id=HIER_DEINE_PDF_ID"

    # Lade PDF herunter
    pdf_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    r = requests.get(DASHBOARD_PDF_URL)
    pdf_temp.write(r.content)
    pdf_temp.flush()

    # --- Schritt 3: PDF in Bild umwandeln ---
    pages = convert_from_path(pdf_temp.name, dpi=150)
    output_png = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    pages[0].save(output_png, "PNG")

    # --- Schritt 4: Bild anzeigen ---
    st.image(output_png, use_column_width=True)

except Exception as e:
    st.error(f"Fehler beim Laden oder Konvertieren: {e}")
