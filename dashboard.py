import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os

EXCEL_URL = "https://drive.google.com/uc?export=download&id=12vDy52LsShWpMuEh0lFABFXXhjgtVTUS"

st.set_page_config(page_title="Hall of Fame Test", layout="wide")
st.markdown("""
    <style>
    body { background-color: #0A0A0A; color: gold; }
    .card {
        background-color: #1A1A1A;
        border-radius: 12px;
        border: 1px solid #FFD700;
        padding: 20px;
        margin: 20px auto;
        text-align: center;
        width: 400px;
    }
    .card h2 { font-size: 28px; color: gold; margin-bottom: 15px; }
    .champion-name { font-size: 34px; font-weight: bold; color: gold; margin: 10px 0; }
    .subtitle { font-size: 18px; color: #FFD700; margin-bottom: 15px; }
    img { max-width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- Excel-Daten laden ---
results_df = pd.read_excel(EXCEL_URL, sheet_name="RESULTS")
reigning_champion = results_df["Champion"].iloc[-1]
last_row = results_df.iloc[-1]
title_defense = int(last_row["WinSeries_Doug"]) if reigning_champion == "Doug" else int(last_row["WinSeries_Matze"])

# --- Dummy-Diagramm (nur als Beispiel) ---
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 2], color="gold", linewidth=2)
fig.patch.set_facecolor("#1A1A1A")
ax.set_facecolor("#1A1A1A")
ax.tick_params(colors="gold")
for spine in ax.spines.values():
    spine.set_edgecolor("#FFD700")

# Diagramm als Base64
buf = BytesIO()
fig.savefig(buf, format="png", facecolor=fig.get_facecolor(), bbox_inches="tight")
chart_b64 = base64.b64encode(buf.getvalue()).decode()

# Lorbeerkranz einbetten
lorbeer_b64 = ""
if os.path.exists("Lorbeerkranz.jpeg"):
    with open("Lorbeerkranz.jpeg", "rb") as f:
        lorbeer_b64 = base64.b64encode(f.read()).decode()
lorbeer_html = f'<img src="data:image/jpeg;base64,{lorbeer_b64}" style="width:100px;" />' if lorbeer_b64 else ""

# --- Komplette Karte rendern ---
card_html = f"""
<div class="card">
    <h2>Reigning Champion</h2>
    {lorbeer_html}
    <div class="champion-name">{reigning_champion}</div>
    <div class="subtitle">Title Defenses: {title_defense}</div>
    <img src="data:image/png;base64,{chart_b64}" />
</div>
"""
st.markdown(card_html, unsafe_allow_html=True)
