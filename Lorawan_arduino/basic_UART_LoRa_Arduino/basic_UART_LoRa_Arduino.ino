// Uploaded by: Nicole Campbell

// Program: UART LoRa Module transmit and recieve with Arduino
// Purpose: This is an example of using the Osoyoo LoRa module with an arduino. 
//          When the program is run on two MCU's, you can type command line text
//          and have it sent over LoRa to the other MCU
// Reference source: https://osoyoo.com/2018/07/26/osoyoo-lora-tutorial-how-to-use-the-uart-lora-module-with-arduino/

// For point-2-point Transmit and Receive, we need two Arduino IDE to run at the same time. 
// So, we need to click the Arduino IDE icon twice. Uplad the code to both Arduino IDE and run both at the same time.

#include <SoftwareSerial.h>

#define M0_PIN  6
#define M1_PIN  5
#define AUX_PIN A0
#define RXD_PIN 3
#define TXD_PIN 2

SoftwareSerial LoraSerial(TXD_PIN, RXD_PIN); //TX, RX

void setup() {
  Serial.begin(9600);
  LoraSerial.begin(9600);

  pinMode(M0_PIN, OUTPUT);
  pinMode(M1_PIN, OUTPUT);
  
  setMode(0); // Set mode to normal operating mode 00
}

void loop() {
  
// ~~~~~ Reading ~~~~~
  if(Serial.available() > 0){//Read from serial monitor and send over UART to LoRa wireless module
    String input = Serial.readString();
    LoraSerial.print(input);    
  }

// ~~~~~ Writing ~~~~~
 // Lora buffer is 512 bytes
  //if(LoraSerial.available() > 1){ // Read UART from LoRa module and send to serial monitor
  while(LoraSerial.available() > 1){
    Serial.write(LoraSerial.read());
  }

  
}



// ~~~~~ Set lora module mode ~~~~~
void setMode(int mode){
    switch (mode)
    {
    case 0:
      digitalWrite(M0_PIN, LOW);
      digitalWrite(M1_PIN, LOW);
      break;
    case 1:
      digitalWrite(M0_PIN, HIGH);
      digitalWrite(M1_PIN, LOW);
      break;
    case 2:
      digitalWrite(M0_PIN, LOW);
      digitalWrite(M1_PIN, HIGH);
      break;
    case 3:
      digitalWrite(M0_PIN, HIGH);
      digitalWrite(M1_PIN, HIGH);
      break;
    
    default:
      return;
    }

    delay(20);
}
