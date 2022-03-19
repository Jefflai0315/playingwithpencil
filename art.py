import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image
from datetime import datetime
import db

COMMENT_TEMPLATE_MD = """{} - {}
> {}"""

lottie_art = requests.get('https://assets4.lottiefiles.com/private_files/lf30_hqhmdw8f.json').json()

conn = db.connect()
comments = db.collect(conn)

def app():
    st_lottie(lottie_art, speed=1, height=200, key="Art")
    st.subheader('GM GM, here are show of my recent artwork!')
    st.markdown("I only do graphic pencil portrait at the moment, **_aren't_ they nice?**")

    col1,col2,col3 = st.columns(3)
    with col1:
        image1 = Image.open('assets/images/photo.jpg')
        st.image(image1,caption='Taeyeon',use_column_width=True)
    
    with col2:
        image2= Image.open('assets/images/photo1.jpg')
        st.image(image2,caption='Momo',use_column_width=True)
    with col3:
        image3= Image.open('assets/images/photo2.jpg')
        st.image(image3,caption='Dahyun',use_column_width=True)

    with st.expander("💬 Open comments"):

    # Show comments

        st.write("**Comments:**")
        print(comments)

        for index, entry in enumerate(comments.itertuples()):
            st.markdown(COMMENT_TEMPLATE_MD.format(entry.name, entry.date, entry.comment))

            is_last = index == len(comments) - 1
            is_new = "just_posted" in st.session_state and is_last
            if is_new:
                st.success("☝️ Your comment was successfully posted.")

        

        # Insert comment

        st.write("**Add your own comment:**")
        form = st.form("comment")
        name = form.text_input("Name")
        comment = form.text_area("Comment")
        submit = form.form_submit_button("Add comment")

        if submit:
            date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            db.insert(conn, [[name, comment, date]])
            if "just_posted" not in st.session_state:
                st.session_state["just_posted"] = True
            st.experimental_rerun()
