import requests 
import base64
import seaborn as sns
import numpy as np
import streamlit as st 
import matplotlib.pyplot as plt
from PIL import Image



def request_token(clientId,clientSecret):
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}
    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')
    headers['Authorization'] = "Basic " + base64Message
    data['grant_type'] = "client_credentials"
    r = requests.post(url, headers=headers, data=data)
    token = r.json()['access_token']
    return token


def get_track_recommendations(seed_tracks,token):
    limit = 10
    recomendation_Url = f"https://api.spotify.com/v1/recommendations?limit={limit}&seed_tracks={seed_tracks}"

    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=recomendation_Url, headers=headers)
    return res.json()

def visualize_recommendations(song_df):
    plt.figure(figsize=(15, 6), facecolor=(.9, .9, .9))  
    song_df['duration_min'] = round(song_df['duration_ms'] / 1000, 0)
    song_df["popularity_range"] = song_df["popularity"] - (song_df['popularity'].min() - 1)


    x = song_df['name']
    y = song_df['duration_min']
    s = song_df['popularity_range']*20
        
    color_labels = song_df['explicit'].unique()
    rgb_values = sns.color_palette("Set1", 8)
    color_map = dict(zip(color_labels, rgb_values))

    plt.scatter(x, y, s, alpha=0.7, c=song_df['explicit'].map(color_map))
    plt.xticks(rotation=90)
    plt.legend()
    # show the graph
    plt.show()

    st.pyplot(plt)

def get_album_art(art_url, track_id):
    r = requests.get(art_url)
    open('album_images/' + track_id + '.jpg', 'wb').write(r.content)

def show_album_art(track_id):
    return Image.open('album_images/' + track_id + '.jpg')