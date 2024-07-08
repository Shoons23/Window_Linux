/* Encoder Library - Basic Example
 * http://www.pjrc.com/teensy/td_libs_Encoder.html
 *
 * This example code is in the public domain.
 */

#include <Encoder.h>

// Change these two numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder myEncL(2, 22);
Encoder myEncR(3, 23);
//   avoid using pins with LEDs attached

void setup() {
  Serial.begin(9600);
  Serial.println("Basic Encoder Test:");
}

long oldPositionL = -999;
long oldPositionR = -999;

void loop() {
  long newPositionL = myEncL.read();
  long newPositionR = myEncR.read();

  bool condi = (newPositionL != oldPositionL) || (newPositionR != oldPositionR);

  if (condi) {
    oldPositionL = newPositionL;
    oldPositionR = newPositionR;

    Serial.print(newPositionL);
    Serial.print(", ");
    Serial.println(newPositionR);
  }
}
