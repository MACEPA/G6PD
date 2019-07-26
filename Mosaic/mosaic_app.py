import os
import base64
import pandas as pd
from io import BytesIO
import plotly.tools as tls
import matplotlib.pyplot as plt
import plotly.graph_objects as go
# custom functions and classes
from mosaic_functions import model_table, prep_fcs, calc_bright_cells
from mosaic_classes import MosaicMetadata
# dash stuff
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
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
    ),
    dt.DataTable(
        id='df'
    ),
    dcc.Dropdown(
        id='file_dropdown'
    ),
    html.Button(
        id='set_file',
        n_clicks=0,
        children='Select file'
    ),
    html.Div([
        dcc.Graph(id='graph')
    ])
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
    [Output('df', 'data'),
     Output('df', 'columns')],
    [Input('submit_button', 'n_clicks')],
    [State('input_dir', 'value'),
     State('fsc_lower', 'value'),
     State('fsc_upper', 'value'),
     State('ssc_lower', 'value'),
     State('ssc_upper', 'value'),
     State('fl1', 'value'),
     State('fsc', 'value'),
     State('ssc', 'value'),
     State('amplification', 'value'),
     State('min_peak_size', 'value')])
def main(n_clicks, input_dir, fsc_lower, fsc_upper,
         ssc_lower, ssc_upper, fl1, fsc, ssc, amplification,
         min_peak_size):
    fsc_filt = [fsc_lower, fsc_upper]
    ssc_filt = [ssc_lower, ssc_upper]
    if n_clicks > 0:
        mosaic = MosaicMetadata(input_dir, fsc_filt, ssc_filt,
                                fl1, fsc, ssc, amplification,
                                min_peak_size)
        # test = FCMeasurement(ID='', datafile=file_dropdown)
        # channels = test.channels

        table = model_table(mosaic)

        dash_data = table.to_dict('records')
        dash_columns = [{'name': i, 'id': i} for i in table.columns]
        return dash_data, dash_columns
    else:
        return pd.DataFrame().to_dict('records'), [{'name': '', 'id': ''}]


def fig_to_uri(in_fig, close_all=True, **save_args):
    """
    Save a figure as a URI
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)


@app.callback(
    [Output('graph', 'figure')],
    [Input('set_file', 'n_clicks')],
    [State('file_dropdown', 'value'),
     State('input_dir', 'value'),
     State('fsc_lower', 'value'),
     State('fsc_upper', 'value'),
     State('ssc_lower', 'value'),
     State('ssc_upper', 'value'),
     State('fl1', 'value'),
     State('fsc', 'value'),
     State('ssc', 'value'),
     State('amplification', 'value'),
     State('min_peak_size', 'value')]
)
def generate_graph(n_clicks, file_dropdown, input_dir, fsc_lower, fsc_upper,
                   ssc_lower, ssc_upper, fl1, fsc, ssc, amplification,
                   min_peak_size):
    fsc_filt = [fsc_lower, fsc_upper]
    ssc_filt = [ssc_lower, ssc_upper]
    if n_clicks > 0:
        mosaic = MosaicMetadata(input_dir, fsc_filt, ssc_filt,
                                fl1, fsc, ssc, amplification,
                                min_peak_size)
        data = prep_fcs(file_dropdown, mosaic)
        bright_outputs, plot_outputs = calc_bright_cells(data, mosaic)
        x_vals, y_vals, intense, freq = plot_outputs
        fig, ax = plt.subplots()
        plt.plot(intense, freq)
        plt.plot(x_vals, y_vals, "o", color='k')
        plotly_fig = tls.mpl_to_plotly(fig)
        graph_dict = {
            'data': [go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines+markers'
            )],
            'layout': {
                'yaxis': {'type': 'log'}
            }
        }
        return [graph_dict]
    else:
        return ['']


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
