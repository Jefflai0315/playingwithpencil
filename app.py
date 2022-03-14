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
import coffee_flow_rate_doc
import coffee
import art
import coffee_flow_rate_doc
# import TeachableMachine as tm



st.set_page_config(page_icon="✏️", page_title="pwp")

# model, live, data, size = tm.init_face_reg()

def main():
    
    menu = st.sidebar.selectbox('Menu',['Art','Coffee','Secret'])
    

    if menu == 'Coffee':
        
        coffee.app()
        if st.button("show documentation", key="coffeeDoc"):
            with st.container():
                coffee_flow_rate_doc.app('style.css')
            
    

    

        
    
    if menu == 'Art':
        art.app()
    

    if menu == 'Secret':
        pass
    

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
    
