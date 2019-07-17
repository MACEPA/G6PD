import math
import argparse
from scipy.signal import find_peaks
from scipy.stats import gaussian_kde
from scipy.interpolate import CubicSpline
from FlowCytometryTools import FCMeasurement
from statsmodels.distributions.empirical_distribution import ECDF


def calc_bright_cells(fsc_filt, ssc_filt,
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
    # data import
    all_fcs = FCMeasurement(ID='', datafile='PATH HERE')
    dat = all_fcs.data

    # remove zero elements
    dat = dat.loc[dat[fl1] > 0]

    # toggle for linear and log data
    if amplification:
        dat[fl1] = dat[fl1].apply(math.log(10))

    # run model
    fsc_ecdf = ECDF(dat[fsc])
    dat[fsc] = fsc_ecdf(dat[fsc])
    ssc_ecdf = ECDF(dat[ssc])
    dat[ssc] = ssc_ecdf(dat[ssc])
    sub_dat = dat.loc[(dat[fsc] >= fsc_filt[0]) and (dat[fsc] <= fsc_filt[1])]
    sub_dat = sub_dat.loc[(sub_dat[ssc] >= ssc_filt[0]) and (sub_dat[ssc] <= ssc_filt[1])]
    fl1h = sub_dat[fl1].as_matrix()

    # age adjustment
    ####BLANK####

    # ks density of fl1 data
    density = gaussian_kde(fl1h).evaluate(fl1h)
    sub_data['density'] = density

    # normalize data for peak intensity = 1
    d_sum = sub_test['density'].sum()
    sub_data['freq'] = sub_data['density'].apply(lambda x: x / d_sum)
    fl1h_max = sub_test[fl1].max()
    sub_data['intensity'] = sub_data[fl1].apply(lambda x: 100 * (x / fl1h_max))
    sub_test.drop_duplicates([fl1, 'density', 'freq', 'intensity'],
                             inplace=True)
    sub_test.sort_values('intensity', inplace=True)

    # Smoothing spline
    smooth_spline = CubicSpline(sub_data['intensity'], sub_test['freq'])
    freq_x = smooth_spline(sub_test['freq'])
    intense = sub_data['intensity'].as_matrix()
    freq = sub_data['freq'].as_matrix()

    # peak finding function!
    peaks1, properties1 = find_peaks(freq_x)
    x_vals = intense[peaks1]
    y_vals = freq[peaks1]

    # return data subset to just peaks
    peaks_data = sub_data.loc[sub_data['freq'].isin(y_vals)]
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
        abs_condition = abs(sub_test['intensity'] - maxima_mean)
        min_condition = min(abs_condition)
        mean_data = sub_test.loc[abs_condition == min_condition]
        meanidx = max(mean_data['intensity'])

    # return percentage bright cells
    if len(maxima) == 2:
        upper_freq = sub_test.loc[sub_test['intensity'] >= meanidx,
                                  'freq']
        bc_percent = round((100 * upper_freq.sum()), 1)
    elif (len(maxima) == 1) & (maxima[0] > 75):
        exp_log_maxima = math.exp(math.log(maxima[0]) - .15)
        abs_condition = abs(sub_test['intensity'] - exp_log_maxima)
        min_condition = min(abs_condition)
        exp_log_data = sub_test.loc[abs_condition == min_condition]
        exp_log_val = max(exp_log_data['intensity'])
        exp_log_freq = exp_log_data.loc[
            exp_log_data['intensity'] >= exp_log_val, 'freq']
        bc_percent = round((100 * exp_log_freq.sum()), 1)
    elif (len(maxima) == 1) & (maxima[0] <= 75):
        exp_log_maxima = math.exp(math.log(maxima[0]) + .15)
        abs_condition = abs(sub_test['intensity'] - exp_log_maxima)
        min_condition = min(abs_condition)
        exp_log_data = sub_test.loc[abs_condition == min_condition]
        exp_log_val = max(exp_log_data['intensity'])
        exp_log_freq = exp_log_data.loc[
            exp_log_data['intensity'] >= exp_log_val, 'freq']
        bc_percent = round((100 * exp_log_freq.sum()), 1)
    else:
        raise ValueError('Something went wrong!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-ff', '--fsc_filt', type=list,
                        default=[.4,.95],
                        help='Minimum and maximum FSC channel values')
    parser.add_argument('-sf', '-ssc_filt', type=list,
                        default=[.05,.6],
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
    calc_bright_cells(fsc_filt=args.ff, ssc_filt=args.sf, fl1=args.fl1, fsc=args.fsc,
                      ssc=args.ssc, amplification=args.a, min_peak_size=args.mps)
