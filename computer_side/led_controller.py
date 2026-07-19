import serial
import time


class LEDController:
    """
    Wraps serial communication with the M0 board.
    The Day 2 AI script only needs to import this class and call
    send_emotion() — no need to worry about serial connection details.
    """

    def __init__(self, port, baud_rate=115200):
        self.ser = serial.Serial(port, baud_rate, timeout=1)
        time.sleep(2)  # Wait for the M0 to finish its auto-reset
        self.last_emotion = None  # Track last sent emotion for de-duplication

    def send_emotion(self, emotion):
        """
        Only sends a command when the emotion actually changes.
        This avoids flooding the serial connection with redundant
        messages every frame, and keeps LED transitions clean instead
        of flickering.
        """
        emotion = emotion.strip().upper()
        if emotion == self.last_emotion:
            return  # No change, skip sending
        message = emotion + "\n"
        self.ser.write(message.encode("utf-8"))
        self.last_emotion = emotion
        print(f"[LED] Sent: {emotion}")

    def close(self):
        self.ser.close()


# ---- Standalone test when running this file directly ----
if __name__ == "__main__":
    SERIAL_PORT = "/dev/tty.usbmodem101"   # Confirmed M0 port on this machine

    controller = LEDController(SERIAL_PORT)

    for emotion in ["HAPPY", "SAD", "ANGRY", "SURPRISE", "NEUTRAL"]:
        controller.send_emotion(emotion)
        time.sleep(2)

    controller.close()