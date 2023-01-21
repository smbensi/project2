import numpy as np
from scipy.signal import correlate2d
from bg_sub.settings import params

class SGM:
    def __init__(self,frame) -> None:
        self.grid = params.GRID_SIZE
        self.horizontal_grids = np.ceil(frame.shape[1]/self.grid)
        self.vertical_grids = np.ceil(frame.shape[0]/self.grid)
        self.mean = np.zeros((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))
        self.variance = np.zeros((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))
        # at initialization all pixels have age of 1
        self.age = np.ones((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))

        self.mean_comp = np.zeros((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))
        self.var_comp = np.zeros((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))
        self.age_comp = np.zeros((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))

        self.thresh_s = 2 # the value proposed in the paper
        self.decay_param = 0.001
        self.thresh_v = 50 # 50x50 threshold for decaying age
        self.thresh_detection = 4 # threshold for determining detection

        # TODO peut etre que je dois definir une matrice de grid parce quelles sembles indeps
        self.apparent = 0
        self.candidate = 1 
        self.model_to_update = None

    def check_age_after_update(self):
        # TODO elle a un probleme cette fonction 
        change_age = (self.age[self.candidate] > self.age[self.apparent]).astype(int)
        change_age[change_age==1] = self.candidate


    def update_apparent_condition(self):
        app = self.apparent
        cand = self.candidate
        cond1 = (M_t[app] - self.mean[app])**2 < (self.thresh_s*self.variance[app])
        cond2 = (M_t[cand] - self.mean[cand])**2 < (self.thresh_s*self.variance[cand])
        if cond1 == False:
            if cond2 == True:
                self.model_to_update = self.candidate
        elif cond1 == True:
            self.model_to_update = self.apparent
        else:
            # TODO initialize the candidate with the current observation
            pass

    def update_mean(self,frame):
        coef = self.age/(self.age + 1)
        
        kernel = np.ones((self.grid,self.grid))
        global M_t  # TODO regarder si ca pose pas de problemes vu qu'utiliser ailleurs
        M_t = correlate2d(frame,kernel,mode="valid")
        M_t = (1/self.grid**2)*M_t[::self.grid,::self.grid]
        self.mean = coef * self.mean + (1-coef)*M_t
        
    def update_variance(self, frame):
        coef = self.age/(self.age + 1)
        max_in_grids = np.zeros_like(self.mean)
        for i in range(self.horizontal_grids):
            for j in range(self.vertical_grids):
                max_in_grids[i,j] = np.min(frame[i*self.grid:(i+1)*self.grid,j*\
                                            j*self.grid:(j+1)*self.grid])
        V_t = (self.mean - max_in_grids)**2
        self.variance = coef * self.variance + (1-coef)*V_t

    def update_age(self):
        self.age = self.age + 1