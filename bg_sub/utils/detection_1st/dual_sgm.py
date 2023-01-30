import numpy as np
from scipy.signal import correlate2d
from bg_sub.settings import params

class SGM:
    def __init__(self,frame) -> None:
        self.grid = params.GRID_SIZE
        self.horizontal_grids = np.ceil(frame.shape[1]/self.grid).astype(int)
        self.vertical_grids = np.ceil(frame.shape[0]/self.grid).astype(int)
        self.mean = np.zeros((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))
        self.variance = np.zeros((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))
        # at initialization all pixels have age of 1
        self.age = np.ones((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))

        self.mean_comp = np.zeros((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))
        self.var_comp = np.zeros((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))
        self.age_comp = np.zeros((params.NUM_MODELS,self.vertical_grids,self.horizontal_grids))

        self.thresh_s = params.THETA_S # the value proposed in the paper
        self.decay_param = params.LAMBDA
        self.thresh_v = params.THETA_V # 50x50 threshold for decaying age
        self.thresh_detection = params.THETA_D # threshold for determining detection

        # FIXME peut etre que je dois definir une matrice de grid parce quelles sembles indeps
        self.apparent = 0
        self.candidate = 1 
        self.model_to_update = None
        self.prev_frame = frame

    def calc_M_t(self,frame):
        kernel = np.ones((self.grid,self.grid))
        M_t = correlate2d(frame, kernel, mode="valid")
        M_t = (1/self.grid**2)*M_t[::self.grid,::self.grid]
        return M_t
    
    def calc_V_t(self, frame):
        model = self.model_to_update
        max_in_grids = np.zeros_like(self.mean[1])
        for i in range(self.vertical_grids-1):
            for j in range(self.horizontal_grids-1):
                max_in_grids[i,j] = np.min(frame[i*self.grid:(i+1)*self.grid,\
                                            j*self.grid:(j+1)*self.grid])
        V_t = (self.mean[model] - max_in_grids)**2
        return V_t

    def check_age_after_update(self):
        # FIXME elle a un probleme cette fonction 
        change_age = (self.age[self.candidate] > self.age[self.apparent]).astype(int)
        change_age[change_age==1] = self.candidate

    def select_model(self):
        model = self.model_to_update
        model_candidate = (model+1)%2
        M_t = self.calc_M_t
        if (M_t - self.mean[model])**2 < self.thresh_s*self.variance[model]:
            self.model_to_update = model
        elif(M_t - self.mean[model_candidate])**2 \
            < self.thresh_s*self.variance[model_candidate]:
            self.model_to_update = model_candidate
        else:
            # FIXME checker que cest bien ca l'initialisation
            # FIXME bien checker est ce quild est possible quon ait un model different par grid
            self.mean[model_candidate] = M_t
            self.variance[model_candidate] = self.calc_V_t
            if self.age[model_candidate] > self.age[model]:
                self.model_to_update = model_candidate
# VERY_IMPORTANT tous les mean variance etc pour linstant sont pris avant compensation
    def update_mean(self,frame):
        # TO_UPGRADE mettre ces deux lignes du dessous dans une fction plus gloable
        # car elles sont reutilisees dans d'autres fonctions
        coef = self.age/(self.age + 1)
        model = self.model_to_update

        M_t = self.calc_M_t(frame)
        self.mean[model] = coef * self.mean[model] + (1-coef)*M_t
        
    def update_variance(self, frame):
        coef = self.age/(self.age + 1)
        model = self.model_to_update
        
        V_t = self.calc_V_t(frame)

        self.variance[model] = coef * self.variance + (1-coef)*V_t

    def update_age(self):
        model = self.model_to_update
        self.age[model] = self.age[model] + 1