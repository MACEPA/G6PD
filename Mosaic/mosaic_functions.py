import math
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.stats import gaussian_kde
from scipy.interpolate import CubicSpline
from FlowCytometryTools import FCMeasurement
from statsmodels.distributions.empirical_distribution import ECDF


def prep_fcs(file_path, fsc_filt, ssc_filt,
             fl1, fsc, ssc, amplification=False):
    """
    :param file_path: Path to FCS file
    :param fsc_filt: FSC gate
    :param ssc_filt: SSC gate
    :param fl1: FL1 channel name
    :param fsc: FSC channel name
    :param ssc: SSC channel name
    :param amplification: Linear vs Log, default False (linear)
    :return: prepped FCS data, as a pandas dataframe
    """
    # data import
    all_fcs = FCMeasurement(ID='A1', datafile=file_path)
    data = all_fcs.data

    # remove zero elements
    data = data.loc[data[fl1] > 0]

    # toggle for linear and log data
    if amplification:
        data[fl1] = data[fl1].apply(math.log(10))

    # run model
    fsc_ecdf = ECDF(data[fsc])
    data[fsc] = fsc_ecdf(data[fsc])
    ssc_ecdf = ECDF(data[ssc])
    data[ssc] = ssc_ecdf(data[ssc])
    sub_data = data.loc[(data[fsc] >= fsc_filt[0]) and (data[fsc] <= fsc_filt[1])]
    sub_data = sub_data.loc[(sub_data[ssc] >= ssc_filt[0]) and (sub_data[ssc] <= ssc_filt[1])]

    return sub_data


def calc_bright_cells(data, fl1, min_peak_size=0.003):
    """
    :param data: input data, pandas dataframe
    :param fl1: FL1 channel name
    :param min_peak_size: Minimum peak size to keep
    :return: bc_percent, mean_fitc, median_fitc, sd_fitc (all floats)
    """
    fl1h = data[fl1].as_matrix()

    # mean, median, sd
    mean_fitc = round(np.mean(100 * (fl1h / max(fl1h))), 1)
    median_fitc = round(np.median(100 * (fl1h / max(fl1h))), 1)
    sd_fitc = round(np.std(100 * (fl1h / max(fl1h))), 1)

    # age adjustment
    ####BLANK####

    # ks density of fl1 data
    density = gaussian_kde(fl1h).evaluate(fl1h)
    data['density'] = density

    # normalize data for peak intensity = 1
    d_sum = data['density'].sum()
    data['freq'] = data['density'].apply(lambda x: x / d_sum)
    fl1h_max = data[fl1].max()
    data['intensity'] = data[fl1].apply(lambda x: 100 * (x / fl1h_max))
    data.drop_duplicates([fl1, 'density', 'freq', 'intensity'],
                             inplace=True)
    data.sort_values('intensity', inplace=True)

    # Smoothing spline
    smooth_spline = CubicSpline(data['intensity'], data['freq'])
    freq_x = smooth_spline(data['freq'])
    intense = data['intensity'].as_matrix()
    freq = data['freq'].as_matrix()

    # peak finding function!
    peaks1, properties1 = find_peaks(freq_x)
    x_vals = intense[peaks1]
    y_vals = freq[peaks1]

    # return data subset to just peaks
    peaks_data = data.loc[data['freq'].isin(y_vals)]
    peaks_data = peaks_data.loc[peaks_data['intensity'].isin(x_vals)]
    peaks_data = peaks_data.loc[peaks_data['freq'] > min_peak_size]
    peaks_data = peaks_data.loc[peaks_data['intensity'] < 99]

    # return maixma and meanidx(?)
    max_int = max(peaks_data['intensity'])
    len_condition = len(peaks_data.loc[peaks_data['intensity'] > max_int - 10])
    if len_condition == len(peaks_data):
        maxima = [max_int]
    else:
        min_int = min(peaks_data['intensity'])
        maxima = [min_int, max_int]
        maxima_mean = sum(maxima) / len(maxima)
        abs_condition = abs(data['intensity'] - maxima_mean)
        mean_data = data.loc[abs_condition == min(abs_condition)]
        meanidx = max(mean_data['intensity'])

    # return percentage bright cells
    if len(maxima) == 2:
        upper_freq = data.loc[data['intensity'] >= meanidx,
                                  'freq']
        bc_percent = round((100 * upper_freq.sum()), 1)
    elif (len(maxima) == 1) & (maxima[0] > 75):
        exp_log_maxima = math.exp(math.log(maxima[0]) - .15)
        abs_condition = abs(data['intensity'] - exp_log_maxima)
        exp_log_data = data.loc[abs_condition == min(abs_condition)]
        exp_log_val = max(exp_log_data['intensity'])
        exp_log_freq = exp_log_data.loc[
            exp_log_data['intensity'] >= exp_log_val, 'freq']
        bc_percent = round((100 * exp_log_freq.sum()), 1)
    elif (len(maxima) == 1) & (maxima[0] <= 75):
        exp_log_maxima = math.exp(math.log(maxima[0]) + .15)
        abs_condition = abs(data['intensity'] - exp_log_maxima)
        exp_log_data = data.loc[abs_condition == min(abs_condition)]
        exp_log_val = max(exp_log_data['intensity'])
        exp_log_freq = exp_log_data.loc[
            exp_log_data['intensity'] >= exp_log_val, 'freq']
        bc_percent = round((100 * exp_log_freq.sum()), 1)
    else:
        raise ValueError('Something went wrong!')

    return bc_percent, mean_fitc, median_fitc, sd_fitc


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
