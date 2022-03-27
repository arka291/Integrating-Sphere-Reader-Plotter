import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import sphere_reader


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1([
        dcc.Link('| Sphere Reader', href='/apps/sphere_reader'),
        dcc.Link('| Simulator |', href='/apps/simulator')
    ], className="row",style={"color": "white", "backgroundColor": "grey", "textAlign": "center"}),
    html.Div(id='page-content', children=[])

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/sphere_reader':
        return sphere_reader.layout
    if pathname == '/apps/global_sales':
        return simulator.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)
