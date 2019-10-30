"""
Author: Cara
Created: 29/10/19 14:20

A class for a plano-convex lens.
"""

import raytracer as rt


class PlanoConvex(rt.OpticalElement):

    def __init__(self, z, curve, n1, n2, aperture, separation):
        type = "plano-convex lens"
        self.z = z
        self.curve = curve
        self.n1 = n1
        self.n2 = n2
        self.aperture = aperture
        self.separation = separation
        self.plane = rt.SphericalRefraction(z_0=z, curve=0, n1=n1, n2=n2, aperture=aperture)
        self.convex = rt.SphericalRefraction(z_0=z + separation, curve=curve, n1=n2, n2=n1,aperture=aperture)
        rt.OpticalElement.__init__(self, type, n1, n2, curve)

    def propagate_ray(self, ray):
        self.plane.propagate_ray(ray)
        self.convex.propagate_ray(ray)

class ConvexPlano(rt.OpticalElement):

    def __init__(self, z, curve, n1, n2, aperture, separation):
        type = "convex-plano lens"
        self.z = z
        self.curve = curve
        self.n1 = n1
        self.n2 = n2
        self.aperture = aperture
        self.separation = separation
        self.plane = rt.SphericalRefraction(z_0=z + separation, curve=0, n1=n2, n2=n1, aperture=aperture)
        self.convex = rt.SphericalRefraction(z_0=z, curve=curve, n1=n1, n2=n2, aperture=aperture)
        rt.OpticalElement.__init__(self, type, n1, n2, curve)

    def propagate_ray(self, ray):
        self.convex.propagate_ray(ray)
        self.plane.propagate_ray(ray)

class BiConvex(rt.OpticalElement):

    def __init__(self, z, curve, n1, n2, aperture, separation):
        type = "convex-plano lens"
        self.z = z
        self.curve = curve
        self.n1 = n1
        self.n2 = n2
        self.aperture = aperture
        self.separation = separation
        self.left = rt.SphericalRefraction(z_0=z, curve=curve, n1=n1, n2=n2, aperture=aperture)
        self.right = rt.SphericalRefraction(z_0=z + separation, curve=-curve, n1=n2, n2=n1, aperture=aperture)
        rt.OpticalElement.__init__(self, type, n1, n2, curve)

    def propagate_ray(self, ray):
        self.left.propagate_ray(ray)
        self.right.propagate_ray(ray)
