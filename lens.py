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
