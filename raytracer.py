"""
Author: Cara
Created: 12/10/2019 21:41

Includes a class for an optical ray.
"""

import scipy as sp

def mod(x):
    return sp.sqrt(x**2)

class Ray:
    """
    Gives a ray with a list of positions and direction vectors.
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
    Base class for all optical elements. Propagates ray through elements.
    """
    def __init__(self, type):
        self.type = type

    def propagate_ray(self, ray):
        """propagate a ray through the optical element"""
        raise NotImplementedError()

class SphericalRefraction(OpticalElement):
    """
    Refractor based on a sphere. Takes position along z, curvature (1/rad), n1, n2, aperture (radius).
    """

    def __init__(self, z_0, curve, n1, n2, aperture):
        self.z_0 = z_0
        self.curve = curve
        self.n1 = n1
        self.n2 = n2
        self.aperture = aperture # specifying in y direction
        type = "spherical refractor"
        OpticalElement.__init__(self, type)

    def intercept(self, ray):
        # curved surface z intercept is at z0, not zero
        # may need special case for zero curvature
        if self.curve == 0:
            # intercept z must be z_0
            # length of flat surface = aperture
            ray.l = sp.sqrt(self.z_0**2 + self.aperture**2)
        else:
            squares_p = sp.power(ray.p(), 2)
            mag_p = sp.sqrt(squares_p[0] + squares_p[1] + squares_p[2])
            rad = 1/self.curve
            ray.l_pos = - sp.dot(ray.p(), ray.k()) + sp.sqrt((sp.dot(ray.p(), ray.k()))**2 - (mag_p**2 - rad**2))
            ray.l_neg = - sp.dot(ray.p(), ray.k()) - sp.sqrt((sp.dot(ray.p(), ray.k()))**2 - (mag_p**2 - rad**2))
            if mod(ray.l_pos) > mod(ray.l_neg):
                ray.l = ray.l_neg
            elif mod(ray.l_pos) < mod(ray.l_neg):
                ray.l = ray.l_pos
            elif mod(ray.l_pos) == mod(ray.l_neg):
                ray.l = ray.l_pos
            else:
                print("Error: Unknown")
                ray.l = None

        if sp.iscomplexobj(ray.l) or mod((ray.l*ray.k())[1]) > self.aperture:
            return None
        else:
            return ray.l
