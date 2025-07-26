import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import os

st.set_page_config(page_title="Doug vs Matt Dashboard", layout="wide")
st.title("🏆 Doug vs. Matt Championships Dashboard")

DB_FILE = "championships.db"

# Prüfen, ob DB vorhanden ist
if not os.path.exists(DB_FILE):
    st.error(f"Die Datenbank '{DB_FILE}' wurde nicht gefunden! Bitte lade sie ins Verzeichnis hoch.")
    st.stop()

# Verbindung zur bestehenden DB
conn = sqlite3.connect(DB_FILE)

# ---- Daten laden ----
def load_data():
    query = """
    SELECT c.id, c.date, v.state, v.city, v.location, 
           c.points_doug, c.points_matt, c.comment
    FROM Championships c
    LEFT JOIN Venues v ON c.venue_id = v.id
    ORDER BY c.date ASC
    """
    return pd.read_sql(query, conn)

# ---- Formular für neue Matches (optional) ----
st.sidebar.header("Neues Championship eintragen")
with st.sidebar.form("match_form", clear_on_submit=True):
    date = st.date_input("Datum", datetime.today())
    state = st.text_input("State")
    city = st.text_input("City")
    location = st.text_input("Location")
    points_doug = st.number_input("Punkte Doug", min_value=0, value=0)
    points_matt = st.number_input("Punkte Matt", min_value=0, value=0)
    comment = st.text_area("Kommentar")
    submitted = st.form_submit_button("Speichern")
    if submitted:
        # Venue-ID suchen (muss existieren)
        cur = conn.cursor()
        cur.execute("SELECT id FROM Venues WHERE state=? AND city=? AND location=?", (state, city, location))
        venue = cur.fetchone()
        if venue:
            venue_id = venue[0]
            with conn:
                conn.execute("""
                    INSERT INTO Championships (date, venue_id, points_doug, points_matt, comment)
                    VALUES (?, ?, ?, ?, ?)
                """, (date.strftime("%Y-%m-%d"), venue_id, points_doug, points_matt, comment))
            st.success("Match gespeichert!")
        else:
            st.error("Venue existiert nicht in der Datenbank! Bitte zuerst in DB hinzufügen.")

# ---- Daten anzeigen ----
df = load_data()

if df.empty:
    st.warning("Noch keine Championships in der Datenbank!")
else:
    # Gewinner/Verlierer bestimmen
    def get_winner(row):
        if row["points_doug"] > row["points_matt"]:
            return "Doug"
        elif row["points_matt"] > row["points_doug"]:
            return "Matt"
        else:
            return "Unentschieden"

    def get_loser(row):
        if row["points_doug"] > row["points_matt"]:
            return "Matt"
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
    matt_wins = (df["winner"] == "Matt").sum()
    total_frames_doug = df["points_doug"].sum()
    total_frames_matt = df["points_matt"].sum()

    st.subheader("Championship Übersicht")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Reigning Champion", reigning_champ)
    col2.metric("Contender", contender)
    col3.metric("Championships Played", total_matches)
    col4.metric("Doug Wins", doug_wins)
    col5.metric("Matt Wins", matt_wins)
    col6.metric("Frames (Doug / Matt)", f"{total_frames_doug} / {total_frames_matt}")

    # Linienchart: Kumulative Siege
    st.subheader("Kumulative Siege über Championships")
    df["champ_index"] = range(1, len(df) + 1)
    df["doug_cum_wins"] = (df["winner"] == "Doug").cumsum()
    df["matt_cum_wins"] = (df["winner"] == "Matt").cumsum()

    fig, ax = plt.subplots()
    ax.plot(df["champ_index"], df["doug_cum_wins"], label="Doug", color="blue")
    ax.plot(df["champ_index"], df["matt_cum_wins"], label="Matt", color="red")
    ax.set_xlabel("Championship-Nummer")
    ax.set_ylabel("Kumulative Siege")
    ax.set_title("Doug vs Matt – Siege im Verlauf")
    ax.legend()
    st.pyplot(fig)

    # Alle Matches anzeigen
    st.subheader("Alle Championships")
    st.dataframe(df)

