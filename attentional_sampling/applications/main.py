import numpy as np
import cv2

def main():
    # CREATE A STREAM: VIDEO OR CAMERA
    filename = "../data/static_bg.mp4" 
    cap = cv2.VideoCapture(filename)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            # raise ErrorInFrameReading
            break

        cv2.imshow("frame", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break



if __name__=="__main__":
    main()