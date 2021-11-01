import numpy as np
import cv2
import MCDWrapper

import time


np.set_printoptions(precision=2, suppress=True)
cap = cv2.VideoCapture('new_vid/20210104_123240_0.mp4')
mcd = MCDWrapper.MCDWrapper()
isFirst = True

frNb = 0
width = int(cap.get(3))
height = int(cap.get(4))
out = cv2.VideoWriter('detetction.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (width,height))


while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    mask = np.zeros(gray.shape, np.uint8)
    if (isFirst):
        mcd.init(gray)
        isFirst = False
    else:
        mask = mcd.run(gray)
    frame[mask > 0, 2] = 255

    out.write(frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    frNb +=1
    if frNb == 170:
        break
    time.sleep(0.01)
    
cap.release()
out.release()

cv2.destroyAllWindows()

