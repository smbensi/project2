from scipy.signal import convolve2d
import numpy as np
import cv2

# TODO : create a new class to keep the spatial and temporal properties
# In the original paper they defined these params:
# alpha_t = 0.1
# alpha_f = 0.01
# alpha_s = 0.05
# phi = 0.05
# k = sqrt(3)

class Fg_map:
    def __init__(self):
        self.M_t = None
        self.M_s = None
        self.alpha_t = 0.1 # temporal learning rate
        self.alpha_s = 0.05 # spatial learning rate
        self.neighborhood = 3
        self.omega = self.neighborhood**2
        self.fg_prob_map = None

    def temporal_prop(self,D_t):
        """
        M_t : estimated by recent history of detection results
        alpha_t : learning rate [0,1]
        D_t : binary detection map
        """

        self.M_t = (1-self.alpha_t)*self.M_t + self.alpha_t*D_t 


    def spatial_prop(self,D_t):
        """measures the coherency of nearby pixels as foreground

        Args:
            D_t : binary detection map

        neighborhood: denotes a spatial neighborhoodborhood
        omega is the area of neighborhoodborhood
        """
        s_n = (1/self.omega)*convolve2d(D_t,np.ones(self.neighborhood,mode='same'))
        self.M_s = (1- self.alpha_s)*self.M_s + self.alpha_s*s_n

    def fg_prob_map(self):
        """
            computes the foreground probability map
        """

        self.fg_prob_map = self.M_t * self.M_s

    def mult_mask_fg_prob(self,mask):
        return mask*self.fg_prob_map

    def loop(self, img, mask):
        self.temporal_prop(mask)
        self.spatial_prop(mask)
        
