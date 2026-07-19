import cv2
from deepface import DeepFace

# ---- 1. Open the webcam ----
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: could not open webcam.")
    exit()

print("Press 'q' to quit.")

# ---- 2. Main loop: read frames and analyze emotion ----
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
        dominant_emotion = result['dominant_emotion']
        print("Detected emotion:", dominant_emotion)
    except Exception as e:
        print("Detection error:", e)

    # ---- 3. Show the camera feed ----
    cv2.imshow("MoodLight - press q to quit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ---- 4. Cleanup ----
cap.release()
cv2.destroyAllWindows()
