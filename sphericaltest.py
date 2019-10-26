"""
Author: Cara
Created: 22/19/2019 14:05

A test for a series of rays travelling through a spherical refracting surface.
"""

import raytracer as rt
from raybundle import Bundle
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

surface = rt.SphericalRefraction(z_0 = 100, curve = 0.03, n1 = 1.0, n2 = 1.5, aperture = 30.)
#surface2 = rt.SphericalRefraction(z_0 = 100, curve = -0.03, n1 = 1.0, n2 = 1.5, aperture = 30.)
output = rt.OutputPlane(z_1 = 250)

fig = plt.figure()
ax = plt.axes(projection="3d")

beam = Bundle(5, 2)

for point in beam.circ_points():
    x = []
    y = []
    z = []
    r = rt.Ray(pos = [point[0], point[1], 0.], direc=[0., 0., 1.])
    surface.propagate_ray(r)
    #surface2.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.plot3D(z, x, y)

plt.show()
