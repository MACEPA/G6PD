import argparse
import numpy as np
import pandas as pd
# import calc_bright_cells function
from Mosaic.calc_bright_cells import calc_bright_cells


def model_table(fsc_filt, ssc_filt,
                fl1, fsc, ssc,
                amplification=False,
                min_peak_size=0.003):
    """
    :param fsc_filt: FSC gate
    :param ssc_filt: SSC gate
    :param fl1: FL1 channel name
    :param fsc: FSC channel name
    :param ssc: SSC channel name
    :param amplification: Linear vs Log, default False (linear)
    :param min_peak_size: Minimum peak size to keep
    :return: no idea yet
    """
    zygosity = np.zeros((len(datapath), 5))
    for i in range(len(datapath)):
        bc_percent, mean_fitc, median_fitc, sd_fitc = calc_bright_cells(
            fsc_filt, ssc_filt, fl1, fsc, ssc,
            amplification, min_peak_size)

        # make table
        zygosity[i, 1] = file_name
        zygosity[i, 2] = mean_fitc
        zygosity[i, 3] = median_fitc
        zygosity[i, 4] = sd_fitc
        zygosity[i, 5] = bc_percent

    zygo_results = pd.DataFrame(data=zygosity, columns=['File Name', 'Mean FL1', 'Median FL1',
                                                        'Std Dev FL1', 'Percent Bright Cells'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ff', '--fsc_filt', type=list,
                        default=[.4, .95],
                        help='Minimum and maximum FSC channel values')
    parser.add_argument('-sf', '-ssc_filt', type=list,
                        default=[.05, .6],
                        help='Minimum and maximum SSC channel values')
    parser.add_argument('-fl1', type=str,
                        default='FL1-A',
                        help='Name of the FL1 channel')
    parser.add_argument('-fsc', type=str,
                        default='FSC-H',
                        help='Name of the FSC channel')
    parser.add_argument('-ssc', type=str,
                        default='SSC-H',
                        help='Name of the SSC channel')
    parser.add_argument('-a', '--amplification', action='store_true',
                        help='Whether or not to run with amplification (log)')
    parser.add_argument('-mps', '--min_peak_size', type=float,
                        default=.003,
                        help='Minimum peak height to keep')
    args = parser.parse_args()
    model_table(fsc_filt=args.ff, ssc_filt=args.sf, fl1=args.fl1, fsc=args.fsc,
                ssc=args.ssc, amplification=args.a, min_peak_size=args.mps)
