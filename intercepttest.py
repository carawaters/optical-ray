import raytracer

s = raytracer.SphericalRefraction(z_0=1, curve=0.25, n1=1, n2=0.8, aperture=3)
r = raytracer.Ray(pos=[1.,2.,3.], direc=[1.,2.,3.])
print(s.intercept(r))

s2 = raytracer.SphericalRefraction(z_0=0, curve=0.8, n1=1, n2=0.8, aperture=10)
r2 = raytracer.Ray(pos=[4.,5.,6.], direc=[1.,2.,3.])
print(s2.intercept(r2))
# imag result, filtered as expected

s3 = raytracer.SphericalRefraction(z_0=1, curve=0.4, n1=1, n2=0.8, aperture=5)
r3 = raytracer.Ray(pos=[7.,8.,9.], direc=[4.,0.,1.])
print(s3.intercept(r3))
# imag result, filtered as expected

# Would be much easier to see these intercepts are in the right place once plotting multiple rays
