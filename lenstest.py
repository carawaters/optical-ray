"""
Author: Cara
Created: 29/10/19 14:53

Test for the lenses created in the lens module.
"""

import lens as ln
import raytracer as rt
import matplotlib.pyplot as plt
from raybundle import Bundle
from mpl_toolkits import mplot3d
import scipy as sp

# lens can be PlanoConcave, ConvexPlano or BiConvex
lens = ln.BiConvex(z=20, curve=0.02, separation=5, n1=1, n2=1.5168, aperture=30)
output = rt.OutputPlane(z_1 = lens.paraxial_focus())

beam = Bundle(5, 3)
origins = beam.con_circs()

# setting up figures and axes - used to allow projection to be set to 3d easily rather than just plotting
fig1 = plt.figure()
ax1 = plt.axes()
ax1.set_title('z = 0')

fig2 = plt.figure()
ax2 = plt.axes()
ax2.set_title('paraxial focus')

fig3 = plt.figure()
ax3 = plt.axes(projection='3d')
ax3.set_title('beam path')

# empty lists for calculating rms deviation later
foc_x = []
foc_y = []

# create each ray and propagate through lens, plotting at origin, at paraxial focus and the path
for o in origins:
    x1 = []
    y1 = []
    r = rt.Ray(pos = [o[0], o[1], 0.], direc=[0., 0., 1.])
    lens.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    x1.append(points[0][0])
    y1.append(points[0][1])
    ax1.plot(x1, y1, 'r.')

    x2 = []
    y2 = []
    x2.append(points[-1][0])
    y2.append(points[-1][1])

    foc_x.append(x2)
    foc_y.append(y2)

    ax2.plot(x2, y2, 'b.')

    x = []
    y = []
    z = []

    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax3.plot(z, y, x, 'r-')

# calculates the rms deviation for each of x and y from the expected focus (0, 0)
# this is only for collimated beams travelling in the z direction only
rmsd_x = sp.sqrt(sp.sum((-sp.array(foc_x))**2)/len(foc_x))
rmsd_y = sp.sqrt(sp.sum((-sp.array(foc_y))**2)/len(foc_y))

print("The RMSD for the x direction is: " + str(rmsd_x))
print("The RMSD for the y direction is: " + str(rmsd_y))

fig4 = plt.figure()
ax4 = plt.axes()
ax4.set_title('2d view')

# used to create rays and plot to give an equivalent 2d view
for i in range(-5, 6):
    y = []
    z = []
    r = rt.Ray(pos = [0., i, 0.], direc=[0., 0., 1.])
    lens.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    for point in points:
        y.append(point[1])
        z.append(point[2])
    ax4.plot(z, y, 'r-')

plt.show()
