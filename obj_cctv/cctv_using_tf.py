import cv2
import numpy as np

# Load SSD MobileNet V2 model and label map
model_path = "frozen_inference_graph.pb"
config_path = "ssd_mobilenet_v2_coco_2018_03_29.pbtxt"

# Load the network
net = cv2.dnn_DetectionModel(model_path, config_path)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Load class labels
with open("object_detection_classes_coco.txt", "rt") as f:
    labels = f.read().rstrip("\n").split("\n")

# RTSP URL of the camera stream
rtsp_url = "rtsp://admin:admin123@192.168.1.3:554/cam/realmonitor?channel=1&subtype=1"

# Open the RTSP stream
# cap = cv2.VideoCapture(rtsp_url)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Error: Unable to open video stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to retrieve frame")
        break

    # Object detection using the network
    class_ids, confidences, boxes = net.detect(frame, confThreshold=0.5)

    # Loop over the detections
    for class_id, confidence, box in zip(class_ids, confidences, boxes):
        label = f"{labels[class_id]}: {confidence:.2f}"

        # Draw the bounding box and label on the frame
        cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
        cv2.putText(
            frame,
            label,
            (box[0], box[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            2,
        )

    # Display the resulting frame
    cv2.imshow("IP Camera Stream with Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
