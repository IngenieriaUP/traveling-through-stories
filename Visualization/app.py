# -*- coding: utf-8 -*-
import os
import re
import dash
import dash_core_components as dcc
import dash_html_components as html
import spacy
from spacy import displacy
import pandas as pd
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer

LANGUAGE = "spanish"
SENTENCES_COUNT = 3

df = pd.read_excel('Relatos_Benvenutto.xlsx')
libro = 'Relatos_Benvenutto'
cap = list(set(df['Capitulo'].tolist()))
opto = {}
for j in cap:
    nparrafos = df[df['Capitulo']==j].count()
    nparrafos = nparrafos[0]
    listaindi = []
    for i in range(nparrafos):
        listaindi.append(str(i+1))
    poke={j: listaindi}
    opto.update(poke)
names = list(opto.keys())
nestedOptions = opto[names[0]]

nlp = spacy.load("../Research/models1")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'Reader'

if 'DYNO' in os.environ:
    # Add Google Analytics
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

app.layout = html.Div(children=[
    html.Div(children=[
        html.H1("Reader: Aplicación web de análisis de Relatos de Viajes"),
        html.Div(children=[
            html.P('Selecciona un capítulo:'),
            dcc.Dropdown(
                id='name-dropdown',
                placeholder='# Capítulo...',
                options=[{'label':name, 'value':name} for name in names],
                value = list(opto.keys())[0], # firts chap
            )], style={'width': '50%', 'display': 'inline-block'}
        ),
        html.Div(children=[
            html.P('Selecciona los párrafos:'),
            dcc.Dropdown(
                id='opt-dropdown',
                placeholder='# Párrafo...',
                multi=True,
                value=opto[list(opto.keys())[0]][0] # First option of first chap
            )], style={'width': '50%', 'display': 'inline-block'}
        ),
        html.H2("Texto analizado"),
        dcc.Textarea(
            id="input-text",
            placeholder='Ingresa el texto que deseas analizar...',
            value=df[df['Capitulo']==list(opto.keys())[0]]['Texto'].tolist()[0], # Text of first option of first chap
            style={'width': '100%',  'height': 300}
        ),
        html.Button('Iniciar análisis', id='button', style={'width': '100%'})
    ], style={'margin':'2%'}),

    html.Div(children=[
        html.H2('Resumen de texto (Algoritmo Textrank)'),
        html.P(id='viz_sum', children='', style={"border-radius": "10px"}),
        html.H2("Análisis de entidades"),
        html.Iframe(id='viz_ent', srcDoc='', height="500p", width="100%",
                    style={"border-radius": "10px"}),
        html.H2("Análisis de dependencias de sintaxis"),
        html.Iframe(id='viz_dep', srcDoc='', height="500p", width="100%",
                    style={"border-radius": "10px"}),
    ], style={'margin':'2%'})
])

def make_summary(value, language, sentence_count):
    parser = PlaintextParser.from_string(value, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer_text = TextRankSummarizer(stemmer)
    resumen = ''
    summarizer_text.stop_words = get_stop_words(language)
    summary_1 = summarizer_text(parser.document, SENTENCES_COUNT)
    for sentence in summary_1:
    	resumen = resumen + str(sentence) + '\n'

    return resumen

@app.callback(
    [dash.dependencies.Output('viz_dep', 'srcDoc'),
     dash.dependencies.Output('viz_ent', 'srcDoc'),
     dash.dependencies.Output('viz_sum', 'children')],
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-text', 'value')]
    )
def update_viz_dep(n_clicks, value):
    if value is None:
        raise dash.exceptions.PreventUpdate

    doc = nlp(value)
    dep_viz = displacy.render([doc], style="dep", page=False)
    ent_viz = displacy.render([doc], style="ent", page=False)
    resumen = make_summary(value, LANGUAGE, SENTENCES_COUNT)

    return dep_viz, ent_viz, resumen

@app.callback(
    [dash.dependencies.Output('opt-dropdown', 'options'),
     dash.dependencies.Output('opt-dropdown', 'value'),],
    [dash.dependencies.Input('name-dropdown', 'value')]
    )
def update_date_dropdown(name):
    return [{'label': i, 'value': i} for i in opto[name]], opto[name][0]

@app.callback(
    dash.dependencies.Output('input-text', 'value'),
    [dash.dependencies.Input('opt-dropdown', 'value')],
    [dash.dependencies.State('name-dropdown', 'value')]
    )
def updateTextarea(selected_value,name):
    dfparte = df[df['Capitulo'] == name]
    dfparte = dfparte['Texto'].tolist()
    temp = ''
    for i in selected_value:
        temp = temp + '\n' + dfparte[int(i) - 1]

    return temp

if __name__ == '__main__':
    if 'DYNO' in os.environ:
        app.run_server(debug=False)
    else:
        app.run_server(debug=True)
