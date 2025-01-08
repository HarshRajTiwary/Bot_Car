import websocket
import time

# ESP32 WebSocket server address
esp_ip = "ws://192.168.239.191:81"

def send_pin_states(ws):
    while True:
        # Get pin states from the user
        pin_states = {
            "D12": input("Enter state for D12 (1 for HIGH, 0 for LOW): "),
            "D13": input("Enter state for D13 (1 for HIGH, 0 for LOW): "),
            "D14": input("Enter state for D14 (1 for HIGH, 0 for LOW): "),
            "D27": input("Enter state for D27 (1 for HIGH, 0 for LOW): "),
        }

        # Send states to ESP32
        for pin, state in pin_states.items():
            message = f"{pin}={state}"
            ws.send(message)
            print(f"Sent: {message}")
        print("All pins updated. Listening for next input...\n")
        time.sleep(1)  # Optional delay

# WebSocket connection
def on_open(ws):
    print("Connected to ESP32 WebSocket server")
    send_pin_states(ws)

def on_message(ws, message):
    print(f"Received: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

# Connect to WebSocket server
ws = websocket.WebSocketApp(
    esp_ip,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close,
)

ws.run_forever()
