#!/usr/bin/env python
import irtools
import numpy as np
from astropy.io import ascii
import logging
import os


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def many(infile, outfile):
    """Calculates Teff using Casagrande et al. (2010) calibrations.

    One column of input file must have 'id' as header
    """
    path = os.path.dirname(os.path.realpath(__file__))
    c10_coef  = ascii.read(os.path.join(path, 'c10teff.csv'))

    obs = asciitable.read(infile)
    k_colors = list(set(obs.dtype.names) & set(c10_coef['color']))
    kc = ['teff_'+x for x in k_colors]
    more_keys = [prefix+elt for elt in kc for prefix in ('','err_') ]
    res_keys = ['id', 'teff_color', 'err_teff_color']
    res_keys.extend(more_keys)
    res = dict.fromkeys(res_keys, '')
    res['id'] = obs['id'][:]
    n_stars = len(obs['id'])

    for color in k_colors:
        tt = []
        ett = []
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
                x = one(color, value, feh, c10_coef, err_value)
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
            #eteff.append(int(tv[1]))
            #eteff.append(int(tv[2]))
            if tv[2] != None:
                eteff.append(int(tv[1])+int(tv[2]))
            else:
                eteff.append(int(tv[1]))
        else:
            teff.append(None)
            eteff.append(None)
    res['teff_color'] = teff
    res['err_teff_color'] = eteff

    #get rid of None s (asciitable can't handle them, apparently)
    for k, v in res.iteritems():
        for i in range(len(v)):
          if v[i] is None:
              res[k][i] = ''

    asciitable.write(res, outfile, delimiter=',', names=res_keys)
    #asciitable.write(res, outfile, delimiter=',',
    #                 names=res_keys, fill_values = (None, '---') )


def one(color, value, feh, c10_coef, err_value=0, err_feh=0):
    """Calculates Teff using Casagrande et al. (2010) calibrations.

    Example:
    >>>c10_coef = asciitable.read('c10teff.csv')
    >>>c10teff.one('bv', 0.35, -0.15, c10_coef, err_value=0.01, err_feh=0.05)
    """

    if(color not in c10_coef['color']):
        print('Calibration not available for color given.')
        return None

    err_msg = ''
    min_value = c10_coef['min_value'][c10_coef['color'] == color]
    max_value = c10_coef['max_value'][c10_coef['color'] == color]
    min_feh = c10_coef['min_feh'][c10_coef['color'] == color]
    max_feh = c10_coef['max_feh'][c10_coef['color'] == color]
    if value < min_value or value > max_value:
        err_msg += 'color value is outside of limits of applicability'
    if feh < min_feh or feh > max_feh:
        err_msg +=  '[Fe/H] is outside of limits of applicability'
    if err_msg != '':
        logger.warning(err_msg)
        return None

    a = []
    for i in range(6):
        a.append(c10_coef['a'+str(i)][c10_coef['color'] == color])
    teff = theta(a, value, feh)

    etv = etf = 0
    if err_value > 0:
        tmv = theta(a, value-err_value, feh)
        tpv = theta(a, value+err_value, feh)
        etv = (tmv-tpv)/2
    if err_feh > 0:
        tmf = theta(a, value, feh-err_feh)
        tpf = theta(a, value, feh+err_feh)
        etf = (tmf-tpf)/2
    err_clbr = c10_coef['err_clbr'][c10_coef['color'] == color]
    err_teff = np.sqrt(etv**2+etf**2+err_clbr**2)

    return int(teff), int(err_teff)


def theta(a, value, feh):
    return 5040/(a[0]+a[1]*value+a[2]*value**2+a[3]*value*feh+
                 a[4]*feh+a[5]*feh**2)


def get_c10coef():
    """Silly function to read the C10 coefficients file.

    Instead of running:
    >>>c10_coef = asciitable.read('c10teff.csv')
    You do:
    >>>c10_coef = c10teff.get_c10coef()
    
    In this way you don't have to worry about where the file actually is,
    as long as it is in the same directory where the c10teff.py code lives.
    """
    path = os.path.dirname(os.path.realpath(__file__))
    return ascii.read(os.path.join(path, 'c10teff.csv'))


if __name__ == "__main__":
    import sys
    many(sys.argv[1], sys.argv[2])
