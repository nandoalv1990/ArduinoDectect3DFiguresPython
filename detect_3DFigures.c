/*
Código para Arduino.
*/
#include <Servo.h>

Servo servo;

void setup() {
  Serial.begin(9600);
  servo.attach(9);//Pin al que está conectado el servo
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();

    if (data == "cubo") {
      servo.write(0);//Posición para el cubo
    } else if (data == "piramide") {
      servo.write(90);//Posición para la pirámide
    } else if (data == "cilindro") {
      servo.write(180);//Posición para el cilindro
    }
  }
}
