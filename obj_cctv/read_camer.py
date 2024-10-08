import cv2
import numpy as np
import time

# List of RTSP URLs for the cameras
ip_camera_urls = [
    "rtsp://admin:admin123@192.168.1.5:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:admin123@192.168.1.4:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:admin123@192.168.1.3:554/cam/realmonitor?channel=1&subtype=1",
]

# Open connections to all cameras
caps = [cv2.VideoCapture(url) for url in ip_camera_urls]

# Retry mechanism for opening the streams
for i, cap in enumerate(caps):
    retries = 5
    while retries > 0 and not cap.isOpened():
        print(f"Retrying to open video stream from camera {i+1}")
        cap.open(ip_camera_urls[i])
        retries -= 1
        time.sleep(1)  # Delay to allow stream to open

    if not cap.isOpened():
        print(f"Error: Unable to open video stream from camera {i+1} after retries")
        exit()

while True:
    frames = []

    # Capture frame-by-frame from each camera
    for cap in caps:
        ret, frame = cap.read()
        if ret:
            # Optionally resize based on original frame size
            h, w = frame.shape[:2]
            frame_resized = cv2.resize(frame, (w // 2, h // 2))  # Resize proportionally
            frames.append(frame_resized)
        else:
            frames.append(
                np.zeros((240, 320, 3), dtype=np.uint8)
            )  # Placeholder if frame not available

    # Combine frames into a grid (2 rows, 2 columns for example)
    if len(frames) == 3:
        row1 = np.hstack((frames[0], frames[1]))
        row2 = np.hstack(
            (frames[2], np.zeros_like(frames[2]))
        )  # Add blank space if necessary
        combined_frame = np.vstack((row1, row2))
    else:
        combined_frame = np.hstack(frames)

    # Display the resulting combined frame
    cv2.imshow("Multiple IP Camera Streams", combined_frame)

    # Press 'q' to exit the video stream
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    time.sleep(0.05)  # Add a small delay to prevent CPU overuse

# Release all captures and close windows
for cap in caps:
    cap.release()
cv2.destroyAllWindows()
