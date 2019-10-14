import raytracer

s = raytracer.SphericalRefraction(z_0=0, curve=0.25, n1=1, n2=0.8, aperture=3)
r = raytracer.Ray(pos=[1.,2.,3.], direc=[1.,2.,3.])
s.intercept(r)
# 0.25834261322605867, as calculated by hand
