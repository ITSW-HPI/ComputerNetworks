from math import pi, sin, cos 
from random import gauss

harmonics = [0, 1, 2, 4, 8, 16, 32, 64, 128, 1024]
x = [i/1000*8  for i in range(1000)]
T = 8
f = 1/T

c = 1/2 * 3/4 # only for these numbers!

noiseSigma = 0.1


def an_coeff(n):
    return 1/(pi*n) * (cos (pi*n/4) - cos(3*pi*n/4) + cos(6*pi*n/4) - cos(7*pi*n/4))
 

def bn_coeff(n):
    return 1/(pi*n) * (sin(3*pi*n/4) - sin(pi*n/4) + sin(7*pi*n/4) - sin(6*pi*n/4) )

def power(n):
    return an_coeff(n)**2 + bn_coeff(n)**2



print ("{}\t{}".format(0, c*c))

for i in range(1, 65):
    print ("{}\t{}".format(i, power(i)))
    
