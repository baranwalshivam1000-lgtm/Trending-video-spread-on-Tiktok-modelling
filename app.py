import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

st.title("TikTok Viral Spread Simulation")

# ---------- Session State ----------
if "edges" not in st.session_state:
    st.session_state.edges = []

# ---------- Input Fields ----------
user1 = st.text_input("Enter User 1", key="user1")
user2 = st.text_input("Enter User 2", key="user2")

# ---------- Add Edge Function ----------
def add_edge():
    u1 = st.session_state.user1.strip()
    u2 = st.session_state.user2.strip()
    edge = (u1, u2)

    if not u1 or not u2:
        st.warning("Enter both users")
    elif u1 == u2:
        st.warning("Same user not allowed")
    elif edge not in st.session_state.edges:
        st.session_state.edges.append(edge)
        st.success("Share Added!")
    else:
        st.warning("Already exists")

    st.session_state.user1 = ""
    st.session_state.user2 = ""

# ---------- Buttons ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.button("Add Share", on_click=add_edge)

with col2:
    reset = st.button("RESET")

with col3:
    example = st.button("Example Data")

# ---------- Example Dataset ----------
if example:
    st.session_state.edges = [
        ("U1","U2"),("U1","U3"),("U2","U4"),
        ("U3","U4"),("U4","U5"),("U5","U6"),("U3","U6")
    ]

if reset:
    st.session_state.edges = []
    st.rerun()

# ---------- Build Directed Graph ----------
G = nx.DiGraph()
G.add_edges_from(st.session_state.edges)

# ---------- Display Table ----------
if st.session_state.edges:
    df = pd.DataFrame(st.session_state.edges, columns=["From","To"])
    st.table(df)

# ---------- Draw Graph ----------
if G.number_of_edges() > 0:
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G, seed=1)
    nx.draw(G, pos, with_labels=True, node_size=2000, font_size=12, ax=ax, arrows=True)
    ax.axis("off")
    st.pyplot(fig)

# ---------- Centrality ----------
deg = nx.degree_centrality(G)
bet = nx.betweenness_centrality(G)
clo = nx.closeness_centrality(G)

df_c = pd.DataFrame({
    "User": list(deg.keys()),
    "Influence (Degree)": list(deg.values()),
    "Bridge (Betweenness)": list(bet.values()),
    "Spread Speed (Closeness)": list(clo.values())
})

if not df_c.empty:
    st.table(df_c)

# ---------- Growth-Decay Model ----------
t = np.linspace(0, 10, 100)
growth = 1 / (1 + np.exp(-1*(t-5)))
decay = np.exp(-0.3*(t-5))
views = growth * decay * 1000

fig2, ax2 = plt.subplots()
ax2.plot(t, views)
ax2.set_title("Viral Growth and Decay")
ax2.set_xlabel("Time")
ax2.set_ylabel("Views")
st.pyplot(fig2)

# ---------- Insights ----------
if not df_c.empty:
    top_inf = df_c.loc[df_c["Influence (Degree)"].idxmax(), "User"]
    top_bridge = df_c.loc[df_c["Bridge (Betweenness)"].idxmax(), "User"]
    top_spread = df_c.loc[df_c["Spread Speed (Closeness)"].idxmax(), "User"]

    st.success(f"Top Influencer: {top_inf}")
    st.info(f"Key Bridge User: {top_bridge}")
    st.warning(f"Fastest Spreader: {top_spread}")