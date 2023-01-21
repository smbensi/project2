import numpy as np
import cv2
import sys
import logging

# import bg_sub
# from bg_sub.utils.detection_1st.motion_comp import MotionComp
# from bg_sub.utils.detection_1st.motion_comp import MotionComp
from bg_sub.utils.detection_1st.motion_comp import MotionComp
from bg_sub.utils.detection_1st.dual_sgm import SGM
from bg_sub.settings import params
from bg_sub.pipeline import pipe_1st
def main():
    filename = "/home/mat/Documents/project2/woman.mp4"
    # filename = sys.argv[1]
    print(filename)

    cap = cv2.VideoCapture(filename)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    
    frame_nb = 0
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if frame_nb ==0:
            mot_comp = MotionComp(frame_gray)
            params.DUAL_SGM = SGM(frame_gray)

        else:
            pipe_1st.pipe_detection(frame_gray)
            mot_comp.find_corners(frame_gray)
        
        frame_nb+=1
        
        cv2.imshow("frame", frame)
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()