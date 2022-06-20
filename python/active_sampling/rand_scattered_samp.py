import numpy as np

def rand_mask(img,n_reuse,mask,phi=0.05):
    """
    the function samples random pixels in the image
    it samples the previous foreground pixel from previous frame 
       
    """
    # TODO : find a nice way to sample pixels other than previous frame
     
    nb_of_pixels = img.size
    pix_to_rand  = int(phi*nb_of_pixels)
    n_new = pix_to_rand - n_reuse



def spatial_exp_importance():
    """
    fill the space between sparse points in the fg region 
    
    """
    pass

def surprise_pix_samp_mask():
    """
    
    """
    pass


