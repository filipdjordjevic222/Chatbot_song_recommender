import os
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pickle
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

# Debug: Print current directory
print(f"Current working directory: {os.getcwd()}")

try:
    # Initialize Spotify client with secrets
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=st.secrets["SPOTIFY_CLIENT_ID"],
            client_secret=st.secrets["SPOTIFY_CLIENT_SECRET"]
        )
    )
except Exception as e:
    st.error(f"""
    Failed to initialize Spotify client. 
    Error: {str(e)}
    Working directory: {os.getcwd()}
    """)
    raise

def search_spotify_tracks(query, limit=10):
    """
    Search for tracks on Spotify and return formatted results
    
    Parameters:
    query (str): Search query for the track
    limit (int): Maximum number of results to return
    
    Returns:
    list: List of dictionaries containing track information
    """
    results = spotify.search(q=query, type='track', limit=limit)
    
    tracks = []
    for track in results['tracks']['items']:
        track_info = {
            'title': track['name'],
            'artist': track['artists'][0]['name'],
            'artist_id': track['artists'][0]['id'],
            'duration_ms': track['duration_ms'],
            'explicit': track['explicit'],
            'album': track['album']['name'],
            'album_cover': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'preview_url': track['preview_url'],
            'popularity': track['popularity'],
            'id': track['id'],
            'release_year': track['album']['release_date'][:4]
        }
        tracks.append(track_info)
    
    return tracks


#create a function to get necessary columns
def get_recommendations(search_results, user_selection_index):
    user_selection_track_data = search_results[user_selection_index]

    #get genre from artist id
    results=spotify.artist(user_selection_track_data['artist_id']) 

    genres=results['genres']


    selection_data = {
        'popularity': user_selection_track_data['popularity'],
        'duration_ms': user_selection_track_data['duration_ms'],
        'explicit': user_selection_track_data['explicit'],
        'pop': 1 if 'pop' in genres else 0,
        'old school hip hop': 1 if 'old school hip hop' in genres else 0,
        'rap': 1 if 'rap' in genres else 0,
        'rock': 1 if 'rock' in genres else 0,
        'hard rock': 1 if 'hard rock' in genres else 0,
        'release_year': user_selection_track_data['release_year']
    }

    selection_data_df = pd.DataFrame([selection_data])

    # Load the scaler
    scaler = pickle.load(open('./scaler/standard_scaler.pkl', 'rb'))

    # Scale the data
    selection_data_scaled = scaler.transform(selection_data_df)

    selection_data_scaled_df = pd.DataFrame(selection_data_scaled, columns=selection_data_df.columns)

    # Load model and predict
    model = pickle.load(open('./models/kmeans_model_11.pkl', 'rb'))

    cluster_prediction = model.predict(selection_data_scaled_df)


    # Load the clustered dataset and filter for the cluster
    clustered_df = pd.read_csv('./data/7_clustered_dataset.csv')
    clustered_df_filtered = clustered_df[clustered_df['cluster'] == cluster_prediction[0]]

    # Get the top 10 most popular songs from the same cluster
    top_10_songs = clustered_df_filtered.sort_values(by='popularity', ascending=False).sample(10)
    
    # Add Spotify URLs for each recommended song
    def get_spotify_url(row):
        # Search for the exact song by artist and title
        query = f"artist:{row['original_artist']} track:{row['original_title']}"
        results = spotify.search(q=query, type='track', limit=1)
        
        if results['tracks']['items']:
            return f"https://open.spotify.com/track/{results['tracks']['items'][0]['id']}"
        return None

    top_10_songs['spotify_url'] = top_10_songs.apply(get_spotify_url, axis=1)
    
    return top_10_songs

