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
sys.path.append('/Users/nakamurasatoru/git/classes')
from rdf import Rdf as rdf

path = "琉球国絵図ほか文字情報.xlsx"

f = open("settings.yml", "r+")
prefix = yaml.load(f, Loader=yaml.SafeLoader)["prefix"]

df = pd.read_excel(path, sheet_name=0, header=None, index_col=None, engine='openpyxl')

r_count = len(df.index)
c_count = len(df.columns)

google_index = 1

import requests
from bs4 import BeautifulSoup

map = {}

for i in range(3, r_count):

    print(i+1, r_count)

    google_url = df.iloc[i, google_index]


    if pd.isnull(google_url):
        continue

    if "goo" not in google_url:
        continue

    print(google_url)

    path = "data/html/" + google_url.split("/")[-1]+".html"

    if not os.path.exists(path):# and False:
    
        try:
            sleep(3)
            r = requests.get(google_url)
            soup = BeautifulSoup(r.text, 'lxml')

            if "Our systems have detected unusual traffic from your computer network" not in str(soup):
                with open(path, mode='w') as f:
                    f.write(str(soup))

        except Exception as e:
            print(e)

    
    if not os.path.exists(path):
        continue

    soup = BeautifulSoup(open(path), 'lxml')

    metas = soup.find_all("meta")

    for meta in metas:
        content = meta.get("content")

        if "ll=" in content:
            geo = content.split("ll=")[1].split(",")
            print(geo)
            map[google_url] = [float(geo[0]), float(geo[1])]

            break

    if google_url in map:
        uri = prefix + "/api/place/" + google_url.split("/")[-1]
        label = df.iloc[i, google_index - 1]

        geohash = rdf.geohash(float(geo[0]), float(geo[1]))

        map[google_url] = {
            "uri" : uri,
            "label" : label,
            "geo" : [float(geo[0]), float(geo[1])],
            "hash" : geohash
        }

f2 = open("data/geo.json", 'w')
json.dump(map, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))