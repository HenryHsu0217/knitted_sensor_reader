#include "BraccioV2.h"
Braccio arm;
/*
 Basic_Movement.ino - version 0.1
 Written by Lukas Severinghaus
 Demonstrates basic movement of the arm using single joint absolute
 and relative positioning. Also shows the use of safe delay with
 and without custom intervals.

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2.1 of the License, or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.
 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */
//Set these values from the min/max gripper joint values below.
#define GRIPPER_CLOSED 85
#define GRIPPER_OPENED 20
int loop_count=0;
String inputString = "";
void setup() {
  Serial.begin(9600);
  Serial.println("Initializing... Please Wait");//Start of initialization, see note below regarding begin method.

  //Update these lines with the calibration code outputted by the calibration program.
  arm.setJointCenter(WRIST_ROT, 0);
  arm.setJointCenter(WRIST, 180);
  arm.setJointCenter(ELBOW, 45);
  arm.setJointCenter(SHOULDER, 0);
  arm.setJointCenter(BASE_ROT, 0);
  arm.setJointCenter(GRIPPER, 0);//Rough center of gripper, default opening position

  //Set max/min values for joints as needed. Default is min: 0, max: 180
  //The only two joints that should need this set are gripper and shoulder.
  arm.setJointMax(GRIPPER, 100);//Gripper closed, can go further, but risks damage to servos
  arm.setJointMin(GRIPPER, 15);//Gripper open, can't open further

  //There are two ways to start the arm:
  //1. Start to default position.
  arm.begin(true);// Start to default vertical position.
  //This method moves the arm to the values specified by setJointCenter
  //and by default will make the arm be roughly straight up.

  //2. Start to custom position.
  //arm.begin(false);
  //arm.setAllNow(base_rot_val, shoulder_val, elbow_val, wrist_val, wrist_rot_val, gripper_val);
  //This method allows a custom start position to be set, but the setAllNow method MUST be run
  //immediately after the begin method and before any other movement commands are issued.


  //NOTE: The begin method takes approximately 8 seconds to start, due to the time required
  //to initialize the power circuitry.
  Serial.println("Initialization Complete");
}

void loop() {
  if (Serial.available() > 0) {
    // Read the incoming byte
    char incomingByte = Serial.read();
    // If the incoming byte is a newline character, process the input
    if (incomingByte == '\n') {
      int inputNumber = inputString.toInt(); // Convert string to integer
      Serial.println(inputNumber); // Print the input number
      arm.setOneAbsolute(ELBOW, inputNumber); // Set servo position
      arm.safeDelay(3000);
      inputString = ""; // Clear the string for next input
    } 
    else {
      // Add the incoming character to the input string
      inputString += incomingByte;
    }
  }
}