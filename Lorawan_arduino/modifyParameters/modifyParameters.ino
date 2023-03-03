// Created by: Nicole Campbell

// Purpose: to set the channel frequency of the lorawan device. Program

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
  pinMode(TXD_PIN, OUTPUT);

  

}

void loop() {

  delay(10);
  Serial.println("try to read parameters");
  // read current parameters
  readParam();

  while(1);

}

// read module parameters
void readParam(){
  
  //set sleep mode
  setMode(3);

  int readcmd = 0xC1;
  //send read parameters command
 LoraSerial.print(readcmd);
 LoraSerial.print(readcmd);
 LoraSerial.print(readcmd);
  //Serial.print(readcmd, HEX);
  while(1){
  //read parameters from UART and print to serial monitor
  if(LoraSerial.available() > 1){
    String input = LoraSerial.readString();
    Serial.println(input);  }
}}

// set lora module chan freq
void setFreq(int freq){
  setMode(3); // set to sleep mode 11 (modify parameters mode)

  // Not-saved format: 0xC2 ADDH ADDL SPED CHAN OPTION

  #define NOTSAVED 0xC2
  int ADDH = 0x00;
  int ADDL = 0x00;
  int SPED = 0x1a;    //0b00011010
  int OPTION = 0x44;  //0b01000100
  int CHAN = 0x17;    // freq = 410Mhz + CHAN (default: 0x17, 433MHz)

  // parameter values
  int paramHI = (((NOTSAVED << 8) + ADDH) << 8) + ADDL;
  int paramLO = (((SPED << 8) + OPTION) << 8) + CHAN;

  //send parameters
  LoraSerial.print(paramHI);
  LoraSerial.print(paramLO);
  
}
  

// set lora module mode
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
