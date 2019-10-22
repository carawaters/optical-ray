"""
Author: Cara
Created: 12/10/2019 21:41

Includes a class for an optical ray.
"""

import scipy as sp

def mod(x):
    return sp.sqrt(x**2)

def snell(ray, norm, n1, n2):
    normsquares = sp.array(norm)**2
    mag_norm = sp.sqrt(normsquares[0] + normsquares[1] + normsquares[2])
    normhat = sp.array(norm)/mag_norm
    theta1 = sp.arccos(sp.dot(ray.k(), normhat))
    if sp.sin(theta1) > n1/n2:
        ray.status = "terminated"
    else:
        theta2 = sp.arcsin(n1/n2 * sp.sin(theta1))
        k2 = sp.array([ray.k()[0], sp.sin(theta2), sp.cos(theta2)])
        return k2

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
        self.poslist = sp.array([sp.array(pos)])
        self.dirlist = sp.array([sp.array(self._dhat)])
        self.status = "propagating"

    def p(self):
        return self.poslist[-1]

    def k(self):
        return self.dirlist[-1]

    def point_append(self, p, k):
        squares_k = k**2
        mag_k = sp.sqrt(squares_k[0] + squares_k[1] + squares_k[2])
        khat = k/mag_k
        self.poslist = sp.append(self.poslist, sp.array([p]), axis = 0)
        self.dirlist = sp.append(self.dirlist, [khat], axis = 0)

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
        # this probably doesn't work for negative curvature as it stands
        if ray.status == "terminated":
            print("The ray has terminated.")
        elif self.curve == 0:
            # intercept z must be z_0
            # length of flat surface = aperture
            p = ray.p()
            cos_ang = sp.dot(ray.k(), sp.array([0., 0., (p[2] - self.z_0)]))/(p[2] - self.z_0)
            ray.l = self.z_0/cos_ang
        else:
            squares_p = ray.p()**2
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
                ray.status = "terminated"

        if sp.iscomplexobj(ray.l) or mod((ray.l*ray.k())[1]) > self.aperture:
            ray.status = "terminated"
        else:
            return ray.l

    def propagate_ray(self, ray):
        if ray.status == "terminated":
            print("Ray is no longer propagating.")
        else:
            intercept = ray.p() + (self.intercept(ray) * ray.k())
            direction = ray.k()
            squares_inter = intercept**2
            mag_inter = sp.sqrt(squares_inter[0] + squares_inter[1] + squares_inter[2])
            norm = intercept/mag_inter
            newdirec = snell(ray, norm, self.n1, self.n2)
            ray.point_append(intercept, newdirec)

class OutputPlane(OpticalElement):

    def __init__(self, z_1):
        type = "output plane"
        self.z_1 = z_1
        OpticalElement.__init__(self, type)

    def intercept(self, ray):
        p = ray.p()
        cos_ang = sp.dot(ray.k(), sp.array([0., 0., (p[2] - self.z_1)]))/(p[2] - self.z_1)
        ray.l2 = (ray.p()[2] - self.z_1)/cos_ang
        return ray.l2

    def propagate_ray(self, ray):
        intercept = ray.p() + (self.intercept(ray) * ray.k())
        ray.point_append(intercept, ray.k())
