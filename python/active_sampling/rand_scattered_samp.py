def rand_mask(img,phi,n_reuse,mask):
    """
    the function samples random pixels in the image
    it samples the previous foreground pixel from previous frame 
       
    """
    # TODO : find a nice way to sample pixels other than previous frame
     
    nb_of_pixels = img.size
    pix_to_rand  = int(phi*nb_of_pixels)

