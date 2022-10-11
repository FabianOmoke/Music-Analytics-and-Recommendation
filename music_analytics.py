from operator import index
import streamlit as st
import pandas as pd
import feature_plot
import track_recommendations

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

search_results = []
tracks = []
albums =[]
artists = []
if search_input is not None and len (search_input)> 0:
    if search_selection == "Track":
        st.write("Results for '" + search_input + "'")
        tracks = sp.search(q='track:'+search_input,type='track', limit=10)
        tracks_list = tracks['tracks']['items']
        if len(tracks_list)> 0:
            st.write("\n" + "__" * 10)
            for track in tracks_list:
                search_results.append( track['name'] + "- By - " + track['artists'][0]['name'])


    elif search_selection == 'Artist':

        st.write("Results for '" + search_input + "'")
        artists = sp.search(q='artist:'+ search_input,type='artist', limit=10)
        artist_list = artists['artists']['items']
        if len(artist_list)> 0:
            for artist in artist_list:
                search_results.append(artist['name'])
               

    elif search_selection == 'Album':
        st.write("Results for '" + search_input + "'")
        albums = sp.search(q='album:'+search_input,type='album', limit=20)
        album_list = albums['albums']['items']
        if len(album_list)> 0:
            for album in album_list:
              search_results.append(album['name'] + "- By - " + album['artists'][0]['name'])
         
selected_artist = None
selected_track = None
selected_album = None

if search_selection == "Track":
   selected_track = st.selectbox("select your song/track", search_results)
elif search_selection == 'Artist':
   selected_artist = st.selectbox("select  Artist", search_results)
elif search_selection == 'Album':
    selected_album = st.selectbox("select  Album", search_results)

if selected_track is not None and len(tracks) > 0:
    tracks_list = tracks['tracks']['items']
    track_id = None
    if len(tracks_list)> 0:
        for track in tracks_list:
            str_temp =  track['name'] + "- By - " + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
                track_album = track['album']['name']
                album_art = track['album']['images'][1]['url']
                track_recommendations.get_album_art(album_art, track_id)

    if track_id is not None:
        album_art = track_recommendations.show_album_art(track_id)
        st.image(album_art)
        track_choices = ["View song features", "View Similar Songs Recommendation"]
        selected_track_choices = st.sidebar.selectbox("Please select Action", track_choices)
        if selected_track_choices == track_choices[0]:
            track_features = sp.audio_features(track_id)
            df = pd.DataFrame(track_features, index=[0])
            select_features =  df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
            feature_plot.plot_features(select_features)
        elif selected_track_choices == track_choices[1]:
            token = track_recommendations.request_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
            song_recommendations_json = track_recommendations.get_track_recommendations(track_id, token)
            recommendation_list = song_recommendations_json['tracks']
            recommendation_df = pd.DataFrame(recommendation_list)
            song_recommendations_short = recommendation_df[['name', 'explicit', 'duration_ms', 'popularity']]
            st.dataframe(song_recommendations_short)
            track_recommendations.visualize_recommendations(song_recommendations_short)

    else:
        st.write("Please get a track from the list")
        
elif selected_album is not None and len(albums) > 0:
    album_list = albums['albums']['items']
    album_id = None
    album_url = None

    if len(album_list) > 0:
        for album in album_list:
            str_temp = album['name'] + "- By - " + album['artists'][0]['name']
            if selected_album == str_temp:
                album_id = album['id']
                album_url = album['uri']
                album_name = album ['name']

    if album_id is not None and album_url is not None:
        st.write("Songs in " + album_name)
        album_tracks = sp.album_tracks(album_id)
        df_album_tracks = pd.DataFrame(album_tracks['items'])
        df_album_short = df_album_tracks.loc[:, ["id", "name", "duration_ms", "explicit", "preview_url"]]

        for idx in df_album_short.index:
                col_1, col_2, col_3, col_4  = st.columns((4,4, 1,1 ))
                col_11, col_12 = st.columns((8, 2))
                col_1.write(df_album_short['id'][idx])
                col_2.write(df_album_short['name'][idx])
                col_3.write(df_album_short['duration_ms'][idx])
                col_4.write(df_album_short['explicit'][idx])
                if df_album_short['preview_url'][idx] is not None:
                    col_11.write(df_album_short['preview_url'][idx])
                    with col_12:
                        st.audio( df_album_short['preview_url'][idx], format="audio/mp3")

elif selected_artist is not None and len(artists) > 0:
        artist_list = artists['artists']['items']
        artist_id = None
        artist_uri = None
        if len(artist_list)> 0:
            for artist in artist_list:
                if selected_artist == artist['name']:
                    artist_id = artist['id']
                    artist_uri = artist['uri']
        if artist_id is not None:
            artist_choice = ["Albums", "Top Songs"]
            selected_artist_action = st.sidebar.selectbox("Please Select Action", artist_choice)
        
        if selected_artist_action is not None:
            if selected_artist_action == artist_choice[0]:
                artist_uri = 'spotify:artist:' + artist_id
                album_results = sp.artist_albums(artist_uri, album_type='album')
                all_albums = album_results['items']
                st.write(all_albums[0]['name'])
                for album in all_albums:
                    with st.container():
                        col1, col2, col3 = st.columns((6,4,2))
                        col1.write(album['name'])
                        col2.write(album['release_date'])
                        col3.write(album['total_tracks'])
            elif selected_artist_action == artist_choice[1]:
                artist_uri = 'spotify:artist:' + artist_id
                top_song_results = sp.artist_top_tracks(artist_uri)
                for track in top_song_results['tracks']:
                    with st.container():
                        col_1, col_2, col_3, col_4  = st.columns((4,4,2,2 ))
                        col_11, col_12 = st.columns((8, 2))
                        col21, col22 = st.columns =((6,6))
                        col31, col32 = st.columns((11,1))

                        col_1.write(track['id'])
                        col_2.write(track['name'])
                        #col_3.write(track['duration_ms'])
                        #col_4.write(track['popularity'])
                        if track['preview_url'] is not None:
                            col_11.write(track['preview_url'])
                            with col_12:
                                st.audio(track['preview_url'], format="audio/mp3")
                        with col_3:
                            def feature_requested():
                                track_features = sp.audio_features(track_id)
                                df = pd.DataFrame(track_features, index=[0])
                                select_features =  df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                                with col31:
                                     st.dataframe(select_features)
                                with col32:
                                    feature_plot.plot_features(select_features)

                            feature_button_state = st.button('Track audio features', key=track['id'], on_click = feature_requested)
                        with col_4:
                            def similar_songs_requested():
                                token = track_recommendations.request_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
                                song_recommendations_json = track_recommendations.get_track_recommendations(track_id, token)
                                recommendation_list = song_recommendations_json['tracks']
                                recommendation_df = pd.DataFrame(recommendation_list)
                                song_recommendations_short = recommendation_df[['name', 'explicit', 'duration_ms', 'popularity']]
                                with col21:
                                    st.dataframe(song_recommendations_short)
                                with col22:
                                    track_recommendations.visualize_recommendations(song_recommendations_short) 

                            similar_button_state = st.button('Similar Songs', key=track['id'], on_click = similar_songs_requested)











