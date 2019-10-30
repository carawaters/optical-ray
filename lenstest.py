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

lens = ln.ConvexPlano(z=20, curve=0.02, separation=5, n1=1, n2=1.5168, aperture=30)
output = rt.OutputPlane(z_1 = lens.paraxial_focus())

beam = Bundle(5, 3)
origins = beam.con_circs()


fig1 = plt.figure()
ax1 = plt.axes()
ax1.set_title('z = 0')

fig2 = plt.figure()
ax2 = plt.axes()
ax2.set_title('paraxial focus')

foc_x = []
foc_y = []

for o in origins:
    x1 = []
    y1 = []
    r = rt.Ray(pos = [o[0], o[1], 0.], direc=[0., 0., 1.])
    lens.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    x1.append(points[1][0])
    y1.append(points[1][1])
    ax1.plot(x1, y1, 'r.')

    x2 = []
    y2 = []
    x2.append(points[-1][0])
    y2.append(points[-1][1])

    foc_x.append(x2)
    foc_y.append(y2)

    ax2.plot(x2, y2, 'b.')

# calculates the rms deviation for each of x and y from the expected focus (0, 0)
rmsd_x = sp.sqrt(sp.sum((-sp.array(foc_x))**2)/len(foc_x))
rmsd_y = sp.sqrt(sp.sum((-sp.array(foc_y))**2)/len(foc_y))

print("The RMSD for the x direction is: " + str(rmsd_x))
print("The RMSD for the y direction is: " + str(rmsd_y))
"""

for i in range(-10, 10):
    y = []
    z = []
    r = rt.Ray(pos = [0., i, 0.], direc=[0., 0, 1.])
    lens.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    for point in points:
        y.append(point[1])
        z.append(point[2])
    plt.plot(z, y, 'r-')


for i in range(-10, 10):
    y = []
    z = []
    r = rt.Ray(pos = [0., i, 0.], direc=[0., -0.25, 1.])
    lens.propagate_ray(r)
    output.propagate_ray(r)
    points = r.vertices()
    for point in points:
        y.append(point[1])
        z.append(point[2])
    plt.plot(z, y, 'b-')
"""


plt.show()
