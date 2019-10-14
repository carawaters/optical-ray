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
        squares_d = self._d**2
        mag_d = sp.sqrt(squares_d[0] + squares_d[1] + squares_d[2])
        self._dhat = self._d/mag_d
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
        self.aperture = aperture # specifying in y direction
        OpticalElement.__init__(self)

    def intercept(self, ray):
        # can only intercept where aperture is
        # curved surface centre is at z0, not zero
        squares_p = self.p**2
        mag_p = sp.sqrt(squares_p[0] + squares_p[1] + squares_p[2])
        rad = 1/self.curve
        ray.l_pos = - sp.dot(ray.p,ray.k) + sp.sqrt((sp.dot(ray.p,ray.k))**2 - (mag_p**2 - rad**2))
        ray.l_neg = - sp.dot(ray.p,ray.k) - sp.sqrt((sp.dot(ray.p,ray.k))**2 - (mag_p**2 - rad**2))
        if ray.l_pos > ray.l_neg:
            ray.l = ray.l_neg
        elif ray.l_pos < ray.l_neg:
            ray.l = ray.l_pos
        elif ray.l_pos = ray.l_neg:
            ray.l = ray.l_pos
        elif (ray.l_pos*ray.k)[1] > self.aperture or (ray.l_pos*ray.k)[1] > self.aperture:
            return None # may not give correct result - 2nd intercept may be > 1st in aperture direction
        else:
            print("Error: Possibility unexpected") # placeholder error

