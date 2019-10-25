"""
Author: Cara
Created: 12/10/2019 21:41

Includes a class for an optical ray.
"""

import scipy as sp

class Ray:
    """
    Gives a ray with a list of positions and direction vectors.
    Initialisation takes 3d lists for position and direction.
    """

    def __init__(self, pos=[0.0, 0.0, 0.0], direc=[0.0, 0.0, 0.0]):
        self._r = sp.array(pos)
        self._d = sp.array(direc)
        mag_d = sp.sqrt(sp.dot(self._d, self._d))
        self._dhat = self._d/mag_d
        self.poslist = sp.array([sp.array(pos)])
        self.dirlist = sp.array([sp.array(self._dhat)])
        self.status = "propagating"

    def p(self):
        return self.poslist[-1]

    def k(self):
        return self.dirlist[-1]

    def point_append(self, p, k):
        mag_k = sp.sqrt(sp.dot(k, k))
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
        self.origin = sp.array([0., 0., 0.])
        type = "spherical refractor"
        OpticalElement.__init__(self, type)

    def intercept(self, ray):
        # aperture not implemented
        if ray.status == "terminated":
            print("The ray has terminated.")
        elif self.curve == 0:
            # intercept z must be z_0
            # length of flat surface = aperture
            ray.l = self.z_0/ray.k()[2]
        elif self.curve > 0:
            self.origin = sp.array([0. , 0., self.z_0]) + sp.array([0., 0., (1/self.curve)])
            op = self.origin - ray.p()
            ray_len = sp.dot(ray.k(), op)
            disc = ray_len**2 - (sp.dot(op, op) - (1/self.curve)**2)
            if disc <= 0:
                print("Imaginary solution.")
                ray.status = "terminated"
            else:
                root = sp.sqrt(disc)
                l = ray_len - abs(root)
                return ray.p() + ray.k() * l
            #r_vec = ray.p() - self.origin
            #print(r_vec)
            #projection = sp.dot(-r_vec, ray.k())
            #print(projection)
            #print(sp.dot(r_vec, r_vec))
            #d = projection**2 - (sp.dot(r_vec, r_vec) - (1/self.curve)**2)
            #print(d)
            #if d <= 0:
                #print("Ray does not intersect.")
                #ray.status = "terminated"
            #else:
                #ray.l = projection - sp.sqrt(d)
        elif self.curve < 0:
            self.origin = self.z_0 - (1/self.curve)
            r_vec = ray.p() - self.origin
            projection = sp.dot(-r_vec, ray.k())
            d = projection**2 - (sp.dot(r_vec, r_vec) - (1/self.curve)**2)
            if d <= 0:
                print("Ray does not intersect.")
                ray.status = "terminated"
            else:
                ray.l = projection + sp.sqrt(d)
        else:
            print("Ray intercept not able to be found.")
            ray.status = "terminated"

            return ray.p() + ray.l * ray.k()

    def snell(self, ray):
        if (sp.sin(self.n1/self.n2))**2 > 1:
            print("Ray could not be refracted.")
            ray.status = "terminated"
        elif ray.status == "terminated":
            print("Ray is no longer propagating.")
        else:
            normal = self.intercept(ray) - self.origin
            norm_hat = normal / sp.sqrt(sp.dot(normal, normal))
            root = sp.sqrt(1 - (self.n1/self.n2)**2 * (1 - sp.dot(ray.k(), norm_hat)))
            new_direc = (self.n1/self.n2) * ray.k() + ((self.n1/self.n2) * sp.dot(ray.k(), norm_hat) - root) * norm_hat
            return new_direc

    def propagate_ray(self, ray):
        intercept = self.intercept(ray)
        newdirec = self.snell(ray)
        if ray.status == "terminated":
            print("Ray is no longer propagating.")
        else:
            ray.point_append(intercept, newdirec)

class OutputPlane(OpticalElement):

    def __init__(self, z_1):
        type = "output plane"
        self.z_1 = z_1
        OpticalElement.__init__(self, type)

    def intercept(self, ray):
        ray.l2 = self.z_1/ray.k()[2]
        return ray.p() + ray.l2 * ray.k()

    def propagate_ray(self, ray):
        intercept = self.intercept(ray)
        if sp.iscomplexobj(intercept):
            print("Ray does not intersect output plane (imaginary).")
            ray.status = "terminated"
        elif ray.status == "terminated":
            print("Ray is no longer propagating.")
        else:
            ray.point_append(intercept, ray.k())
