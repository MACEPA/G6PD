import os
import argparse
from FlowCytometryTools import FCMeasurement
from Mosaic.mosaic_functions import model_table, prep_fcs, calc_bright_cells
from Mosaic.mosaic_classes import MosaicMetadata

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_table import DataTable as DT
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
    # 
    # data = prep_fcs(file_path, mosaic)
    # bc_percent, mean_fitc, median_fitc, sd_fitc = calc_bright_cells(data, mosaic)


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
