GRID_SIZE=4
NUM_MODELS = 2


#  PARAMS PROPOSED IN PAPER
THETA_S = 2 # threshold for matching
LAMBDA = 0.001 # decaying parameter for age
THETA_V = 50 # 50x50 threshold for decaying age
THETA_D = 4 # threshold for determining detection

# initialization of the variance: moderate value eg 20x20
# the age was truncated at 30 to keep a minimum learning rate 


DEBUG = True

# FIXME voir comment on definit autrement un objet global
DUAL_SGM = None