import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import os

# --- STYLING ---
st.set_page_config(page_title="Doug vs Matt Hall of Fame", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #111111;
        color: gold;
    }
    .big-title {
        font-size: 50px;
        text-align: center;
        color: gold;
        font-weight: bold;
    }
    .sub-title {
        font-size: 24px;
        text-align: center;
        color: #FFD700;
    }
    .metric {
        background-color: #222222;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: gold;
        font-size: 22px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="big-title">🏆 Doug vs. Matt Hall of Fame 🏆</div>', unsafe_allow_html=True)

# --- LORBEERKRANZ ---
lorbeer_path = "Lorbeerkranz.jpeg"
if os.path.exists(lorbeer_path):
    st.image(lorbeer_path, width=150)

DB_FILE = "championships.db"

# --- Prüfen, ob DB vorhanden ist ---
if not os.path.exists(DB_FILE):
    st.error(f"Die Datenbank '{DB_FILE}' wurde nicht gefunden! Bitte lade sie ins Verzeichnis hoch.")
    st.stop()

conn = sqlite3.connect(DB_FILE)

# --- Daten laden ---
def load_data():
    query = """
    SELECT c.id, c.date, v.state, v.city, v.location, 
           c.points_doug, c.points_matt, c.comment
    FROM Championships c
    LEFT JOIN Venues v ON c.venue_id = v.id
    ORDER BY c.date ASC
    """
    return pd.read_sql(query, conn)

df = load_data()

if df.empty:
    st.warning("Noch keine Championships eingetragen!")
else:
    # Gewinner/Verlierer bestimmen
    def get_winner(row):
        if row["points_doug"] > row["points_matt"]:
            return "Doug"
        elif row["points_matt"] > row["points_doug"]:
            return "Matze"
        else:
            return "Unentschieden"

    def get_loser(row):
        if row["points_doug"] > row["points_matt"]:
            return "Matze"
        elif row["points_matt"] > row["points_doug"]:
            return "Doug"
        else:
            return "Niemand"

    df["winner"] = df.apply(get_winner, axis=1)
    df["loser"] = df.apply(get_loser, axis=1)

    # KPIs
    last_match = df.iloc[-1]
    reigning_champ = last_match["winner"]
    contender = last_match["loser"]
    total_matches = len(df)
    doug_wins = (df["winner"] == "Doug").sum()
    matze_wins = (df["winner"] == "Matze").sum()
    total_frames_doug = df["points_doug"].sum()
    total_frames_matze = df["points_matt"].sum()

    # --- KPI Layout ---
    st.markdown(f'<div class="sub-title">Reigning Champion: <b>{reigning_champ}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">Contender: <b>{contender}</b></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown(f'<div class="metric">Championships Played<br><b>{total_matches}</b></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric">Total Wins<br><b>Doug: {doug_wins} | Matze: {matze_wins}</b></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric">Total Frames<br><b>Doug: {total_frames_doug} | Matze: {total_frames_matze}</b></div>', unsafe_allow_html=True)

    # --- Winning Series Chart (Linienchart) ---
    df["champ_index"] = range(1, len(df) + 1)
    df["doug_cum_wins"] = (df["winner"] == "Doug").cumsum()
    df["matze_cum_wins"] = (df["winner"] == "Matze").cumsum()

    st.subheader("🏁 Winning Series (Kumulative Siege)")
    fig, ax = plt.subplots()
    ax.plot(df["champ_index"], df["doug_cum_wins"], label="Doug", color="blue", linewidth=2)
    ax.plot(df["champ_index"], df["matze_cum_wins"], label="Matze", color="red", linewidth=2)
    ax.set_facecolor("#111111")
    ax.set_xlabel("Championships")
    ax.set_ylabel("Kumulative Siege")
    ax.set_title("Doug vs Matze – Kumulative Siege", color="gold")
    ax.tick_params(colors="gold")
    ax.legend()
    st.pyplot(fig)

    # --- Frames Chart (Balkendiagramm) ---
    st.subheader("🎯 Total Frames")
    fig2, ax2 = plt.subplots()
    ax2.bar(["Doug", "Matze"], [total_frames_doug, total_frames_matze], color=["blue", "red"])
    ax2.set_facecolor("#111111")
    ax2.set_title("Gesamt Frames", color="gold")
    ax2.set_ylabel("Frames", color="gold")
    ax2.tick_params(colors="gold")
    st.pyplot(fig2)

    # --- Alle Matches anzeigen ---
    st.subheader("Alle Championships")
    st.dataframe(df)

