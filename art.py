import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image

lottie_art = requests.get('https://assets4.lottiefiles.com/private_files/lf30_hqhmdw8f.json').json()

def app():
    st_lottie(lottie_art, speed=1, height=200, key="Art")
    st.subheader('GM GM, here are show of my recent artwork!')
    st.markdown("I only do graphic pencil portrait at the moment, nice **_aren't_ they?**")
    image1 = Image.open("https://github.com/Jefflai0315/playingwithpencil/blob/main/assets/images/photo.jpg")
    st.image(image1,caption='Taeyeon',width=600)
    image2= Image.open("https://github.com/Jefflai0315/playingwithpencil/blob/main/assets/images/photo1.jpg")
    st.image(image2,caption='Momo',width=600)
    image3= Image.open("https://github.com/Jefflai0315/playingwithpencil/blob/main/assets/images/photo2.jpg")
    st.image(image3,caption='Dahyun',width=600)