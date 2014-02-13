from numpy import *

def wmean(x, err_x):
    """Computes weighted mean and internal/external errors.

    """
    n = len(x)
    w = 1./power(err_x, 2)     # weights
    mx = average(x, weights=w) # mean
    ierr_mx = sqrt(1./sum(w))  # internal error
    if n > 1:                  # external error
        eerr_mx = sqrt(sum(power(x-mx, 2)*w)/((n-1)*sum(w)))
    else:
        eerr_mx = None
    return mx, ierr_mx, eerr_mx
