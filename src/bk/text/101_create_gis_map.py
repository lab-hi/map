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

json_open = open("/Users/nakamurasatoru/git/d_hi/okinawa/viewer/static/data/all.json", 'r')
metadata = json.load(json_open)

####

json_open = open("data/all.json", 'r')
all = json.load(json_open)

map = {}
for obj in all:
    map[obj["@id"]] = obj

####

rows = []
rows.append(["分類", "表記", "説明文", "詳細", "緯度", "軽度"])

for c1 in metadata:
    for c2 in c1["collections"]:
        for m in c2["manifests"]:

            if "spatial_hash" in m:

                label = m["label"]
                desc = m["説明文"] if "説明文" in m else ""
                category = m["分類"] if "分類" in m else ""

                hash = map[m["spatial_hash"]]

                lat = hash["http://schema.org/latitude"][0]["@value"]
                long = hash["http://schema.org/longitude"][0]["@value"]

                row = [category, label, desc, m["@id"].replace("api/data", "item"), lat, long]
                rows.append(row)

                

import csv

with open('data/test.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(rows)
    