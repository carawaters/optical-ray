"""
Author: Cara
Created: 29/10/19 10:10

A test for a bundle of rays passing through a spherical surface, plotting spot diagrams.
"""

import raytracer as rt
from raybundle import Bundle
import matplotlib.pyplot as plt
import scipy as sp

surface = rt.SphericalRefraction(z_0 = 100, curve = 0.03, n1 = 1.0, n2 = 1.5, aperture = 30.)
output = rt.OutputPlane(z_1 = surface.paraxial_focus())

fig1 = plt.figure()
ax1 = plt.axes()
fig2 = plt.figure()
ax2 = plt.axes()

beam = Bundle(5, 3)
origins = beam.con_circs()

foc_x = []
foc_y = []

for o in origins:
    x1 = []
    y1 = []
    r = rt.Ray(pos = [o[0], o[1], 0.], direc=[0., 0., 1.])
    surface.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    x1.append(points[1][0])
    y1.append(points[1][1])
    ax1.plot(x1, y1, 'r.')
    ax1.set_title('z = 0')

    x2 = []
    y2 = []
    x2.append(points[-1][0])
    y2.append(points[-1][1])

    foc_x.append(x2)
    foc_y.append(y2)

    ax2.plot(x2, y2, 'b.')
    ax2.set_title('paraxial focus')

rmsd_x = sp.sqrt(sp.sum((-sp.array(foc_x))**2)/len(foc_x))
rmsd_y = sp.sqrt(sp.sum((-sp.array(foc_y))**2)/len(foc_y))

print("The RMSD for the x direction is: " + str(rmsd_x))
print("The RMSD for the y direction is: " + str(rmsd_y))

plt.show()
