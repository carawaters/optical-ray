"""
Author: Cara
Created: 12/10/2019 21:41

Includes a class for an optical ray.
"""

import scipy as sp


class Ray:
"""
Ray class gives a ray with a list of positions and direction vectors.
Initialisation takes 3d lists for position and direction.
"""

    ray_ps = []
    ray_ks = []

    def __init__(self, pos=[0.0, 0.0, 0.0], direc=[0.0, 0.0, 0.0]):
        self._r = sp.array(pos)
        self._d = sp.array(direc)
        self.poslist = [sp.array(pos)]
        self.dirlist = [sp.array(direc)]

    def p(self):
        return self._r

    def k(self):
        return self._d

    def append(self, p, k):
        self.poslist.append(sp.array(p))
        self.dirlist.append(sp.array(k))

    def vertices(self):
        return self.ray_ps
