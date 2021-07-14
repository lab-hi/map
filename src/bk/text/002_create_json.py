import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import yaml
import requests
import sys
import argparse

from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace

f = open("settings.yml", "r+")
prefix = yaml.load(f, Loader=yaml.SafeLoader)["prefix"]

path = "琉球国絵図ほか文字情報.xlsx"

all = Graph()

df = pd.read_excel(path, sheet_name=0, header=None, index_col=None, engine='openpyxl')

r_count = len(df.index)
c_count = len(df.columns)

google_index = 1

import requests
from bs4 import BeautifulSoup

pins = {
    "トカラ列島" : {
        "id" : "tokara",
        "range" : [3, 126]
    },
    "大島" : {
        "id" : "oshima",
        "range" : [127, 197]
    },
    "鬼界嶋" : {
        "id" : "kikai",
        "range" : [198, 542]
    },
    "「琉球国悪鬼納島絵図」" : {
        "id" : "aku",
        "range" : [543, 834]
    },
    "「琉球国八島絵図」" : {
        "id" : "yashima",
        "range" : [835, 1086]
    }
}

cols = {
    "正保国絵図": {
        "id" : "shoho",
        "index" : 3
    },
    
}

'''
    "個人蔵「琉球国絵図」": {
        "id" : "kojin",
        "index" : 7
    },
    "都城島津家文書「琉球幷諸島図」": {
        "id" : "miyako",
        "index" : 19
    },
    "鹿児島県立図書館所蔵「薩琉海路図」": {
        "id" : "kagoshima",
        "index" : 23
    },
    "内閣文庫所蔵「琉球明細総図」": {
        "id" : "naikaku",
        "index" : 27
    },
    '''

partOfMap = {}

for key in cols:
    value = cols[key]
    id = value["id"]
    subject = prefix + "/api/data/" + id
    subject_res = URIRef(subject)

    stmt = (subject_res, URIRef(RDFS.label), Literal(key))
    all.add(stmt)

    partOfMap[value["index"]] = subject_res

map = {}

###########

json_open = open("data/geo.json", 'r')
geo = json.load(json_open)

for url in geo:
    obj = geo[url]

    if pd.isnull(obj["label"]):
        continue

    geo_subject = URIRef(obj["uri"])

    stmt = (geo_subject, RDFS.label, Literal(obj["label"]))
    all.add(stmt)

    stmt = (geo_subject, RDF.type, URIRef("https://jpsearch.go.jp/term/type/Place"))
    all.add(stmt)

    stmt = (geo_subject, URIRef("http://schema.org/relatedLink"), URIRef(url))
    all.add(stmt)

    hash = URIRef(obj["hash"])

    stmt = (geo_subject, URIRef("http://schema.org/geo"), hash)
    all.add(stmt)

    latlong = obj["geo"]

    stmt = (hash, URIRef("http://schema.org/latitude"), Literal(latlong[0]))
    all.add(stmt)

    stmt = (hash, URIRef("http://schema.org/longitude"), Literal(latlong[1]))
    all.add(stmt)

############

for i in range(3, r_count):

    for key in pins:

        row = pins[key]["range"]

        if row[0] <= i  and i <= row[1]:
            key_row_index = row[0]
            category_id = pins[key]["id"]
            

    for col in cols:

        value = cols[col]

        id = value["id"]

        index = value["index"] # shoho

        uuid = df.iloc[i, index]

        if pd.isnull(uuid):
            uuid = id + "-" + category_id + "-" + str(i).zfill(8)

        label = df.iloc[i, index + 1]
        description = df.iloc[i, value["index"] + 2]

        if pd.isnull(label):
            continue

        print(uuid)

        subject = prefix + "/api/data/" + uuid # id + "-" + str(i).zfill(4)
        subject_res = URIRef(subject)

        stmt = (subject_res, URIRef("http://schema.org/description"), Literal("Sort: "+str(i).zfill(4)))
        all.add(stmt)

        stmt = (subject_res, URIRef(RDFS.label), Literal(label))
        all.add(stmt)

        if not pd.isnull(description):
            stmt = (subject_res, URIRef("http://schema.org/description"), Literal("説明文: "+description))
            all.add(stmt)

        umi = df.iloc[i, value["index"] + 3]

        if not pd.isnull(umi):
            stmt = (subject_res, URIRef("http://schema.org/description"), Literal("航路: "+umi))
            all.add(stmt)

        remark = df.iloc[i, value["index"] + 4]

        if not pd.isnull(remark):
            stmt = (subject_res, URIRef("http://schema.org/description"), Literal("備考: "+str(remark)))
            all.add(stmt)

        category = df.iloc[i, value["index"] + 5]

        if not pd.isnull(category):
            stmt = (subject_res, URIRef("http://schema.org/description"), Literal("分類: "+str(category)))
            all.add(stmt)

        #### is part of

        stmt = (subject_res, URIRef("http://schema.org/isPartOf"), partOfMap[index])
        all.add(stmt)


        #### 

        category_uri = URIRef(str(partOfMap[index]+"-"+category_id))
        stmt = (subject_res, URIRef("http://schema.org/category"), category_uri)
        all.add(stmt)

        key_label =  df.iloc[key_row_index, index]
        if pd.isnull(key_label):
            key_label = "Unknown"
        
        stmt =  (category_uri, RDFS.label, Literal(key_label))
        all.add(stmt)

        #### 
        google_url = df.iloc[i, 1]
        if not pd.isnull(google_url) and google_url in geo:
            # geohash = geo[google_url]
            place_uri = geo[google_url]["uri"]
            
            stmt = (subject_res, URIRef("http://schema.org/spatial"), URIRef(place_uri))
            all.add(stmt)

path = "data/all.json"
all.serialize(destination=path, format='json-ld')
all.serialize(destination=path.replace(".json", ".ttl"), format='turtle')

# コピー
import shutil
shutil.copyfile(path, "/Users/nakamurasatoru/git/d_hi/okinawa/viewer/static/data/items.json")