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

def a(t, n):
    return an_coeff(n) * sin(2*pi*n*f* t)

def b(t, n):
    return bn_coeff(n) * cos(2*pi*n*f* t)

def harmonic (t, uppern):
    return c + sum (a(t, i) for i in range(1, uppern))  + sum (b(t, i) for i in range(1, uppern)) 


def lowpass (t):
    return c + sum (1./(i*i) * a(t, i) for i in range(1, 11))  + sum (1./(i*i) * b(t, i) for i in range(1, 11)) 

def bandpass (t):
    return c + sum (1./abs(9.5-i) * a(t, i) for i in range(1, 21))  + sum (1./abs(9.5-i) * b(t, i) for i in range(1, 21)) 


result = {}
for h in harmonics:
    result[h] = [harmonic(t, h+1) for t in x]
result["lowpass"] = [lowpass(t) for t in x]
result["bandpass"] = [bandpass(t) for t in x]
result["lowpass_noisy"] = [lowpass(t) + gauss(0, noiseSigma) for t in x ]
result["bandpass_noisy"] = [bandpass(t) + gauss(0, noiseSigma) for t in x]

    
print ("t\t" + "\t".join(str(h) for h in harmonics) +"\t low \t band \t lowNoise \t bandNoise"  )
for t, i in enumerate(x):
    print(str(i) + "\t" + "\t".join(str(result[h][t]) for h in harmonics)
          + "\t" + str(result["lowpass"][t]) + "\t" + str(result["bandpass"][t])
          + "\t" + str(result["lowpass_noisy"][t]) + "\t" + str(result["bandpass_noisy"][t])
          )
    
    
    
    
    
