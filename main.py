import cv2
import websocket
from utils.predictor import predict_color

esp_ip = "ws://192.168.239.191:81"

def send_command(ws, command):
    try:
        ws.send(command)
    except Exception as e:
        print(f"Error sending command: {e}")

def control_car(ws, predicted_label):
    if predicted_label == "empty":  # Move forward
        send_command(ws, "D12=1")  # Motor 1 Forward
        send_command(ws, "D27=1")  # Motor 2 Forward
        send_command(ws, "D13=0")  # Motor 1 Stop
        send_command(ws, "D14=0")  # Motor 2 Stop
        print("Car moving forward.")
    elif predicted_label == "red":  # Stop
        send_command(ws, "D12=0")
        send_command(ws, "D27=0")
        send_command(ws, "D13=0")
        send_command(ws, "D14=0")
        print("Car stopped.")
    elif predicted_label == "green":  # Turn left
        send_command(ws, "D12=1")
        send_command(ws, "D27=0")
        send_command(ws, "D13=0")
        send_command(ws, "D14=1")
        print("Car turning left.")
    elif predicted_label == "blue":  # Turn right
        send_command(ws, "D12=0")
        send_command(ws, "D27=1")
        send_command(ws, "D13=1")
        send_command(ws, "D14=0")
        print("Car turning right.")
    else:
        print("Unknown color detected, stopping the car.")
        send_command(ws, "D12=0")
        send_command(ws, "D27=0")
        send_command(ws, "D13=0")
        send_command(ws, "D14=0")

def capture_and_predict_rgb(ws):
    esp32_cam_url = "http://192.168.239.123:81/stream"

    cap = cv2.VideoCapture(esp32_cam_url)

    if not cap.isOpened():
        print("Error: Could not open ESP32-CAM stream.")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from ESP32-CAM.")
            break

        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        radius = 10
        cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
        cv2.imshow("Frame", frame)

        center_pixel = frame[center_y, center_x]
        r, g, b = center_pixel
        test_rgb = [r, g, b]

        predicted_label = predict_color(test_rgb)
        print(f"Predicted label for RGB {test_rgb}: {predicted_label}")

        control_car(ws, predicted_label)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def on_open(ws):
    print("Connected to ESP32 WebSocket server.")
    print("Starting color prediction and car control.")
    capture_and_predict_rgb(ws)

def on_message(ws, message):
    print(f"Received: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed.")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        esp_ip,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()
