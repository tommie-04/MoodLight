cat > README.md << 'EOF'
# MoodLight – AI Emotion-Aware Study Lamp

Detects the user's facial emotion via webcam and reflects it through 
color-coded LEDs controlled by an Adafruit Metro M0 Express (CircuitPython).

## Status: In Progress (Hackathon Day 1 complete)
- [x] M0 listens for serial commands and controls 5 emotion-coded LEDs
- [x] Computer-side Python script sends commands via pyserial
- [ ] Real-time facial emotion detection (DeepFace)
- [ ] End-to-end integration

## Hardware
- Adafruit Metro M0 Express
- 5 LEDs (yellow / blue / red / green / clear)

## Structure
- `m0_side/code.py` – CircuitPython script running on the M0
- `computer_side/led_controller.py` – sends emotion commands over serial
EOF