import streamlit as st
import requests
from streamlit_lottie import st_lottie
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import pandas as pd
from datetime import datetime


st.set_page_config(page_icon="✏️", page_title="pwp")

lottie_art = requests.get('https://assets4.lottiefiles.com/private_files/lf30_hqhmdw8f.json').json()
lottie_coffee = requests.get('https://assets9.lottiefiles.com/packages/lf20_urr8jb9p.json').json()

def main():
    
    menu = st.sidebar.selectbox('Menu',['Art','Coffee'])


    

    if menu == 'Coffee':
        st_lottie(lottie_coffee, speed=1, height=400, key="Coffee")
        st.title('This is where we can talk about coffee!')
        st.header('For Coffee lovers')
        st.markdown('This is my espresson shot flow today, it is **_really_ cool**.')
        ref = db.reference("/")
        print(ref)
        my_dict = ref.get()
        coffee_number = list(my_dict.keys())
        selected_coffee = st.selectbox('Select Coffee',coffee_number)
        last_coffee = my_dict[f'{selected_coffee}']
        df = pd.DataFrame(list(last_coffee.items()),columns = ['Time','Weight']) 
        first_time = int(df['Time'][0])
        df['Time'] = df['Time'].apply(lambda x: int(x)-first_time )
        df.set_index('Time', inplace = True)
        ts = int(first_time)
        curr_date=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        

        st.line_chart(df)


        with st.expander('see my coffee flow rate data'):
            st.write(df)
    
    if menu == 'Art':
        st_lottie(lottie_art, speed=1, height=200, key="Art")
        pass

        

   


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
    