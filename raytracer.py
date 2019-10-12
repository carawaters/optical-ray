"""
Author: Cara
Created: 12/10/2019 21:41

Includes a class for an optical ray, with a point and direction vector.
"""

import scipy as sp


class Ray:

    ray_ps = []
    ray_ks = []

    def __init__(self, pos=[0.0, 0.0, 0.0], direc=[0.0, 0.0, 0.0]):
        self._r = sp.array(pos)
        self._d = sp.array(direc)

    def p(self):
        return self._r

    def k(self):
        return self._d

    def append(self, p, k):
        self.ray_ps.append(p)
        self.ray_ks.append(k)

    def vertices(self):
        return self.ray_ps

