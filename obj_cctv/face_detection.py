import threading
import cv2

from deepface import DeepFace


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print(cap)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


counter = 0
face_match = False

refcence_img = cv2.imread("refrence.jpg")
print(refcence_img)

def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, refcence_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False

while True:
    ret, frame = cap.read()
    print("yes")
    print(ret, frame)

    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),))
            except ValueError:
                # print("face not found")
                pass
        counter += 1

        if face_match:
            cv2.putText(frame, "MATCH!", (20,450),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, "NO MATCH!", (20,450),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3) #BGR

        cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break


cv2.destroyAllWindows()