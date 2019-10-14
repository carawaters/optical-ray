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

    """
    def __init__(self, type):
        self.type = type

    def propagate_ray(self, ray):
        """propagate a ray through the optical element"""
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
        type = "spherical refractor"
        OpticalElement.__init__(self, type)

    def intercept(self, ray):
        # can only intercept where aperture is
        # curved surface centre is at z0, not zero
        squares_p = sp.power(ray.p(),2) # unsupported operand type, 'method' and 'int'
        mag_p = sp.sqrt(squares_p[0] + squares_p[1] + squares_p[2])
        rad = 1/self.curve
        ray.l_pos = - sp.dot(ray.p(),ray.k()) + sp.sqrt((sp.dot(ray.p(),ray.k()))**2 - (mag_p**2 - rad**2))
        ray.l_neg = - sp.dot(ray.p(),ray.k()) - sp.sqrt((sp.dot(ray.p(),ray.k()))**2 - (mag_p**2 - rad**2))
        if mod(ray.l_pos) > mod(ray.l_neg):
            ray.l = ray.l_neg
        elif mod(ray.l_pos) < mod(ray.l_neg):
            ray.l = ray.l_pos
        elif mod(ray.l_pos) == mod(ray.l_neg):
            ray.l = ray.l_pos
        else:
            print("Error: Possibility unexpected") # placeholder error

        # check for intercepting past aperture of surface
        if mod((ray.l*ray.k())[1]) > self.aperture:
            return None
        else:
            return ray.l
