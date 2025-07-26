import streamlit as st
import pandas as pd
import excel2img
import os
import tempfile

# Google Drive Excel (Dashboard-Blatt)
EXCEL_URL = "https://drive.google.com/uc?export=download&id=12vDy52LsShWpMuEh0lFABFXXhjgtVTUS"

st.set_page_config(page_title="Intercontinental Championship – Hall of Fame", layout="wide")
st.markdown("<h1 style='text-align:center; color:gold;'>Intercontinental Championship – Hall of Fame</h1>", unsafe_allow_html=True)

try:
    # Lade Excel herunter
    temp_excel = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    temp_excel.write(pd.read_excel(EXCEL_URL).to_excel(index=False))
    temp_excel.flush()

    # Exportiere das Blatt 'Dashboard' als PNG
    output_png = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
    excel2img.export_img(temp_excel.name, output_png, "Dashboard")

    # Zeige das Bild an
    st.image(output_png, use_column_width=True)

except Exception as e:
    st.error(f"Fehler beim Laden oder Konvertieren der Excel: {e}")
