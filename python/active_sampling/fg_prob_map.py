from scipy.signal import convolve2d
import numpy as np

# TODO : create a new class to keep the spatial and temporal properties
class Fg_map:
    def __init__(self):
        self.M_t = None
        self.M_s = None
        self.alpha_t = 1 # temporal learning rate
        self.alpha_s = 1 # spatial learning rate
        self.neigh = 3
        self.omega = self.neigh**2
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

        neigh: denotes a spatial neighborhood
        omega is the area of neighborhood
        """
        s_n = (1/self.omega)*convolve2d(D_t,np.ones(self.neigh,mode='same'))
        self.M_s = (1- self.alpha_s)*self.M_s + self.alpha_s*s_n

    def fg_prob_map(self):
        """
            computes the foreground probability map
        """

        self.fg_prob_map = self.M_t * self.M_s

    def mult_mask_fg_prob(self,mask):
        return mask*self.fg_prob_map
