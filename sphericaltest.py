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

y = []
z = []

surface.propagate_ray(r1)
output.propagate_ray(r1)

points = r1.vertices()
print(points)
print(points.shape[0])
for i in range(points.shape[0]):
    y.append(points[i][1])
    z.append(points[i][2])

print(y)
print(z)

plt.plot(z, y, '-')
plt.show()
