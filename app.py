import streamlit as st
import requests
from streamlit_lottie import st_lottie


st.set_page_config(page_icon="✏️", page_title="pwp")

lottie_book = requests.get('https://assets4.lottiefiles.com/private_files/lf30_hqhmdw8f.json').json()
st_lottie(lottie_book, speed=1, height=200, key="initial")
