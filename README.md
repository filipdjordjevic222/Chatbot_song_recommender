# Song Recommender

## Overview

The Song Recommender is an intelligent music recommendation system designed to deliver personalized song suggestions based on user preferences. Based on the Spotify API, Million Song Dataset and Bilboard Hot 100 to provide user personalaised recommendations. It integrates the Spotify API and the Million Song Dataset, utilizing clustering techniques to group similar songs and suggest tracks based on user preferences.

## Demo

![Demo](/app/Demo.gif)



## Methodology

The Song Recommender combines Billboard Hot 100 data and the Million Song Dataset, cleans and merges the datasets for consistency and accuracy, and enriches them with additional song features fetched via the Spotify API. Using clustering techniques, the project determines optimal song groups with KMeans, selecting 11 clusters based on evaluation metrics. The recommendation system suggests songs by identifying cluster similarities, with an optional filter for popular tracks. Finally, an interactive Streamlit app allows users to explore personalized song recommendations and view detailed results in a user-friendly interface.

Dataset: 

The Million Song Dataset provides the core data for song analysis and clustering.

Clustering:

The Elbow Method and Silhouette Score were used to evaluate and choose the optimal number of clusters.

The KMeans algorithm was applied with 11 clusters for song recommendation.


![Elbow-silhouette](/app/clustering.png)    

## Resources

Spotify API https://developer.spotify.com/documentation/web-api

Million Songs Dataset http://millionsongdataset.com

Bliboard hot 100 https://www.billboard.com/charts/hot-100/


## Requirements

Python, Spotify API credentials, spotipy, Streamlit and other dependancies listed in requirements.txt

## Steps To Run

Clone the repository:

```git clone <repository-url>```
```cd <repository-folder>```

Install required Python packages:

```pip install -r requirements.txt```

Update .env file with your Spotify API credentials:

```SPOTIFY_CLIENT_ID=<your-client-id>```

```SPOTIFY_CLIENT_SECRET=<your-client-secret>```

You can get these credentials from the Spotify Developer Platform.

Start the application:

```streamlit run app.py```


