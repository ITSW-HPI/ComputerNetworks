import numpy as np
from scipy.stats import binom
from math import exp, log10

codeword_length = 127
snr_seq = np.logspace (-1, 1, num=31)
correct_bits = range(8)

def ber (snr, mod="dbpsk"):
    """TODO: implement errfc for other modulation schemes"""
    if mod=="dbpsk":
        return 0.5*exp(-snr)
    else:
        raise ValueError 

def per (snr, codeword_length, correctable, modulation="dbpsk"):
    """
    A packet is in error if more than the correctable number of
    bit errors occur.

    The number of bit errors inside a packet follows a binomial
    distribution, with parameter lenght of the codeword and the BER, resulting from modulation and SNR.

    The probability of a packet error is hence the probability
    that this random variable of bit error numbers is larger than the
    number of correctable number of bit errors. 
    """

    biterrorprob = ber(snr, modulation)

    packetsucc = binom.cdf ( correctable, codeword_length, biterrorprob)
    packeterrprob = 1 - packetsucc 
    
    return packeterrprob

def throughput (codeword_length, correctable, per):
    payload = codeword_length - correctable
    return payload * (1-per)


bch = {}
bch[127] = { 0:127, 1: 120, 2: 113, 3:106, 4: 99, 5: 92, 6:85, 7:78, 9:71, 10: 64}


print("snr\t"
      + "\t".join("e" + str(x) + "\tt" + str(x)
                  for x in correct_bits),
      end=""
      )

for snr in snr_seq:
    # print ("\n" + str(log10(snr)), end="")
    print ("\n" + str(snr), end="")
    for c in correct_bits: 
        correctable = 127 - bch[127][c]
        
        tmp_per = per (snr, 127, correctable)
        tmp_tp = throughput (127, correctable, tmp_per)

        print ("\t{}\t{}".format(tmp_per, tmp_tp), end="")

print()





