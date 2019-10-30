"""
Author: Cara
Created: 30/10/19 10:52

A test for a concave spherical refracting surface.
"""

import raytracer as rt
from raybundle import Bundle
import matplotlib.pyplot as plt
import scipy as sp
from mpl_toolkits import mplot3d

# create a spherical surface and an output plane at the paraxial focus
surface = rt.SphericalRefraction(z_0 = 100, curve = -0.03, n1 = 1.0, n2 = 1.5, aperture = 30.)
# a concave lens only has an imaginary focus behind it
output = rt.OutputPlane(z_1 = 250)

# creates a collimated beam with (radius, line density around outer circumference)
beam = Bundle(2, 3)

fig = plt.figure()
ax = plt.axes()

"""
origins = beam.con_circs()

# get points of rays into individual arrays and plot them
for o in origins:
    x = []
    y = []
    z = []
    r = rt.Ray(pos = [o[0], o[1], 0.], direc=[0., 0., 1.])
    surface.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.plot3D(z, x, y, 'r-')
"""

for i in range(-10, 10):
    y = []
    z = []
    r = rt.Ray(pos = [0., i, 0.], direc=[0., 0., 1.])
    surface.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    for point in points:
        y.append(point[1])
        z.append(point[2])
    plt.plot(z, y, 'r-')

plt.show()
