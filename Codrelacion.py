
import spacy
from spacy import displacy
from collections import Counter
import pandas as pd
import re
from nltk.tokenize import sent_tokenize,word_tokenize
nlp =spacy.load('C:/Users/Ryu/Documents/GitHub/Relatos/Research/models1')
import unidecode
def trans(text):
    temp=text.split(' ')
    for k,i in enumerate(temp):
        i=re.sub(r'[“”´!?¡¿]*','',i)
        i=re.sub(r'[0-9]*','',i)
        if i.isupper():
            if i=='DE'or i=='LA'or i=='DEL'or i=='EL':
                i=i.lower()
            firstl=i[0]
            otros=''
            for j in range(1,len(i)):
                otros=otros+i[j].lower()
            palabra=firstl+otros
            temp[k]=palabra
        else:
            temp[k]=i
    prueba=' '.join(temp)
    return prueba
def nerprueba(a):
    doc = nlp(a)
    listemp=[]
    listemp1=[]
    for entity in doc.ents:
        listemp.append(entity)
    return listemp,doc
def listadep6(lisg,doc):
    porlo=word_tokenize(str(doc))
    for i in lisg:
        dela=word_tokenize(str(i))
        listapro=[]
        for l in dela:
            for p,k in enumerate(porlo):
                if l==k:
                    listapro.append(p)
        listapro=list(set(listapro))
        listapro2=[]
        for l in listapro:
            count=0
            for k in listapro:
                if abs(l-k)<len(dela):
                    count=count+1
            if count==len(dela):
                listapro2.append(l)
        if listapro2!=[]:
            lp=listapro2[len(listapro2)-1]
            texto=''
            texto=str(i)
            texto=texto.strip()
            porlo[lp]=texto
            for l in range(len(listapro2)-1):
                listapro2[l]=lp+(l+1-len(listapro2))
            listapro2.pop(len(listapro2)-1)
            listafin=[]
            for l in range(len(porlo)):
                if l in listapro2:
                    pass
                else:
                    listafin.append(porlo[l])
            porlo=listafin
    return porlo
def relacionar(libro):
    df=libro
    o=re.sub('[“]+|[”]+|["]+','',df)
    listaprueba=sent_tokenize(o)
    for j,i in enumerate(listaprueba):
        if j==0:
        	i=i.split('\n')
        	i=i[0]
        i=i.split('\n')
        i=' '.join(i)
        i=trans(i)
        listaprueba[j]=i.strip()
        listaent=[]
        listadep=[]
        for k in listaprueba:
            lisg,doc=nerprueba(k)
            ubi=[]
            per=[]
            for i in lisg:
                if i.label_=='LOC':
                    ubi.append(i)
                elif i.label_=='PER':
                    per.append(i)
            if len(ubi)>0 and len(per)>0:
                porlo=listadep6(lisg,doc)
                for i in ubi:
                    for j in per:
                        if i.start_char<j.start_char:
                            if abs(porlo.index(str(i)) - porlo.index(str(j))) <11:
                                depr=[i,i.label_,j,j.label_]
                                listadep.append(depr)
                        else:
                            if abs(porlo.index(str(i)) - porlo.index(str(j))) <11:
                                depr=[j,j.label_,i,i.label_]
                                listadep.append(depr)
    df2=pd.DataFrame(listadep)
    return df2