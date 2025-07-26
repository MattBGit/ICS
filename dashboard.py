import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from io import BytesIO

# --- Google Drive Excel (deine Datei) ---
EXCEL_URL = "https://drive.google.com/uc?export=download&id=12vDy52LsShWpMuEh0lFABFXXhjgtVTUS"

# --- Styling ---
st.set_page_config(page_title="Intercontinental Championship – Hall of Fame", layout="wide")
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
        margin-bottom: 20px;
    }
    .box {
        background-color: #1A1A1A;
        border-radius: 12px;
        border: 1px solid #FFD700;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .box h2 {
        font-size: 26px;
        color: gold;
        margin-bottom: 15px;
    }
    .champion-name {
        font-size: 36px;
        font-weight: bold;
        color: gold;
        margin: 10px 0;
    }
    .subtitle {
        font-size: 18px;
        color: #FFD700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Überschrift ---
st.markdown('<div class="big-title">Intercontinental Championship – Hall of Fame</div>', unsafe_allow_html=True)

# --- Daten laden ---
try:
    results_df = pd.read_excel(EXCEL_URL, sheet_name="RESULTS")
    statistics_df = pd.read_excel(EXCEL_URL, sheet_name="STATISTICS")
except Exception as e:
    st.error(f"Fehler beim Laden der Excel-Datei von Google Drive: {e}")
    st.stop()

# --- Champion-Infos ---
reigning_champion = results_df["Champion"].iloc[-1]
contender = "Doug" if reigning_champion == "Matze" else "Matze"
last_row = results_df.iloc[-1]
title_defense = int(last_row["WinSeries_Doug"]) if reigning_champion == "Doug" else int(last_row["WinSeries_Matze"])

# --- Statistikwerte ---
total_wins_doug = statistics_df.loc[statistics_df["Player Comparison"] == "Total Championship won", "Doug"].values[0]
total_wins_matze = statistics_df.loc[statistics_df["Player Comparison"] == "Total Championship won", "Matze"].values[0]
frames_doug = statistics_df.loc[statistics_df["Player Comparison"] == "Total Frames Won", "Doug"].values[0]
frames_matze = statistics_df.loc[statistics_df["Player Comparison"] == "Total Frames Won", "Matze"].values[0]

# --- Diagrammdaten ---
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

def render_chart_box(title, plot_func):
    """Rendert eine komplette Box mit Titel und eingebettetem Diagramm."""
    st.markdown(f'<div class="box"><h2>{title}</h2>', unsafe_allow_html=True)

    # Diagramm generieren
    fig, ax = plt.subplots()
    style_plot(ax, fig)
    plot_func(ax)

    # Diagramm in BytesIO speichern und anzeigen
    buf = BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
    st.image(buf.getvalue())
    st.markdown('</div>', unsafe_allow_html=True)

# --- Zwei-Spalten-Layout ---
left_col, right_col = st.columns([1, 2])

# --- Linke Spalte ---
with left_col:
    # Box: Reigning Champion (mit Lorbeerkranz)
    st.markdown('<div class="box"><h2>Reigning Champion</h2>', unsafe_allow_html=True)
    lorbeer_path = "Lorbeerkranz.jpeg"
    if os.path.exists(lorbeer_path):
        st.image(lorbeer_path, width=120)
    st.markdown(f'<div class="champion-name">{reigning_champion}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">Title Defenses: {title_defense}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Box: Total Championship Wins
    def plot_wins(ax):
        ax.bar(["Doug", "Matze"], [total_wins_doug, total_wins_matze], color=["blue", "red"])
        ax.set_ylabel("Wins", color="gold")
    render_chart_box("Total Championship Wins", plot_wins)

    # Box: Total Frame Wins
    def plot_frames(ax):
        ax.bar(["Doug", "Matze"], [frames_doug, frames_matze], color=["blue", "red"])
        ax.set_ylabel("Frames", color="gold")
    render_chart_box("Total Frame Wins", plot_frames)

# --- Rechte Spalte ---
with right_col:
    # Box: Championship Chart (kumulative Siege)
    def plot_champ_chart(ax):
        ax.plot(x, wins_doug, label="Doug", color="blue", linewidth=2)
        ax.plot(x, wins_matze, label="Matze", color="red", linewidth=2)
        ax.set_xlabel("Championships", color="gold")
        ax.set_ylabel("Kumulative Siege", color="gold")
        ax.legend(facecolor="#1A1A1A", edgecolor="gold", labelcolor="gold")
    render_chart_box("Championship Chart", plot_champ_chart)

    # Box: Win Streaks
    def plot_streaks(ax):
        ax.plot(x, streak_doug, label="Doug", color="blue", linewidth=2)
        ax.plot(x, streak_matze, label="Matze", color="red", linewidth=2)
        ax.set_xlabel("Championships", color="gold")
        ax.set_ylabel("Gewinner in Folge", color="gold")
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.legend(facecolor="#1A1A1A", edgecolor="gold", labelcolor="gold")
    render_chart_box("Win Streaks", plot_streaks)
