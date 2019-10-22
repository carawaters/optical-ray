"""
Author: Cara
Created: 22/19/2019 14:05

A test for a ray travelling through a spherical refracting surface.
"""

import raytracer as rt
import matplotlib.pyplot as plt

surface = rt.SphericalRefraction(z_0 = 100, curve = 0.03, n1 = 1.0, n2 = 1.5, aperture = 30.)
output = rt.OutputPlane(z_1 = 250)

r1 = rt.Ray(pos = [0., 5., 0.], direc = [0., 2., 3.])
r2 = rt.Ray(pos = [0., 8., 0.], direc = [0., -2., 3.])

y1 = []
z1 = []

y2 = []
z2 = []

surface.propagate_ray(r1)
output.propagate_ray(r1)

surface.propagate_ray(r2)
output.propagate_ray(r2)

points1 = r1.vertices()
points2 = r2.vertices()

for i in range(points1.shape[0]):
    y1.append(points1[i][1])
    z1.append(points1[i][2])

for i in range(points2.shape[0]):
    y2.append(points2[i][1])
    z2.append(points2[i][2])

plt.plot(z1, y1, 'r-')
plt.plot(z2, y2, 'b-')

plt.show()
