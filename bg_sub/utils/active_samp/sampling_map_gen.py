import numpy as np
import random 
import cv2
import math

from settings import params

class ActiveSamplingMap():
    def __init__(self,frame) -> None:
        # the active sampling mask is obtained by a combination of 3 masks by a 
        # pixel-wise OR as M_t = M_RS_t or M_SEI_t or M_SP_t
        self.samp_mask = np.zeros_like(frame)
        self.rand_scattered_mask = np.zeros_like(frame)
        self.spatial_exp_imp_mask = np.zeros_like(frame)
        self.phi = 0.05 # for Random Scattered usuallly between [0.05,0.1]
        self.k_sei = np.sqrt(3)

    def calc_rand_scattered_sampling(self,frame, D_t, P_FG):
        '''
            phi% pixels of entire pixels are selected through randomly
            scattered sampling
        '''
        N = np.size(frame) # nb of pixels in frame 
        N_reuse = np.sum(D_t)
        nb_rand_samp = np.round(self.phi*N - N_reuse)
        
        indices = [(i,j) for i in range(frame.shape[0]) for j  in range(frame.shape[1]) 
                            if D_t[i,j] < 0.5]

        # randomly selct pixels that are not in the detection map 
        rand_ind = np.array(random.sample(indices,nb_rand_samp))
        self.rand_scattered_mask[rand_ind[:,0],rand_ind[:,1]] = 1

        # for debugging
        if params.DEBUG:
            cv2.imshow("random scattered sampling", frame*self.rand_scattered_mask)
            cv2.waitKey(1)

    def calc_spatially_expanding_importance_sampling(self, P_FG, frame):
        ''' 
            RS is too sparse to construct a complete fg region and might miss small
            objects. necessary to fill the space between sparse points in the fg region
        '''
        N = np.size(frame)
        Ns = np.sum(self.rand_scattered_mask)
        omega_s = self.k_sei*math.sqrt(N/Ns)
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if self.rand_scattered_mask[i,j] == 1:
                    phi_t = np.round(P_FG[i,j]*omega_s)
                    self.spatial_exp_imp_mask[i-phi_t:i+phi_t,j-phi_t:j+phi_t]=1


    def calc_surprise_pixel_sampling(self):
        pass

    def sampling_map_gen():
        '''
            to keep the efficiency of the additional load (computation of fg map)
            restrict the SEARCH SPACE
            extract the candidate pixel positions to run the background subtraction
            and model update

            Also extract the positions randomly as 5% of entire pixels to detect the
            newly appeared objects
        '''
        pass