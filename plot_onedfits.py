#!/usr/bin/env python

import onedfits
import matplotlib.pyplot as plt
import numpy as np


def main(spectrum, wmin, wmax, fname, ymin=0.00, ymax=1.05):
    w, f, hd = onedfits.main(spectrum)
    k = np.logical_and(w > wmin, w < wmax)
    wk, fk = w[k], f[k]
    plt.figure(figsize=(7, 5))
    plt.plot(wk, fk)
    plt.ylim([ymin, ymax])
    plt.savefig(fname)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
               description='Plots a section of a 1D FITS spectrum')
    parser.add_argument('spectrum', help='the FITS file')
    parser.add_argument('wmin', help='Initial wavelength', type=float)
    parser.add_argument('wmax', help='Final wavelength', type=float)
    parser.add_argument('fname', help='Name of output file')
    parser.add_argument('-ymin', '--ymin', default=0.00, type=float,\
                        help='Minimum value of y-axis')
    parser.add_argument('-ymax', '--ymax', default=1.05, type=float,\
                        help='Maximum value of y-axis')
    args = parser.parse_args()
    main(args.spectrum, args.wmin, args.wmax, args.fname,
         args.ymin, args.ymax)
