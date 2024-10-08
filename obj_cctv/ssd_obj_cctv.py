import cv2
import numpy as np

# Load pre-trained MobileNet SSD model for object detection
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "mobilenet_iter_73000.caffemodel")

# List of RTSP URLs for the cameras
ip_camera_urls = [
    "rtsp://admin:admin123@192.168.1.5:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:admin123@192.168.1.4:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:admin123@192.168.1.3:554/cam/realmonitor?channel=1&subtype=1",
]

# Open connections to all cameras
caps = [cv2.VideoCapture(url) for url in ip_camera_urls]

# Check if connections are successful
for i, cap in enumerate(caps):
    if not cap.isOpened():
        print(f"Error: Unable to open video stream from camera {i+1}")
        exit()

while True:
    frames = []

    # Capture frame-by-frame from each camera
    for cap in caps:
        ret, frame = cap.read()
        if ret:
            # Perform object detection on each frame
            blob = cv2.dnn.blobFromImage(
                cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5
            )
            net.setInput(blob)
            detections = net.forward()

            # Draw detection results on the frame
            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                if confidence > 0.5:  # Confidence threshold
                    idx = int(detections[0, 0, i, 1])
                    box = detections[0, 0, i, 3:7] * np.array(
                        [frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]]
                    )
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

            # Resize each frame to make a grid (optional based on your needs)
            frame_resized = cv2.resize(
                frame, (320, 240)
            )  # Resize to 320x240 for example
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

    # Display the resulting combined frame with detections
    cv2.imshow("CCTV Object Detection", combined_frame)

    # Press 'q' to exit the video stream
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release all captures and close windows
for cap in caps:
    cap.release()
cv2.destroyAllWindows()
