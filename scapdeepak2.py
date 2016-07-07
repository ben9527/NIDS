#!/bin/python2.7

from scapy.all import *

# attributes in our dataset CSIC 2010
attributes= ["Host","Content-Length","Length1","Content-Type"]
features= {'typ':["Content-Type"]}

# usual kinds of request and their numbering in order
methods= ["GET","POST","DELETE","HEAD","PUT","TRACE","CONNECT"]

#usual kinds of Content-Type and their numbering in order
typ=[" application/x-www-form-urlencoded"," application/json"," multipart/form-data", " application/ocsp-request", 
" text/plain;charset=UTF-8"]

#store key value pair of HTTP payload 
dictionary = {}

#file to store data offline
f = open('httpdatadeepak', 'w')


#return index KEY for words in dictionary
def search(searchFor):
    for k in features:
        for v in features[k]:
            if searchFor in v:
                return k
    return None

def isHttp(packet):
    packet = str(packet)
    return "HTTP" in packet and any(i in packet for i in methods)

# filters the payload on basis of only the attributes required to us
def filter(load):
    lv = load.split('\r\n')
    for i in lv:
        p = i.find(':')
        if p != -1:
            key = i[:p]
            value = i[p+1:]
            if key=='Content-Type':
                #EVAL CONverts string to preexisting variable name
                dictionary[key]=str(eval(search(key)).index(value))
            elif key in attributes:
                dictionary[key]=str(value)
           
           #assign default value
            for k in attributes:
                if k not in dictionary:
                    dictionary[k]=str('NULL')

    for k,v in dictionary.items():
        f.flush()
        print >> f,k+': '+v
    print >> f
    dictionary.clear()

def pfunc(packet): 
    if isHttp(packet):
        print packet.load
        for att in methods:
            if att in str(packet):
                dictionary['Method'] = str(methods.index(att)) 
                dictionary['Length1']= str(len(packet.payload.load))
        load = packet.load
        filter(packet.load)

sniff(prn=pfunc)