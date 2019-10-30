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
        self._dhat = self._d / mag_d
        self.poslist = sp.array([sp.array(pos)])
        self.dirlist = sp.array([sp.array(self._dhat)])
        self.status = "propagating"

    def p(self):
        return self.poslist[-1]

    def k(self):
        return self.dirlist[-1]

    def point_append(self, p, k):
        """
        Appends the lists of position and direction vectors with the position and the normalised direction vector.
        """
        mag_k = sp.sqrt(sp.dot(k, k))
        khat = k / mag_k
        self.poslist = sp.append(self.poslist, sp.array([p]), axis=0)
        self.dirlist = sp.append(self.dirlist, [khat], axis=0)

    def vertices(self):
        return self.poslist


class OpticalElement:
    """
    Base class for all optical elements.
    """

    def __init__(self, type, n1, n2, curve):
        self.type = type
        self.n1 = n1
        self.n2 = n2
        self.curve = curve

    def propagate_ray(self, ray):
        """propagate a ray through the optical element"""
        raise NotImplementedError()

    def snell(self, ray):
        """
        Carries out Snell's law.

        :return: new direction of a ray vector after undergoing snell's law
        """
        # prevent total internal reflection
        if (sp.sin(self.n1 / self.n2)) ** 2 > 1:
            print("Ray could not be refracted.")
            ray.status = "terminated"
        elif ray.status == "terminated":
            print("Ray is no longer propagating.")
        else:
            if self.n2 > self.n1:
                normal = self.normal(ray)
                # carry out vector form of snell's law
                root = sp.sqrt(1 - (self.n1 / self.n2) ** 2 * (1 - sp.dot(ray.k(), normal)))
                new_direc = (self.n1 / self.n2) * ray.k() + (
                        (self.n1 / self.n2) * sp.dot(ray.k(), normal) - root) * normal
            else:
                normal = self.normal(ray)
                # carry out vector form of snell's law
                root = sp.sqrt(1 - (self.n1 / self.n2) ** 2 * (1 + sp.dot(ray.k(), normal)))
                new_direc = (self.n1 / self.n2) * ray.k() + (
                        (self.n1 / self.n2) * sp.dot(ray.k(), normal) - root) * normal
            return new_direc

    def normal(self, ray):
        raise NotImplementedError()

    def paraxial_focus(self):
        """
        Calculates paraxial focus by propogating rays close to the optical axis and finding their intercept.

        :return: predicted paraxial focus of the surface
        """
        if self.curve < 0:
            print("No real focus.")
        else:
            r1 = Ray(pos=[0., 0.1, 0.], direc=[0., 0., 1.])
            self.propagate_ray(r1)
            dist = -r1.p()[1] / r1.k()[1]
            focus = r1.p()[2] + dist * r1.k()[2]
            print("The paraxial focus is: " + str(focus) + "mm")
            return focus


class SphericalRefraction(OpticalElement):
    """
    Refractor based on a sphere. Takes position along z, curvature (1/rad), n1, n2, aperture (radius).
    """

    def __init__(self, z_0, curve, n1, n2, aperture):
        self.z_0 = z_0
        self.curve = curve
        self.aperture = aperture  # specifying in y direction
        self.origin = sp.array([0., 0., 0.])
        type = "spherical refractor"
        OpticalElement.__init__(self, type, n1, n2, curve)

    def intercept(self, ray):
        """
        Calculates the intercept of the original ray with the surface. Checks if flat, convex or concave.

        :return: point of intersection
        """
        if ray.status == "terminated":
            print("The ray has terminated.")
        # for flat surface
        elif self.curve == 0:
            length = self.z_0 / ray.k()[2]
            plane_int = ray.p() + ray.k() * length
            return plane_int
        # for convex surface
        elif self.curve > 0:
            self.origin = sp.array([0., 0., self.z_0]) + sp.array([0., 0., (1 / self.curve)])
            op = self.origin - ray.p()
            # find projection of vector between ray and sphere origins onto ray direction
            ray_len = sp.dot(ray.k(), op)
            # calculate discriminant of solution to quadratic
            disc = ray_len ** 2 - (sp.dot(op, op) - (1 / self.curve) ** 2)
            if disc < 0:
                print("Imaginary solution.")
                ray.status = "terminated"
            else:
                root = sp.sqrt(disc)
                # carry out rest of solution
                length = ray_len - abs(root)
                sph_int = ray.p() + ray.k() * length
                return sph_int
        # for concave surface
        elif self.curve < 0:
            self.origin = sp.array([0., 0., self.z_0]) - sp.array([0., 0., abs(1 / self.curve)])
            op = self.origin - ray.p()
            ray_len = sp.dot(ray.k(), op)
            disc = ray_len ** 2 - (sp.dot(op, op) - (1 / self.curve) ** 2)
            if disc < 0:
                print("Imaginary solution.")
                ray.status = "terminated"
            else:
                root = sp.sqrt(disc)
                length = ray_len + abs(root)
                sph_int = ray.p() + ray.k() * length
                return sph_int
        else:
            print("Ray intercept not able to be found.")
            ray.status = "terminated"

    def normal(self, ray):
        """
        :return: normal vector to spherical surface at intercept
        """
        if self.curve == 0:
            return sp.array([0., 0., 1.])
        else:
            norm = self.intercept(ray) - self.origin
            norm_hat = norm / sp.sqrt(sp.dot(norm, norm))
            return norm_hat

    def propagate_ray(self, ray):
        intercept = self.intercept(ray)
        newdirec = self.snell(ray)
        if ray.status == "terminated":
            print("Ray is no longer propagating.")
        # test for ray not intercepting due to aperture
        elif intercept[1] > self.aperture:
            print("Ray does not intercept surface.")
            ray.status = "terminated"
        else:
            ray.point_append(intercept, newdirec)


class OutputPlane(OpticalElement):
    """
    A plane with which the rays intersect to plot their final position.
    """

    def __init__(self, z_1):
        type = "output plane"
        self.z_1 = z_1
        OpticalElement.__init__(self, type, n1=None, n2=None, curve=None)

    def intercept(self, ray):
        if ray.status == "terminated":
            print("Ray is no longer propagating.")
        else:
            # intercept calculated similarly to as with spherical surface
            ray.l2 = (self.z_1 - ray.p()[2]) / ray.k()[2]
            return ray.p() + ray.l2 * ray.k()

    def propagate_ray(self, ray):
        if ray.status == "terminated":
            print("Ray is no longer propagating.")
        else:
            intercept = self.intercept(ray)
            ray.point_append(intercept, ray.k())
