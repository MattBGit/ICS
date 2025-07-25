import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import base64
import os

# --- Google Drive Excel ---
EXCEL_URL = "https://drive.google.com/uc?export=download&id=12vDy52LsShWpMuEh0lFABFXXhjgtVTUS"

# --- Styling ---
st.set_page_config(page_title="Intercontinental Championship – Hall of Fame", layout="wide")
st.markdown("""
    <style>
    body { background-color: #0A0A0A; color: gold; }
    .big-title {
        font-size: 46px;
        text-align: center;
        color: gold;
        font-weight: bold;
        margin-bottom: 25px;
    }
    .header-box {
    background-color: #000000;
    border: 1px solid #FFD700;
    border-radius: 10px;
    padding: 15px;
    display: flex;
    align-items: center;
    margin-bottom: 25px;
}

.header-text {
    font-size: 40px;
    color: gold;
    font-weight: bold;
    margin-left: 20px;
}

    h2 {
        color: gold;
        margin-bottom: 10px;
    }
    .card {
        background-color: #1A1A1A;
        border-radius: 12px;
        border: 1px solid #FFD700;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .champion-name { font-size: 34px; font-weight: bold; color: gold; margin: 10px 0; }
    .subtitle { font-size: 18px; color: gold; margin-bottom: 15px; }
    img { max-width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- Titelzeile mit Logo ---
logo_path = "International_Championship_Logo_Only.png"  # Stelle sicher, dass du dein Logo so benennst
if os.path.exists(logo_path):
    logo_b64 = base64.b64encode(open(logo_path, "rb").read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:60px;" />'
else:
    logo_html = ""

st.markdown(f"""
<div class="header-box">
    {logo_html}
    <div class="header-text">Intercontinental Championship – Hall of Fame</div>
</div>
""", unsafe_allow_html=True)

# --- Excel laden ---
try:
    results_df = pd.read_excel(EXCEL_URL, sheet_name="RESULTS")
    statistics_df = pd.read_excel(EXCEL_URL, sheet_name="STATISTICS")
except Exception as e:
    st.error(f"Fehler beim Laden der Excel-Datei: {e}")
    st.stop()

# --- Champion-Daten ---
reigning_champion = results_df["Champion"].iloc[-1]
last_row = results_df.iloc[-1]
title_defense = int(last_row["WinSeries_Doug"]) if reigning_champion == "Doug" else int(last_row["WinSeries_Matze"])

# Lorbeerkranz (Base64 für Champion-Box)
lorbeer_b64 = ""
if os.path.exists("Lorbeerkranz_noBG.png"):
    with open("Lorbeerkranz_noBG.png", "rb") as f:
        lorbeer_b64 = base64.b64encode(f.read()).decode()
lorbeer_html = f'<img src="data:image/jpeg;base64,{lorbeer_b64}" style="width:100px;" />' if lorbeer_b64 else ""

# --- Champion-Karte ---
champion_html = f"""
<div class="card">
    <div style="font-size:36px; color:gold; font-weight:bold; margin-bottom:15px; text-align:center;">
        Reigning Champion
    </div>
    {lorbeer_html}
    <div class="champion-name">{reigning_champion}</div>
    <div class="subtitle">Title Defenses: {title_defense}</div>
</div>
"""

# --- Statistikdaten für Charts ---
total_wins_doug = statistics_df.loc[statistics_df["Player Comparison"] == "Total Championship won", "Doug"].values[0]
total_wins_matze = statistics_df.loc[statistics_df["Player Comparison"] == "Total Championship won", "Matze"].values[0]
frames_doug = statistics_df.loc[statistics_df["Player Comparison"] == "Total Frames Won", "Doug"].values[0]
frames_matze = statistics_df.loc[statistics_df["Player Comparison"] == "Total Frames Won", "Matze"].values[0]

x = results_df["# Championship "]
wins_doug = results_df["Total_Wins_Doug"]
wins_matze = results_df["Total_Wins_Matze"]
streak_doug = results_df["WinSeries_Doug"]
streak_matze = results_df["WinSeries_Matze"]

def style_plot(ax, fig):
    fig.patch.set_facecolor("#1A1A1A")
    ax.set_facecolor("#1A1A1A")
    ax.tick_params(colors="gold")
    for spine in ax.spines.values():
        spine.set_edgecolor("#FFD700")

# --- Zwei-Spalten-Layout ---
left, right = st.columns([1, 2])

# --- Linke Spalte ---
with left:
    # Champion-Box
    st.markdown(champion_html, unsafe_allow_html=True)

    # Championship Wins (Balkendiagramm)
    fig1, ax1 = plt.subplots(figsize=(4,4))
    style_plot(ax1, fig1)
    bars1 = ax1.bar(["Doug", "Matze"], [total_wins_doug, total_wins_matze], color=["blue", "red"])
    ax1.set_ylabel("Wins", color="gold")
    ax1.set_title("Total Championship Wins", color="gold", fontsize=18, pad=20)
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height/2, str(int(height)),
                 ha='center', va='center', color='gold', fontsize=14, fontweight='bold')
    st.pyplot(fig1)

    # Frame Wins (Balkendiagramm)
    fig2, ax2 = plt.subplots(figsize=(4,4))
    style_plot(ax2, fig2)
    bars2 = ax2.bar(["Doug", "Matze"], [frames_doug, frames_matze], color=["blue", "red"])
    ax2.set_ylabel("Frames", color="gold")
    ax2.set_title("Total Frame Wins", color="gold", fontsize=18, pad=20)
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height/2, str(int(height)),
                 ha='center', va='center', color='gold', fontsize=14, fontweight='bold')
    st.pyplot(fig2)

# --- Rechte Spalte ---
with right:
    # Championship Chart (kleineres Linienchart)
    fig3, ax3 = plt.subplots(figsize=(6,3))  # kleiner gemacht
    style_plot(ax3, fig3)
    ax3.plot(x, wins_doug, label="Doug", color="blue", linewidth=2)
    ax3.plot(x, wins_matze, label="Matze", color="red", linewidth=2)
    ax3.set_xlabel("Championships", color="gold")
    ax3.set_ylabel("Wins", color="gold")
    ax3.set_title("Championship Chart", color="gold", fontsize=18, pad=20)
    ax3.legend(facecolor="#1A1A1A", edgecolor="gold", labelcolor="gold")
    st.pyplot(fig3)

    # Winning Streaks (kleineres Linienchart)
    fig4, ax4 = plt.subplots(figsize=(6,3))  # kleiner gemacht
    style_plot(ax4, fig4)
    ax4.plot(x, streak_doug, label="Doug", color="blue", linewidth=2)
    ax4.plot(x, streak_matze, label="Matze", color="red", linewidth=2)
    ax4.set_xlabel("Championships", color="gold")
    ax4.set_ylabel("Consecutive Wins", color="gold")
    ax4.set_title("Winning Streaks", color="gold", fontsize=18, pad=20)
    ax4.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax4.legend(facecolor="#1A1A1A", edgecolor="gold", labelcolor="gold")
    st.pyplot(fig4)

