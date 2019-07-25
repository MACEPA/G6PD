import os
from FlowCytometryTools import FCMeasurement
from mosaic_functions import model_table, prep_fcs, calc_bright_cells
from mosaic_classes import MosaicMetadata

import dash
import dash_core_components as dcc
import dash_html_components as html
# from dash_table import DataTable as DT
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(
        id='input_dir',
        type='text',
        value='C:/Users/lzoeckler/Desktop/maria_data/Archive_facs'
    ),
    html.Button(
        id='set_dir',
        n_clicks=0,
        children='Set directory'
    ),
    dcc.Dropdown(
        id='file_dropdown'
    ),
    dcc.Input(
        id='fsc_lower',
        type='number',
        value=.4
    ),
    dcc.Input(
        id='fsc_upper',
        type='number',
        value=.95
    ),
    dcc.Input(
        id='ssc_lower',
        type='number',
        value=.05
    ),
    dcc.Input(
        id='ssc_upper',
        type='number',
        value=.6
    ),
    dcc.Input(
        id='fl1',
        type='text',
        value='FL1-A'
    ),
    dcc.Input(
        id='fsc',
        type='text',
        value='FSC-H'
    ),
    dcc.Input(
        id='ssc',
        type='text',
        value='SSC-H'
    ),
    dcc.RadioItems(
        id='amplification',
        options=[{'label': 'True', 'value': 1},
                 {'label': 'False', 'value': 0}],
        value=1
    ),
    dcc.Input(
        id='min_peak_size',
        type='number',
        value=.00003
    ),
    html.Button(
        id='submit_button',
        n_clicks=0,
        children='Set parameters'
    ),
    html.Div(
        id='test_id'
    )
    # DT(
    #     id='df',
    #     columns=[],
    #     data={}
    # )
])


# @app.callback(
#     Output('df', )
# )


@app.callback(
    Output('file_dropdown', 'options'),
    [Input('set_dir', 'n_clicks')],
    [State('input_dir', 'value')])
def set_file_paths(n_clicks, directory):
    files = os.listdir(directory)
    files = [file for file in files if file.endswith('.fcs')]
    options = [{'label': file, 'value': '{}/{}'.format(directory, file)} for file in files]
    return options


@app.callback(
    Output('test_id', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('input_dir', 'value'),
     State('file_dropdown', 'value'),
     State('fsc_lower', 'value'),
     State('fsc_upper', 'value'),
     State('ssc_lower', 'value'),
     State('ssc_upper', 'value'),
     State('fl1', 'value'),
     State('fsc', 'value'),
     State('ssc', 'value'),
     State('amplification', 'value'),
     State('min_peak_size', 'value')])
def main(n_clicks, input_dir, file_dropdown, fsc_lower, fsc_upper,
         ssc_lower, ssc_upper, fl1, fsc, ssc, amplification,
         min_peak_size):
    fsc_filt = [fsc_lower, fsc_upper]
    ssc_filt = [ssc_lower, ssc_upper]
    if file_dropdown:
        mosaic = MosaicMetadata(input_dir, fsc_filt, ssc_filt,
                                fl1, fsc, ssc, amplification,
                                min_peak_size)
        # test = FCMeasurement(ID='', datafile=file_dropdown)
        # channels = test.channels
        #
        # # table = model_table(mosaic)
        #
        data = prep_fcs(file_dropdown, mosaic)
        bc_percent, mean_fitc, median_fitc, sd_fitc = calc_bright_cells(data, mosaic)

        return bc_percent
    else:
        return "waiting..."


# @app.callback(
#     Output(),
#     Input()
# )
# def generate_table(df, max_rows=10):
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in df.columns])] +
#         # Body
#         [html.Tr([
#             html.Td(df.iloc[i][col]) for col in df.columns
#         ]) for i in range(min(len(df), max_rows))]
#     )


if __name__ == '__main__':
    app.run_server(debug=True)
    # input_dir = 'C:/Users/lzoeckler/Desktop/maria_data/Archive_facs'
    # file_path = 'C:/Users/lzoeckler/Desktop/maria_data/Archive_facs/1.fcs'
    # fsc_filt = [0.4, 0.95]
    # ssc_filt = [0.05, 0.6]
    # fl1 = 'FL1-A'
    # fsc = 'FSC-H'
    # ssc = 'SSC-H'
    # amplification = 1
    # min_peak_size = 0.00003
    # mosaic_object = MosaicMetadata(input_dir, fsc_filt, ssc_filt,
    #                                fl1, fsc, ssc, amplification,
    #                                min_peak_size)
    # data = prep_fcs(file_path, mosaic_object)
    # bc_percent, mean_fitc, median_fitc, sd_fitc = calc_bright_cells(data, mosaic_object)
    # print(bc_percent)
