import argparse
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
# custom functions and classes
from mosaic_functions import model_table, prep_fcs, calc_bright_cells
from mosaic_classes import MosaicMetadata


def main(input_dir, generate_table, file_name, generate_graph,
         fsc_filt, ssc_filt, fl1, fsc, ssc, amplification,
         min_peak_size):
    mosaic = MosaicMetadata(input_dir, fsc_filt, ssc_filt,
                            fl1, fsc, ssc, amplification,
                            min_peak_size)

    if generate_table:
        table = model_table(mosaic)
        table.to_csv('C:/Users/lzoeckler/Desktop/MOSAIC/mosaic_zygosity.csv', index=False)

    if generate_graph:
        file_path = '{}/{}.fcs'.format(mosaic.input_dir, file_name)
        data = prep_fcs(file_path, mosaic)
        outputs = calc_bright_cells(data, mosaic)
        pp = PdfPages('C:/Users/lzoeckler/Desktop/MOSAIC/test_graph.pdf')
        f = plt.figure()
        f.add_subplot()
        plt.plot(outputs.intensity, outputs.frequency)
        plt.plot(outputs.x_vals, outputs.y_vals, "o", color='k')
        title = 'file: {}'.format(file_name)
        plt.title(title)
        plt.tight_layout()
        pp.savefig(f)
        plt.close()
        pp.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--input_dir', type=str,
                        default='C:/Users/lzoeckler/Desktop/maria_data/Archive_facs',
                        help='Directory that contains FCS files')
    parser.add_argument('-gt', '--generate_table', action='store_true',
                        help='Whether or not to generate the zygosity table')
    parser.add_argument('-fn', '--file_name', type=str,
                        default=None,
                        help='File name of the file to generate a graph of')
    parser.add_argument('-gg', '--generate_graph', action='store_true',
                        help='Whether or not to generate a brightness graph')
    parser.add_argument('-ff', '--fsc_filt', nargs='+',
                        default=[.4, .95],
                        help='Minimum and maximum FSC channel values')
    parser.add_argument('-sf', '--ssc_filt', nargs='+',
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
                        default=.00003,
                        help='Minimum peak height to keep')
    args = parser.parse_args()
    main(input_dir=args.input_dir, generate_table=args.generate_table, file_name=args.file_name,
         generate_graph=args.generate_graph, fsc_filt=args.fsc_filt, ssc_filt=args.ssc_filt,
         fl1=args.fl1, fsc=args.fsc, ssc=args.ssc, amplification=args.amplification,
         min_peak_size=args.min_peak_size)
