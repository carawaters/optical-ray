"""
Author: Cara
Created: 22/19/2019 14:05

A test for a series of rays travelling through a spherical refracting surface.
"""

import raytracer as rt
import matplotlib.pyplot as plt

surface = rt.SphericalRefraction(z_0 = 20, curve = 0.05, n1 = 1.0, n2 = 1.5, aperture = 30.)
output = rt.OutputPlane(z_1 = 30)

for i in range(20):
    r = rt.Ray(pos = [0., i, 0.], direc = [0., 0., 1.])
    y = []
    z = []
    surface.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    for point in points:
        y.append(point[1])
        z.append(point[2])
    plt.plot(z, y, 'r-')

plt.show()
