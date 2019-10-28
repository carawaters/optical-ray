"""
Author: Cara
Created: 25/10/19 12:37

Gives a class of ray bundles.
"""

from raytracer import Ray
import scipy as sp
import matplotlib.pyplot as plt

class Bundle:
    """
    Creates a ray bundle, representing a collimated beam, centred at the origin.
    Uses line density.
    """

    def __init__(self, radius, density):
        self.radius = radius
        self.density = density
        self._rays = []

    def circ_points(self, radius):
        points = []
        # version which used self.radius in num - fig 6
        # version corrected to radius of this loop - fig 7
        for t in sp.linspace(0, 2 * sp.pi, num = 2 * sp.pi * radius * self.density, endpoint = True):
            x = radius * sp.cos(t)
            y = radius * sp.sin(t)
            points.append((x, y))
        print(points)
        return points

    def con_circs(self):
        con_points = []
        for r in sp.linspace(0, self.radius, num = self.radius * self.density, endpoint = True):
            new_points = self.circ_points(r)
            con_points.extend(new_points)
        print(con_points)
        return con_points
