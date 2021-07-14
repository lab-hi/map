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
import datetime

m = open("data/data2.json", 'r')
m = json.load(m)

f = open("../settings.yml", "r+")
prefix = yaml.load(f, Loader=yaml.SafeLoader)["prefix"]

items = []

map = {}

today = datetime.datetime.now()

for item in m:
    label = item["label"]

    values = item["value"]

    if label in ["セット"]:
        pass
    elif label in ["まとめ"]:
        for value in values:
            map[value["dcterms:identifier"]] = value["rdfs:label"]
    else:
        for value in values:

            parent_id = value["schema:isPartOf^^uri"].split("/")[-1]

            obj = {
                "label" :  value["rdfs:label"],
                "objectID" : value["dcterms:identifier"],
                "thumbnail" : value["schema:image"],
                "category" : [value["schema:category"]],
                "図" : [map[parent_id]],
                "member" : value["schema:relatedLink"],
                "curation" : prefix + "/curation/{}.json".format(parent_id),
                "manifest" : value["schema:url"],
                "_updated" : format(today, '%Y-%m-%d'),
                "description" : [value["schema:description"]],
                "番号" : [value["description:番号"]],
                "備考" : [value["description:備考"]],
                "現在の地名" : [value["description:現在の地名"]],
                "リンク" : [value["description:リンク"]],
                "latitude" : [value["schema:latitude"]],
                "longitude" : [value["schema:longitude"]],
            }

            fulltext = ""

            for key in obj:
                value = obj[key]
                if type(value) is list:
                    value = ", ".join(value)
                fulltext += ", " + value

            f2 = open("/Users/nakamurasatoru/git/d_hi/map/okinawa/suikeichuzu/static/data/item/{}.json".format(obj["objectID"]), 'w')
            json.dump(obj, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

            obj["fulltext"] = fulltext

            items.append(obj)

f2 = open("/Users/nakamurasatoru/git/d_hi/map/okinawa/suikeichuzu/static/data/index.json", 'w')
json.dump(items, f2, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))