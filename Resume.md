# Project 2 : Detecting moving object in non stationnary background
## Mathias Bensimhon

# Contents

1. [Introduction](#1.Introduction)
2. [Conclusion](#2.Conclusion)


# 1.Introduction

- Finding moving objects in the scene is a funcdamental problem in the research of Computer Vision.
- **important**: computational efficiency and detection accuracy 
- `detection` : baseline function for succeeding high level processing
- non-stationary cameras: background is changed by the camera movement.
- 3 approaches:
  - **mosaic-based approach**: procedure to make a panorama image using image registration and then a background subtraction algo is applied.
  *problems*: image stitching errors in panorama images lead to many false detections.
  - **segmentation-based approach**: separate the object motion from the camera motion (graph-cut optimization and non-parametric belief propagation(BP) to solve the Markov Random Field)
  *problems*: too much slow and sensitive to parameters due to complexity of the model
  - **compensation-based approach**


# 2.Conclusion