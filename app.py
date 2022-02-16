from dash import Dash, html, dcc, Output, Input
import altair as alt
from vega_datasets import data


# Read in global data
iris = data.iris()
iris_columns = iris.loc[:, iris.columns != 'species']

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='xcol-widget',
        value='petalLength',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in iris_columns]),
    dcc.Dropdown(
        id='ycol-widget',
        value='petalWidth',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in iris_columns])
    ])


# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol-widget', 'value'),
    Input('ycol-widget', 'value'),
)
def plot_altair(xcol, ycol):
    chart = alt.Chart(iris).mark_point().encode(
        x=xcol,
        y=ycol,
        color = 'species',
        tooltip='petalLength').interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)