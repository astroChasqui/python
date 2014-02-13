#!/usr/bin/env python
import c10teff
from astropy.io import ascii

def main(color, value, feh):
    c10_coef = ascii.read('/home/ivan/Dropbox/Code/python/q2/Data/'+\
                          'ColorTeff/c10teff.csv')
    res = c10teff.one(color, value, feh, c10_coef)
    if res != None:
        print(res[0])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
               description='use Casagrande et al. (2010) calibrations to '+\
                           'calculate Teff of a dwarf or subgiant star using'+\
                           'its measured colors')
    parser.add_argument('color', help='identification (e.g., bv for B-V)')
    parser.add_argument('color_value',
                        help='measurement (e.g., 0.641 for the solar B-V)',
                        type=float)
    parser.add_argument('feh', help='the star\'s iron abundance', type=float)
    args = parser.parse_args()
    main(args.color, args.color_value, args.feh)
