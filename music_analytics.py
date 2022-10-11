import streamlit as st

# Spotify Initialization
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY_CLIENT_ID = '2ec294682f3d4d53a0b933dc486bd294'
SPOTIFY_CLIENT_SECRET = '4c3845c0b99442239e636930b6410122'
# SPOTIFY_REDIRECT_URI = ''
auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)
sp.me 

st.header('Music Analytics App') 
search_options = ['Track', 'Artist', 'Album' ]
search_selection = st.sidebar.selectbox('Your Search Choice Please', search_options)

search_input = st.text_input(search_selection + " [Keyword Search] ")
Search_button = st.button("Search")

if search_input is not None and len (search_input)> 0:
    if search_selection == "Track":
        st.write("Search for Track")
        tracks = sp.search(q='track:'+search_input,type='track', limit=10)
        tracks_list = tracks['tracks']['items']
        if len(tracks_list)> 0:
            for track in tracks_list:
                st.write(track['name'] + "- By - " + track['artists'][0]['name'])


    elif search_selection == 'Artist':

        st.write("Search for Artist")
        artist = sp.search(q='artist:'+ search_input,type='artist', limit=10)
        artist_list = artist['artist']['items']
        if len(artist_list)> 0:
            for artist in artist_list:
                st.write(artist['name'] + "- By - " + artist['artists'][0]['name'])
               

    elif search_selection == 'Album':
        st.write("Search for Album")
        albums = sp.search(q='album:'+search_input,type='album', limit=20)
        album_list = albums['albums']['items']
        if len(album_list)> 0:
            for album in album_list:
                st.write(album['name'] + "- By - " + album['artists'][0]['name'])
                #print('Track ID:' + album['id'] + " / Artist ID -" + album['artists'][0]['id'])
         


