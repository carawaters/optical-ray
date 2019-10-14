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

    def __init__(self, pos=[0.0, 0.0, 0.0], direc=[0.0, 0.0, 0.0]):
        self._r = sp.array(pos)
        self._d = sp.array(direc)
        squares = self._d**2
        mag = sp.sqrt(squares[0] + squares[1] + squares[2])
        self._dhat = self._d/mag
        self.poslist = [sp.array(pos)]
        self.dirlist = [sp.array(direc)]

    def p(self):
        return self._r

    def k(self):
        return self._dhat

    def append(self, p, k):
        self.poslist.append(sp.array(p))
        self.dirlist.append(sp.array(k))

    def vertices(self):
        return self.poslist

class OpticalElement:
    """

    """

    def __init__(self):
        # add attributes

    def propagate_ray(self, ray):
        "propagate a ray through the optical element"
        raise NotImplementedError()

class SphericalRefraction(OpticalElement):
    """

    """

    def __init__(self, z_0, curve, n1, n2, aperture):
        self.z_0 = z_0
        self.curve = curve
        self.n1 = n1
        self.n2 = n2
        self.aperture = aperture
        OpticalElement.__init__(self)
