import streamlit as st

st.header('Music Analytics App') 
search_options = ['Track', 'Artist', 'Album' ]
search_selection = st.sidebar.selectbox('Your Search Choice Please', search_options)

st.text_input(search_selection + "[Keyword Search]")
Search_button = st.button("Search")

