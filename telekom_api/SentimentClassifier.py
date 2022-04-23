import string
from xmlrpc.client import Boolean
import unidecode
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report

komentare = pd.read_csv("https://raw.githubusercontent.com/shegood/hatespeech_classification/main/komentare.csv")
komentare = komentare.dropna()

komentare["Vaha"] = komentare["Vaha"].apply(int)


f = open("pingwords.txt", "r")

pingwords = f.read().split(";")
f.close()

f = open("curses.txt", "r")

curses = f.read().split(";")
f.close()

f = open("threats.txt", "r")

threats = f.read().split(";")
f.close()

def pocet_vyhrazok(koment):
    pocet = 0
    for vyhrazka in threats:
        pocet += koment.count(vyhrazka)
    return pocet*8

def pocet_nadavok(koment):
    pocet = 0
    for nadavka in curses:
        pocet += koment.count(nadavka)
    return pocet*5

def pocet_ping(koment):
    pocet = 0
    for pingslovo in pingwords:
        pocet += koment.count(pingslovo)
    return pocet*4


df2 = pd.DataFrame()

#zmazat diakritiku a dat rovnake i
komentare['Komentar'] = komentare['Komentar'].apply(lambda x : unidecode.unidecode(x))
komentare['Komentar'] = komentare['Komentar'].apply(lambda x : x.replace('y','i'))

#pocet velkych pismen na dlzku
df2['velke/dlzka'] = komentare['Komentar'].apply(lambda x : sum(1 for c in x if c.isupper()))/komentare['Komentar'].apply(len)

#dat vsetko na male
komentare['Komentar']=komentare['Komentar'].apply(lambda x : x.lower())

#spocitat vykricniky a otazniky
df2['vykricniky']=komentare['Komentar'].apply(lambda x : x.count('!'))
df2['otazniky']=komentare['Komentar'].apply(lambda x : x.count('?'))

#spocitaj dlzku
df2['dlzka']=komentare['Komentar'].apply(len)

#znamienka na dzlku
df2['znamienka na dlzku'] = (df2['vykricniky']+df2['otazniky'])/df2['dlzka']

#spocitat skarede slova
df2["pocet vyhrazok"] = komentare["Komentar"].apply(pocet_vyhrazok)
df2["pocet nadavok"]=komentare["Komentar"].apply(pocet_nadavok)
df2["pocet pingslov"]=komentare["Komentar"].apply(pocet_ping)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(df2, komentare['Vaha'], test_size=0.1)

from sklearn.naive_bayes import MultinomialNB
haterecmodel = MultinomialNB().fit(df2, komentare['Vaha'])

haterecmodel = MultinomialNB().fit(X_train, y_train)
odhad = haterecmodel.predict(X_test)

############################################

def hodnot(listkomentarov):
    """
    1. Zober komentare
    2. Precisti ich 
    3.
    """    
    komenty = pd.DataFrame()
    temp = pd.Series(listkomentarov)
    temp = temp.apply(lambda x : unidecode.unidecode(x))
    
    temp = temp.replace('', np.nan)
    temp = temp.dropna()
    
    
    temp = temp.apply(lambda x : x.replace('y','i'))
    
    komenty['velke/dlzka']= temp.apply(lambda x : sum(1 for c in x if c.isupper()))/temp.apply(len)
    
    temp = temp.apply(lambda x : x.lower())
    
    komenty['vykricniky']=temp.apply(lambda x: x.count("!"))
    komenty['otazniky']=temp.apply(lambda x: x.count("?"))
    komenty['dlzka']=temp.apply(len)
    komenty['znamienka na dlzku']=((komenty["vykricniky"] + komenty["otazniky"]) / komenty["dlzka"] )
    komenty['pocet nadavok']=temp.apply(pocet_nadavok)
    komenty['pocet vyhrazok']=temp.apply(pocet_vyhrazok)
    komenty['pocet pingslov']=temp.apply(pocet_ping)

    odhadnutie = haterecmodel.predict(komenty)

    return odhadnutie

test_dokumenty = ["jolana laznibatova je sefka", "ty stetka posrata chod do pice", "kupil by som si metlu", "theee kkt to si sef"]

print(hodnot(test_dokumenty))

key = "03b6d42892c04758a81fc795de4d64f3"
endpoint = "https://kolkoo.cognitiveservices.azure.com/"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def my_sentiment_analysis(document: string) -> Boolean:
    #sem vloz preklad <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    response = client.analyze_sentiment(documents=[document])
    if response.confidence_scores.negative <= 0.4:
        return False
    
    hatefulness = hodnot([document])

    return hatefulness[0] == 2


