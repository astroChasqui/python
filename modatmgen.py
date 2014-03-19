#!/usr/bin/env python
import q2

def main(teff, logg, feh, vt, grid, file_name):
    s = q2.Star()
    s.teff = teff
    s.logg = logg
    s.feh = feh
    s.vt = vt
    s.get_model_atmosphere(grid)
    q2.moog.create_model_in(s, file_name)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
               description='generates an input model atmosphere for MOOG'
             )
    parser.add_argument('teff', help='effective temperature (K)', type=int)
    parser.add_argument('logg', help='surface gravity [cgs]', type=float)
    parser.add_argument('feh', help='iron abundance', type=float)
    parser.add_argument('vt', help='microturbulence (km/s)', type=float)
    parser.add_argument('grid', help='model atmosphere type')
    parser.add_argument('file_name', help='MOOG input model file name')
    args = parser.parse_args()
    main(args.teff, args.logg, args.feh, args.vt, args.grid, args.file_name)
