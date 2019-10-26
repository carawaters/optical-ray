"""
Author: Cara
Created: 25/10/19 12:37

Gives a class of ray bundles.
"""

from raytracer import Ray
import scipy as sp

class Bundle:
    """
    Creates a ray bundle, representing a collimated beam, centred at the origin.
    Uses line density.
    """

    def __init__(self, radius, density):
        self.radius = radius
        self.density = density
        self._rays = []

    def circ_points(self):
        points = []
        for t in sp.arange(0, 2 * sp.pi, 1/self.radius * self.density):
            x = self.radius * sp.cos(t)
            y = self.radius * sp.sin(t)
            points.append((x, y))
        return points
