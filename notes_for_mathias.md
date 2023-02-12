# Project2
```math
SE = \frac{\sigma}{\sqrt{n}}

```
## Principal idea

> Create a background subtraction model to detect moving object from background in non
> stationary background

## Reference

1. Detection of Moving Objects with Non-Stationary Cameras in 5.8ms: Bringing
Motion Detection to your Mobile Device [link](https://www.cv-foundation.org/openaccess/content_cvpr_workshops_2013/W03/papers/Yi_Detection_of_Moving_2013_CVPR_paper.pdf)

2. Active Attentional Sampling for Speed-up of Background Subtraction [link1](https://www.researchgate.net/publication/261200446_Active_attentional_sampling_for_speed-up_of_background_subtraction) [link2](https://sci-hub.se/10.1109/cvpr.2012.6247914)

3. ROBUST AND FAST MOVING OBJECT DETECTION IN A NON-STATIONARY CAMERA
VIA FOREGROUND PROBABILITY BASED SAMPLING [link](https://sci-hub.se/10.1109/ICIP.2015.7351738)

### 23/01 implementation of the second paper

1. peut etre creer des methodes statiques dans l'objet

# choses a faire

TO DO
* creer un environnement de debug en s'aidant de limplementation du **premier** papier
* creer des visualisations pour les masques qu'on cree

DONE

09/02

15 min pour creer des visualitions des masques de spatially expanding importance sampling. Bien comprendre l'idee derriere

# Spatially Expanding importance sampling

donc sur chaque pt tq M_RS(t) == 1 , on prend le P_FG et donc tous les points dans la zone E_t(i)=round(r_t(i) x w_s)