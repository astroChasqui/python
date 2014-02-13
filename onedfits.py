from astropy.io import fits
from astropy.wcs import WCS
import numpy as np

def main(filename):
    '''Read a 1D spectrum (wavelength, flux)

    USAGE: w, f, hd = onedfits.main("spectrum.fits")
    '''
    sp = fits.open(filename)
    header = sp[0].header
    flux = sp[0].data

    wcs = WCS(header)
    index = np.arange(header['NAXIS1'])

    wavelength = wcs.wcs_pix2world(index[:,np.newaxis], 0)
    wavelength = wavelength.flatten()

    return wavelength, flux, header
