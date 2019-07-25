import os
import argparse
from FlowCytometryTools import FCMeasurement
from Mosaic.mosaic_functions import model_table, prep_fcs, calc_bright_cells
from Mosaic.mosaic_classes import MosaicMetadata

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(
        id='input_dir',
        type='text',
        value='Input directory here'
    ),
    dcc.Dropdown(
        id='file_dropdown'
    ),
    dcc.Input(
        id='fsc_filt',
        type='text',
        value='[.4, .95]'
    ),
    dcc.Input(
        id='ssc_filt',
        type='text',
        value='[.05, .6]'
    ),
    dcc.Input(
        id='fl1',
        type='number',
        value=9
    ),
    dcc.Input(
        id='fsc',
        type='number',
        value=7
    ),
    dcc.Input(
        id='ssc',
        type='number',
        value=8
    ),
    dcc.RadioItems(
        id='amplification',
        options=[True, False],
        value=False
    ),
    dcc.Input(
        id='min_peak_size',
        type='number',
        value=.003
    ),
    html.Button(
        id='submit_bottom',
        n_clicks=0,
        children='Submit'
    )
])


@app.callback(
    Output('file_dropdown', 'options'),
    [Input('input_dir', 'value')])
def set_file_paths(directory):
    return os.listdir(directory)


@app.callback(
    Output('test_id', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('input_dir', 'value'),
     State('file_dropdown', 'value'),
     State('fsc_filt', 'value'),
     State('ssc_filt', 'value'),
     State('fl1', 'value'),
     State('fsc', 'value'),
     State('ssc', 'value'),
     State('amplification', 'value'),
     State('min_peak_size', 'value')])
def main(input_dir, file_path, fsc_filt, ssc_filt,
         fl1, fsc, ssc, amplification=False,
         min_peak_size=0.003):

    mosaic = MosaicMetadata(input_dir, fsc_filt, ssc_filt,
                            fl1, fsc, ssc, amplification,
                            min_peak_size)
    test = FCMeasurement(ID='', datafile=file_path)
    channels = test.channels

    # table = model_table(mosaic)

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