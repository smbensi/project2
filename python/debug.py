import numpy as np
import cv2
import MCDWrapper


from bg_sub.utils.active_samp.sampling_map_gen import FgMap, ActiveSamplingMask

import time
# import active_sampling.rand_scattered_samp as active_sampling
# import active_sampling.fg_prob_map as fg_map


np.set_printoptions(precision=2, suppress=True)
# cap = cv2.VideoCapture('python/new_vid/20210104_123240_0.mp4')
cap = cv2.VideoCapture('woman.mp4')
mcd = MCDWrapper.MCDWrapper()
isFirst = True

frNb = 0
width = int(cap.get(3))
height = int(cap.get(4))
# out = cv2.VideoWriter('detetction.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (width,height))
# foreground_probability_map = fg_map.Fg_map()

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    # if not isFirst:
    #     active_sampling.rand_mask(img=gray,mask=mask)

    mask = np.zeros(gray.shape, np.uint8)
    if (isFirst):
        mcd.init(gray)
        fg_map = FgMap(gray)
        active_mask = ActiveSamplingMask(gray)
        isFirst = False
    else:
        mask = mcd.run(gray)
        mask_normalized = mask/255
        mapp = fg_map.calc_fg_map(gray, mask_normalized)
        maskk = active_mask.calc_sampling_mask(gray,mask_normalized, mapp)
        # mask2 = active_mask.calc_spatially_expanding_importance_sampling()
    frame[mask > 0, 2] = 255
    # if not isFirst:
        # foreground_probability_map.loop(frame, mask)
    # out.write(frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    frNb +=1
    # if frNb == 170:
    #     break
    time.sleep(0.01)
print(f"nb of frames: {frNb}")
cap.release()
# out.release()

cv2.destroyAllWindows()

