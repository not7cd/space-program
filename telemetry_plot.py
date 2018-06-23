import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import csv

from os import listdir
from os.path import isfile, join

TELEMETRY_PATH = "telemetry/"

server = Flask(__name__)
app = dash.Dash()

telemetry_files = [
    {"label": f, "value": join(TELEMETRY_PATH, f)}
    for f in listdir(TELEMETRY_PATH)
    if isfile(join(TELEMETRY_PATH, f))
]


app.layout = html.Div(
    [
        html.H1("KSP Telemetry Archive"),
        dcc.Dropdown(
            id="my-dropdown", options=telemetry_files, value=telemetry_files[0]["value"]
        ),
        dcc.Graph(id="my-graph"),
        dcc.Graph(id="g-force"),
    ]
)


@app.callback(Output("my-graph", "figure"), [Input("my-dropdown", "value")])
def update_graph(selected_dropdown_value):

    alt = {"x": [], "y": []}
    with open(selected_dropdown_value, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            alt["x"].append(row["met"])
            alt["y"].append(row["mean_altitude"])

    return {"data": [alt]}

@app.callback(Output("g-force", "figure"), [Input("my-dropdown", "value")])
def update_graph_g_force(selected_dropdown_value):

    g_force = {"x": [], "y": []}
    with open(selected_dropdown_value, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            g_force["x"].append(row["met"])
            g_force["y"].append(row["g_force"])

    return {"data": [g_force]}


if __name__ == "__main__":
    app.run_server(debug=True)
