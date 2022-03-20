
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
# import tm  -- tm not working yet 



st.set_page_config(page_icon="✏️", page_title="pwp")

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
            "private_key": os.environ.get('PRIVATE_KEY').replace('\\n', '\n'),
            "client_email": os.environ.get("CLIENT_EMAIL"),
            "token_uri": "https://oauth2.googleapis.com/token"
            })

            print(cred)
            
            default_app = firebase_admin.initialize_app(cred, {
                'databaseURL':"https://product-design-f47db-default-rtdb.asia-southeast1.firebasedatabase.app" 
            })
    main()
    
