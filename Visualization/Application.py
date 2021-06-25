import streamlit as st
import visualise_spacy_tree
import re
from nltk.tokenize import sent_tokenize
import spacy
from spacy import displacy
import pandas as pd
from codsyntax import *
import plotly.express as px
from spacy.tokens import Token

#funcion para dar color a los nodos
def darcolor(doc):
	try:
		Token.set_extension('plot', default={})
	except:
		pass
	for token in doc:
		node_label = '{0} [{1}] /{2})'.format(token.orth_, token.i, token.pos_)
		token._.plot['label'] = node_label
		if token.pos_ == 'VERB':
			token._.plot['color'] = 'green'
		elif token.pos_=='PROPN':
			token._.plot['color']='red'
		elif token.pos_=='NOUN':
			token._.plot['color']='blue'
	return doc

@st.cache(allow_output_mutation=True)
def load_model(name):
    nlp=spacy.load(name)
    return nlp
nlp = load_model('models1')
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""
LANGUAGE = "spanish"
#leer archivo
df=pd.read_csv('Relatos_Benvenutto.csv',sep='\t')
dfvacio=df['Texto']
libro='Relatos_Benvenutto'
#lista de capitulos
@st.cache
def listar(df):
	cap=list(set(df['Capitulo'].tolist()))
	cap.sort()
	return cap
st.title('Análisis de relatos de viajes con NLP')
st.sidebar.header('Introducción')
st.sidebar.markdown('Esta app es una herramienta para el análisis de textos del género literario relatos de viajes.')
if st.sidebar.checkbox('Ver más'):
	st.sidebar.markdown('Esta herramienta permite un análisis macro y micro del texto. En el análisis macro se tiene dos modulos, un mapa el cual muestra los personajes relacionados con la locaciones y un extractor de patrones de sintaxix que muestra los patrones más frecuentes del texto. Por otra parte, en el análisis micro se presenta una selección por capítulo, parrafo y oración del texo el cual aparecerá en el cuadro de texto. Asimismo, dentro del análisis se reconoce las entidaes y genera un árbol de sintaxis.')
#Check Macro
if st.checkbox('Análisis macro'):
	st.header("Mapa")
	df3=pd.read_excel('Plazuelas.xlsx')
	listazero=[10]*len(df3)
	fig = px.scatter_mapbox(df3, lat="lat", lon="lon", hover_name="Plazuelas",hover_data=['Lugar actual'],
                        color_discrete_sequence=["red"], zoom=12, height=500, size=listazero)        
	fig.update_layout(mapbox_style="open-street-map")
	st.plotly_chart(fig)
	st.header("Patrones frecuentes")
	if st.checkbox("Mostrar patrones"):
		muestra=st.text_input('Número de patrones a mostrar')
		if muestra!='':
			df2=pd.read_csv('pospattern.csv',sep=';')
			st.write(df2.head(int(muestra)))
	st.markdown("Extraer los patrones del texto")
	if st.button("Extraer"):
		st.write('Espere mientras tanto')
		spatronesintax(df)
#Check micro
if st.checkbox('Análisis micro'):
	cap=listar(df)
	#seleccion de capitulos
	chapter=st.sidebar.selectbox('Capítulo',cap)
	@st.cache
	#indices de los parrafos
	def indices(chapter):
		nparrafos=df[df['Capitulo']==chapter].count()
		nparrafos=nparrafos[0]
		listaindi=[]
		for i in range(nparrafos):
			listaindi.append(str(i+1))
		return listaindi
	#seleccion de parrafos
	parafos=st.sidebar.multiselect('Párrafo',indices(chapter))
	@st.cache
	#cargar parrafo seleccionado
	def uptextarea(parafos,df,chapter):
		dfparte=df[df['Capitulo']==chapter]
		dfparte=dfparte['Texto'].tolist()
		temp=''
		for i in parafos:
			temp=temp+'\n'+dfparte[int(i)-1]+'.'
		temp=temp.strip()
		return temp
	mrparrafo=uptextarea(parafos,df,chapter)
	@st.cache
	#juntar oraciones seleccionadas
	def oraciones(oraci6,indices):
		temp=''
		for i in indices:
			temp=temp+' '+oraci6[int(i)]
		temp=temp.strip()
		return temp	
	#si quiere seleccionar por oraciones
	oraci6=sent_tokenize(mrparrafo)
	indiceoraciones=list(range(len(oraci6)))
	indiceoraciones.append('Seleccionar todo')
	oracionselec=st.sidebar.multiselect('Oración',indiceoraciones)
	if 'Seleccionar todo' in oracionselec:
		my_text=st.text_area('Texto a analizar',oraciones(oraci6,list(range(len(oraci6)))),height=270)
	else:
		my_text=st.text_area('Texto a analizar',oraciones(oraci6,oracionselec),height=180)
	#funcion de entidades
	def entity_analyzer(my_text):
		#nlp = load_model('models1')
		docx = nlp(my_text)
		if docx.ents!=():
			ent_viz = displacy.render([docx], style="ent", page=False)
			html = ent_viz.replace("\n", " ")
			html=HTML_WRAPPER.format(html)
		else:
			html='No'
		return html
	#funcion de dependecias-arbol
	def dep_analyzer(my_text):
		#nlp = load_model('models1')
		docx = nlp(my_text)
		docx=darcolor(docx)
		png = visualise_spacy_tree.create_png(docx)
		return png
	#seccion entidades

	st.header("Reconocimiento de entidades")
		#mostrar las entidades en el texto
	if st.button("Analizar"):
		html=entity_analyzer(my_text)
		if html=='No':
			st.markdown('No se encontró entidades')
		else:
			st.write(html, unsafe_allow_html=True)
	#Arbol de sintaxis
	st.header("Árbol de sintaxis")
	if st.checkbox("Gráfico"):
		html=dep_analyzer(my_text)
		st.image(html, output_format='PNG')
		

	