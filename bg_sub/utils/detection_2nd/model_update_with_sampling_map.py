import numpy as np

from settings import params

class Bg_model():
    '''
        updating the model on 4x4 grid
    '''
    def __init__(self,frame) -> None:
        super().__init__()
        self.horizontal_grids = np.ceil(frame.shape[1]/params.GRID_SIZE)
        self.vertical_grids = np.ceil(frame.shape[0]/params.GRID_SIZE)
        self.mean = np.zeros((self.vertical_grids,self.horizontal_grids))
        self.variance = np.zeros((self.vertical_grids,self.horizontal_grids))
        self.time_varying_lr = 0 # ca sent pas bon ce 0

    def mean_update(self, G_s,frame):
        '''
            mean is updated by the weight sum of previous model mu(t-1) and 
            current observation m_t
            modify the updating rule considering only the selected pixels.
            so we update only if a grid contains selected pixels
            when a grid does not contain any selected pixels, we keep the mean
            unchanged

            Input:
            G_s : pixels selected in the  image using selective attention (per grid)
        '''
        m_t = np.zeros(self.vertical_grids,self.horizontal_grids)

        for i in len(self.vertical_grids):
            for j in len(self.horizontal_grids):
                pixels_selected = np.sum(G_s[j,i])
                m_t[j,i] = (1/pixels_selected)* \
                    np.sum(G_s[j,i]*frame[params.GRID_SIZE*i:params.GRID_SIZE(i+1),\
                                          params.GRID_SIZE*j:params.GRID_SIZE(j+1)])


        self.mean = (1-self.time_varying_lr)*self.mean + \
            self.time_varying_lr*m_t

    def variance_update(self, G_s, frame):
        '''
            variance is updated by the weight sum of previous model var(t-1) and
            current observation v_t
            when a grid does not contain any selected pixels we initialize the 
            variance to a high value (surement parce qu'il n'y a pas de pixel 
            interessant)
        '''
        v_t = np.zeros(self.vertical_grids,self.horizontal_grids)

        for i in len(self.vertical_grids):
            for j in len(self.horizontal_grids):
                v_t[j,i] = np.max((self.mean[j,i] - G_s[j,i]* \
                    frame[params.GRID_SIZE*i:params.GRID_SIZE(i+1),\
                          params.GRID_SIZE*j:params.GRID_SIZE(j+1)])**2)

        self.variance = (1-self.time_varying_lr)*self.variance + \
            self.time_varying_lr*v_t