import streamlit as st
import re
import spacy
from spacy import displacy
import pandas as pd
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from codsyntax import *
import plotly.express as px
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
LANGUAGE = "spanish"
SENTENCES_COUNT = 3
df=pd.read_excel('Relatos_Benvenutto.xlsx')
dfvacio=df['Texto']
libro='Relatos_Benvenutto'
@st.cache
def listar(df):
	cap=list(set(df['Capitulo'].tolist()))
	return cap
st.title('Prueba')
cap=listar(df)
chapter=st.sidebar.selectbox('Capitulo',cap)
@st.cache
def indices(chapter):
	nparrafos=df[df['Capitulo']==chapter].count()
	nparrafos=nparrafos[0]
	listaindi=[]
	for i in range(nparrafos):
		listaindi.append(str(i+1))
	return listaindi
parafos=st.sidebar.multiselect('Parrafo',indices(chapter))
@st.cache
def uptextarea(parafos,df,chapter):
	dfparte=df[df['Capitulo']==chapter]
	dfparte=dfparte['Texto'].tolist()
	temp=''
	for i in parafos:
		temp=temp+'\n'+dfparte[int(i)-1]+'.'
	temp=temp.strip()
	return temp
my_text=st.text_area('Text a analizar',uptextarea(parafos,df,chapter))

@st.cache(allow_output_mutation=True)
def load_model(name):
    nlp=spacy.load(name)
    return nlp

@st.cache
def entity_analyzer(my_text):
	nlp = load_model('models1')
	docx = nlp(my_text)
	ent_viz = displacy.render([docx], style="ent", page=False)
	html = ent_viz.replace("\n", " ")
	return html
@st.cache
def dep_analyzer(my_text):
	nlp = load_model('models1')
	docx = nlp(my_text)
	ent_viz = displacy.render([docx], style="dep", page=False)
	html = ent_viz.replace("\n", " ")
	return html
if st.checkbox("Reconocimiento de entidades"):
	if st.button("Analyze"):
		html=entity_analyzer(my_text)
		st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
def summarize(my_text):
	parser = PlaintextParser.from_string(my_text,Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer_text = TextRankSummarizer(stemmer)
	resumen=''
	summarizer_text.stop_words = get_stop_words(LANGUAGE)
	summary_1 =summarizer_text(parser.document,SENTENCES_COUNT)
	for sentence in summary_1:
		resumen=resumen+ str(sentence)+'\n'
	return resumen
if st.checkbox("Text Summarization"):
	summary_r=summarize(my_text)
	st.success(summary_r)
if st.checkbox("Patrones de sintaxis"):
	if st.checkbox("Mostrar tabla"):
		muestra=st.text_input('Número de patrones a mostrar')
		if muestra!='':
			df2=pd.read_excel('pospattern.xlsx')
			st.write(df2.head(int(muestra)))
	if st.checkbox("Grafico"):
		html=dep_analyzer(my_text)
		st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
	if st.button("Extraer"):
		st.write('Espere mientras tanto')
		spatronesintax(df)
if st.checkbox("Mapa"):
	df3=pd.read_excel('Plazuelas.xlsx')
	fig = px.scatter_mapbox(df3, lat="lat", lon="lon", hover_name="Plazuelas",hover_data=['Lugar actual'],
                        color_discrete_sequence=["red"], zoom=12, height=300)
	fig.update_layout(mapbox_style="open-street-map")
	st.plotly_chart(fig)
	
