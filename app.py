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


st.set_page_config(page_icon="✏️", page_title="pwp")

lottie_art = requests.get('https://assets4.lottiefiles.com/private_files/lf30_hqhmdw8f.json').json()
lottie_coffee = requests.get('https://assets9.lottiefiles.com/packages/lf20_urr8jb9p.json').json()

def main():
    
    menu = st.sidebar.selectbox('Menu',['Art','Coffee','Secret'])

    



    

    if menu == 'Coffee':
        st_lottie(lottie_coffee, speed=1, height=400, key="Coffee")
        st.subheader('This is where we can talk about coffee!')
        st.markdown('A flow chart of my espresso shot today, it is **_really_ cool**.')
        st.markdown('It is linked to my [firebase](https://console.firebase.google.com/u/0/project/product-design-f47db/database/product-design-f47db-default-rtdb/data)')
        ref = db.reference("/data")
        print(ref)
        my_dict = ref.get()
        coffee_number = list(my_dict.keys())
        coffee_number1 =[]
        print(coffee_number)

        for i in range(len(coffee_number)):
            print(coffee_number[i])
            coffee_number1.append(datetime.utcfromtimestamp(int(coffee_number[i])))

        selected_coffee = st.sidebar.selectbox('Select Coffee',coffee_number1)
        if selected_coffee is not None:
            selected_coffee = int(selected_coffee.replace(tzinfo=timezone.utc).timestamp())
            last_coffee = my_dict[f'{selected_coffee}']
            df = pd.DataFrame(list(last_coffee.items()),columns = ['Time','Weight']) 
            first_time = float(df['Time'][0])
            df['Time'] = df['Time'].apply(lambda x: int(x)-first_time )
            df.set_index('Time', inplace = True)
            ts = int(first_time)
            curr_date=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

            # print(df)
            # st.line_chart(df,use_container_width=True)
            chart = df.reset_index()
            # print(chart)
            c = alt.Chart(chart).mark_line().encode(alt.Y('Weight:Q',scale=alt.Scale(domain=(0, 40),clamp=True)), x='Time')
            st.altair_chart(c, use_container_width=True)

            with st.expander('see my coffee flow rate data'):
                st.write(df)

        
        with st.sidebar.expander('Set your coffee output'):
            ref = db.reference("/")
            coffee_dosage = ref.child('coffee_dosage').get()
            coffee_gram = st.text_input("How much coffee (grams)?",coffee_dosage)
            print(ref.update({"coffee_dosage" : f'{coffee_gram}'}))

            if 'on_state' not in st.session_state:
                on_state = "1"
            else:
                on_state = st.session_state.on_state

            
            # print('on state',on_state)
            _,_,_,col1,col2= st.columns(5)
            col1.markdown('Turn:')
            if col2.button('Off' if on_state == "1" else 'On'):
                if on_state == "1":
                    ref.update({"on_state" : "0"})
                    st.session_state.on_state = "0"
                    # print('if on state is true',st.session_state.on_state)
                    with st.spinner('Turning off...'):
                        time.sleep(0.3)
                        st.experimental_rerun()
                else:
                    ref.update({"on_state" : "1"})
                    st.session_state.on_state = "1"
                    # print('if on state is false',st.session_state.on_state)
                    with st.spinner('Turning on...'):
                        time.sleep(0.3)
                        st.experimental_rerun()
        
        



        
    
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
    
