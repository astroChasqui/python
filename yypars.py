#!/usr/bin/env python
import q2

def main(Star):
    sp = q2.yypars.SolvePars(key_parameter_known='logg')
    sp.smooth_window_len_logl = 5
    sp.smooth_window_len_mv = 11
    sp.smooth_window_len_r = 7
    pp = q2.yypars.PlotPars()
    q2.yypars.solve_one(Star, sp, pp)
    print(Star.name)
    print("-"*len(Star.name))
    print("Age (Gyr) = {0:.1f} [{1:.1f} - {2:.1f}] [{3:.1f} - {4:.1f}]".
          format(Star.yyage["most_probable"],
                 Star.yyage["lower_limit_1sigma"],
                 Star.yyage["upper_limit_1sigma"],
                 Star.yyage["lower_limit_2sigma"],
                 Star.yyage["upper_limit_2sigma"])
         )
    print("Mass (Msun) = {0:.2f} [{1:.2f} - {2:.2f}] [{3:.2f} - {4:.2f}]".
          format(Star.yymass["most_probable"],
                 Star.yymass["lower_limit_1sigma"],
                 Star.yymass["upper_limit_1sigma"],
                 Star.yymass["lower_limit_2sigma"],
                 Star.yymass["upper_limit_2sigma"])
         )

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
               description='Uses Y2 isochrones to derive stellar parameters')
    parser.add_argument('name', help='The name of the star')
    parser.add_argument('teff', help='effective temperature (K)', type=int)
    parser.add_argument('err_teff', help='error', type=int)
    parser.add_argument('logg', help='surface gravity [cgs]', type=float)
    parser.add_argument('err_logg', help='error', type=float)
    parser.add_argument('feh', help='iron abundance', type=float)
    parser.add_argument('err_feh', help='error', type=float)
    main(parser.parse_args())
