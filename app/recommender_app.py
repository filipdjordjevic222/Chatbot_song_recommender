import streamlit as st
import pandas as pd
from functions import search_spotify_tracks, get_recommendations
#load data
def load_data():
    return pd.read_csv('../data/7_clustered_dataset.csv')
data=load_data()

#function to recommend songs
def recommend_songs(song_name, data):

    if song_name == "":
        st.write("Please enter a song name")
        return

    #search for the song on spotify
    results = search_spotify_tracks(song_name)
    if results:
        st.write(f"Title: {results[0]['title']}, Artist: {results[0]['artist']}")
    else:
        st.write(f"No results found for **{song_name}**")
        return


    #get recommendations
    recommendations = get_recommendations(results)
    return recommendations

#streamlit app layout
st.set_page_config(page_title="Song Recommender", page_icon="🎵", layout="centered")

st.title("Song Recommender 🎶")

st.markdown(
    """
    Welcome to **Song Recommender**, your go-to tool for discovering new favorite songs.
    Search for a song and explore the magic behind the music!
    """
)

# User Input for song name
song_name = st.text_input("Enter the name of a song:", placeholder=" ")

#search results for the song
if st.button("Find Recommendations"):
    if song_name:
        st.write(f"Songs similar to: **{song_name}**")
        recommendations = recommend_songs(song_name, data)
        st.subheader("Recommended Songs:")
        for _, row in recommendations.iterrows():
            st.markdown(
                f"Title: {row['original_title']}  \n"
                f"Artist: {row['original_artist']}  \n"
                f"Album: {row['album']}  \n"
                f"Genres: {row['genres']}  \n"
                f"Release Date: {row['release_date']}"
            )
            st.image(row['album_cover'], width=100)



