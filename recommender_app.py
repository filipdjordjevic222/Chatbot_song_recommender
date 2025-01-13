#1.import of the libraries
import os
import streamlit as st
import pandas as pd
from functions import search_spotify_tracks, get_recommendations
#import sys
#sys.path.append('./')
#2.load data
def load_data():
    return pd.read_csv('./data/7_clustered_dataset.csv')
data=load_data()

#streamlit app layout
st.set_page_config(page_title="Song Recommender", page_icon="🎵", layout="centered")

# Initialize session state for page management
if 'page' not in st.session_state:
    st.session_state.page = 'page_1'  # Default to first page

#---------- Page 1: Song Search----------------
#searchinterface, 
# stores the song name in session state,
# and reruns the app to update the page

if st.session_state.page == 'page_1':
    #display the title and the description 
    st.title("Song Recommender 🎶")
    st.markdown(
        """
        Welcome to **Song Recommender**, your go-to tool for discovering new favorite songs.
        Search for a song and explore the magic behind the music!
        """
    )
    #create a text input for the song name
    song_name = st.text_input("Enter the name of a song:", placeholder=" ")
    #create a button to search for the song
    search_clicked = st.button("Search")
    
    if search_clicked and song_name:
        st.session_state.song_name = song_name #store the song name in session state
        st.session_state.page = 'page_2' #switch to the next page
        st.rerun()  # Add this to force an immediate rerun(refresh the page)
    elif search_clicked:
        st.error("Please enter a song name")# error message if the song name is not entered

#------ Page 2: Song Selection------
# displays the search results,
# allows the user to select a song,
# and reruns the app to update the page with the selected song

elif st.session_state.page == 'page_2':
    st.title("Select Your Song")
    #search for the song using stored song name
    results = search_spotify_tracks(st.session_state.song_name)
    if results:
        #store the search results in session state
        st.session_state.search_results = results
        st.write(f"Search results for: **{st.session_state.song_name}**")
        #create a dataframe from the search results and drop down for songs
        songs_df = pd.DataFrame(results)
        selected_song = st.selectbox(
            "Choose your song:",
            options=songs_df.apply(lambda x: f"{x['title']} - {x['artist']}", axis=1)
        )
        #navigation buttons in columns
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back to Search"):
                st.session_state.page = 'page_1'
                st.rerun() #refresh the page
        with col2:
            if st.button("Get Recommendations"):
                st.session_state.selected_song = selected_song #store the selected song in session state
                st.session_state.page = 'page_3' #switch to the next page
                st.rerun() #refresh the page
    else:
        st.error("No songs found. Please try another search.")
        if st.button("Back to Search"):
            st.session_state.page = 'page_1'

# ---------Page 3: Recommendations---------
elif st.session_state.page == 'page_3':
    st.title("Recommended Songs")
    st.write(f"Songs similar to: **{st.session_state.selected_song}**")
    
    # Use the stored search results from session state instead of searching again
    if 'search_results' in st.session_state:
        #get the index of the selected song
        selected_song_index = next(
            (i for i, r in enumerate(st.session_state.search_results) 
             if f"{r['title']} - {r['artist']}" == st.session_state.selected_song),
            None
        )
        
        if selected_song_index is not None:
            # Pass both the search results and the selected index
            recommendations = get_recommendations(st.session_state.search_results, selected_song_index)
            #get the recommendations if found
            if recommendations is not None:
                for _, row in recommendations.iterrows():
                    with st.container():
                        #create columns for the image, title, artist, album, genres, and release date
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
                            #create a button to listen to the song on spotify
                            if row['spotify_url']:
                                st.markdown(f"[![Spotify](https://img.shields.io/badge/Listen_on-Spotify-1DB954?style=for-the-badge&logo=spotify&logoColor=white)]({row['spotify_url']})")
            else:
                st.error("Sorry, no recommendations found for this song.")
        else:
            st.error("Error retrieving song details. Please try again.")
    else:
        st.error("Session data lost. Please try searching again.")
        st.session_state.page = 'page_1'

    # Add navigation buttons in columns at the bottom
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Song Selection"):
            st.session_state.page = 'page_2'
            st.rerun()
    with col2:
        if st.button("New Search"):
            # Clear any stored results
            if 'search_results' in st.session_state:
                del st.session_state.search_results
            if 'selected_song' in st.session_state:
                del st.session_state.selected_song
            st.session_state.page = 'page_1'
            st.rerun()