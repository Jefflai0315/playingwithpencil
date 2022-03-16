
#include <WiFiNINA.h>
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









//////////////////////////////////////////////////~~~~~SETUP CODE~~~~~//////////////////////////////////////////////////

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

}

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
  if (w> target - 5 ) {
    myservo.write(90);
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_RED, HIGH);
    while (w> target - 5 ){
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




//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


void check_state(){
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
}





//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void printData() {
  Serial.println("Board Information:");
  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  Serial.println();
  Serial.println("Network Information:");
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.println(rssi);

  byte encryption = WiFi.encryptionType();
  Serial.print("Encryption Type:");
  Serial.println(encryption, HEX);
  Serial.println();
}
