
import streamlit as st
from streamlit_lottie import st_lottie
import firebase_admin
from firebase_admin import credentials
import coffee_flow_rate_doc
import coffee
import art
import coffee_flow_rate_doc
import os
import json
from dotenv import load_dotenv
load_dotenv()

# import tm  -- tm not working yet 

st.write(os.getenv('KEY'))

try:
    st.set_page_config(page_icon="✏️", page_title="pwp")
except:
    pass

# model, live, data, size = tm.init_face_reg()

def main():
    
    menu = st.sidebar.selectbox('Menu',['Art','Coffee','Secret'])

    if menu == 'Coffee' :
        myKey = 'my_key'
        if myKey not in st.session_state:
            st.session_state[myKey] = False

        if st.session_state[myKey]:
            if st.button('Coffee Profilling page'):
                st.session_state[myKey] = False
                st.experimental_rerun()
            coffee_flow_rate_doc.app()
                
        else:
            if st.button('Show Documentation'):
                st.session_state[myKey] = True
                st.experimental_rerun()
            coffee.app()
        
        
    

    elif menu == 'Coffee':
        coffee.app()
        
   
    
    if menu == 'Art':
        art.app()
    

    if menu == 'Secret':
        # result = tm.app()
        # if result ==0:
        #     st.success("Welcome Jeff!")
        # else:
        #     st.warning("You are not Jeff")
        st.info('feature on the way!')
    

        

if __name__ == "__main__":
    if not firebase_admin._apps:
        try:
            # For LOCAL
            cred = credentials.Certificate('cred.json')
            print(cred)
            default_app = firebase_admin.initialize_app(cred, {
                'databaseURL':"https://product-design-f47db-default-rtdb.asia-southeast1.firebasedatabase.app" 
            })
        except:
            # For PROD
            
            cred = credentials.Certificate({
            "type": "service_account",
            "project_id": "product-design-f47db",
            "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
            "private_key": os.environ.get('PRIVATE_KEY').replace('\\n', '\n'),
            "client_email": os.environ.get("CLIENT_EMAIL"),
            "client_id": os.environ.get('CLIENT_ID'),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.environ.get('CLIENT_CERT_URL')
            })

        
            
            default_app = firebase_admin.initialize_app(cred, {
                'databaseURL':"https://product-design-f47db-default-rtdb.asia-southeast1.firebasedatabase.app" 
            })
    main()
    
