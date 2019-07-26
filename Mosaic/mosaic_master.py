import argparse
import matplotlib.pyplot as plt
# custom functions and classes
from mosaic_functions import model_table, prep_fcs, calc_bright_cells
from mosaic_classes import MosaicMetadata


def main(input_dir, fsc_filt, ssc_filt,
         fl1, fsc, ssc, amplification,
         min_peak_size):
    mosaic = MosaicMetadata(input_dir, fsc_filt, ssc_filt,
                            fl1, fsc, ssc, amplification,
                            min_peak_size)

    table = model_table(mosaic)
    table.to_csv('C:/Users/lzoeckler/Desktop/mosaic_zygosity.csv')

    # data = prep_fcs(file_dropdown, mosaic)
    # bright_outputs, plot_outputs = calc_bright_cells(data, mosaic)
    # x_vals, y_vals, intense, freq = plot_outputs
    # fig, ax = plt.subplots()
    # plt.plot(intense, freq)
    # plt.plot(x_vals, y_vals, "o", color='k')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--input_dir', type=str,
                        default='C:/Users/lzoeckler/Desktop/maria_data/Archive_facs',
                        help='Directory that contains FCS files')
    parser.add_argument('-ff', '--fsc_filt', type=list,
                        default=[.4, .95],
                        help='Minimum and maximum FSC channel values')
    parser.add_argument('-sf', '--ssc_filt', type=list,
                        default=[.05, .6],
                        help='Minimum and maximum SSC channel values')
    parser.add_argument('--fl1', type=str,
                        default='FL1-A',
                        help='Name of the FL1 channel')
    parser.add_argument('--fsc', type=str,
                        default='FSC-H',
                        help='Name of the FSC channel')
    parser.add_argument('--ssc', type=str,
                        default='SSC-H',
                        help='Name of the SSC channel')
    parser.add_argument('-a', '--amplification', action='store_true',
                        help='Whether or not to run with amplification (log)')
    parser.add_argument('-mps', '--min_peak_size', type=float,
                        default=.003,
                        help='Minimum peak height to keep')
    args = parser.parse_args()
    main(input_dir=args.input_dir, fsc_filt=args.fsc_filt, ssc_filt=args.ssc_filt,
         fl1=args.fl1, fsc=args.fsc, ssc=args.ssc, amplification=args.amplification,
         min_peak_size=args.min_peak_size)
