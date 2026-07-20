import time
import board
import digitalio
import analogio
import supervisor
import sys


# One color per state, including NEUTRAL
led_pins = {
    
    "NEUTRAL":  board.D7,   # Clear/White LED — steady baseline state
    "DISGUST":  board.D6,   # Blue LED
    "HAPPY":    board.D5,   # Yellow LED
    "ANGRY":    board.D4,   # Red LED
    "SURPRISE": board.D3,   # Green LED
    
}

leds = {}
for emotion, pin in led_pins.items():
    led = digitalio.DigitalInOut(pin)
    led.direction = digitalio.Direction.OUTPUT
    led.value = False
    leds[emotion] = led

# light up the matching LED, turn off the rest 
def set_emotion(emotion):
    for name, led in leds.items():
        led.value = (name == emotion)

# Start in NEUTRAL state while waiting
set_emotion("NEUTRAL")

# Non-blocking serial read
def read_command():
    if supervisor.runtime.serial_bytes_available:
        line = sys.stdin.readline().strip().upper()
        return line
    return None

# Light sensor setup
light_sensor = analogio.AnalogIn(board.A0)

# Calibrated from real readings: about 43000-54000 in normal light
DARK_THRESHOLD = 20000

def is_dark():
    return light_sensor.value < DARK_THRESHOLD

# Non-blocking blink state for the "too dark" warning
blink_state = False
last_blink_toggle = time.monotonic()
BLINK_INTERVAL = 0.6

#  Main loop
print("MoodLight ready. Waiting for emotion commands...")

confirmed_emotion = "NEUTRAL"

while True:
    command = read_command()
    if command:
        print("Received:", command)
        if command in leds:
            confirmed_emotion = command
        else:
            # Unknown/unrecognized command -> fall back to NEUTRAL
            confirmed_emotion = "NEUTRAL"

    # Darkness check overrides normal emotion display
    if is_dark():
        now = time.monotonic()
        if now - last_blink_toggle > BLINK_INTERVAL:
            blink_state = not blink_state
            last_blink_toggle = now
        for name, led in leds.items():
            led.value = (name == "NEUTRAL" and blink_state)
    else:
        set_emotion(confirmed_emotion)