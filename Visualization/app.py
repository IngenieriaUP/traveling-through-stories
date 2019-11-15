# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import spacy
from spacy import displacy
from sumy.utils import get_stop_words
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
LANGUAGE = "spanish"
SENTENCES_COUNT = 10
import pandas as pd
import re

nlp = spacy.load("../Research/models1")

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
        html.Iframe(id='viz_ent', srcDoc='', height="500p", width="50%"),
        html.H2('Resumen de texto (Algoritmo Textrank)'),
        html.Iframe(id='viz_sum', srcDoc='', height="500p", width="50%")
    ], style={'margin':'2%'})
])

@app.callback(
    [dash.dependencies.Output('viz_dep', 'srcDoc'),
     dash.dependencies.Output('viz_ent', 'srcDoc'),
     dash.dependencies.Output('viz_sum', 'srcDoc')],
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-text', 'value')])
def update_viz_dep(n_clicks, value):
    if value is None:
        raise dash.exceptions.PreventUpdate

    doc = nlp(value)
    dep_viz = displacy.render([doc], style="dep", page=False)
    ent_viz = displacy.render([doc], style="ent", page=False)
    parser = PlaintextParser.from_string(value,Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer_text = TextRankSummarizer(stemmer)
    resumen=''
    summarizer_text.stop_words = get_stop_words(LANGUAGE)
    summary_1 =summarizer_text(parser.document,SENTENCES_COUNT)
    for sentence in summary_1:
    	resumen=resumen+ str(sentence)+'\n'

    return dep_viz, ent_viz, resumen

if __name__ == '__main__':
    app.run_server(debug=True)
