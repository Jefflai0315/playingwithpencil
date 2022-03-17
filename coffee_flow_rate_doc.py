import streamlit as st
from PIL import Image
from assets import code_text


def app():
    st.header('Espresso Flow Profiling with Arduino MKR WIFI 1010 ☕')
    st.markdown('**This tutorial will illustrate the working of an loadcell and servo, as well as remotely controlling servo visuallising data via [my Streamlit app](https://playingwithpencil.herokuapp.com/).**')
    col1,col2 = st.columns([3,1])
    
    image0 = Image.open("assets/images/espresso_line_chart.png")
    image00 = Image.open("assets/images/coffee.jpg")
    with col1:
      st.image(image0,caption='Sneak peak into the result 👀',width=500)
    with col2:
      st.image(image00,caption='Making espresso',width=135)
    st.markdown('''---''')

    st.header('Things used in this project')
    st.markdown("""
    ##### Hardward Components:
    
    - Arduino MKR Wifi 1020
    - Loadcell
    - HX711
    - Servo
    - Red LED
    - Green LED
    - (laser cut) Weighing platform
    - Bolts and screws
    - Resistors
    - Jumper wires""")
    st.markdown('''---''')

    st.header('Story')
    st.markdown('**What is espresso flow profilling and why does it matters?**')

    st.markdown(''' “Flow profiling” is about controling the flow rate of water going through the machine’s boiler and the puck of coffee.
     The quality of an espresso shot depends on 3 things: coffee grind size, coffee to water ratio and time.
     Although the espresso machine I have at home can dispense water for a preset amount of time, 
     I wouldn't trust the dispensing as every pull of espresso can **never be the same**.  (e.g. different coffee type with same grind size setting and same amount of coffee can take different time to get the correct coffee to water ratio ). ''')
    
    st.markdown('To tackle that, I used to dispense the water manually. That is to hold down the dispense button until reaching disired (espresso) weight.')
    st.markdown('It is a **pain point** as I am not able to focus on studying the coffee flow profiling. Hence I think it is worth the effort to use microcontroller to help me automate the process abit, so that I can save money from buying a premiere espresso machine that does the same thing.')
    st.markdown('My _**first goal**_ 🏁  is to hire a mechanism that help me hold down the button until a desired weight is obtained. This mechanism requires 3 things:')
    
    st.markdown(">>1. **Servo motor** secured right above the dispensing button that will hold down the button by instructing servo to turn 90 degree anticlockwise ")
    st.markdown(">> 2. **Load cell and HX711** that actively tracks the weight of the espresso liquid dispensed. Once reached desired weight, the servo to return to original position via signals from arduino")
    st.markdown(">> 3. **LEDs**. green led to show servo is holding down the button, while red led to show it returns to its original position")
    
    col3,col4,col5 = st.columns(3)
    with col3:
      image1 = Image.open("assets/images/servo.jpg")
      st.image(image1,caption='1. my_servo.write(160)',width=200)

    with col4:
      image2= Image.open("assets/images/loadcell.jpg")
      st.image(image2,caption='2. loadcell on weighting platform',width=200)

    with col5:
      image3= Image.open("assets/images/led.jpg")
      st.image(image3,caption='3. visual cues',width=200)

    st.markdown('My _**second goal**_ 🏁 is to use Streamlit to display my espresso flow profilling data **and** control the state of my servo. If the state is "on", the weight data will be send to firebase, else it will be stuck in a loop (can see my code)''')
    st.markdown("_Press 'Coffee Profilling page' button at the top of the page to see the data visualisation. you can also watch the video at the end to see how it works!_")
    st.markdown("""---""")

    st.markdown("""## Step 1: Setup the Hardware""")
    
    image4 = Image.open("assets/images/arduino_coffee_weighing_flowrate_project.png")
    st.image(image4,caption="Schematic diagram",width=600)

    col6,col7 = st.columns(2)

    with col6:
      st.markdown('''
      ##### PinWiring to Arduino MKR WIFI 1010

      DT--------------------------Digital 10

      SCK------------------------Digital 11

      G LED---------------------Digital 4

      R LED---------------------Digital 5

      SERVO--------------------Digital 9

      GND-----------------------GND

      VCC------------------------5V ''')
      
    with col7:
      st.markdown('''
      ##### PinWiring to HX711 

      RED-------------------------E+

      BLACK----------------------E-

      GREEN----------------------A+

      WHITE----------------------A-

      ''')

    st.markdown("**Reminder:** Don't forget the resistors!")

    st.markdown('''---''')


    st.subheader("Step 2: Before the code")
    st.markdown('''
    ##### Include these
    - **<HX711.h>** library for HX711 that amplifies signals from cells and reporting them to another microcontroller
    - **<WiFiNINA.h>** enables network connection (local and Internet) with the Arduino MKR WiFi 1010
    - **<Servo.h>** library which comes with the Arduino IDE
    - **"Firebase_Arduino_WiFiNINA.h"** which is a Google Firebase Realtime Database Arduino Client Library for Arduino MKR WiFi 1010
    - **"arduino_secrets.h"** is where you keep the confidentials safely and excluding them from the main sketch file ''')
    
    st.markdown("""**Note:** If library not pre-installed, you can search it under Tool > Manage libraries > _search for the library_""")

    st.markdown("""
    **Important:** In order to send and receive data from a database in real-time in Firebase, we have to setup our firebase first.
    
    Follow this tutorial to [setup your Firebase and connect to Arduino MKR WIFI 1010](https://create.arduino.cc/projecthub/OscarF10/mkr-wifi-1010-firebase-9a7399)""")
    st.markdown('''---''')


    st.subheader("Step 3: Ready for the code!")
    st.markdown('I have broken down my code into sections for easy reference.')
    
    code1,code2,code3,code4,code_arduino = code_text.app()

    with st.expander("Include libraries and define variables"):
        st.code(code1, "C") 

    with st.expander("Setup code"):
        st.code(code2,"C")

    with st.expander("Loop"):
        st.code(code3,"C")

    with st.expander("check_status() function"):
        st.code(code4,"C")

    st.markdown('The Full code can be found on my [github repository](https://github.com/Jefflai0315/playingwithpencil/blob/main/assets/coffee_flow_ratetest.ino) \n**or** Download by clicking the button!')
    with open('assets/coffee_flow_ratetest.ino', 'rb') as f1:
      st.download_button('Download Arduino code', f1, file_name='coffee_flowrate.ino')

    st.markdown('**Additional:** You will also need to calibrate the loadcell/HX711. Just download the file below, upload to your arduino, open up the serial monitor and follow the steps.')
    with open('assets/HX711_Calibration_no_eeprom.ino', 'rb') as f2:
      st.download_button('Download Calibration code', f2, file_name='HX711_Calibration_no-_eeprom.ino')

    st.markdown('''---''')
    st.subheader('Last but not least: Demonstration')
    video_file = open('assets/images/coffee_flowrate.mp4', 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes)
    st.markdown('''
    ##### Video description
    - changing desired weight value in grams
    - turning on and off button from Streamlit to control servo remotely
    - watching loadcell read weight data and sending to firebase
    - when desired weight is obtained, firebase continue to receive data as the state is still "on"
    - once the cup is removed ( weight drastically reduced), the state becomes "off" and no data is send to firebase

    ##### What is not shown
    - implementation of Streamlit code
    - deployment of Streamlit app on Heroku
    - how to visuallise my firebase espresso flow profilling data on Steamlit (Just press the Coffee Profilling page button on top to see!)
     ''')

    st.markdown('''
    Streamlit is itself a vast topic to cover, but I can share some links that are related.
    >>[my github repository of Steamlit code](https://github.com/Jefflai0315/playingwithpencil)

    >>[deploy Streamlit to Heroku](https://medium.com/analytics-vidhya/how-to-deploy-a-streamlit-app-with-heroku-5f76a809ec2e)
    ''')


    st.markdown('''---''')
    st.subheader('Finally: Conclusion')
    st.markdown("""
    ##### Advantages:
    
    1. I no longer need to hold down the dispensing button. And enjoy watching the thick espresso pull out of the portafiler!
    2. I am able to study the flow profilling data collected, so that I can alter the grind size of my newly bought coffee beans.
    3. Show that I can make simple modifications to my espresso machine to save some bucks for upgrading my machine :D
    """)

    st.markdown("""
    ##### Restropective:
    
    1. Since the button is only found on my Streamlit app now, it can be incovenient if I do not have any devices with me. It will be good if I can have a physical button beside the machine to change the state of the machine.
    2. The electrical components and wirings are exposed and placed close to a liquid dispenser's boiler. I will need to alter the length of the wires such that I can keep the electrical components away/ at the side or top of the espresso machine. It will be nice if i can compact all the parts into a small module.
    3. The servo arm is not ideal to ensure proper contact with the button. Besides, the current rotating angle / servo position should be reconsider as the motion is prompt to misalignment.
    """)


    st.markdown('_credit: for dear TA for helping me to resolve the error in the HX711_calibration_no_eeprom file_')
