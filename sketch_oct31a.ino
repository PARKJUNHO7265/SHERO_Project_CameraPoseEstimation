/*
 * Programming Lab : AVSC , SungKyunKwan University
 *                   (Autonomous Vehicle Separating and Coupling)
 *    Written by
 *            JunHo Park, JinSeok Park, HyunWoong Jeong, JuHeon Lee, YoungYook Hong, JinWoo Lim
 *            School of Electrical and Electronics Engineering (PARK)
 *            School of Software Programming (Jeong)
 *            School of Mechanical Engineering Department (Lee, Hong, Lim)
 *            Sungkyunkwan University.
 *
 *    Advisor : JaeWook Jeon
 *            Professor of
 *            School of Electrical and Electronics Engineering
 *            Sungkyunkwan University.
 *
 *    Leader  : YoongHyun Kwon
 *            School of Electrical, Electronics and Computer Engineering
 *            Sungkyunkwan University.
 *    
 *    Mentor  : SungCheon Park
 *            Electronics and Telecommunications Research Institute
 *            
 *    File name : AVSC_FINAL.ino
 *    
 *    Written on Oct 27, 2020
 */

#define DEBUG true

//Motor define
#define dirPin_L 30 
#define stepPin_L 3
#define dirPin_R 40
#define stepPin_R 4

//Sensor and LEDs
#define CDS A0   // Illuminance sensor
#define Light 6    // Light for bright
#define RedLight 7  //Red Light
#define YelLight_L 8  //Left Yellow Light
#define YelLight_R 9 //Right Yellow Light

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);
#include <SPI.h>  // 아두이노 SPI 라이브러리 포함


char sensorPrintout[4];  
String income_wifi = "";
String AVSC_MODE = "";

void setup() {
    Serial.begin(9600);
    Serial3.begin(9600);
    pinMode(CDS, INPUT);  
    pinMode(Light,OUTPUT);  
    pinMode(RedLight,OUTPUT);
    pinMode(YelLight_L,OUTPUT);
    pinMode(YelLight_R,OUTPUT);
    pinMode(stepPin_L, OUTPUT);
    pinMode(dirPin_L, OUTPUT);
    pinMode(stepPin_R, OUTPUT);
    pinMode(dirPin_R, OUTPUT);

//Wifi setting
    sendData("AT+RST\r\n",2000,DEBUG);
    sendData("AT+CWMODE=2\r\n",1000,DEBUG); // configure as access point (working mode: AP+STA)
    sendData("AT+CWSAP=\"AVSC_CAR\",\"avscpassword\",11,3\r\n",1000,DEBUG); // make AP with Password
    sendData("AT+CIFSR\r\n",1000,DEBUG); // get AVSC_CAR ip address
    sendData("AT+CIPMUX=1\r\n",1000,DEBUG); // configure for multiple connections
    sendData("AT+CIPSERVER=1,80\r\n",1000,DEBUG); // turn on server on port 80
}

void loop() {
  
    //Speed of motor
    int rotate_speed = 200;
    int rotate_speed_down = 500;
    int rotate_speed_DOWN = 100;
    
    //Steps of motor
    int stepsPerRevolution = 4000;
    int stepsPerRevolution_Turn = 100;
    
    if (Serial3.available()) { 
        if (Serial3.find("+IPD,")) {
            income_wifi = Serial3.readStringUntil('\r');
            String wifi_temp = income_wifi.substring(income_wifi.indexOf("GET /")+5, income_wifi.indexOf("HTTP/1.1")-1);
              
            //Get signal "M1" from Python
            if(wifi_temp == "M1") {
                 Serial.println(wifi_temp);
                 digitalWrite(dirPin_L, HIGH);
                 digitalWrite(dirPin_R, HIGH);
                 //Turn on LEDs for "Turn Signals" 
                 digitalWrite(RedLight,LOW);
                 digitalWrite(YelLight_L,HIGH);
                 //Move to Left
                 for (int i = 0; i < stepsPerRevolution_Turn; i++) {
                      for(int j = 0; j < 5; j++){
                          digitalWrite(stepPin_L, HIGH);
                          delayMicroseconds(rotate_speed_DOWN);
                          digitalWrite(stepPin_L, LOW);
                          delayMicroseconds(rotate_speed_DOWN);
                      }
                      digitalWrite(stepPin_R, HIGH);
                      delayMicroseconds(rotate_speed_down);
                      digitalWrite(stepPin_R, LOW);
                      delayMicroseconds(rotate_speed_down);
                 }
                   //Turn on LEDs for "Break Signals"
                   digitalWrite(RedLight,HIGH);
                   digitalWrite(YelLight_L,LOW);
            }
            
            //Get signal "M2" from Python
            else if(wifi_temp == "M2") {
                 Serial.println(wifi_temp);
                 digitalWrite(dirPin_L, LOW);
                 digitalWrite(dirPin_R, LOW);
                 //Turn on LEDs for "Turn Signals"
                 digitalWrite(RedLight,LOW);
                 digitalWrite(YelLight_R,HIGH);
                 //Move to Right
                 for (int i = 0; i < stepsPerRevolution_Turn; i++) {
                     for(int j = 0; j < 5; j++){
                          digitalWrite(stepPin_R, HIGH);
                          delayMicroseconds(rotate_speed_DOWN);
                          digitalWrite(stepPin_R, LOW);
                          delayMicroseconds(rotate_speed_DOWN);
                     }
                     digitalWrite(stepPin_L, HIGH);
                     delayMicroseconds(rotate_speed_down);
                     digitalWrite(stepPin_L, LOW);
                     delayMicroseconds(rotate_speed_down);
                 }
                    //Turn on LEDs for "Break Signals"
                    digitalWrite(RedLight,HIGH);
                    digitalWrite(YelLight_R,LOW);
            }
            
            //Get signal "M3" from Python
            else if(wifi_temp == "M3") {
                digitalWrite(dirPin_L, LOW);
                digitalWrite(dirPin_R, HIGH);
                digitalWrite(RedLight,LOW); 
                //Move forward
                for (int i = 0; i < stepsPerRevolution; i++) {
                     digitalWrite(stepPin_L, HIGH);
                     delayMicroseconds(rotate_speed);
                     digitalWrite(stepPin_L, LOW);
                     delayMicroseconds(rotate_speed);
                     digitalWrite(stepPin_R, HIGH);
                     delayMicroseconds(rotate_speed);
                     digitalWrite(stepPin_R, LOW);
                     delayMicroseconds(rotate_speed);
                }
                digitalWrite(RedLight,HIGH);
            }
            //Get signal "M4" from Python
            else if(wifi_temp == "M4") {
                Serial.println("M4");
                
            }
        }   
    }
    
    //Code for Car's headlight
    int val = analogRead(CDS);    // Value of Illuminance Sensor
    if(val > 780) {               // If it gets dark
      digitalWrite(Light, HIGH);    // Turn on the Light 
    }
    
    else {                        
      digitalWrite(Light, LOW);     // Turn off the Light
    }
   
    delay(200);                  
}

//Serial Communication with Wifi Module   
String sendData(String command, const int timeout, boolean debug) {
    String response = "";
    Serial3.print(command);
    long int time = millis();
    
    while( (time+timeout) > millis()) {
        while(Serial3.available()) {
            char c = Serial3.read();
            response+=c;
        }
    }
    
    if(debug) Serial.print(response);
    return response;
    }
