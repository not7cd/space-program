import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import csv

from os import listdir
from os.path import isfile, join

TELEMETRY_PATH = "telemetry/"

telemetry_files = [
    {"label": f, "value": join(TELEMETRY_PATH, f)}
    for f in listdir(TELEMETRY_PATH)
    if isfile(join(TELEMETRY_PATH, f))
]

app = dash.Dash()

app.layout = html.Div(
    [
        html.H1("KSP Telemetry Archive"),
        dcc.Dropdown(
            id="my-dropdown", options=telemetry_files, value=telemetry_files[0]["value"]
        ),
        dcc.Graph(id="my-graph"),
    ]
)


@app.callback(Output("my-graph", "figure"), [Input("my-dropdown", "value")])
def update_graph(selected_dropdown_value):

    data = {"x":[], "y":[]}
    with open(selected_dropdown_value, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data["x"].append(row['ut'])
            data["y"].append(row['mean_altitude'])

    return {"data": [data]}


if __name__ == "__main__":
    app.run_server()
