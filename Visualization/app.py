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

    html.Nav(children=[
        html.H1(children='RideR'),

        html.P(children='''
            Herramienta de Analisis de Texto.
    ''')], style={'margin':'2%'}),

    html.Div(children=[
        dcc.Textarea(
            id="input-text",
            placeholder='Ingresa el texto que deseas analizar...',
            value='',
            style={'width': '100%'}
        ),
        html.Button('Iniciar análisis', id='button', style={'width': '100%'})
    ], style={'margin':'2%'}),

    html.Div(children=[
        html.H2("Análisis de dependencias de sintaxis"),
        html.Iframe(id='viz_dep', srcDoc='', height="500p", width="100%"),
        html.H2("Análisis de entidades"),
        html.Iframe(id='viz_ent', srcDoc='', height="500p", width="100%")
    ], style={'margin':'2%'})
])

@app.callback(
    [dash.dependencies.Output('viz_dep', 'srcDoc'),
     dash.dependencies.Output('viz_ent', 'srcDoc')],
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-text', 'value')])
def update_viz_dep(n_clicks, value):
    if value is None:
        raise dash.exceptions.PreventUpdate

    doc = nlp(value)
    dep_viz = displacy.render([doc], style="dep", page=False)
    ent_viz = displacy.render([doc], style="ent", page=False)

    return dep_viz, ent_viz

if __name__ == '__main__':
    app.run_server(debug=True)
