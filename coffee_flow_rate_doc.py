import streamlit as st
from PIL import Image


def app(css):
    st.subheader('Arduino MKR Wifi 1020 on Espresso Flow Profiling')
    st.markdown('A good pull of espresso shot requires 3 things: coffee grind size,water to coffee ratio and time. Although the espresso machine I have at home can dispense a preset amount of water on every espresso pull, I cant trust the preset water dispense as they are many factor that will impact the flow rate (e.g. cofee grind size). ')
    st.markdown('To tackle that, I used to dispense the water manually. That is to hold down the dispense button until reaching disired (espresso) weight.')
    st.markdown('While it is not very painful, I think it is worth the effort to use arduino to help me automate the process abit, so that I can save money from buying a premiere espresso machine that does the same thing.')
    st.markdown('My _**first goal**_  is to create a weighing scale to track my espresso dispensed while a servo motor holding down the dispensing button.')


    st.markdown("""
    ### Components:
    
    - Arduino MKR Wifi 1020
    - Loadcell
    - HX711
    - Servo
    - Red LED
    - Green LED
    - (laser cut) Weighing platform
    - Bolts and screws
    - Resistors
    - Wires""")

    st.markdown("""
    ### Advantages:
    
    1.
    2.
    3.
    """)

    st.markdown("""
    ### Disadvantages:
    
    1.
    2.
    3.
    """)




    image1 = Image.open("assets/images/arduino_coffee_weighing_flowrate_project.png")
    st.image(image1,caption='Schematic diagram',width=400)

    code1 = """include <WiFiNINA.h>
#include "arduino_secrets.h"            //contains wifi credentials
#include "Firebase_Arduino_WiFiNINA.h"  //Firebase Arduino based on WiFiNINA-install from manage libraries
#include <HX711.h>                      // Loadcell amplifier library
#include <Servo.h>                     

#define FIREBASE_HOST "product-design-f47db-default-rtdb.asia-southeast1.firebasedatabase.app"  //Firebase Realtime database URL
#define FIREBASE_AUTH "38Acl7WfCZmDatBj329ccaRaZEZToxUI7dZ1w39r" //from Firebase Database secrets
#define LED_RED 4   //display during off_state
#define LED_GREEN 5 // display during on_state


//-----------------------------1. Create servo and loadcell objects-----------------------------------------

Servo myservo; 
int pos = 0;    // variable to store the servo position

HX711 loadcell;
const int LOADCELL_DOUT_PIN = 10; // HX711 circuit wiring
const int LOADCELL_SCK_PIN = 11;  // HX711 circuit wiring
float calibration_factor =  -695.82; //adjustment setting for loadcell
float w = 0; // weight calculation
String w_string = " "; //string version to be uploaded to firebase ( standardise data type since interacting with Streamlit)



//-----------------------------2. Sensitive data in the Secret tab/arduino_secrets.h--------------------------

char ssid[] = SECRET_SSID;        // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password (use for WPA, or use as key for WEP)
int status = WL_IDLE_STATUS;     // the Wifi radio's status



//-----------------------------3. Define Firebase data object--------------------------------------------------

FirebaseData firebaseData;
String path = "/data"; 
String timestamp;
String Init_timestamp; // to group data for a single cup of espresso flow
int target; // to store require coffee_dosage gotten from firebase
String on_state = "1"; // it means machine is ready to dispense, "0" means off state


"""
    with st.expander("Define code"):
        st.code(code1, "C") 

    code2 = """//////////////////////////////////////////////////~~~~~SETUP CODE~~~~~//////////////////////////////////////////////////

void setup() {
  Serial.begin(9600);

  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to network: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
  }

  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  // you're connected now, so print out the data:
  Serial.println("You're connected to the network!");
 
  Serial.println("----------------------------------------");

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH, SECRET_SSID, SECRET_PASS);
  Firebase.reconnectWiFi(true); //Let's say that if the connection is down, try to reconnect automatically


  // getting data from firebase
  Firebase.getString(firebaseData, "/coffee_dosage");
  Serial.println("Value: " + firebaseData.stringData());
  target = firebaseData.stringData().toInt();
  Serial.print("Required Coffee in grams: ");
  Serial.print(target);
  Serial.println("----------------------------------------");

  

  //-------------------------- SETUP LOADCELL, SERVO AND LED CUE -----------------------------
  
  loadcell.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  loadcell.set_scale(calibration_factor);
  loadcell.tare();
  myservo.attach(9);
  myservo.write(90); 
  delay(500);
  myservo.write(80);
  delay(500);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  
  check_state(); // function define below

}"""
    with st.expander("Setup code",expanded=True):
        st.code(code2,"C")

    code3 = """//////////////////////////////////////////////////~~~~~LOOP~~~~~//////////////////////////////////////////////////

void loop() {

  Firebase.getString(firebaseData, "/on_state");
  if (firebaseData.stringData()== "0"){
    check_state();
  }
  
  timestamp = String(WiFi.getTime());
  Serial.print("Time: ");
  Serial.println(timestamp);
  w = loadcell.get_units(5) ;
  Serial.print("Weight: ");
  Serial.println(w);
  w_string = String(w);


  if (w<=0){
    w = loadcell.get_units(5);
    Serial.println("Weight: 0");
  }

  // upload data to firebase
  if (Firebase.setString(firebaseData, path + "/" + Init_timestamp  + "/" + timestamp , w_string) ) {
    Serial.println("Wrote to database");  
  } else {
    Serial.println(firebaseData.errorReason());
  }
 
  Serial.println("----------------------------------------");

  // stop 4 grams before desired weight ( as pressure from the espresso machine will force the remaining liquid out from the coffee puck)
  if (w> target - 4 ) {
    myservo.write(90);
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_RED, HIGH);
    while (w> target - 4 ){
      timestamp = String(WiFi.getTime());
      w_string = String(w);
      (Firebase.setString(firebaseData, path + "/" + Init_timestamp  + "/" + timestamp , w_string) );
      Serial.println("Wrote to database");  
      delay(2000); //slow down data collection
      w = loadcell.get_units(5) ;
    } // change the state of the machine to "0" once cup is removed.
    Firebase.setString(firebaseData, "/on_state" , "0"); 
    Firebase.getString(firebaseData, "/on_state");
    Serial.print("Firebase on_state: ");
    Serial.println(firebaseData.stringData());
  }
}


"""
    with st.expander("Loop",expanded=True):
        st.code(code3,"C")

    code4 = """void check_state(){
  Firebase.getString(firebaseData, "/on_state"); // check the on_state from firebase
  Serial.print("Firebase on_state: ");
  Serial.println(firebaseData.stringData());
  on_state = firebaseData.stringData();
  if (on_state== "0"){
    myservo.write(90);
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_RED, HIGH);
    while (on_state !="1") {
      Firebase.getString(firebaseData, "/on_state");
      Serial.print("Firebase on_state: ");
      Serial.println(firebaseData.stringData());
      delay(500);
      on_state = firebaseData.stringData();
    };

  //--------------------- RESETING REQUIREMENT AND SCALE ---------------------
  
  Firebase.getString(firebaseData, "/coffee_dosage");
  Serial.println("Value: " + firebaseData.stringData());
  target = firebaseData.stringData().toInt();
  Serial.print("Required Coffee in grams: ");
  Serial.println(target);

  loadcell.set_scale(calibration_factor);
  loadcell.tare();
  pinMode(LED_GREEN, OUTPUT);
  digitalWrite(LED_GREEN, HIGH);
  pinMode(LED_RED, OUTPUT);
  digitalWrite(LED_RED, LOW);
  

  //-------------------------- START MEASUREMENT OF FLOW -----------------------------
  
  myservo.write(160);
  Serial.println("Initially weight: ");
  Serial.println(loadcell.get_units(5));
  Init_timestamp = String(WiFi.getTime());
  Serial.println("------------------------------------------------------------------------------------");
  Serial.println("Uploading value to firebase");
  }
}"""
    with st.expander("check_status function"):
        st.code(code4,"C")

    st.markdown('Full code can be found [Here](http://www.google.com)!')
    
    # with open(css) as f:
    #     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    # button_clicked = st.button("OK")
    
