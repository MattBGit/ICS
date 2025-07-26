import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# --- Google Drive Excel (Freigabe-Link) ---
EXCEL_URL = "https://drive.google.com/uc?export=download&id=12vDy52LsShWpMuEh0lFABFXXhjgtVTUS"

# --- Styling ---
st.set_page_config(page_title="Intercontinental Championship – Hall of Fame", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #0A0A0A;
        color: gold;
    }
    .big-title {
        font-size: 46px;
        text-align: center;
        color: gold;
        font-weight: bold;
        margin-bottom: 25px;
    }
    .card {
        background-color: #1A1A1A;
        border-radius: 12px;
        border: 1px solid #FFD700;
        padding: 15px;
        margin-bottom: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .card-title {
        font-size: 24px;
        font-weight: bold;
        color: gold;
        margin-bottom: 10px;
    }
    .champion-name {
        font-size: 32px;
        font-weight: bold;
        color: gold;
        margin: 8px 0;
    }
    .subtitle {
        font-size: 18px;
        color: #FFD700;
        margin-bottom: 10px;
    }
    .image-container {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Titel ---
st.markdown('<div class="big-title">Intercontinental Championship – Hall of Fame</div>', unsafe_allow_html=True)

# --- Daten laden ---
try:
    results_df = pd.read_excel(EXCEL_URL, sheet_name="RESULTS")
    statistics_df = pd.read_excel(EXCEL_URL, sheet_name="STATISTICS")
except Exception as e:
    st.error(f"Fehler beim Laden der Excel-Datei: {e}")
    st.stop()

# --- KPIs ---
reigning_champion = results_df["Champion"].iloc[-1]
last_row = results_df.iloc[-1]
title_defense = int(last_row["WinSeries_Doug"]) if reigning_champion == "Doug" else int(last_row["WinSeries_Matze"])

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

# --- Funktion für Karten ---
def render_card(title, content=None, plot_func=None, lorbeer=False):
    st.markdown(f'<div class="card"><div class="card-title">{title}</div>', unsafe_allow_html=True)

    if lorbeer and os.path.exists("Lorbeerkranz.jpeg"):
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image("Lorbeerkranz.jpeg", width=100)
        st.markdown('</div>', unsafe_allow_html=True)

    if content:
        st.markdown(content, unsafe_allow_html=True)

    if plot_func:
        fig, ax = plt.subplots()
        style_plot(ax, fig)
        plot_func(ax)
        st.pyplot(fig)

    st.markdown('</div>', unsafe_allow_html=True)

# --- Layout: zwei Spalten ---
left, right = st.columns([1, 2])

# --- Linke Spalte ---
with left:
    # Champion-Karte
    content = f'<div class="champion-name">{reigning_champion}</div><div class="subtitle">Title Defenses: {title_defense}</div>'
    render_card("Reigning Champion", content=content, lorbeer=True)

    # Total Championship Wins
    def plot_wins(ax):
        ax.bar(["Doug", "Matze"], [total_wins_doug, total_wins_matze], color=["blue", "red"])
        ax.set_ylabel("Wins", color="gold")
    render_card("Total Championship Wins", plot_func=plot_wins)

    # Total Frame Wins
    def plot_frames(ax):
        ax.bar(["Doug", "Matze"], [frames_doug, frames_matze], color=["blue", "red"])
        ax.set_ylabel("Frames", color="gold")
    render_card("Total Frame Wins", plot_func=plot_frames)

# --- Rechte Spalte ---
with right:
    # Championship Chart (kumulative Siege)
    def plot_champ(ax):
        ax.plot(x, wins_doug, label="Doug", color="blue", linewidth=2)
        ax.plot(x, wins_matze, label="Matze", color="red", linewidth=2)
        ax.set_xlabel("Championships", color="gold")
        ax.set_ylabel("Kumulative Siege", color="gold")
        ax.legend(facecolor="#1A1A1A", edgecolor="gold", labelcolor="gold")
    render_card("Championship Chart", plot_func=plot_champ)

    # Winning Streaks
    def plot_streak(ax):
        ax.plot(x, streak_doug, label="Doug", color="blue", linewidth=2)
        ax.plot(x, streak_matze, label="Matze", color="red", linewidth=2)
        ax.set_xlabel("Championships", color="gold")
        ax.set_ylabel("Gewinner in Folge", color="gold")
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.legend(facecolor="#1A1A1A", edgecolor="gold", labelcolor="gold")
    render_card("Winning Streaks", plot_func=plot_streak)

