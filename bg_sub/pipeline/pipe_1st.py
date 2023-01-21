import numpy as np
import cv2

from bg_sub.utils.detection_1st import dual_sgm
from bg_sub.settings import params

def pipe_detection(frame):
    
    assert frame.ndim==2, f"wrong dimension of {frame}"

    params.DUAL_SGM.update_mean(frame)
    params.DUAL_SGM.update_variance(frame)
    params.DUAL_SGM.update_age()