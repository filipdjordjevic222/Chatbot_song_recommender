# import libraries
import openai
from openai import OpenAI
import streamlit as st
import os
import pandas as pd
from functions import search_spotify_tracks, get_recommendations
from tools import get_tools, parse_tool_call

openai_api_key = st.secrets["OPENAI_API_KEY"]

#streamlit app layout
st.set_page_config(page_title="Music Recommendation Chatbot", page_icon="🎵", layout="centered")

st.title("🎵 Music Recommendation Chatbot ")
st.markdown(
        """
        Welcome to **Music Recommendation Chatbot**, your go-to tool for discovering new favorite songs.
        Search for a song and explore the magic behind the music!
        """
    )

SYSTEM_PROMPT = """
You are a music expert assistant. Provide informative and engaging responses about music-related topics only
If the user asks about anything unrelated to music, politely decline and ask them to ask about music-related topics only.
"""

placeholder = st.container()

# Add a refresh button to restart the session at the bottom
if st.button("Refresh"):
    # Add a refresh button to restart the session at the bottom
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello! I'm your music recommendation assistant. I can help you discover new songs based on your favorites. Would you like to find some music recommendations? Just tell me a song you like!"}
    ]
    st.session_state["search_results"] = None
    # clear the placeholder
    placeholder.empty()

# Initialize session state
if "messages" not in st.session_state or st.session_state["messages"] == []:
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hello! I'm your music recommendation assistant. I can help you discover new songs based on your favorites. Would you like to find some music recommendations? Just tell me a song you like!"}
    ]
# Initialize session states for song recommendation flow
if "search_results" not in st.session_state or st.session_state["search_results"] is None:
    st.session_state["search_results"] = None

# Display the chat history inside the placeholder container
with placeholder:
    for msg in st.session_state["messages"][1:]:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI()
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    messages = st.session_state["messages"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=get_tools()
    )

    message, recommendations = parse_tool_call(response.choices[0].message)

    st.session_state["messages"].append({"role": "assistant", "content": message})
    st.chat_message("assistant").write(message)

    if recommendations is not None:
        # Loop thorugh dataframe and display each row
        #st.dataframe(recommendations)
        for index, row in recommendations.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                         st.image(row['album_cover'], width=100)
                with col2:
                         st.markdown(
                             f"**{row['original_title']}**  \n"
                             f"Artist: {row['original_artist']}  \n"
                             f"Album: {row['album']}  \n"
                             f"Genres: {row['genres']}  \n"
                             f"Release Date: {row['release_date']}"
                         )
                with col3:
                         if row['spotify_url']:
                             st.markdown(f"[![Spotify](https://img.shields.io/badge/Listen_on-Spotify-1DB954?style=for-the-badge&logo=spotify&logoColor=white)]({row['spotify_url']})")


