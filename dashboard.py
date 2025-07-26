import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from io import BytesIO
import base64

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
    .card {
        background-color: #1A1A1A;
        border-radius: 12px;
        border: 1px solid #FFD700;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .card h2 {
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
    img {
        max-width: 100%;
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
last_row = results_df.iloc[-1]
title_defense = int(last_row["WinSeries_Doug"]) if reigning_champion == "Doug" else int(last_row["WinSeries_Matze"])

# --- Statistiken ---
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

def render_full_card(title, content_html=None, plot_func=None, extra_image=None):
    """Erstellt eine HTML-Card, die Titel, optionales Bild und Diagramm als Base64 enthält."""
    chart_html = ""
    if plot_func:
        fig, ax = plt.subplots()
        style_plot(ax, fig)
        plot_func(ax)
        buf = BytesIO()
        fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        chart_html = f'<img src="data:image/png;base64,{img_b64}" />'

    lorbeer_html = ""
    if extra_image and os.path.exists(extra_image):
        with open(extra_image, "rb") as img_file:
            img_b64 = base64.b64encode(img_file.read()).decode()
            lorbeer_html = f'<img src="data:image/png;base64,{img_b64}" style="width:100px;" />'

    card_html = f"""
    <div class="card">
        <h2>{title}</h2>
        {lorbeer_html if lorbeer_html else ""}
        {content_html if content_html else ""}
        {chart_html if chart_html else ""}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# --- Zwei-Spalten-Layout ---
left_col, right_col = st.columns([1, 2])

# --- Linke Spalte ---
with left_col:
    # Reigning Champion (Lorbeerkranz, Name, Title Defenses)
    content = f'<div class="champion-name">{reigning_champion}</div><div class="subtitle">Title Defenses: {title_defense}</div>'
    render_full_card("Reigning Champion", content_html=content, extra_image="Lorbeerkranz.jpeg")

    # Total Championship Wins
    def plot_wins(ax):
        ax.bar(["Doug", "Matze"], [total_wins_doug, total_wins_matze], color=["blue", "red"])
        ax.set_ylabel("Wins", color="gold")
    render_full_card("Total Championship Wins", plot_func=plot_wins)

    # Total Frame Wins
    def plot_frames(ax):
        ax.bar(["Doug", "Matze"], [frames_doug, frames_matze], color=["blue", "red"])
        ax.set_ylabel("Frames", color="gold")
    render_full_card("Total Frame Wins", plot_func=plot_frames)

# --- Rechte Spalte ---
with right_col:
    # Championship Chart (kumulative Siege)
    def plot_champ_chart(ax):
        ax.plot(x, wins_doug, label="Doug", color="blue", linewidth=2)
        ax.plot(x, wins_matze, label="Matze", color="red", linewidth=2)
        ax.set_xlabel("Championships", color="gold")
        ax.set_ylabel("Kumulative Siege", color="gold")
        ax.legend(facecolor="#1A1A1A", edgecolor="gold", labelcolor="gold")
    render_full_card("Championship Chart", plot_func=plot_champ_chart)

    # Win Streaks
    def plot_streaks(ax):
        ax.plot(x, streak_doug, label="Doug", color="blue", linewidth=2)
        ax.plot(x, streak_matze, label="Matze", color="red", linewidth=2)
        ax.set_xlabel("Championships", color="gold")
        ax.set_ylabel("Gewinner in Folge", color="gold")
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.legend(facecolor="#1A1A1A", edgecolor="gold", labelcolor="gold")
    render_full_card("Win Streaks", plot_func=plot_streaks)

