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

from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace

import argparse    # 1. argparseをインポート

import glob

files = glob.glob("item/*/manifest.json")

for file in files:
    cn = file.split("/")[-2]

    json_open = open(file, 'r')
    manifest = json.load(json_open)

    opath = "../docs/iiif/" + cn + "/manifest.json"
    os.makedirs(os.path.dirname(opath), exist_ok=True)

    f2 = open(opath, 'w')
    json.dump(manifest, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))