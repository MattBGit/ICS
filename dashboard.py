import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Match Dashboard", layout="wide")
st.title("🏆 Wettkampf-Dashboard (Online)")

# ---- CONFIG: Google Drive File Link ----
# Hier die Datei-ID deiner Google-Drive-Excel eintragen
# GOOGLE_DRIVE_LINK = "https://drive.google.com/uc?export=download&id=DEINE_DATEI_ID"
df = pd.read_excel("example_results.xlsx")

@st.cache_data
def load_data():
    df = pd.read_excel(GOOGLE_DRIVE_LINK)
    df.columns = [c.strip().lower() for c in df.columns]
    return df

df = load_data()

# Optional: Datumsspalte
df["date"] = pd.to_datetime(df.get("date", pd.NaT)) if "date" in df.columns else pd.NaT
players = pd.concat([df["winner"], df["loser"]]).unique()

# ---- Sidebar Filter ----
st.sidebar.header("Filter")
city_filter = st.sidebar.multiselect("City", df["city"].unique(), default=df["city"].unique())
location_filter = st.sidebar.multiselect("Location", df["location"].unique(), default=df["location"].unique())
df_filtered = df[(df["city"].isin(city_filter)) & (df["location"].isin(location_filter))]

# ---- Statistiken ----
matches_played = pd.DataFrame(players, columns=["player"])
matches_played["matches"] = matches_played["player"].apply(
    lambda p: ((df_filtered["winner"] == p) | (df_filtered["loser"] == p)).sum()
)
matches_played["wins"] = matches_played["player"].apply(lambda p: (df_filtered["winner"] == p).sum())
matches_played["losses"] = matches_played["matches"] - matches_played["wins"]
matches_played["winrate"] = (matches_played["wins"] / matches_played["matches"] * 100).round(1)

# ---- KPIs ----
st.subheader("Gesamtstatistiken")
col1, col2, col3 = st.columns(3)
col1.metric("Gesamt Matches", len(df_filtered))
col2.metric("Spieler", len(players))
top_player = matches_played.sort_values("wins", ascending=False).iloc[0]
col3.metric("Top Spieler (Siege)", f"{top_player['player']} ({top_player['wins']})")

# ---- Leaderboard ----
st.subheader("🏅 Leaderboard (Top 10 nach Siegen)")
leaderboard = matches_played.sort_values("wins", ascending=False).head(10)
st.dataframe(leaderboard[["player", "matches", "wins", "losses", "winrate"]])

# ---- Diagramme ----
st.subheader("Siege pro Spieler (Top 10)")
fig, ax = plt.subplots()
ax.bar(leaderboard["player"], leaderboard["wins"])
ax.set_ylabel("Siege")
ax.set_xlabel("Spieler")
ax.set_title("Top 10 Spieler")
plt.xticks(rotation=45)
st.pyplot(fig)

# ---- Trend (nur wenn Datum existiert) ----
if "date" in df_filtered.columns and df_filtered["date"].notna().any():
    st.subheader("Matches über Zeit")
    df_time = df_filtered.copy()
    df_time["month"] = df_time["date"].dt.to_period("M")
    matches_over_time = df_time.groupby("month").size()
    fig2, ax2 = plt.subplots()
    matches_over_time.plot(ax=ax2)
    ax2.set_ylabel("Matches")
    ax2.set_xlabel("Monat")
    ax2.set_title("Trend der Matches")
    st.pyplot(fig2)

# ---- Alle Matches ----
st.subheader("Alle Matches (gefiltert)")
st.dataframe(df_filtered)

st.caption("Datenquelle: Google Drive – einfach Excel austauschen, Link bleibt gleich.")
