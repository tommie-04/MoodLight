# MoodLight – AI Emotion-Aware Study Lamp

Detects the user's facial emotion via webcam and reflects it through
color-coded LEDs controlled by an Adafruit Metro M0 Express (CircuitPython).

## Problem
Students often become frustrated, stressed, or mentally fatigued while
studying without realizing it.

## Solution
MoodLight uses AI facial emotion recognition (DeepFace) to detect the
user's emotional state through a webcam, then reflects it through a
physical LED array connected to a Metro M0 Express board — giving
immediate visual feedback to help the user become more aware of their
emotional state while studying.

## Architecture

Laptop
  -> OpenCV (webcam capture)
  -> DeepFace (emotion detection)
  -> Debounce logic (stabilizes rapid emotion flickers)
  -> pyserial (USB serial)
  -> Metro M0 Express (CircuitPython)
  -> LEDs + Photoresistor

## Emotion → LED Mapping
| Emotion  | LED Color |
|----------|-----------|
| Happy    | Yellow    |
| Disgust  | Blue      |
| Angry    | Red       |
| Surprise | Green     |
| Neutral (also covers sad/fear) | Clear/White |

## Environment Awareness
In addition to emotion detection, MoodLight monitors ambient light using
a photoresistor (5528) wired as a voltage divider into pin A0. If the
room becomes too dark, the white LED blinks as a gentle reminder to turn
on the lights — this takes priority over the emotion display to protect
the user's eyes during long study sessions. 

## Hardware
- Adafruit Metro M0 Express
- 5 LEDs (yellow / blue / red / green / clear) + 330-ohm resistor
- Photoresistor (5528) + 10K-ohm resistor (voltage divider into A0)
- Breadboard, jumper wires

![MoodLight wiring](images/wiring_setup.jpg)

## Project Structure

MoodLight/
- computer_side/
  - moodlight_main.py — main app: camera + AI + LED integration
  - led_controller.py — serial communication with the M0
  - emotion_detector.py — standalone emotion detection test
  - list_cameras.py — utility to find the correct camera index
  - debug_emotion_scores.py — utility to inspect raw DeepFace scores
- m0_side/
  - code.py — CircuitPython script running on the M0 (LEDs + photoresistor)
- images/
  - wiring_setup.jpg — hardware wiring photo
- .gitignore
- README.md

## Setup
1. Flash `m0_side/code.py` onto the Metro M0 Express as `code.py`
2. Create a Python virtual environment (Python 3.11 recommended —
   TensorFlow does not yet support newer versions):
   - `python3.11 -m venv venv`
   - `source venv/bin/activate`
   - `pip install pyserial opencv-python deepface tf-keras`
3. Update `SERIAL_PORT` in `computer_side/moodlight_main.py` to match
   your M0's serial port
4. Run: `python computer_side/moodlight_main.py`

## Team / Author
UC San Diego SIPP Hackathon Team Wolves --- Tommie Liang