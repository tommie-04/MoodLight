import board
import digitalio
import supervisor
import sys


# One color per state, including NEUTRAL
led_pins = {
    
    "NEUTRAL":  board.D7,   # Clear/White LED — steady baseline state
    "DISGUST":      board.D6,   # Blue LED
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

# Start in NEUTRAL state so the lamp is never "dark" while waiting
set_emotion("NEUTRAL")

# Non-blocking serial read 
def read_command():
    if supervisor.runtime.serial_bytes_available:
        line = sys.stdin.readline().strip().upper()
        return line
    return None

# Main loop
print("MoodLight ready. Waiting for emotion commands...")

while True:
    command = read_command()
    if command:
        print("Received:", command)
        if command in leds:
            set_emotion(command)
        else:
            # Unknown/unrecognized command -> back to NEUTRAL
            set_emotion("NEUTRAL")