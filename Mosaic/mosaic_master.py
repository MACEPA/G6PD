import os
import argparse
from FlowCytometryTools import FCMeasurement
from Mosaic.mosaic_functions import model_table, prep_fcs, calc_bright_cells
from Mosaic.mosaic_classes import MosaicObject


def main(input_dir, fsc_filt, ssc_filt,
         fl1, fsc, ssc, amplification=False,
         min_peak_size=0.003):

    mosaic = MosaicObject(input_dir, fsc_filt, ssc_filt,
                          fl1, fsc, ssc, amplification,
                          min_peak_size)
    test = FCMeasurement(ID='', datafile='{}/1.fcs'.format(input_dir))
    channels = test.channels

    table = model_table(mosaic)

    file_path = mosaic.get_files()
    data = prep_fcs(file_path, mosaic)
    bc_percent, mean_fitc, median_fitc, sd_fitc = calc_bright_cells(data, mosaic)


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
    main(input_dir=args.id, fsc_filt=args.ff, ssc_filt=args.sf, fl1=args.fl1,
         fsc=args.fsc, ssc=args.ssc, amplification=args.a, min_peak_size=args.mps)