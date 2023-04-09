// Created by: Nicole Campbell

// Program: UART LoRa Module transmit and recieve with Arduino
// Purpose: Writing: Reads from serial monitor and send over UART to LoRa wireless module, and
//          Reading: Reads UART data from LoRa module and sends to serial port where server.py can receive



#include <SoftwareSerial.h>

// Lora module pins
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

// Reference: https://osoyoo.com/2018/07/26/osoyoo-lora-tutorial-how-to-use-the-uart-lora-module-with-arduino/
