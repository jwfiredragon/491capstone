 // Uploaded by: Nicole Campbell

// Program: Osoyoo LoRa Tutorial — How to Use the Uart LoRa Module with Arduino
// Purpose: This is an example of using the Osoyoo LoRa module with an arduino. 
//          When the program is run on two MCU's, you can type command line text
//          and have it sent over LoRa to the other MCU
// Source: https://osoyoo.com/2018/07/26/osoyoo-lora-tutorial-how-to-use-the-uart-lora-module-with-arduino/


// For point-2-point Transmit and Receive, we need two Arduino IDE to run at the same time. 
// So, we need to click the Arduino IDE’s icon for twice. 
// Run both at the same time and copy the code to both the Arduino IDE.


#include <SoftwareSerial.h>

#define M0_PIN  6
#define M1_PIN  5
#define AUX_PIN A0
#define RXD_PIN 3
#define TXD_PIN 2

SoftwareSerial LoraSerial(TXD_PIN, RXD_PIN); //TX, RX
// (Send and Receive)

void setup() {
  Serial.begin(9600);
  LoraSerial.begin(9600);

  pinMode(M0_PIN, OUTPUT);
  pinMode(M1_PIN, OUTPUT);
  
  setMode(0); // Set mode to normal operating mode 00

}

void loop() {
  
  
  if(Serial.available() > 0){//Read from serial monitor and send over UART to LoRa wireless module
    String input = Serial.readString();
    LoraSerial.println(input);    
  }
 
  if(LoraSerial.available() > 1){//Read UART from LoRa wireless module and send to serial monitor
    String input = LoraSerial.readString();
    Serial.println(input);    
  }
  delay(20);
}


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

    delay(10);
}


// After above operations are completed, click the upload button.
// Once it is done with uploading, open up the Serial Monitor at each side. 
// Now, you can try to type some words at the Serial Monitor and wait for it to appear at another side. 
// For example in my picture, when I type “123” in Serial Monitor COM16, 
// it will be sent over and appear at Serial Monitor COM5.
