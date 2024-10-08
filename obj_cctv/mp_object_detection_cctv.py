import cv2
import mediapipe as mp

# Initialize MediaPipe Object Detection
mp_object_detection = mp.solutions.object_detection
mp_drawing = mp.solutions.drawing_utils

# List of RTSP URLs for the cameras
ip_camera_urls = [
    "rtsp://admin:admin123@192.168.1.5:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:admin123@192.168.1.4:554/cam/realmonitor?channel=1&subtype=1",
    "rtsp://admin:admin123@192.168.1.3:554/cam/realmonitor?channel=1&subtype=1"
]

# Open connections to all cameras
caps = [cv2.VideoCapture(url) for url in ip_camera_urls]

# Check if connections are successful
for i, cap in enumerate(caps):
    if not cap.isOpened():
        print(f"Error: Unable to open video stream from camera {i+1}")
        exit()

# Initialize MediaPipe object detector
with mp_object_detection.ObjectDetection(model_selection=0, min_detection_confidence=0.5) as object_detection:
    while True:
        frames = []

        # Capture frame-by-frame from each camera
        for cap in caps:
            ret, frame = cap.read()
            if ret:
                # Convert the BGR image to RGB for MediaPipe processing
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Detect objects in the frame
                results = object_detection.process(image_rgb)
                
                # Draw object detection results on the frame
                if results.detections:
                    for detection in results.detections:
                        mp_drawing.draw_detection(frame, detection)
                
                # Resize each frame to make a grid (optional based on your needs)
                frame_resized = cv2.resize(frame, (320, 240))  # Resize to 320x240 for example
                frames.append(frame_resized)
            else:
                frames.append(np.zeros((240, 320, 3), dtype=np.uint8))  # Placeholder if frame not available

        # Combine frames into a grid (2 rows, 2 columns for example)
        if len(frames) == 3:
            row1 = np.hstack((frames[0], frames[1]))
            row2 = np.hstack((frames[2], np.zeros_like(frames[2])))  # Add blank space if necessary
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
