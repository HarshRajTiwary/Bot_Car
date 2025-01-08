import cv2
from utils.predictor import predict_color  # Import the prediction function

def capture_and_predict_rgb():
    # ESP32-CAM stream URL
    esp32_url = "http://192.168.239.123:81/stream"

    # Initialize video capture from ESP32-CAM
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open ESP32-CAM stream.")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from ESP32-CAM.")
            break

        # Draw a circle at the center of the frame
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        radius = 10
        cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
        cv2.imshow("Frame", frame)

        # Get the RGB values from the center of the circle
        center_pixel = frame[center_y, center_x]
        r, g, b = center_pixel
        test_rgb = [r, g, b]

        # Predict the color label
        predicted_label = predict_color(test_rgb)
        print(f"Predicted label for RGB {test_rgb}: {predicted_label}")

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_predict_rgb()
