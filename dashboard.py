import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# --- STYLING ---
st.set_page_config(page_title="Interkontinentale Meisterschaft – Hall of Fame", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #0A0A0A;
        color: gold;
    }
    .big-title {
        font-size: 48px;
        text-align: center;
        color: gold;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 22px;
        text-align: center;
        color: #FFD700;
        margin-bottom: 20px;
    }
    .metric {
        background-color: #1A1A1A;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: gold;
        font-size: 20px;
        margin: 5px;
        border: 1px solid #FFD700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="big-title">Interkontinentale Meisterschaft – Hall of Fame</div>', unsafe_allow_html=True)

# Lorbeerkranz-Bild anzeigen (muss im gleichen Ordner wie dieses Skript liegen)
lorbeer_path = "Lorbeerkranz.jpeg"
if os.path.exists(lorbeer_path):
    st.image(lorbeer_path, width=160)

# --- Excel-Datei laden ---
excel_file = "International_Championship_List_of_Fame.xlsx"
if not os.path.exists(excel_file):
    st.error(f"Excel-Datei '{excel_file}' nicht gefunden! Bitte ins gleiche Verzeichnis legen.")
    st.stop()

results_df = pd.read_excel(excel_file, sheet_name="RESULTS")
statistics_df = pd.read_excel(excel_file, sheet_name="STATISTICS")

# --- KPIs berechnen ---
total_championships = results_df.shape[0]
reigning_champion = results_df["Current Champion"].dropna().iloc[-1] if "Current Champion" in results_df.columns else results_df["Champion"].iloc[-1]
contender = "Doug" if reigning_champion == "Matze" else "Matze"

total_wins_doug = statistics_df.loc[statistics_df["Player Comparison"] == "Total Championship won", "Doug"].values[0]
total_wins_matze = statistics_df.loc[statistics_df["Player Comparison"] == "Total Championship won", "Matze"].values[0]
frames_doug = statistics_df.loc[statistics_df["Player Comparison"] == "Total Frames Won", "Doug"].values[0]
frames_matze = statistics_df.loc[statistics_df["Player Comparison"] == "Total Frames Won", "Matze"].values[0]

# --- KPIs anzeigen ---
st.markdown(f'<div class="sub-title">Reigning Champion: <b>{reigning_champion}</b></div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-title">Contender: <b>{contender}</b></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.markdown(f'<div class="metric">Championships Played<br><b>{total_championships}</b></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric">Total Wins<br><b>Doug: {total_wins_doug} | Matze: {total_wins_matze}</b></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric">Total Frames<br><b>Doug: {frames_doug} | Matze: {frames_matze}</b></div>', unsafe_allow_html=True)

# --- Daten für Diagramme vorbereiten ---
x = results_df["# Championship "]
wins_doug = results_df["Total_Wins_Doug"]
wins_matze = results_df["Total_Wins_Matze"]
streak_doug = results_df["WinSeries_Doug"]
streak_matze = results_df["WinSeries_Matze"]

# --- Diagramm 1: Kumulative Siege ---
st.subheader("🏁 Winning Series (Kumulative Siege)")
fig1, ax1 = plt.subplots()
fig1.patch.set_facecolor("#0A0A0A")
ax1.set_facecolor("#0A0A0A")
ax1.plot(x, wins_doug, label="Doug", color="blue", linewidth=2)
ax1.plot(x, wins_matze, label="Matze", color="red", linewidth=2)
ax1.set_xlabel("Championships", color="gold")
ax1.set_ylabel("Kumulative Siege", color="gold")
ax1.set_title("Doug vs Matze – Kumulative Siege", color="gold")
ax1.tick_params(colors="gold")
ax1.legend(facecolor="#0A0A0A", edgecolor="gold", labelcolor="gold")
st.pyplot(fig1)

# --- Diagramm 2: Total Frames ---
st.subheader("🎯 Total Frames")
fig2, ax2 = plt.subplots()
fig2.patch.set_facecolor("#0A0A0A")
ax2.set_facecolor("#0A0A0A")
ax2.bar(["Doug", "Matze"], [frames_doug, frames_matze], color=["blue", "red"])
ax2.set_ylabel("Frames", color="gold")
ax2.set_title("Gesamt Frames", color="gold")
ax2.tick_params(colors="gold")
st.pyplot(fig2)

# --- Diagramm 3: Winning Streaks ---
st.subheader("🔥 Winning Streaks (in Folge)")
fig3, ax3 = plt.subplots()
fig3.patch.set_facecolor("#0A0A0A")
ax3.set_facecolor("#0A0A0A")
ax3.plot(x, streak_doug, label="Doug", color="blue", linewidth=2)
ax3.plot(x, streak_matze, label="Matze", color="red", linewidth=2)
ax3.set_xlabel("Championships", color="gold")
ax3.set_ylabel("Gewinner in Folge", color="gold")
ax3.set_title("Doug vs Matze – Siegesserien", color="gold")
ax3.tick_params(colors="gold")
ax3.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # nur ganze Zahlen
ax3.legend(facecolor="#0A0A0A", edgecolor="gold", labelcolor="gold")
st.pyplot(fig3)

# --- Alle Matches anzeigen ---
st.subheader("Alle Championships (aus Excel)")
st.dataframe(results_df)

