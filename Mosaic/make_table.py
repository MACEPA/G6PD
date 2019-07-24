import os
import numpy as np
import pandas as pd
# import calc_bright_cells function
from Mosaic.calc_bright_cells import prep_fcs, calc_bright_cells


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
        data = prep_fcs(fp, fsc_filt, ssc_filt, fl1, fsc, ssc, amplification)
        bc_percent, mean_fitc, median_fitc, sd_fitc = calc_bright_cells(data,
                                                                        fl1,
                                                                        min_peak_size)

        # make table
        zygosity[i, 1] = fp
        zygosity[i, 2] = mean_fitc
        zygosity[i, 3] = median_fitc
        zygosity[i, 4] = sd_fitc
        zygosity[i, 5] = bc_percent

    zygo_results = pd.DataFrame(data=zygosity, columns=['File Name', 'Mean FL1', 'Median FL1',
                                                        'Std Dev FL1', 'Percent Bright Cells'])
    return zygo_results

