import numpy as np
import cv2
import sys
import logging

def main():
    filename = sys.argv[1]
    print(filename)

    cap = cv2.VideoCapture(filename)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            print("No frame")
            continue
        cv2.imshow("frame", frame)
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()