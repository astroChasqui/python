#!/usr/bin/env python

from astropy.io import ascii
from irtools import wmean
import numpy as np

class Tables:
    dummy = 0

def main(path, rvstd):
    spectra = ascii.read("list.ec", Reader=ascii.NoHeader)
    obj = ascii.read("list.obj", Reader=ascii.NoHeader)

    refs, rv_refs, erv_refs, idx_refs = [], [], [], []
    for x in ascii.read(rvstd):
        refs.append(x[0])
        rv_refs.append(x[1])
        erv_refs.append(x[2])
        i = 0
        for s in spectra:
            if str(s[0]) == path+"/"+x[0]+".ec.fits":
                idx_refs.append(i)
            i += 1

    rv_bary, rjd = [], []
    for x in ascii.read("rvcor.out"):
        rjd.append(x[0]-2400000)
        rv_bary.append(x[2])

    fx = Tables
    for i in range(1, len(refs)+1):
        setattr(fx, str(i), ascii.read("fx."+str(i)))

    f = open('list.rv', 'w')
    for j in range(len(spectra)):
        rv, erv = [], []
        for i in range(1, len(refs)+1):
            rv.append(getattr(fx, str(i))[j][0] + rv_bary[j] +
                              rv_refs[i-1] - rv_bary[idx_refs[i-1]] )
            erv.append( max([getattr(fx, str(i))[j][1], erv_refs[i-1]]) )
        mrv, emrv_i, emrv_e = wmean(rv, erv)
        emrv = emrv_i + emrv_e
        fname = spectra[j][0]
        fname_rv0 = path+"_rv0/"+ \
                    fname[len(path)+1:].replace(".ec.fits", ".rv0.fits")
        f.write("{0:30s} {1:7.2f} {2:5.2f} {3:7.2f} {4:36s} {5:.5f} {6}\n".
                format(fname, mrv, emrv, rv_bary[j],
                       fname_rv0, rjd[j], obj[j][0].strip('"')))
    f.close

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
              description='Use after running sfxcor.cl in IRAF.\
                           Creates list.rv file which will be used by\
                           sdopcor.cl.')
    parser.add_argument('path', help='path to spectra')
    parser.add_argument('rvstd', help='RV standards file')
    args = parser.parse_args()
    main(args.path, args.rvstd)
