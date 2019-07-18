import os
import argparse
import numpy as np
import pandas as pd
# import calc_bright_cells function
from Mosaic.calc_bright_cells import calc_bright_cells


def model_table(input_dir, fsc_filt, ssc_filt,
                fl1, fsc, ssc,
                amplification=False,
                min_peak_size=0.003):
    """
    :param input_dir: Directory containing all FCS files
    :param fsc_filt: FSC gate
    :param ssc_filt: SSC gate
    :param fl1: FL1 channel name
    :param fsc: FSC channel name
    :param ssc: SSC channel name
    :param amplification: Linear vs Log, default False (linear)
    :param min_peak_size: Minimum peak size to keep
    :return: no idea yet
    """
    all_files = os.listdir(input_dir)
    zygosity = np.zeros((len(all_files), 5))
    for i in range(len(all_files)):
        fp = all_files[i]
        bc_percent, mean_fitc, median_fitc, sd_fitc = calc_bright_cells(
            fp, fsc_filt, ssc_filt, fl1, fsc, ssc,
            amplification, min_peak_size)

        # make table
        zygosity[i, 1] = fp
        zygosity[i, 2] = mean_fitc
        zygosity[i, 3] = median_fitc
        zygosity[i, 4] = sd_fitc
        zygosity[i, 5] = bc_percent

    zygo_results = pd.DataFrame(data=zygosity, columns=['File Name', 'Mean FL1', 'Median FL1',
                                                        'Std Dev FL1', 'Percent Bright Cells'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--input_dir', type=str,
                        help='Directory that contains FCS files')
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
    model_table(input_dir=args.id, fsc_filt=args.ff, ssc_filt=args.sf, fl1=args.fl1,
                fsc=args.fsc, ssc=args.ssc, amplification=args.a, min_peak_size=args.mps)
