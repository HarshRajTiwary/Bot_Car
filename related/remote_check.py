import websocket
from pynput import keyboard
import time

esp_ip = "ws://192.168.239.191:81"

def on_open(ws):
    print("Connected to ESP32 WebSocket server")
    print("Use the arrow keys to control the car:")
    print("↑: Forward, ↓: Backward, →: Turn Right, ←: Turn Left, SPACE: Stop")

    def on_press(key):
        try:
            if key == keyboard.Key.up:  # Forward (D12 and D27 HIGH)
                ws.send("D12=1")
                ws.send("D27=1")
                ws.send("D13=0")
                ws.send("D14=0")
                print("Command Sent: Forward")

            elif key == keyboard.Key.down:  # Backward (D13 and D14 HIGH)
                ws.send("D12=0")
                ws.send("D27=0")
                ws.send("D13=1")
                ws.send("D14=1")
                print("Command Sent: Backward")

            elif key == keyboard.Key.left:  # Turn Left (D12 and D14 HIGH)
                ws.send("D12=1")
                ws.send("D27=0")
                ws.send("D13=0")
                ws.send("D14=1")
                print("Command Sent: Turn Left")

            elif key == keyboard.Key.right:  # Turn Right (D27 and D13 HIGH)
                ws.send("D12=0")
                ws.send("D27=1")
                ws.send("D13=1")
                ws.send("D14=0")
                print("Command Sent: Turn Right")

            elif key == keyboard.Key.space:  # Stop (All LOW)
                ws.send("D12=0")
                ws.send("D27=0")
                ws.send("D13=0")
                ws.send("D14=0")
                print("Command Sent: Stop")
        except Exception as e:
            print(f"Error during key press: {e}")

    def on_release(key):
        pass

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

def on_message(ws, message):
    print(f"Received: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

ws = websocket.WebSocketApp(
    esp_ip,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)

ws.run_forever()
