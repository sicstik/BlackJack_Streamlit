import streamlit as st
import pandas
import random

st.set_page_config(layout="centered")
card_df = pandas.read_csv("csv/cards.csv")
card_file_path = "Images/Cards/"

IMAGE_WIDTH = 75


def check_playing():
    if "playing" in st.session_state:
        return st.session_state["playing"]
    else:
        if "playing" not in st.session_state:
            st.session_state["playing"] = 0
            return 0


def initialize_sessions():
    string_of_sessions = ["cpu_score", "cpu_card1", "cpu_card2",
                          "player_score", "player_card1", "player_card2", "playing", "stay",
                          "hit", "hit_cards"]
    for session in string_of_sessions:
        if session not in st.session_state:
            if session == "hit_cards":
                st.session_state[session] = []
            else:
                st.session_state[session] = 0


def delete_sessions():
    string_of_sessions = ["cpu_score", "cpu_card1", "cpu_card2",
                          "player_score", "player_card1", "player_card2", "playing", "stay",
                          "hit", "hit_cards"]
    for session in string_of_sessions:
        del st.session_state[session]


def write_score_out():
    if st.session_state["stay"] < 1 and st.session_state["player_score"] < 22:
        st.write(f":green[Your Score = {int(st.session_state["player_score"])}]")
        st.write(f":blue[CPU Score = {int(st.session_state["cpu_card1"]["value"])}]")
    elif st.session_state["player_score"] >= 22:
        st.write(f":green[Your Score = {int(st.session_state["player_score"])}]")
        st.write(f":blue[CPU Score = {int(st.session_state["cpu_card1"]["value"])}]")
    else:
        st.write(f":green[Your Score = {int(st.session_state["player_score"])}]")
        st.write(f":blue[CPU Score = {int(st.session_state["cpu_score"])}]")


def button_play_again():
    delete_sessions()
    initialize_sessions()
    # st.experimental_rerun()


def give_card():
    # Get 2 Cards
    first_card_number = random.randrange(start=0, stop=51)
    second_card_number = random.randrange(start=0, stop=51)

    first_card_df = card_df.iloc[first_card_number]
    second_card_df = card_df.iloc[second_card_number]
    return first_card_df


def hit_cards():
    if "hit_cards" not in st.session_state:
        st.session_state["hit_cards"] = []
        return st.session_state["hit_cards"]
    else:
        return st.session_state["hit"]


def check_hit_lose():
    if st.session_state["player_score"] >= 22:
        st.title(":red[You Lose!!]")


def cpu_check_ace(cpu_first_card, cpu_second_card):
    if cpu_first_card["value"] == 1:
        cpu_first_card["value"] = 11

    if st.session_state["playing"] == 0:
        if cpu_second_card["value"] == 1:
            if cpu_first_card["value"] + 11 < 22:
                cpu_second_card["value"] = 11
            else:
                cpu_second_card["value"] = 1
    else:
        if cpu_second_card["value"] == 1:
            if st.session_state["cpu_score"] + 11 < 22:
                cpu_second_card["value"] = 11
            else:
                cpu_second_card["value"] = 1


def player_check_ace(player_first_card, player_second_card):
    if player_first_card["value"] == 1:
        player_first_card["value"] = 11

    if st.session_state["playing"] == 0:
        if player_second_card["value"] == 1:
            if player_first_card["value"] + 11 < 22:
                player_second_card["value"] = 11
            else:
                player_second_card["value"] = 1
    else:
        if player_second_card["value"] == 1:
            if st.session_state["player_score"] + 11 < 22:
                player_second_card["value"] = 11
            else:
                player_second_card["value"] = 1


def hit():
    if "hit" not in st.session_state:
        st.session_state["hit"] = 1
        check_hit_lose()
        return st.session_state["hit"]
    else:
        check_hit_lose()
        return st.session_state["hit"]


def stay():
    st.session_state["stay"] = 1


def build_page(cpu_first_card, cpu_second_card, player_first_card, player_second_card):

    global cpu_first_score
    initialize_sessions()

    # CPU Setup
    # -------------------------------------------------------------------
    st.subheader("CPU")
    if st.session_state["playing"] == 0:
        col1, col2 = st.columns(2)
        with col1:
            card1 = f"{card_file_path}{cpu_first_card["cards"]}"
            st.image(image=card1, width=IMAGE_WIDTH)

        with col2:
            card2 = f"{card_file_path}red_back.png"
            st.image(image=card2, width=IMAGE_WIDTH)

        cpu_check_ace(cpu_first_card, cpu_second_card)
        cpu_score = cpu_first_card["value"] + cpu_second_card["value"]
        cpu_first_score = cpu_first_card["value"]
        st.write(cpu_first_score)
        st.session_state["cpu_card1"] = cpu_first_card
        st.session_state["cpu_card2"] = cpu_second_card
        st.session_state["cpu_score"] = cpu_score

    elif st.session_state["hit"] > 0 and st.session_state["stay"] < 1:
        col1, col2 = st.columns(2)
        with col1:
            card1 = f"{card_file_path}{st.session_state["cpu_card1"]["cards"]}"
            st.image(image=card1, width=IMAGE_WIDTH)

        with col2:
            card2 = f"{card_file_path}red_back.png"
            st.image(image=card2, width=IMAGE_WIDTH)

        # cpu_score = cpu_first_card["value"] + cpu_second_card["value"]
        cpu_first_score = st.session_state["cpu_card1"]["value"]
        st.write(cpu_first_score)

    else:
        count_card_list = -1
        card_list = []
        col1, col2 = st.columns(2)
        # Get first 2 saved cards
        with col1:
            card1 = f"{card_file_path}{st.session_state["cpu_card1"]["cards"]}"
            st.image(image=card1, width=IMAGE_WIDTH)

        with col2:
            card2 = f"{card_file_path}{st.session_state["cpu_card2"]["cards"]}"
            st.image(image=card2, width=IMAGE_WIDTH)

        st.session_state["cpu_score"] = st.session_state["cpu_card1"]["value"] + st.session_state["cpu_card2"]["value"]
        st.write(int(st.session_state["cpu_score"]))
        # Add new cards until 17 is reached
        while st.session_state["cpu_score"] < 17:
            new_card = give_card()
            cpu_check_ace(cpu_first_card, new_card)
            st.session_state["cpu_score"] += new_card["value"]
            card_list.append(new_card["cards"])
            count_card_list += 1
            card = f"{card_file_path}{new_card["cards"]}"
            st.image(image=card, width=IMAGE_WIDTH)
            st.info(f"CPU new score = {int(st.session_state["cpu_score"])}")

    # Player Setup
    # --------------------------------------------------------------------------------
    st.subheader("Player")
    if check_playing() == 0:
        col1, col2 = st.columns(2)
        with col1:
            card1 = f"{card_file_path}{player_first_card["cards"]}"
            st.image(image=card1, width=IMAGE_WIDTH)

        with col2:
            card2 = f"{card_file_path}{player_second_card["cards"]}"
            st.image(image=card2, width=IMAGE_WIDTH)

        player_check_ace(player_first_card, player_second_card)
        player_score = player_first_card["value"] + player_second_card["value"]

        st.write(player_score)
        st.session_state["player_score"] = player_score
        st.session_state["player_card1"] = player_first_card
        st.session_state["player_card2"] = player_second_card

    elif st.session_state["hit"] > 0 and st.session_state["stay"] < 1:
        player_card_list = []
        col1, col2 = st.columns(2)
        with col1:
            card1 = f"{card_file_path}{st.session_state["player_card1"]["cards"]}"
            st.image(image=card1, width=IMAGE_WIDTH)

        with col2:
            card2 = f"{card_file_path}{st.session_state["player_card2"]["cards"]}"
            st.image(image=card2, width=IMAGE_WIDTH)

        # Add new cards for each time hit occurs
        new_card = give_card()
        player_check_ace(player_first_card, new_card)
        st.session_state["player_score"] += new_card["value"]
        player_score = st.session_state["player_score"]
        hit_cards()
        player_card_list = st.session_state["hit_cards"]
        player_card_list.append(new_card)
        st.session_state["hit_cards"] = player_card_list

        for cards in player_card_list:
            card = f"{card_file_path}{cards["cards"]}"
            st.image(image=card, width=IMAGE_WIDTH)
        st.session_state["player_score"] = player_score
        write_score_out()
        check_hit_lose()

    else:
        player_check_ace(st.session_state["player_card1"], st.session_state["player_card2"])
        col1, col2 = st.columns(2)
        with col1:
            card1 = f"{card_file_path}{st.session_state["player_card1"]["cards"]}"
            st.image(image=card1, width=IMAGE_WIDTH)

        with col2:
            card2 = f"{card_file_path}{st.session_state["player_card2"]["cards"]}"
            st.image(image=card2, width=IMAGE_WIDTH)

        hit_cards()
        player_card_list = st.session_state["hit_cards"]
        if len(player_card_list) > 0:
            for cards in player_card_list:
                card = f"{card_file_path}{cards["cards"]}"
                st.image(image=card, width=IMAGE_WIDTH)
        player_score = st.session_state["player_score"]
        write_score_out()

    st.session_state["playing"] += 1
    check_win()


def stay_rebuild_page():
    times_rebuilt = st.session_state["playing"]
    # first_build_page()


def check_win():
    if st.session_state["stay"] > 0:
        if st.session_state["player_score"] < st.session_state["cpu_score"] < 22:
            st.subheader(":red[You Lose!]")
        elif st.session_state["player_score"] == st.session_state["cpu_score"]:
            st.subheader("TIE!")
        else:
            st.subheader(":green[You Win!]")
    else:
        st.write("")
