/*ThermoDev1 27/5/21
 * uses MAX31855 to read in temperature of a thermocuple and print out once per second
 * Will read in on interrupt a number to control a 1 KHz PMW output 
 * number  0 to 1000 giving microseconds output on period
 * 
 */

#include <SPI.h>
#include "Adafruit_MAX31855.h"

#define MAXDO   12
#define MAXCS   11
#define MAXCLK  13

#define pmwOut  3  // PMW power on output 
#define sigLed  2  // indicates PWM running

int powerOn = 100; // duty cycle power on pulse in uS (1000 = full on)

// initialize the Thermocouple
Adafruit_MAX31855 thermocouple(MAXCLK, MAXCS, MAXDO);

void setup() {
  cli();//stop interrupts
  Serial.begin(9600);
  
  // set up PWM (o/p use D3 for positive)
  pinMode(pmwOut, OUTPUT); // PWM output pin
  pinMode(sigLed, OUTPUT); // signal Led
  // set up timer interrupt to send out temperature data
  //set timer1 interrupt at 1Hz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  OCR1A = 15624;// = (16*10^6) / (1*1024) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS12 and CS10 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  sei();//allow interrupts
} //end setup

ISR(TIMER1_COMPA_vect){  // function to read in TC temperature on 1Hz interrupt
   double a = thermocouple.readInternal(); // temp of chip
   double c = thermocouple.readCelsius();  // temp of external thermocouple
   if (isnan(c)) {
     Serial.println("Something wrong with thermocouple!");
   } 
   else {
     Serial.println(c);  
   }
} // end of get Temperature interrupt   

void loop() {
  //
  if (Serial.available() > 0) { //if there is data read in 
    String data = Serial.readStringUntil('\n');
    powerOn = data.toInt(); //convert input string value to int
    digitalWrite(sigLed, !digitalRead(sigLed)); // toggle the signal Led output
  }
  // PMW 
  digitalWrite(pmwOut, HIGH); // turn output power on
  delayMicroseconds(powerOn); // Approximately eg 100 = 10% duty cycle @ 1KHz
  digitalWrite(pmwOut, LOW);  // output power off 
  delayMicroseconds(1000 - powerOn); 
 } //end of loop()


   
