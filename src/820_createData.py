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
import hashlib
import geohash2
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import glob

files = glob.glob("item/*/data.csv")

items = []

items.append({
        "label": "セット",
        "value": [
            {
                "dcterms:identifier": "kuniezu",
                "rdfs:label": "琉球国絵図・デジタル展示",
                "uri": "http://example.org/data/kuniezu"
            }
        ]
    })

rows = []

items.append({
        "label": "まとめ",
        "value": rows})

for file in files:

    m_path = file.replace("data.csv", "manifest.json")

    m = open(m_path, 'r')
    m = json.load(m)

    label = m["label"]

    ##########

    with open(file.replace("data.csv", "row.csv")) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append({
                "": "",
                "dcterms:identifier": row[1],
                "description:curation": row[5],
                "description:本文": row[7],
                "jps:sourceInfo": row[9],
                "rdfs:label": row[2],
                "schema:image": row[3],
                "schema:spatial": row[8],
                "schema:temporal": row[6],
                "schema:url": row[4],
                "temporal:label": row[6],
                "uri": row[0]
            })




    ##########

    values = []

    with open(file) as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            values.append({
                "uri": row[0],
                "dcterms:identifier": row[1],
                "ID": row[3],
                "rdfs:label": row[4],
                "schema:description": row[5],
                "schema:category": row[6],
                "description:現在の地名": row[7],
                "description:リンク": row[8],
                "description:備考": row[9],
                "description:番号": row[10],
                "schema:longitude": row[11],
                "schema:latitude": row[12],
                "schema:geo^^uri": row[13],
                "xywh": row[14],
                "schema:url": row[15],
                "canvas": row[16],
                "schema:relatedLink": row[17],
                "schema:image": row[18],
                "schema:isPartOf^^uri": row[19],
                "description:図": row[20],
            })

    items.append({
        "label": label,
        "value" : values
    })

f2 = open("data/data2.json", 'w')
json.dump(items, f2, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))