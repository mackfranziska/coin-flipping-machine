import sys
import time
import picamera
import RPi.GPIO as GPIO

GPIO.setwarnings(False) 

# Declare the camera
camera = picamera.PiCamera()
 
# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
 
# Define GPIO signals to use
# GPIO19,GPIO21,GPIO26,GPI13
StepPins = [19,21,26,13]
 
# Set all pins as output
for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)
 
# Define advanced sequence
# as shown in manufacturers datasheet
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

steps = 0
rounds = 1 # How many times has the motor spinned?

# Initialize variables for motor

StepDir = 1 # Set to 1 or 2 for clockwise
            # Set to -1 or -2 for anti-clockwise
            # The complete step sequence consists of 8 steps (slower but higher torque)
            # If StepDir is set to -2 or 2 the number of steps is reduced to 4
            # (faster but h=lower torque).

WaitTime = 0.0015
rotations = 50*3 # 50 equals 360 degrees
 
# Start main loop
while True:
    
    if (steps < rotations):
         
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
            steps = steps + 1
        if (StepCounter<0):
            StepCounter = StepCount
         
        # Wait before moving on
        time.sleep(WaitTime)

    else:
        print("done with round:")
        print(rounds)
        rounds = rounds + 1
        
        # Take the picture of the coin
        camera.capture('/home/pi/Documents/stepper/img/test' + str(rounds) + '.jpg')
        print("new picture taken")
        time.sleep(3)
        print("starting next round:")
        # Reset step-counter
        steps = 0
    
GPIO.cleanup()

