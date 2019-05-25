#!/usr/bin/env python
'''
Created on Mar 7, 2019

@author: solan
'''
import sys
import os

from os import listdir
from os.path import isfile, join
from collections import defaultdict, OrderedDict
import re
import json
def txttojson():
    index = []
    with open('outputFile.txt', "r") as text:
        content=(text.readlines())
    content = [x.strip() for x in content]

    for word in content:

        postings = re.sub(r"[^a-zA-Z0-9]+", ' ',word)

        splits= postings.split()
 
        index.append(splits)
    invInd = {}
    #print(index)
    for word in index:
        for l in range(1,len(word)):
            invInd.setdefault(word[0],[])
            invInd[word[0]].append(word[l])
        
    with open('positionalindex1.txt', 'w') as outfile:
            json.dump(invInd, outfile)  
        
def querysearch(text):
    try: 
        global PosInvInd
        with open('positionalindex1.txt') as jsonfile:
            PosInvInd= json.load(jsonfile) 
            #print(PosInvInd.items())
            global queryT  
            match= {}
            temp = {} 
            queryT=list(text.split())  
            for word in queryT:
                if word == 'AND':
                    andInd= queryT.index(word)
                elif word == 'OR':
                    orInd= queryT.index(word)
                else:
                    continue
                    
            if queryT.__contains__("AND") and queryT.__contains__("OR"):
                if (andInd>orInd):
                    match= AND_TermsFromDictionary(queryT[andInd-1].lower(),queryT[andInd+1].lower())
                    temp= OR_TermsFromDictionary(queryT[orInd-1].lower())
                    match.update(temp)
                    return(match)
                else:
                    match= AND_TermsFromDictionary(queryT[andInd-1].lower(),queryT[andInd+1].lower())
                    temp= OR_TermsFromDictionary(queryT[orInd+1].lower())
                    match.update(temp)
                    return(match)
                
            elif queryT.__contains__("AND"):
                match= AND_TermsFromDictionary(queryT[andInd-1].lower(),queryT[andInd+1].lower()) 
                return(match)
            
            elif queryT.__contains__("OR"):
                match= OR_TermsFromDictionary(queryT[orInd-1].lower(),queryT[orInd+1].lower()) 
                return(match)
    except KeyError as error:
        print('Invalid query: stopwords are not included in the index and hence not accepted in the query. Pl. follow the format specified.')                     
 
def OR_TermsFromDictionary(*args):
    dicDoc={}
    for word in args:
        for k,v in PosInvInd.items():
            if(word==k):        
                dicDoc.update({word:v})          
    return dicDoc

def AND_TermsFromDictionary(t1,t2):
    INV={}              
    a= PosInvInd[t1]
    b= PosInvInd[t2]

    for key1 in a:
        for key2 in b:
            if key1==key2:
                INV.setdefault(t1,[]).append(key1)
                INV.setdefault(t2,[]).append(key2)
    return INV
               
txttojson()
query= input('Enter the query in form: word1 OR word2, word1 AND word2, word1 OR word2 AND word3, word1 AND word2 OR word3 :')
result= querysearch(query)
print(result)