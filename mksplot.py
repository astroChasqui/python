#!/usr/bin/env python
"""Creates an IRAF script to measure EWs of many lines and stars

Needs a linelist CSV file with a column "wavelength" and a speclist CSV
file with the names of the spectra in column "id" (without .fits
extension).

By default, a getew.cl file is created, which can be called from IRAF
as cl> cl < getew.cl. That will show you all lines, one by one, for each
star, so you can measure EWs quickly and save them into the splot.log
file. Then you can use rdsplot.py to create a CSV file with your EW 
measurements. You can change the name of getew.cl to anything you want
with the file_out argument.

The directory argument is used to specify the directory where the
spectra are currently located. By default, it is assumed that the
spectra are in the working folder.
"""
__author__ = 'Ivan Ramirez (UT Austin)'
__email__ = 'ivan@astro.as.utexas.edu'


import os
import logging
from pandas import read_csv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def main(linelist, speclist, file_out='getew.cl', directory=''):
    try:
        ll = read_csv(linelist)
    except:
        logger.error('Could not read file '+linelist+'.')
        return
    try:
        nl = str(len(ll['wavelength']))
        logger.info(nl+" lines found in "+linelist+".")
    except:
        logger.error('No "wavelength" column in '+linelist+'.')
        return
    try:
        sl = read_csv(speclist)
    except:
        logger.error('Could not read file '+speclist+'.')
        return
    try:
        ns = str(len(sl['id']))
        logger.info(ns+" stars found in "+speclist)
    except:
        logger.error('No "id" column in '+speclist+'.')
        return
    f = open(file_out, 'w')
    for w in ll['wavelength']:
        if w < 0:
            continue
        for s in sl['id']:
            ds = os.path.join(directory, s)
            f.write("splot {0:30s} xmin={1:.2f} xmax={2:.2f} "\
                    "ymin=0.4 ymax=1.1\n".
                    format(ds, w-2.5, w+2.5))
    f.close()
    print(file_out+" created.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
               description='')
    parser.add_argument('linelist',
                        help='A CSV file with a "wavelength" column')
    parser.add_argument('speclist',
                        help='A CSV file with a star "id" column')
    parser.add_argument('-f', '--file_out', default='getew.cl',
                        help='output CL file')
    parser.add_argument('-d', '--directory', default='',
                        help='location of the spectra')
    args = parser.parse_args()
    main(args.linelist, args.speclist, args.file_out, args.directory)
