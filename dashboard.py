# --- Championship Wins (Bar Chart) ---
st.markdown('<div class="card"><h2>Total Championship Wins</h2>', unsafe_allow_html=True)
fig1, ax1 = plt.subplots()
style_plot(ax1, fig1)
bars1 = ax1.bar(["Doug", "Matze"], [total_wins_doug, total_wins_matze], color=["blue", "red"])
ax1.set_ylabel("Wins", color="gold")
# Summen über Balken zeichnen
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height + 0.5, str(int(height)),
             ha='center', va='bottom', color='gold', fontsize=12, fontweight='bold')
st.pyplot(fig1)
st.markdown('</div>', unsafe_allow_html=True)

# --- Frame Wins (Bar Chart) ---
st.markdown('<div class="card"><h2>Total Frame Wins</h2>', unsafe_allow_html=True)
fig2, ax2 = plt.subplots()
style_plot(ax2, fig2)
bars2 = ax2.bar(["Doug", "Matze"], [frames_doug, frames_matze], color=["blue", "red"])
ax2.set_ylabel("Frames", color="gold")
# Summen über Balken zeichnen
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, height + 0.5, str(int(height)),
             ha='center', va='bottom', color='gold', fontsize=12, fontweight='bold')
st.pyplot(fig2)
st.markdown('</div>', unsafe_allow_html=True)
