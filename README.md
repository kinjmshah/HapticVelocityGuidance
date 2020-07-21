# Proposing a framework for evaluating haptic feedback as a modality for velocity guidance

This repository accompanies the hardware and algorithm described in ***[Proposing a framework for evaluating haptic feedback as a modality for velocity guidance](https://kinjmshah.github.io/files/haptics2020_WIP.pdf)***. LEDs were included in the initial setup as a debugging measure. They have been included in the details below but can be left out. The activation of the LEDs accompanies the activation of the vibration motors.

**Hardware and Software Requirements:**
1. Raspberry Pi Zero W
    - Raspberry Pi setup as per official documentation ([link](://www.raspberrypi.org/documentation/))
      - python3
      - Wifi Enabled
2. 2 vibration motors
3. 2 LEDs
4. IMU (Adafruit BNO055)
5. Sleeve to hold IMU and vibration motors on the user's arm as depicted in paper
6. Micro SD Card

A detailed assembly of the circuit above may be described in future updates of this work. However, the program in this repository will still work with any standard circuit configuration with the LEDs, vibration motors, and Raspberry Pi. The Raspberry Pi must be setup such that Wifi communication between a computer and the RP. The files `execute.py` and `guidance.py` should be transferred to the RPi.

**Execution Instructions:**
1. Transfer `execute.py` and `guidance.py` to Raspbery Pi (ensure both are in the same directory)
2. Execute `python3 execute.py cmd1 cmd2 cmd3` from within the directory where the two files are located
3. Command line arguments
    - 1st command line argument: subject number (starting with 001)
    - 2nd command line argument: enter target velocity (in radians per second), enter 1 if setting 1 for the 3rd command line argument since the varying target is preset
    - 3rd command line argument: target velocity (0 or 1: 0 for constant target velocity, 1 for varied target velocity)

**Visualization Using `plots.py`:**
plots.py assumes data exists for both a constant velocity run (saved as patient `001`) and a varied velocity run (saved as patient `002`). These patient numbers can be changed from within `plots.py`.

1. Transfer patient files back to computer into `data` directory within this Github repository
2. Execute `plots.py` file

