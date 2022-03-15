
import streamlit as st
import requests
from streamlit_lottie import st_lottie
from firebase_admin import db
import pandas as pd
from datetime import datetime, timezone
import altair as alt
import time
from streamlit_autorefresh import st_autorefresh


lottie_coffee = requests.get('https://assets9.lottiefiles.com/packages/lf20_urr8jb9p.json').json()    
    
def app():    
    st_lottie(lottie_coffee, speed=1, height=400, key="Coffee")
    st.subheader('This is where we can talk about coffee!')
    st.markdown('A line chart of my espresso pull today, it is **_really_ cool**.')
    ref = db.reference("/data")
    my_dict = ref.get()
    coffee_number = list(my_dict.keys())
    coffee_number_last5 =[]

    for i in range(len(coffee_number)):
        if i >len(coffee_number)-5:
            coffee_number_last5.append(datetime.utcfromtimestamp(int(coffee_number[i])))

    

    selected_coffee = st.sidebar.selectbox('Select Coffee',coffee_number_last5)
    if selected_coffee is not None:
        selected_coffee = int(selected_coffee.replace(tzinfo=timezone.utc).timestamp())
        last_coffee = my_dict[f'{selected_coffee}']
        df = pd.DataFrame(list(last_coffee.items()),columns = ['Time','Weight']) 
        first_time = float(df['Time'][0])
        df['Time'] = df['Time'].apply(lambda x: float(x)-first_time )
        df['Weight'] = df['Weight'].apply(lambda x: float(x) )
        df['Different per second'] =  df['Weight'].diff(periods=1)
        df['Flow rate'] = df['Different per second'].rolling(3).mean()
        df.set_index('Time', inplace = True)
        ts = int(first_time)
        curr_date=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        
        chart = df.reset_index()
        # print(chart)
        a = alt.Chart(chart).mark_line().encode(alt.Y('Weight:Q',axis=alt.Axis(title='Weight (grams)', titleColor='#5276A7'),scale=alt.Scale(domain=(0, 40),clamp=True)), x='Time')
        b = alt.Chart(chart).mark_line(color='#57A44C').encode(alt.Y('Flow rate:Q',axis=alt.Axis(title='Flow rate (gram/second)', titleColor='#57A44C'),scale=alt.Scale(domain=(0, 5),clamp=True)), x='Time')
        c = alt.layer(a,b).resolve_scale(y ='independent')
        st.altair_chart(c, use_container_width=True)



        st.markdown('It is linked to my [firebase](https://console.firebase.google.com/u/0/project/product-design-f47db/database/product-design-f47db-default-rtdb/data)')
        with st.expander('see my coffee flow rate data'):
            st.write(df)

    
    with st.sidebar.expander('Set your coffee output'):
        ref = db.reference("/")
        coffee_dosage = ref.child('coffee_dosage').get()
        coffee_gram = st.text_input("How much coffee (grams)?",coffee_dosage)
        ref.update({"coffee_dosage" : f'{coffee_gram}'})

        if 'on_state' not in st.session_state:
            on_state = "1"
        else:
            on_state = ref.child('on_state').get()

        
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
                    
            else:
                ref.update({"on_state" : "1"})
                st.session_state.on_state = "1"
                # print('if on state is false',st.session_state.on_state)
                with st.spinner('Turning on...'):
                    time.sleep(0.3)
        count = st_autorefresh(interval=2000, limit=100, key="fizzbuzzcounter")
        print(count)



                   