import numpy as np
from scipy.signal import convolve2d
import cv2


class Fg_map():
    def __init__(self,frame) -> None:
        self.temporal_lr = None
        self.spatial_lr = None
        self.temporal_map = np.zeros_like(frame) #must be the same dimension as the input frame
        self.spatial_map = np.zeros_like(frame) #must be the same dimension as the input frame

    def build_fg_map(self,D_t):
        '''
            assumption: objects movements are smooth spatially and temporally
            build the foreground probability map using TEMPORAL and SPATIAL 
            properties
        '''
        self.calc_spatial_prop(D_t)
        self.calc_temporal_prop(D_t)
        p_fg = self.temporal_map*self.spatial_map
        return p_fg

    def calc_temporal_prop(self,D_t):
        '''
            M_t: defined as recent history of the foreground at each pixel

            Input:
                D_t : binary detection map D_t(n)=1 if belongs to foreground
                      0 otherwise
        '''
        self.temporal_map = (1-self.temporal_lr)*self.temporal_map + \
            self.temporal_lr * D_t
    
    def calc_spatial_prop(self, D_t):
        '''
            M_s: measures the coherency of nearby pixels of foreground

            Input:
                D_t : binary detection map D_t(n)=1 if belongs to foreground
                      0 otherwise
        '''
        
        # area of neighborhood
        omega = 3
        D_t_conv = convolve2d(D_t,np.ones(omega,omega),mode="same")

        self.spatial_map = (1-self.spatial_lr)* self.spatial_map + \
            self.spatial_lr*(1/omega**2)*D_t_conv