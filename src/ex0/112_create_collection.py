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


main_file_path = "data/main.xlsx"

prefix = "https://lab-hi.github.io/map"
odir = "../docs"

def get_collection(df):

    label = df.iloc[1, 0]
    url = df.iloc[1, 1]

    return label, url


df_item = pd.read_excel(main_file_path, sheet_name="item", header=None, index_col=None, engine="openpyxl")
df_collection = pd.read_excel(main_file_path, sheet_name="collection", header=None, index_col=None, engine="openpyxl")

r_count = len(df_item.index)
c_count = len(df_item.columns)

collection_label, collection_url = get_collection(df_collection)

manifests = []

map = {}

for i in range(0, c_count):
    label = df_item.iloc[0, i]
    uri = df_item.iloc[1, i]
    # type = df.iloc[2, i]
    target=df_item.iloc[3,i]

    if target == "metadata":
        obj = {}
        map[i] = obj
        obj["label"] = label

    if uri == "http://purl.org/dc/terms/title":
        title_index = i

    if label == "manifest":
        manifest_index = i

    if uri == "http://xmlns.com/foaf/0.1/thumbnail":
        thumbnail_index = i
    

for j in range(4, r_count):

    manifest_uri = df_item.iloc[j, manifest_index]

    if pd.isnull(manifest_uri):
        continue

    thumbnail = df_item.iloc[j, thumbnail_index]
    if pd.isnull(thumbnail):
        continue

    title = df_item.iloc[j, title_index]
    if pd.isnull(title):
        title= "No Title"

    metadata = []

    ds = {}

    for index in map:
        value = df_item.iloc[j, index]
        if not pd.isnull(value) and value != 0:
            values = str(value).split("|")
            for value in values:
                value = value.strip()
                label = map[index]["label"]

                if label not in ds:
                    ds[label] = []

                if value not in ds[label]:

                    metadata.append({
                        "label": label,
                        "value" : value
                    })

                    if label not in ds:
                        ds[label] = []

                    ds[label].append(value)

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Manifest",
        "@id": manifest_uri,
        "label": title,
    }

    if thumbnail != 0:
        manifest["thumbnail"] = thumbnail

    if len(metadata) > 0:
        manifest["metadata"] = metadata

    manifests.append(manifest)
    
    
collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": collection_url,
    "@type": "sc:Collection",
    "label": collection_label,
    "manifests": manifests,
    "vhint": "use-thumb"
}

opath = collection_url.replace(prefix, odir)
tmp = os.path.split(opath)

os.makedirs(tmp[0], exist_ok=True)

f2 = open(opath, 'w')
json.dump(collection, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

