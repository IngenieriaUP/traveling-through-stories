import spacy
nlp = spacy.load('models1')
from nltk.tokenize import sent_tokenize
import unidecode
import pandas as pd
import re
from prefixspan import PrefixSpan
#https://spacy.io/api/annotation
def separo(listapos,pos=True):
	listaobj=[]
	if pos:
		for i in listapos:
			listap=[]
			for j in i:
				listap.append(j.pos_)
			listaobj.append(listap)
	else:
		for i in listapos:
			listap=[]
			for j in i:
				listap.append(j.dep_)
			listaobj.append(listap)
	return listaobj
def labeltonum(oye):
	pola=[]
	for i in oye:
	    pola.extend(i)
	pola=list(set(pola))
	listanum=[]
	#listalen=[]
	for i in oye:
	    listaux=[]
	    for j in i:
	    	p=pola.index(j)
	    	listaux.append(p)
	    #listalen.append(len(listaux))
	    listanum.append(listaux)
	return listanum,pola
def subfinder(mylist, pattern):
	matches = []
	for i in range(len(mylist)):
	    if mylist[i] == pattern[0] and mylist[i:i+len(pattern)] == pattern:
	        matches.append(pattern)
	return matches
def correr(lista4,oye2):
	#indis2=[]
	indk=[]
	indk2=[]
	count=0
	for k in range(len(lista4)):
	    temp=''
	    count=0
	    for j,i in enumerate(oye2):
	        a=subfinder(i,lista4[k][1])
	        if a!=[]:
	            count=count+1
	            temp=j
	    if temp!='':
	        if count>4:
	            #indis2.append(temp)
	            indk.append(lista4[k][1])
	            indk2.append(count)
	    #--------------------------------------------
	    
	df3=pd.DataFrame(indk2,columns={'contar'})
	df3['indis']=indk
	#df3['ejemploi']=indis2
	df3=df3.sort_values('contar',ascending=False)
	return df3
def spatronesintax(libro,posv=True):
	#empieza
	df=libro
	#df=pd.read_excel('../Visualization/Relatos_Benvenutto.xlsx')
	tes=df['Texto'].tolist()
	for i in range(len(tes)):
		tes[i]=tes[i]+'.\n'
	tes=''.join(tes)
	#o=re.sub('…|[.]{3}','.',tes)
	o=re.sub('[“]+|[”]+|["]+','',tes)
	listaprueba=sent_tokenize(o)
	listapos=[]
	for i in listaprueba:
		i=i.strip()
		doc=nlp(i)
		listapos.append(doc)
	oye=separo(listapos,posv)
	listanum,pola=labeltonum(oye)
	#dfl=pd.DataFrame(listalen)
	#dfl['ok']=listanum
	ps = PrefixSpan(oye)
	ps=PrefixSpan(listanum)
	lista=ps.frequent(int(len(oye)*0.5))
	lista2=[]
	for i in lista:
	    if len(i[1])>5:
	        lista2.append(i)
	df2=correr(lista2,listanum)
	listatrans=[]
	for i in df2['indis']:
	    listaux2=[]
	    for j in i:
	        listaux2.append(pola[j])
	    listatrans.append(listaux2)
	df2['transformer']=listatrans
	df2.to_excel('pospattern.xlsx',index=False)

