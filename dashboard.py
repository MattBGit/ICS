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
    .chart-box {
        background-color: #1A1A1A;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        border: 1px solid #FFD700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="big-title">Interkontinentale Meisterschaft – Hall of Fame</div>', unsafe_allow_html=True)

# Lorbeerkranz anzeigen (muss im gleichen Verzeichnis liegen)
lorbeer_path = "Lorbeerkranz.jpeg"
if os.path.exists(lorbeer_path):
    st.image(lorbeer_path, width=160)

# --- Excel laden ---
excel_file = "International_Championship_List_of_Fame.xlsx"
if not os.path.exists(excel_file):
    st.error(f"Excel-Datei '{excel_file}' nicht gefunden! Bitte ins gleiche Verzeichnis legen.")
    st.stop()

results_df = pd.read_excel(excel_file, sheet_name="RESULTS")
statistics_df = pd.read_excel(excel_file, sheet_name="STATISTICS")

# --- KPIs ---
total_championships = results_df.shape[0]

# Reigning Champion = letzter Eintrag in 'Champion'
reigning_champion = results_df["Champion"].iloc[-1]
contender = "Doug" if reigning_champion == "Matze" else "Matze"

# Gesamtstatistiken aus dem STATISTICS-Blatt
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

# --- Diagrammdaten ---
x = results_df["# Championship "]
wins_doug = results_df["Total_Wins_Doug"]
wins_matze = results_df["Total_Wins_Matze"]
streak_doug = results_df["WinSeries_Doug"]
streak_matze = results_df["WinSeries_Matze"]

# --- Diagramm 1: Kumulative Siege ---
with st.container():
    st.markdown('<div class="chart-box"><h3 style="color:gold;">🏁 Winning Series (Kumulative Siege)</h3>', unsafe_allow_html=True)
    fig1, ax1 = plt.subplots()
    fig1.patch.set_facecolor("#1A1A1A")
    ax1.set_facecolor("#1A1A1A")
    ax1.plot(x, wins_doug, label="Doug", color="blue", linewidth=2)
    ax1.plot(x, wins_matze, label="Matze", color="red", linewidth=2)
    ax1.set_xlabel("Championships", color="gold")
    ax1.set_ylabel("Kumulative Siege", color="gold")
    ax1.tick_params(colors="gold")
    ax1.legend(facecolor="#1A1A1A", edgecolor="gold", labelcolor="gold")
    st.pyplot(fig1)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Diagramm 2: Total Frames ---
with st.container():
    st.markdown('<div class="chart-box"><h3 style="color:gold;">🎯 Total Frames</h3>', unsafe_allow_html=True)
    fig2, ax2 = plt.subplots()
    fig2.patch.set_facecolor("#1A1A1A")
    ax2.set_facecolor("#1A1A1A")
    ax2.bar(["Doug", "Matze"], [frames_doug, frames_matze], color=["blue", "red"])
    ax2.set_ylabel("Frames", color="gold")
    ax2.tick_params(colors="gold")
    st.pyplot(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Diagramm 3: Winning Streaks ---
with st.container():
    st.markdown('<div class="chart-box"><h3 style="color:gold;">🔥 Winning Streaks (in Folge)</h3>', unsafe_allow_html=True)
    fig3, ax3 = plt.subplots()
    fig3.patch.set_facecolor("#1A1A1A")
    ax3.set_facecolor("#1A1A1A")
    ax3.plot(x, streak_doug, label="Doug", color="blue", linewidth=2)
    ax3.plot(x, streak_matze, label="Matze", color="red", linewidth=2)
    ax3.set_xlabel("Championships", color="gold")
    ax3.set_ylabel("Gewinner in Folge", color="gold")
    ax3.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # nur ganze Zahlen
    ax3.tick_params(colors="gold")
    ax3.legend(facecolor="#1A1A1A", edgecolor="gold", labelcolor="gold")
    st.pyplot(fig3)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Alle Matches anzeigen ---
st.subheader("Alle Championships (aus Excel)")
st.dataframe(results_df)
