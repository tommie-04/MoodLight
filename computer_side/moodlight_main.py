import cv2
from deepface import DeepFace
from led_controller import LEDController

# Configuration
SERIAL_PORT = "/dev/tty.usbmodem101"    # should be your confirmed M0 port
CAMERA_INDEX = 0                        # confirmed working camera
DEBOUNCE_THRESHOLD = 5                  # consecutive frames needed to confirm a state change

# DeepFace outputs 7 emotions
EMOTION_MAP = {
    "happy": "HAPPY",
    "disgust": "DISGUST",
    "angry": "ANGRY",
    "surprise": "SURPRISE",
    "neutral": "NEUTRAL",
    "sad": "NEUTRAL",
    "fear": "NEUTRAL",
}

# Set up webcam and LED controller
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("Error: could not open webcam.")
    exit()

led = LEDController(SERIAL_PORT)

print("MoodLight running. Press 'q' to quit.")

# Debounce state
candidate_emotion = None
candidate_count = 0
confirmed_emotion = "NEUTRAL"

# Main loop(Only on when emotions happen on 5 times in a row or more)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: failed to grab frame.")
        break

    try:
        results = DeepFace.analyze(
            frame,
            actions=['emotion'],
            enforce_detection=False,
            silent=True
        )
        result = results[0] if isinstance(results, list) else results
        raw_emotion = result['dominant_emotion']
        mapped_emotion = EMOTION_MAP.get(raw_emotion, "NEUTRAL")

        if mapped_emotion == candidate_emotion:
            candidate_count += 1
        else:
            candidate_emotion = mapped_emotion
            candidate_count = 1

        if candidate_count >= DEBOUNCE_THRESHOLD and confirmed_emotion != candidate_emotion:
            confirmed_emotion = candidate_emotion
            led.send_emotion(confirmed_emotion)

        print(f"Raw: {raw_emotion:10s} | Confirmed: {confirmed_emotion}")

    except Exception as e:
        print("Detection error:", e)

    cv2.imshow("MoodLight - press q to quit", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup 
cap.release()
cv2.destroyAllWindows()
led.close()
