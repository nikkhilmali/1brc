import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Initialize MediaPipe Object Detection
# base_options = python.BaseOptions(
#     model_asset_path="efficientdet_lite0.tflite"
# )  # Path to your model
# options = vision.ObjectDetectorOptions(base_options=base_options, score_threshold=0.5)
# detector = vision.ObjectDetector.create_from_options(options)



# Initialize video capture (replace with your IP camera URL if needed)
cap = cv2.VideoCapture(0)  # Use 0 for webcam or replace with IP camera URL

if not cap.isOpened():
    print("Error: Unable to access the camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame.")
        break

    # Convert the BGR image to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Detect objects in the frame
    detection_result = detector.detect(mp_image)

    # Visualize the detection results
    image_copy = np.copy(rgb_frame)
    if detection_result.detections:
        for detection in detection_result.detections:
            # Get the bounding box using methods
            bbox = detection.bounding_box

            # Draw the bounding box using bbox methods
            # cv2.rectangle(
            #     image_copy,
            #     (
            #         int(bbox.xmin * frame.shape[1]),
            #         int(bbox.ymin * frame.shape[0]),
            #     ),  # Scale to frame size
            #     (
            #         int(bbox.xmax * frame.shape[1]),
            #         int(bbox.ymax * frame.shape[0]),
            #     ),  # Scale to frame size
            #     (0, 255, 0),
            #     2,
            # )

    # Convert the annotated image back to BGR for display
    annotated_image = cv2.cvtColor(image_copy, cv2.COLOR_RGB2BGR)

    # Display the resulting frame
    cv2.imshow("Live Object Detection", annotated_image)

    # Press 'q' to exit the video stream
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
