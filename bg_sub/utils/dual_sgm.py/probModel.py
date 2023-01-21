import numpy as np

class ProbModel:
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
