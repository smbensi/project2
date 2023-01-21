import cv2
import sys

def main():
    # video test
    filename = sys.argv[1]
    print(filename)
    cap = cv2.VideoCapture()
    cap.open(filename)

    # Check if the file is opened successfully
    if not cap.isOpened():
        print("Error opening the file")

    while True:
        ret,  frame = cap.read()
        if ret == False:
            print("didn't catch the frame")
            break

        cv2.imshow('Frame', frame)
        cv2.waitKey(1)

    # When everything is done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()