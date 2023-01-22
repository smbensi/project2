import numpy as np
from scipy.signal import correlate2d

class DualGM:
    def __init__(self,frame_gray) -> None:
        self.NUM_MODELS = 2
        self.GRID_SIZE = 4
        rows, cols = frame_gray.shape[:2]
        self.WIDTH_GRIDS = cols//self.GRID_SIZE
        self.HEIGHT_GRIDS = rows//self.GRID_SIZE
        
        self.mean = np.zeros((self.NUM_MODELS,self.HEIGHT_GRIDS,self.WIDTH_GRIDS))
        self.var = np.zeros((self.NUM_MODELS,self.HEIGHT_GRIDS,self.WIDTH_GRIDS))
        self.age = np.ones((self.NUM_MODELS,self.HEIGHT_GRIDS,self.WIDTH_GRIDS))

        # after motion compensation
        self.mean_comp = np.zeros((self.NUM_MODELS,self.HEIGHT_GRIDS,self.WIDTH_GRIDS))
        self.var_comp = np.zeros((self.NUM_MODELS,self.HEIGHT_GRIDS,self.WIDTH_GRIDS))
        self.age_comp = np.ones((self.NUM_MODELS,self.HEIGHT_GRIDS,self.WIDTH_GRIDS))

        # for each grid if we work with the apparent or candidate model
        self.index_model = np.zeros((self.HEIGHT_GRIDS,self.WIDTH_GRIDS))

        self.prev_frame = frame_gray
        self.frame = frame_gray

    def update_params(self,frame_gray):
        self.prev_frame = self.frame
        self.frame = frame_gray

    def calc_M_t(self):
        kernel = np.ones((self.GRID_SIZE,self.GRID_SIZE))
        M_t = correlate2d(self.frame, kernel, mode="valid")
        M_t = (1/self.GRID_SIZE**2)*M_t[::self.GRID_SIZE,::self.GRID_SIZE]
        return M_t

    def calc_V_t(self):
        max_in_grids = np.zeros_like(self.mean[1])
        diff = (self.mean[self.index_model] - self.frame)**2
        for i in range(self.HEIGHT_GRIDS-1):
            for j in range(self.WIDTH_GRIDS-1):
                max_in_grids[i,j] = np.max(diff[i*self.GRID_SIZE:(i+1)*self.GRID_SIZE,\
                                            j*self.GRID_SIZE:(j+1)*self.GRID_SIZE])
        V_t = max_in_grids
        return V_t


    def update_mean(self):
        lr = self.age_comp/(self.age_comp + 1)
        M_t = self.calc_M_t
        self.mean = lr * self.mean_comp + (1-lr) * M_t
    
    def update_var(self):
        lr = self.age_comp/(self.age_comp + 1)
        V_t = self.calc_V_t
        self.var = lr * self.var_comp + (1-lr) * V_t
    
    def update_age(self):
        self.age = self.age_comp + 1