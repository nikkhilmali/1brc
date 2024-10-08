import cv2

# Replace with your IP camera's RTSP URL
# Example: "rtsp://<username>:<password>@<camera-ip>:<port>/<path>"
rtsp_url = "rtsp://admin:admin123@192.168.1.5:554/cam/realmonitor?channel=1&subtype=1"

# Open a connection to the RTSP stream (using TCP)
cap = cv2.VideoCapture(rtsp_url)

# Check if the connection was successful
if not cap.isOpened():
    print("Error: Unable to open video stream")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to retrieve frame")
        break

    # Display the resulting frame
    cv2.imshow("IP Camera Stream", frame)

    # Press 'q' to exit the video stream
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the capture when done
cap.release()
cv2.destroyAllWindows()
