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

# Add session state management
if 'page' not in st.session_state:
    st.session_state.page = 'page_1'

#---------- Page 1: Song Search----------------
if st.session_state.page == 'page_1':
    st.title("Song Recommender 🎶")
    st.markdown(
        """
        Welcome to **Song Recommender**, your go-to tool for discovering new favorite songs.
        Search for a song and explore the magic behind the music!
        """
    )
    
    song_name = st.text_input("Enter the name of a song:", placeholder=" ")
    if st.button("Search"):
        if song_name:
            st.session_state.song_name = song_name
            st.session_state.page = 'page_2'
        else:
            st.error("Please enter a song name")

#------ Page 2: Song Selection------
elif st.session_state.page == 'page_2':
    st.title("Select Your Song")
    
    results = search_spotify_tracks(st.session_state.song_name)
    if results:
        st.session_state.search_results = results  # Store results in session state
        st.write(f"Search results for: **{st.session_state.song_name}**")
        
        # Create selection for songs
        songs_df = pd.DataFrame(results)
        selected_song = st.selectbox(
            "Choose your song:",
            options=songs_df.apply(lambda x: f"{x['title']} - {x['artist']}", axis=1)
        )
        
        # Navigation buttons in columns
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back to Search"):
                st.session_state.page = 'page_1'
        with col2:
            if st.button("Get Recommendations"):
                st.session_state.selected_song = selected_song
                st.session_state.page = 'page_3'
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
        selected_song_index = next(
            (i for i, r in enumerate(st.session_state.search_results) 
             if f"{r['title']} - {r['artist']}" == st.session_state.selected_song),
            None
        )
        
        if selected_song_index is not None:
            # Pass both the search results and the selected index
            recommendations = get_recommendations(st.session_state.search_results, selected_song_index)
            
            if recommendations is not None:
                for _, row in recommendations.iterrows():
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
    with col2:
        if st.button("New Search"):
            # Clear any stored results
            if 'search_results' in st.session_state:
                del st.session_state.search_results
            if 'selected_song' in st.session_state:
                del st.session_state.selected_song
            st.session_state.page = 'page_1'