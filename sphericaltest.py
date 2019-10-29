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
output = rt.OutputPlane(z_1 = surface.paraxial_focus())

fig = plt.figure()
ax = plt.axes()

r1 = rt.Ray(pos = [0., 10, 0.], direc = [0., 0., 1.])
r2 = rt.Ray(pos = [0., -10, 0.], direc = [0., 0., 1.])

surface.propagate_ray(r1)
output.propagate_ray(r1)
surface.propagate_ray(r2)
output.propagate_ray(r2)

pts1 = r1.vertices()
pts2 = r2.vertices()

x1 = []
y1 = []
z1 = []

x2 = []
y2 = []
z2 = []

for i in pts1:
    x1.append(i[0])
    y1.append(i[1])
    z1.append(i[2])

for j in pts2:
    x2.append(j[0])
    y2.append(j[1])
    z2.append(j[2])

ax.plot(z1, y1)
ax.plot(z2, y2)

"""
beam = Bundle(5, 3)
origins = beam.con_circs()


for o in origins:
    x = []
    y = []
    z = []
    r = rt.Ray(pos = [o[0], o[1], 0.], direc=[0., 0., 1.])
    surface.propagate_ray(r)
    #surface2.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.plot3D(z, x, y)
"""

plt.show()
