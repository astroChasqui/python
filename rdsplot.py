#!/usr/bin/env python
"""Reads splot.log file from IRAF to create a CSV linelist

splot.log should be the result of many EW measurements
file_in: your splot.log file
template: a CSV linelist that will be used as template to search for values
in splot.log file
file_out: a CSV file with the results of the search
window=0.1: wavelength window to look for lines (0.1 A is the default)
"""
__author__ = 'Ivan Ramirez (UT Austin)'
__email__ = 'ivan@astro.as.utexas.edu'


import logging
import numpy as np
from pandas import read_csv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

def main(file_in, template, file_out, window=0.1, inspect=False):
    logger.info('Reading input file: '+file_in)
    f = open(file_in, 'r')
    sp, ww, ew = [], [], []
    frl = f.readlines()
    for nline, line in zip(range(1, len(frl)+1), frl):
        if inspect:
            print ("Line {0}: {1}".format(nline, line))
        if '[' in line:
            xi = line.rfind('/')+1
            if xi == 0:
                xi = line.rfind('[')+1
            line = line.replace(".fits", "")
            xf = line.find(']')
            spectrum = line[xi:xf]
        if len(line) > 1 and line[4:10] != 'center' and '[' not in line \
           and line.replace(" ", "") != "\n":
                linex = line.split()
                sp.append(spectrum)
                ww.append(float(linex[0]))
                ew.append(float(linex[3]))
    f.close()

    x = read_csv(template)

    stars = sorted(set(sp))
    f = open(file_out, 'w')
    f.write('wavelength,species,ep,gf,'+','.join(stars)+'\n')

    print("Multiple measurements of the same line on the same star will "+\
          "be listed here:")
    print("id                wave     ew  stdev %err  n")
    print("--------------- ------- -----  ----- ---- --")
    for wave, spi, epi, gfi in \
                     zip(x['wavelength'], x['species'], x['ep'], x['gf']):
        line = str(wave)+','+ \
               str(spi)+','+str(epi)+','+str(gfi)
        there_is_data = False
        ni = 0
        for star in stars:
            if wave < 0: #HFS
                if prev_line.split(',')[4+ni] != '':
                    line += ',0'
                else:
                    line += ','
                ni += 1
                continue
            match_ww = np.where((abs(np.array(ww)-wave) < window))
            match_sp = np.where(np.array(sp) == star)
            ks = set(match_ww[0])&set(match_sp[0])
            ews = [ew[k] for k in ks]
            if len(ews) > 0:
                line += ','+str(round(1000*np.mean(ews),1))
                there_is_data = True
                if len(ews) > 1:
                    mews = 1000*np.mean(ews)
                    sews = 1000*np.std(ews)
                    err_ews = 100*sews/mews
                    print( '{0:15s} {1:.2f} {2:5.1f} {3:5.1f} {4:5.1f} {5:2d}'.
                          format(star, round(wave,2), round(mews,1),
                                 round(sews,1), round(err_ews, 1), len(ews))
                                 )
            else:
                line += ','
            prev_line = line
        if there_is_data or wave < 0:
            if (''.join(line.split(',')[4:]) != ''):
                f.write(line+'\n')
    f.close()
    logger.info('Output file: '+file_out)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
               description='reads an IRAF splot.log file and puts EW '+\
                           'measurements into a CSV file')
    parser.add_argument('file_in', help='the splot.log file')
    parser.add_argument('template', help='a template line list')
    parser.add_argument('file_out', help='output CSV file')
    parser.add_argument('-w', '--window', default=0.1, type=float,\
                        help='wavelength window to search for lines')
    parser.add_argument('-i', '--inspect', action="store_true",\
                        help='inspect input splot.log file (could be useful to figure out where in that file is the code crashing)')
    args = parser.parse_args()
    main(args.file_in, args.template, args.file_out, args.window, args.inspect)
