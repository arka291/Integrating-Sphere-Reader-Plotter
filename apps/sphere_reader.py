import base64
import datetime
import io
from app import app
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
from dash import dash_table
import pandas as pd

layout = html.H1('Integrating Sphere Reader',
                 style={"color": "white", "backgroundColor": "black", "textAlign": "center"}), \
         html.H2([
             dcc.Upload(
                 id='upload-datasets',
                 children=html.H3([html.A('Upload Text or CSV or XLS Files')],
                                  style={"textAlign": "center", "borderStyle": "dashed"}),

                 # Allow multiple files to be uploaded
                 multiple=True

             ),

             html.Div(id='output-div', style={'backgroundColor': 'black'}),
             html.H5(id='output-datatable'),

         ]),


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'txt' or 'csv' in filename:
            # Assume that the user uploaded a txt file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter='\t', index_col=False)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.H3([
        html.Div(filename, style={"textAlign": "center"}),
        html.Div(datetime.datetime.fromtimestamp(date), style={"textAlign": "center"}),
        html.P("Insert X axis datasets", style={"textAlign": "center"}),
        dcc.Dropdown(id='xaxis-datasets', style={"textAlign": "center"},
                     options=[{'label': x, 'value': x} for x in df.columns]),
        html.P("Insert Y axis datasets", style={"textAlign": "center"}),
        dcc.Dropdown(id='yaxis-datasets', style={"textAlign": "center"},
                     options=[{'label': x, 'value': x} for x in df.columns]),
        html.P("Insert secondary Y axis datasets", style={"textAlign": "center"}),
        dcc.Dropdown(id='2yaxis-datasets', style={"textAlign": "center"},
                     options=[{'label': x, 'value': x} for x in df.columns]),

        html.Button(id="submit-button", children="Create Graph",
                    style={'font-size': '12px', 'display': 'inline-block',
                           'width': '100%', 'height': '40px', 'textAlign': 'center', 'borderWidth': '5px'}),
        html.Hr(),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={'backgroundColor': 'rgb(60, 60, 60)', 'color': 'white'},
        ),
        dcc.Store(id='stored-datasets', data=df.to_dict('series')),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(
    Output('output-datatable', 'children'),
    Input('upload-datasets', 'contents'),
    [State('upload-datasets', 'filename'),
     State('upload-datasets', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@app.callback(
    Output('output-div', 'children'),
    [Input('submit-button', 'n_clicks'),
     Input('stored-datasets', 'data'),
     Input('xaxis-datasets', 'value'),
     Input('yaxis-datasets', 'value'),
     Input('2yaxis-datasets', 'value')])
def make_graphs(n, data, x_data, y_data, y2_data):
    # print(data)
    if n is None:

        return dash.no_update

    elif x_data == 'Spectrometer Wavelength' and y_data == 'Spectrometer Intensity' and y2_data == None:

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data[x_data], y=data[y_data]))
        fig.layout.template = 'plotly_dark'
        fig.update_xaxes(type='log')
        fig.update_yaxes(type='log')
        fig.update_xaxes(title_text="<b>Wavelength[nm]</b>")
        fig.update_yaxes(title_text="<b>Spectral Intensity[W/nm]</b>")
        fig.update_layout(title_text="wavelength vs intensity")

        return dcc.Graph(figure=fig)

    elif x_data == "Sphere_evaluation_file Luminance" and y_data == "Sphere_evaluation_file EQE" and y2_data == "Sphere_evaluation_file P_eff":
        subfig = make_subplots(specs=[[{"secondary_y": True}]])
        fig = px.line(data_frame=data, x=x_data, y=y_data)
        fig2 = px.line(data_frame=data, x=x_data, y=y2_data)
        fig2.update_traces(yaxis="y2")
        subfig.add_traces(fig.data + fig2.data)
        subfig.layout.height = 800
        subfig.layout.width = 800
        subfig.layout.template = 'plotly_dark'  # 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none'
        subfig.layout.xaxis.title = "<b>Luminance [cd/m^2]</b>,abs."
        subfig.layout.xaxis.type = "log"
        subfig.layout.yaxis.title = "<b>EQE[%]</b>"
        subfig.layout.yaxis.type = "linear"
        subfig.layout.yaxis.range = [0, 10]
        subfig.layout.yaxis2.title = "<b>P_eff[lm/W]</b>"
        subfig.layout.yaxis2.type = "linear"
        subfig.layout.yaxis2.range = [0, 10]
        subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
        return dcc.Graph(figure=subfig)

    elif x_data == "Sphere_evaluation_file Voltage" and y_data == "Sphere_evaluation_file Current density" and y2_data == "Sphere_evaluation_file Luminance":

        subfig = make_subplots(specs=[[{"secondary_y": True}]])

        fig = px.line(data_frame=data, x=x_data, y=y_data,
                      log_x=True, log_y=True, template='ggplot2')
        fig2 = px.line(data_frame=data, x=x_data, y=y2_data,
                       log_x=True, log_y=True, template='ggplot2')

        fig2.update_traces(yaxis="y2")
        subfig.add_traces(fig.data + fig2.data)
        subfig.layout.height = 800
        subfig.layout.width = 800
        subfig.layout.template = 'plotly_dark'
        subfig.layout.xaxis.title = "Voltage"
        subfig.layout.xaxis.type = "log"
        subfig.layout.yaxis2.type = "log"
        subfig.layout.yaxis.type = "log"
        subfig.layout.yaxis.title = "Luminance"
        subfig.layout.yaxis2.title = "Current Density"
        subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
        return dcc.Graph(figure=subfig)
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data[x_data], y=data[y_data]))
        fig.layout.template = 'plotly_dark'
        fig.update_xaxes(type='log')
        fig.update_yaxes(type='log')
        return dcc.Graph(figure=fig)
