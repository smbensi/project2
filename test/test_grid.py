import numpy as np


a = np.arange(24).reshape((6,4))
a[0,1]=12
print(a)

grid = 2 
vert_grid = a.shape[0]//2
hor_grid = a.shape[1]//2
# for i in range(hor_grid):
#     for j in range(vert_grid):
#         print(np.max(a[i*grid:(i+1)*grid,j*grid:(j+1)*grid]))
# b = np.zeros((vert_grid,hor_grid))
# max_in_grids = np.zeros_like(b)
# for i in range(hor_grid):
#     for j in range(vert_grid):
#         max_in_grids[i,j] = np.max(a[i*grid:(i+1)*grid,j*\
#                                     j*grid:(j+1)*grid])
        
# print(max_in_grids)

# c = 7*np.ones((4,4))
# d = (a<c).astype(int)
# d[d==1]=5
# print(d)

corners_x = np.arange(0,a.shape[1],vert_grid)
corners_y = np.arange(0,a.shape[0],hor_grid)
corners_x_rep = np.repeat(corners_x,len(corners_y))
corners_y_rep = np.tile(corners_y,len(corners_x))
corners = np.array([corners_x_rep,corners_y_rep]).transpose()
print(corners_x_rep)
print(corners_y_rep)
print(corners.tolist())
print(corners[1],type(corners[1]),corners[1].shape)