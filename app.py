# from tkinter import Image
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import pandas as pd
from datetime import datetime, timezone
import altair as alt
import time
from PIL import Image
import app1
import coffee
# import TeachableMachine as tm


PAGES = {
    "App1": app1,
}


st.set_page_config(page_icon="✏️", page_title="pwp")

lottie_art = requests.get('https://assets4.lottiefiles.com/private_files/lf30_hqhmdw8f.json').json()
lottie_coffee = requests.get('https://assets9.lottiefiles.com/packages/lf20_urr8jb9p.json').json()
# model, live, data, size = tm.init_face_reg()

def main():
    
    menu = st.sidebar.selectbox('Menu',['Art','Coffee','Secret'])
    

    if menu == 'Coffee':
        coffee.app()
        
        

    
                    
        
        



        
    
    #     line_chart = alt.Chart(df).mark_line().encode(x='Year',
    # y='mean(Miles_per_Gallon)')
    #     st.altair_chart(line_chart)

    
    if menu == 'Art':
        
        st_lottie(lottie_art, speed=1, height=200, key="Art")
        st.subheader('GM GM, here are show of my recent artwork!')
        st.markdown("I only do graphic pencil portrait at the moment, nice **_aren't_ they?**")
        image1 = Image.open("https://github.com/Jefflai0315/playingwithpencil/blob/main/assets/images/photo.jpg")
        st.image(image1,caption='Taeyeon',width=600)
        image2= Image.open("https://github.com/Jefflai0315/playingwithpencil/blob/main/assets/images/photo1.jpg")
        st.image(image2,caption='Momo',width=600)
        image3= Image.open("https://github.com/Jefflai0315/playingwithpencil/blob/main/assets/images/photo2.jpg")
        st.image(image3,caption='Dahyun',width=600)

    if menu == 'Secret':
        result = tm.capture_face()
        if result == True:
            st.title('Hello jeff')
    
    

        

   


# str(datetime.timedelta(seconds=duration))
    
    
    

if __name__ == "__main__":
    if not firebase_admin._apps:
        #  # For LOCAL
        cred = credentials.Certificate('cred.json')
        default_app = firebase_admin.initialize_app(cred, {
            'databaseURL':"https://product-design-f47db-default-rtdb.asia-southeast1.firebasedatabase.app" 
        })

        # For PROD
        # default_app = firebase_admin.initialize_app(
        # credentials.Certificate({
        # "type": "service_account",
        # "project_id": "product-design-f47db",
        # "private_key": os.environ.get('private_key').replace('\\n', '\n'),
        # "client_email": os.environ["client_email"],
        # "token_uri": "https://oauth2.googleapis.com/token",
        # }), 
        # {
        # 'databaseURL':"https://product-design-f47db-default-rtdb.asia-southeast1.firebasedatabase.app" 
        # })
    main()
    
