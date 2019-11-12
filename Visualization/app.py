# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='RideR'),

    html.Div(children='''
        RideR: Herramienta de Analisis de Texto.
    '''),

    dcc.Textarea(
        id="input-text",
        placeholder='Enter a text...',
        value='',
        style={'width': '100%'}
    ),
    html.Button('Submit', id='button'),

    # TODO: Make width variable (related to sentence token count)
    html.Div(children=[
        html.Iframe(id='viz_dep', srcDoc='', height="300p", width="750p"),
        html.Iframe(id='viz_ent', srcDoc='', height="300p", width="750p")
    ])

])

@app.callback(
    dash.dependencies.Output('viz_dep', 'srcDoc'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-text', 'value')])
def update_viz_dep(n_clicks, value):
    if value != None:
        doc = nlp(value)
        return displacy.render([doc], style="dep", page=False)

@app.callback(
    dash.dependencies.Output('viz_ent', 'srcDoc'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-text', 'value')])
def update_viz_ent(n_clicks, value):
    if value != None:
        doc = nlp(value)
        return displacy.render([doc], style="ent", page=False)

if __name__ == '__main__':
    app.run_server(debug=True)
