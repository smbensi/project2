import numpy as np
import random 
import cv2
import math
from scipy import signal

from settings import params


'''
SELECTIVE ATTENTION SCHEME

video image can be categorized into
    1. background region                        -> sparse attention/scanning
    2. unimportant dynamic scene region         -> sparse attention/scanning
    3. important moving object appearing region -> attention on these region
GOAL: focus on foreground area --> necessary calculation would be reduced significantly

To get active sampling mask we use 3 properties: temporal, spatial, frequency
Based on these properties we make a fg propability map P_FG

active sampling strategy updated every frame according to (P_FG)^(t-1)
3 sampling strategies:
    1. randomly scattered sampling (RSS)
    2. spatially expanding importance sampling (SEIS)
    3. surprise pixel sampling
using these sampling methods we build the sampling mask M_t

Using the mask M_t, selective pixel-wise background subtraction is performed only for
the pixels of M_t(n)=1


'''


#### FOREGROUND PROBABILITY MAP GENERATION
#### ESTIMATION OF FOREGROUND PROPERTIES
# alpaha_t 0.1 , alpha_f = 0.01, alpha_s = 0.05, phi = 0.05, k=sqrt(3) in section6
class FgMap():

    def __init__(self, frame_gray) -> None:
        self.frame = frame_gray

        self.temporal_prop = np.zeros_like(frame_gray)
        self.spatial_prop  = np.zeros_like(frame_gray)
        self.freq_prop     = np.zeros_like(frame_gray)
        
        self.detection_mask = np.zeros_like(frame_gray)
        self.mask_t_1       = np.zeros_like(frame_gray)
        self.mask_t_2       = np.zeros_like(frame_gray)
        
        self.fg_map       = np.zeros_like(frame_gray)

    def update_temporal(self):
        alpha_t = params.ALPHA_T # defined in sction 6 of the paper
        self.temporal_prop = (1-alpha_t)* self.temporal_prop + alpha_t * self.detection_mask

    def compute_s_t(self):
        s_t = np.zeros_like(self.frame)
        omega = params.OMEGA
        kernel = np.ones((omega,omega))
        s_t = (1/omega**2)*signal.correlate2d(self.detection_mask,kernel,mode='same')
        return s_t


    def update_spatial(self):
        alpha_s = params.ALPHA_S
        s_t = self.compute_s_t()
        self.spatial_prop = (1-alpha_s)*self.spatial_prop + alpha_s * s_t
        
    def compute_f_t(self):
        blinking = (self.mask_t_1 !=self.mask_t_2)&(self.mask_t_1 !=self.detection_mask)
        f_t = blinking.astype(int)
        return f_t

    def update_freq(self):
        alpha_f = params.ALPHA_F
        f_t = self.compute_f_t()
        self.freq_prop = (1-alpha_f)*self.freq_prop + alpha_f*f_t 

    def update_properties(self):
        self.update_temporal()
        self.update_spatial()
        self.update_freq()
    
    def calc_fg_map(self,frame,detection_mask):
        self.frame = frame
        self.detection_mask = detection_mask        
        self.update_properties()
        self.mask_t_2 = self.mask_t_1
        self.mask_t_1 = detection_mask
        self.fg_map = self.temporal_prop * self.spatial_prop * (1-self.temporal_prop)

        # essayons ca pour voir si ca marche
        return self.fg_map



class ActiveSamplingMask():
    def __init__(self,frame) -> None:

        # Params to update every frame
        self.frame          = frame
        self.detection_mask = np.zeros_like(frame)
        self.fg_map = np.zeros_like(frame)

        # the active sampling mask is obtained by a combination of 3 masks by a 
        # pixel-wise OR as M_t = M_RS_t or M_SEI_t or M_SP_t
        self.samp_mask = np.zeros_like(frame)

        # The sampling mask is obtained by a combination of 3 masks
        self.rand_scattered_mask    = np.zeros_like(frame)
        self.spatial_exp_imp_mask   = np.zeros_like(frame)
        self.surprise_pix_samp_mask = np.zeros_like(frame)


        self.phi = params.PHI # for Random Scattered usuallly between [0.05,0.1]
        self.k_sei = params.K_SEI

    def calc_rand_scattered_sampling(self):
        '''
            phi% pixels of entire pixels are selected through randomly
            scattered sampling
        '''
        frame = self.frame
        D_t = self.detection_mask
        N = np.size(frame) # nb of pixels in frame 
        N_reuse = np.sum(D_t)
        nb_rand_samp = np.round(self.phi*N - N_reuse).astype(int)
        
        indices = [(i,j) for i in range(frame.shape[0]) for j  in range(frame.shape[1]) 
                            if D_t[i,j] < 0.5]

        # randomly selct pixels that are not in the detection map 
        rand_ind = np.array(random.sample(indices,nb_rand_samp))
        self.rand_scattered_mask[rand_ind[:,0],rand_ind[:,1]] = 1


        if params.DEBUG:
            debg = np.expand_dims(frame,axis=2)
            debg = np.repeat(debg,3,axis=2)
            debg[self.rand_scattered_mask>0,2]=255
            cv2.imshow("random scattered sampling", debg)
            cv2.waitKey(1)

    def calc_spatially_expanding_importance_sampling(self):
        ''' 
            RS is too sparse to construct a complete fg region and might miss small
            objects. necessary to fill the space between sparse points in the fg region
        '''
        frame = self.frame
        P_FG = self.fg_map
        N = np.size(frame)
        Ns = np.sum(self.rand_scattered_mask)
        omega_s = self.k_sei*math.sqrt(N/Ns)
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if self.rand_scattered_mask[i,j] == 1:
                    phi_t = np.round(P_FG[i,j]*omega_s)
                    # TODO bug ici 
                    # TypeError: slice indices must be integers or None or have an __index__ method
                    self.spatial_exp_imp_mask[i-phi_t:i+phi_t,j-phi_t:j+phi_t]=1
        # TODO rajouter du debug

    def calc_surprise_pixel_sampling(self):
        pass

    def calc_sampling_mask(self,frame,detection_mask,fg_map):
        '''
            to keep the efficiency of the additional load (computation of fg map)
            restrict the SEARCH SPACE
            extract the candidate pixel positions to run the background subtraction
            and model update

            Also extract the positions randomly as 5% of entire pixels to detect the
            newly appeared objects
        '''
        self.frame = frame
        self.detection_mask = detection_mask
        self.fg_map = fg_map

        self.calc_rand_scattered_sampling()
        self.calc_spatially_expanding_importance_sampling()
        self.calc_surprise_pixel_sampling()
        self.samp_mask = (self.rand_scattered_mask 
                            or self.surprise_pix_samp_mask
                            or self.spatial_exp_imp_mask).astype(int)
        return self.samp_mask