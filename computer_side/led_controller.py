import serial
import time


class LEDController:
    """
    Wraps serial communication with the M0 board.
    """

    def __init__(self, port, baud_rate=115200):
        self.ser = serial.Serial(port, baud_rate, timeout=1)
        time.sleep(2)  # Wait for the M0 to finish its auto-reset
        self.last_emotion = None  # Track last sent emotion for de-duplication

    def send_emotion(self, emotion):
        """
        Only sends a command when the emotion actually changes.
        """
        emotion = emotion.strip().upper()
        if emotion == self.last_emotion:
            return                          # No change, skip sending
        message = emotion + "\n"
        self.ser.write(message.encode("utf-8"))
        self.last_emotion = emotion
        print(f"[LED] Sent: {emotion}")

    def close(self):
        self.ser.close()


# ---- Standalone test when running this file directly ----
if __name__ == "__main__":
    SERIAL_PORT = "/dev/tty.usbmodem101"    # should be your M0 port 

    controller = LEDController(SERIAL_PORT)

    for emotion in ["HAPPY", "SAD", "ANGRY", "SURPRISE", "NEUTRAL"]:
        controller.send_emotion(emotion)
        time.sleep(2)

    controller.close()