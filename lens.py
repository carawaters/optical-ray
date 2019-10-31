"""
Author: Cara
Created: 29/10/19 14:20

Includes classes for plano-concave, convex-plano and biconvex lenses.
"""

import raytracer as rt


class PlanoConcave(rt.OpticalElement):
    """
    Creates a plano-concave lens, formed from a plane and a convex spherical surface (in terms of previous definition).
    """

    def __init__(self, z, curve, n1, n2, aperture, separation):
        type = "plano-convex lens"
        self.z = z
        self.curve = curve
        self.n1 = n1
        self.n2 = n2
        self.aperture = aperture
        self.separation = separation
        self.plane = rt.SphericalRefraction(z_0=z, curve=0, n1=n1, n2=n2, aperture=aperture)
        self.convex = rt.SphericalRefraction(z_0=z + separation, curve=curve, n1=n2, n2=n1, aperture=aperture)
        rt.OpticalElement.__init__(self, type, n1, n2, curve)

    def propagate_ray(self, ray):
        self.plane.propagate_ray(ray)
        self.convex.propagate_ray(ray)


class ConvexPlano(rt.OpticalElement):
    """
    Creates a convex-plano lens, formed from a convex spherical surface and a plane.
    """

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
    """
    Creates a biconvex lens, formed from a convex spherical surface followed by a concave spherical surface.
    """

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
