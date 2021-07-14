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

import glob

files = glob.glob("item/*/manifest.json")

map = {}

for file in files:
    json_open = open(file, 'r')
    manifest = json.load(json_open)

    id = file.split("/")[-2]

    label = manifest["label"]

    obj = {"label" : label}
    map[id] = obj


f2 = open("/Users/nakamurasatoru/git/d_hi/map/suikeichuzu/static/data/settings.json", 'w')
json.dump(map, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))
