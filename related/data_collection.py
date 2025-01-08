import cv2
import pandas as pd
import time

output_file = "dataset/color_data.csv"
try:
    data = pd.read_csv(output_file)
except FileNotFoundError:
    data = pd.DataFrame(columns=["R", "G", "B", "Label"])

def capture_and_store_rgb():
    esp32_url = "http://192.168.239.123:81/stream"

    cap = cv2.VideoCapture(esp32_url)

    if not cap.isOpened():
        print("Error: Could not open ESP32-CAM stream.")
        return

    while True:
        color_label = input("Enter the color label (or type 'exit' to quit): ")
        if color_label.lower() == 'exit':
            break

        print(f"Capturing RGB values for label '{color_label}' for 15 seconds. Press 'q' to quit early.")

        start_time = time.time()
        rgb_values = []

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

            elapsed_time = time.time() - start_time
            if elapsed_time > 15:
                break

            center_pixel = frame[center_y, center_x]
            r, g, b = center_pixel
            rgb_values.append([r, g, b, color_label])

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        global data
        new_data = pd.DataFrame(rgb_values, columns=["R", "G", "B", "Label"])
        data = pd.concat([data, new_data], ignore_index=True)
        data.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_store_rgb()