import streamlit as st
import functions


def set_hit():
    st.session_state["hit"] += 1


cpu_card1 = functions.give_card()
cpu_card2 = functions.give_card()
player_card1 = functions.give_card()
player_card2 = functions.give_card()

# ----------------------------------------------------------------
# Write Title
st.header(":green[Welcome to Black Jack!]")

# Build Page
functions.build_page(cpu_card1, cpu_card2, player_card1, player_card2)

# Create Buttons
if st.session_state["player_score"] < 22 and st.session_state["stay"] == 0:
    hit_button = st.button(label="Hit", key="bHit", on_click=set_hit, args=())
    stay_button = st.button(label="Stay", key="bStay", on_click=functions.stay, args=())

buttonAgain = st.button(label="Play Again", key="bplayagain", on_click=functions.button_play_again, args=())

