import numpy as np
import random

def rand_mask(img,mask,phi=0.05):
    """
    the function samples random pixels in the image
    it samples the previous foreground pixel from previous frame 
       
    """
    #  : find a nice way to sample pixels other than previous frame
     
    nb_of_pixels = img.size
    pix_to_samp  = int(phi*nb_of_pixels)
    n_reuse_ind = np.where(mask==1)
    n_reuse_ind = np.stack(n_reuse_ind).transpose()
    n_reuse = n_reuse_ind.shape[0]
    n_new_to_sample = pix_to_samp - n_reuse

    ind_to_sample_from = np.stack(np.where(mask==0)).transpose()
    n_new = random.sample(ind_to_sample_from.shape[0],k=n_new_to_sample)

    pixels_samp = np.stack((n_reuse,n_new),axis=1)




def spatial_exp_importance():
    """
    fill the space between sparse points in the fg region 
    
    """
    pass

def surprise_pix_samp_mask():
    """
    
    """
    pass


