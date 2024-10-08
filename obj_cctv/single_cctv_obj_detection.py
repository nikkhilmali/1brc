import cv2
import mediapipe as mp

# Initialize MediaPipe Object Detection
mp_object_detection = mp.solutions.object_detection
mp_drawing = mp.solutions.drawing_utils

# Set up the MediaPipe object detector
object_detection = mp_object_detection.ObjectDetection(min_detection_confidence=0.5)

# RTSP URL of the camera stream
rtsp_url = "rtsp://admin:admin123@192.168.1.3:554/cam/realmonitor?channel=1&subtype=1"

# Open the RTSP stream
cap = cv2.VideoCapture(rtsp_url)
if not cap.isOpened():
    print("Error: Unable to open video stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to retrieve frame")
        break

    # Convert frame to RGB as MediaPipe works with RGB images
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for object detection
    results = object_detection.process(rgb_frame)

    # Draw detection boxes and landmarks on the frame
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(frame, detection)

    # Display the resulting frame with object detection
    cv2.imshow("IP Camera Stream with Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
