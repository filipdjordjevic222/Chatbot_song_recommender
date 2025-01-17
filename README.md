# Music Recommendation Chatbot

## Overview

The ***Music Recommendation Chatbot*** is an intelligent music recommendation system that delivers personalized song suggestions based on user preferences. It leverages the Spotify API, the Million Song Dataset, and Billboard Hot 100 data to provide highly accurate and user-tailored recommendations. With an interactive Streamlit app, users can explore personalized song recommendations and view detailed results in a user-friendly interface.

App starts by user interaction with chatbot, entering a favorite song. Then the app will fetch similar tracks using the Spotify API. Leveraging clustering techniques, it suggests related tracks along with detailed information such as album, artist, genres, and release date, complete with Spotify links for easy listening. Previous recommendations remain visible, ensuring a seamless and engaging discovery experience.

## Presentation

https://www.canva.com/design/DAGcXZHNbTk/Jc7QEMEfB_22wc7jQzTcfQ/edit

## Demo

![Demo](/media/DEMO.gif)

## APP

https://chatbot-song-recommender.streamlit.app/


## Features

- Personalized Recommendations: Suggests songs based on the user’s input, such as favorite tracks or artists.

- Data Integration: Combines Spotify API, Million Song Dataset, and Billboard Hot 100 for enhanced data richness.

- Clustering Techniques: Utilizes KMeans clustering to group similar songs and recommend tracks with precision.

- Interactive App: User-friendly Streamlit interface for exploring recommendations and song details.

- **AI-Powered Chatbot:** A conversational assistant powered by OpenAI helps users discover personalized song recommendations and explore music-related queries.


## Methodology

***Data Sources:***

Million Song Dataset: The core dataset for song analysis and clustering.

Billboard Hot 100: Provides information on popular and trending tracks.

Spotify API: Enriches the dataset with additional song features like tempo, danceability, and more.

***Data Processing:***

Data Cleaning and Merging: Ensures consistency and accuracy by combining and processing multiple datasets.

Feature Enrichment: Fetches additional song attributes via the Spotify API to enhance recommendations.

***Clustering:***

Optimal Clusters:

Evaluation Techniques: The Elbow Method and Silhouette Score were used to determine the optimal number of clusters.

Final Choice: An 11-cluster solution was implemented to balance interpretability and granularity, providing meaningful segmentation for over 9,000 songs.

***Recommendation Engine:***

Cluster-Based Suggestions: Identifies cluster similarities to recommend songs that align with the user’s preferences.   

## Resources

Spotify API https://developer.spotify.com/documentation/web-api

Million Songs Dataset http://millionsongdataset.com

Bliboard hot 100 https://www.billboard.com/charts/hot-100/


## Requirements

Python, Spotify API credentials, OpenAI API credentials, spotipy, Streamlit and other dependancies listed in requirements.txt

## Steps To Run

Clone the repository:

```git clone <repository-url>```
```cd <repository-folder>```

Install required Python packages:

```pip install -r requirements.txt```

Update .env file with your Spotify API credentials:

```SPOTIFY_CLIENT_ID=<your-client-id>```

```SPOTIFY_CLIENT_SECRET=<your-client-secret>```

```OPENAI_API_KEY=<your-openai-api-key>```

You can get these credentials from the Spotify Developer Platform.
You can get your OpenAI API key from https://platform.openai.com/

Start the application:

```streamlit run app.py```

## Further Development

- Add more features to the chatbot (voice to text search)
- Add more data sources
- Improve clustering for higher accuracy
- Improve recommendation engine to add mood and genre
- Add more user data storage mechanisms

