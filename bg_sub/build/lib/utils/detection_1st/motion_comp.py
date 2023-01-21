import numpy as np
import cv2
import matplotlib.pyplot as plt

class MotionComp:
    def __init__(self,frame) -> None:
        self.height_grid = 32
        self.width_grid = 24
        self.horizontal_grid = frame.shape[1]//self.width_grid
        self.vertical_grid = frame.shape[0]//self.height_grid
        self.prev_frame = frame

        self.prev_frame = None
        # self.frame = None
        self.grid_corners = None

    
    def find_corners(self, frame, debug=False):
      corners = np.zeros((self.horizontal_grid,self.vertical_grid))
      for i in self.vertical_grid:
        for j in self.horizontal_grid:
          corners[i,j] = cv2.goodFeaturesToTrack(frame,100,0.01,10)



      if debug:
        

      


      # FIXME ce seront tjrs les memes corners donc vaut mieux les mettre en init
      corners_x = np.arange(0,self.frame.shape[1],self.height_grid)
      corners_y = np.arange(0,self.frame.shape[0],self.width_grid)
      # construct an array of the corners point
      corners_x_rep = np.repeat(corners_x,self.horizontal_grid)
      corners_y_rep = np.tile(corners_y,self.vertical_grid)
      corners = np.array([corners_x_rep,corners_y_rep]).transpose().tolist()
      return corners

    def calc_klt(self):
      # Use KLT feature tracker to track corners in each grid
      # TODO jusqua 19h30
      # en fait j'ai rien compris les corners c'est plus les edges dans chaque grid
      # donc on va surement aller chercher les goodFeaturesToTrack
      # divide the input image at time t into 32x24 grids and perform KLT
      # on every corner of the grid with the image from time t-1
      status, err = cv2.calcOpticalFlowPyrLK(self.prev_frame,self.frame,)
  
  #     points_t_minus_1 = []
  # points_t = []
  # for x, y in grids:
  #   points_t_minus_1.append((x - grid_cols / 2, y - grid_rows / 2))
  #   points_t.append((x + grid_cols / 2, y + grid_rows / 2))
  # points_t_minus_1 = np.float32(points_t_minus_1).reshape(-1, 1, 2)
  # points_t = np.float32(points_t).reshape(-1, 1, 2)
  # status, err = cv2.calcOpticalFlowPyrLK(image_t_minus_1, image_t, points_t_minus_1, points_t)



'''
from chatGPT

import cv2
import numpy as np

def create_motion_compensated_background_model(image_t, image_t_minus_1, grid_size=(32, 24), var_threshold=10, decay_lambda=0.01):
    # Divide image_t into grids
    rows, cols = image_t.shape[:2]
    grid_rows, grid_cols = grid_size
    grid_height = rows // grid_rows
    grid_width = cols // grid_cols

    # Use KLT feature tracker to track corners in each grid
    points_t_minus_1 = []
    for i in range(grid_rows):
        for j in range(grid_cols):
            x1 = j * grid_width
            y1 = i * grid_height
            x2 = x1 + grid_width
            y2 = y1 + grid_height
            grid_corners = cv2.goodFeaturesToTrack(image_t[y1:y2, x1:x2], maxCorners=1, qualityLevel=0.01, minDistance=5)
            if grid_corners is not None:
                points_t_minus_1.append(grid_corners[0][0])

    # Use RANSAC to estimate homography matrix that warps image_t_minus_1 to image_t
    points_t, _, _ = cv2.calcOpticalFlowPyrLK(image_t_minus_1, image_t, points_t_minus_1, None)
    _, homography_t_t_minus_1, _ = cv2.findHomography(points_t_minus_1, points_t, cv2.RANSAC)

    # Create motion compensated background model for each grid in image_t
    compensated_background_models = []
    for i in range(grid_rows):
        for j in range(grid_cols):
            # Get center of grid in image_t
            x1 = j * grid_width
            y1 = i * grid_height
            x2 = x1 + grid_width
            y2 = y1 + grid_height
            grid_center_t = np.array([x1 + grid_width // 2, y1 + grid_height // 2])

            # Warp center of grid to image_t_minus_1 using homography matrix
            grid_center_t_minus_1 = cv2.perspectiveTransform(np.array([[grid_center_t]]), homography_t_t_minus_1)[0][0]

            # Find overlapping grids in image_t_minus_1
            min_x = int(grid_center_t_minus_1[0] - grid_width // 2)
            max_x = int(grid_center_t_minus_1[0] + grid_width // 2)
            min_y = int(grid_center_t_minus_1[1] - grid_height // 2)
            max_y = int(grid_center_t_minus_1[1] + grid_height // 2)
            overlapping_grids = [(i, j) for i in range(

'''

'''

or


import cv2
import numpy as np

def construct_compensated_bg_model(image_t, image_t_minus_1, grid_size, threshold_variance):
  # Divide the image at time t into a grid of size grid_size
  rows, cols = image_t.shape[:2]
  grid_rows, grid_cols = grid_size
  grid_centers_x = np.arange(grid_cols / 2, cols, grid_cols)
  grid_centers_y = np.arange(grid_rows / 2, rows, grid_rows)
  grids = []
  for x in grid_centers_x:
    for y in grid_centers_y:
      grids.append((x, y))

  # Use KLT feature tracker to track corners of each grid in image_t_minus_1 to image_t
  points_t_minus_1 = []
  points_t = []
  for x, y in grids:
    points_t_minus_1.append((x - grid_cols / 2, y - grid_rows / 2))
    points_t.append((x + grid_cols / 2, y + grid_rows / 2))
  points_t_minus_1 = np.float32(points_t_minus_1).reshape(-1, 1, 2)
  points_t = np.float32(points_t).reshape(-1, 1, 2)
  status, err = cv2.calcOpticalFlowPyrLK(image_t_minus_1, image_t, points_t_minus_1, points_t)

  # Use RANSAC to estimate a homography matrix that warps image_t_minus_1 to image_t
  inliers, _ = cv2.findHomography(points_t_minus_1, points_t, cv2.RANSAC)
  H_t_minus_1_to_t, _ = cv2.findHomography(points_t_minus_1[inliers == 1], points_t[inliers == 1])

  # Compute the compensated background model for each grid
  compensated_bg_models = []
  for x, y in grids:
    # Find the group of grids that overlap with the current grid
    overlap_grids = []
    for x_overlap, y_overlap in grids:
      if abs(x - x_overlap) < grid_cols and abs(y - y_overlap) < grid_rows:
        overlap_grids.append((x_overlap, y_overlap))

    # Mix the SGMs at time t-1 of the overlapping grids to obtain the compensated background model
    mu_t_minus_1 = 0
    sigma_t_minus_1 = 0
    alpha_t_minus_1 = 0
    total_overlap = 0
    for x_overlap, y_overlap in overlap_grids:
      # Assume that the SGM at time t-1 for this grid has already been computed and stored in some data structure
      mu_overlap_t_minus_

'''