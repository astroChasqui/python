#!/usr/bin/env python
import irtools
import numpy as np
from astropy.io import ascii
import logging
import os


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def many(infile, outfile, calibration="casagrande10"):
    """Calculates Teff using the Alonso et al. (1996) or the Casagrande
    et al. (2010) calibrations.

    One column of input file must have 'id' as header
    """
    coef = get_coef(calibration)

    obs = ascii.read(infile)
    k_colors = list(set(obs.dtype.names) & set(coef['color']))
    kc = ['teff_'+x for x in k_colors]
    more_keys = [prefix+elt for elt in kc for prefix in ('','err_') ]
    res_keys = ['id', 'teff_color', 'err_teff_color']
    res_keys.extend(more_keys)
    res = dict.fromkeys(res_keys, '')
    res['id'] = obs['id'][:]
    n_stars = len(obs['id'])

    for color in k_colors:
        tt, ett = [], []
        for i in range(n_stars):
            if obs[color][i] != '':
                value = float(obs[color][i])
                err_value = 0
                if 'err_'+color in obs.dtype.names:
                    if obs['err_'+color][i] == '':
                        err_value = 0
                    else:
                        err_value = float(obs['err_'+color][i])
                if obs['feh_in'][i] == '':
                    obs['feh_in'][i] = 0
                feh = float(obs['feh_in'][i])
                if 'err_feh_in' in obs.keys():
                    err_feh = float(obs['err_feh_in'][i])
                else:
                    err_feh = 0.05
                if color == 'by_' and 'c1' in obs.keys() \
                   and calibration == 'alonso96':
                    if obs['c1'][i] != "":
                        x = one(color, value, feh, coef, err_value, err_feh,\
                                c1=float(obs['c1'][i]))
                else:
                    x = one(color, value, feh, coef, err_value)
            else:
                x = None
            if x:
                tt.append(x[0])
                ett.append(x[1])
            else:
                tt.append(None)
                ett.append(None)
        res['teff_'+color] = tt
        res['err_teff_'+color] = ett

    teff = []
    eteff = []
    for i in range(n_stars):
        tt = []
        ett = []
        for color in k_colors:
            if res['teff_'+color][i] > 0:
                tt.append(res['teff_'+color][i])
                ett.append(res['err_teff_'+color][i])
        if len(tt) > 0:
            tv = irtools.wmean(tt, ett)
            teff.append(int(tv[0]))
            if tv[2] != None:
                eteff.append(int(tv[1])+int(tv[2]))
            else:
                eteff.append(int(tv[1]))
        else:
            teff.append(None)
            eteff.append(None)
    res['teff_color'] = teff
    res['err_teff_color'] = eteff

    #get rid of None s
    for k, v in res.iteritems():
        for i in range(len(v)):
          if v[i] is None:
              res[k][i] = ''

    ascii.write(res, outfile, delimiter=',', names=res_keys)


def one(color, value, feh, coef, err_value=0, err_feh=0, c1=None):
    """Calculates Teff using a color-Teff calibration.

    Example:
    >>>coef = colorteff.get_coef('casagrande10')
    >>>colorteff.one('bv', 0.35, -0.15, coef, err_value=0.01, err_feh=0.05)
    """

    if(color not in coef['color']):
        print('Calibration not available for color given.')
        return None, None

    err_msg = ''
    min_value = coef['min_value'][coef['color'] == color]
    max_value = coef['max_value'][coef['color'] == color]
    min_feh = coef['min_feh'][coef['color'] == color]
    max_feh = coef['max_feh'][coef['color'] == color]
    if value < min_value or value > max_value:
        err_msg += 'color value is outside of limits of applicability'
    if feh < min_feh or feh > max_feh:
        err_msg +=  '[Fe/H] is outside of limits of applicability'
    if err_msg != '':
        logger.warning(err_msg)
        return None, None

    a = []
    for i in range(6):
        a.append(coef['a'+str(i)][coef['color'] == color])
    teff = theta(a, value, feh)
    if 'ac1' in coef.keys() and color == 'by_' and c1 != None:
        ac1 = coef['ac1'][coef['color'] == color]
        teff = theta(a, value, feh, ac1, c1)

    etv = etf = 0
    if err_value > 0:
        tmv = theta(a, value-err_value, feh)
        tpv = theta(a, value+err_value, feh)
        etv = (tmv-tpv)/2
    if err_feh > 0:
        tmf = theta(a, value, feh-err_feh)
        tpf = theta(a, value, feh+err_feh)
        etf = (tmf-tpf)/2
    err_clbr = coef['err_clbr'][coef['color'] == color]
    err_teff = np.sqrt(etv**2+etf**2+err_clbr**2)

    return int(teff), int(err_teff)


def theta(a, value, feh, ac1=None, c1=None):
    if ac1 and c1:
        return 5040/(a[0]+a[1]*value+a[2]*value**2+a[3]*value*feh+
                     a[4]*feh+a[5]*feh**2+ac1*value*c1)
    else:
        return 5040/(a[0]+a[1]*value+a[2]*value**2+a[3]*value*feh+
                     a[4]*feh+a[5]*feh**2)

def get_coef(calibration):
    """Silly function to read the color-Teff coefficients file.

    Instead of running:
    >>>c10_coef = ascii.read('casagrande10.csv')
    You do:
    >>>c10_coef = c10teff.get_c10coef('casagrande10')

    In this way you don't have to worry about where the file actually is,
    as long as it is inside the Data directory relative to where the
    colorteff.py code lives.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    return ascii.read(os.path.join(path, 'Data', calibration+'.csv'))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
               description='use color-Teff calibrations to '+\
                           'calculate Teff of a dwarf or subgiant star from'+\
                           'its measured colors')
    parser.add_argument('infile', help='input file (csv)')
    parser.add_argument('outfile', help='output file (csv)')
    parser.add_argument('-c', '--calib', default="casagrande10",\
                        help='alonso96 or casagrande10 (default)')
    args = parser.parse_args()
    many(args.infile, args.outfile, args.calib)
