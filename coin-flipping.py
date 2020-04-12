# Stepper Motor Control
# Matt Hawkins 2012
# Modified by Franziska Mack

import sys
import time
import picamera
import RPi.GPIO as GPIO

GPIO.setwarnings(False) 

# Declare the camera
camera = picamera.PiCamera()
 
# Define halfstep sequence
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
 
StepCount = len(Seq)
StepCounter = 0

StepsPerRound = 0
RoundsCompleted = 1 # How many times has the motor spinned?

# Initialize variables for motor

StepDir = 1 # Set to 1 or 2 for clockwise
            # Set to -1 or -2 for anti-clockwise
            # The complete step sequence consists of 8 steps (slower but higher torque)
            # If StepDir is set to -2 or 2 the number of steps is reduced to 4
            # (faster but h=lower torque).

WaitTime = 0.0015
Rotations = 150 # 50 equals 360 degrees
 
# Start main loop
while True:
    
    GPIO.setmode(GPIO.BCM)
    
    StepPins = [19,21,26,13]

    for pin in StepPins:
      GPIO.setup(pin,GPIO.OUT)
      GPIO.output(pin, False)
    
    if (StepsPerRound < Rotations):
         
        for pin in range(0, 4):
            xpin = StepPins[pin]#
            if Seq[StepCounter][pin]!=0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
         
        StepCounter += StepDir
         
        # If we reach the end of the sequence
        # start again
        if (StepCounter==StepCount):
            StepCounter = 0
            StepsPerRound = StepsPerRound + 1
        if (StepCounter<0):
            StepCounter = StepCount
         
        # Wait before moving on
        time.sleep(WaitTime)

    else:
        GPIO.cleanup()
        print("done with round:")
        print(RoundsCompleted)
        RoundsCompleted = RoundsCompleted + 1
        
        # Take the picture of the coin
        camera.capture('/home/pi/Documents/stepper/img/test' + str(RoundsCompleted) + '.jpg')
        print("new picture taken")
        time.sleep(3)
        print("starting next round:")
        # Reset step-counter
        StepsPerRound = 0