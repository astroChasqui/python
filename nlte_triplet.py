#!/usr/bin/env python
from q2.abundances import nlte_triplet

def main(teff, logg, feh, ao):
    return nlte_triplet(teff, logg, feh, ao)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
               description='calculate non-LTE corrections for the 777 nm O I triplet lines using the grid by Ramirez et al. (2007)')
    parser.add_argument('teff', help='effective temperature (K)', type=float)
    parser.add_argument('logg', help='log of surface gravity [cgs]', type=float)
    parser.add_argument('feh', help='metallicity', type=float)
    parser.add_argument('ao1', help='LTE oxygen abundance 7771.9 A', type=float)
    parser.add_argument('ao2', help='LTE oxygen abundance 7774.2 A', type=float)
    parser.add_argument('ao3', help='LTE oxygen abundance 7775.4 A', type=float)
    args = parser.parse_args()
    goahead = True
    if args.teff < 4400 or args.teff > 7400:
        print('Teff outside of range of applicability [4400, 7400]')
        goahead = False
    if args.logg < 2.0 or args.logg > 5.0:
        print('log g outside of range of applicability [2.0, 5.0]')
        goahead = False
    if args.feh < -1.4 or args.feh > 0.4:
        print('[Fe/H] outside of range of applicability [-1.4, 0.4]')
        goahead = False
    if (args.ao1 < 7.0 and args.ao1 < 7.0 and args.ao2 < 7.0) or \
       (args.ao1 > 10.0 and args.ao1 > 10.0 and args.ao2 > 10.0):
        print('All LTE oxygen abundances are outside of range of applicability [7.0, 10.0]')
        goahead = False

    if goahead:
        main(args.teff, args.logg, args.feh, [args.ao1, args.ao2, args.ao3])
