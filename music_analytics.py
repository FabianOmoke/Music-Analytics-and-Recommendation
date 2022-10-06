import streamlit as st

search_options = ['Track', 'Artist', 'Album' ]
st.sidebar.selectbox('Your Search Choice Please', search_options)
st.header('Music Analytics App')