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

json_open = open("data/curation.json", 'r')
curation = json.load(json_open)

json_open = open("data/all.json", 'r')
all = json.load(json_open)

uuids = {}

selections = curation["selections"]

for selection in selections:
    members = selection["members"]

    for member in members:
        label = member["label"]
        uuids[label] = member["@id"]

map = {}
for obj in all:
    map[obj["@id"]] = obj

items = {}

for key in map:
    obj = map[key]

    
    if "http://schema.org/isPartOf" in obj:
        

        category = obj["http://schema.org/category"][0]["@id"]

        if category not in items:
            items[category] = {}

        sort_key = ""
        descriptions = obj["http://schema.org/description"]

        for desc in descriptions:
            value = desc["@value"]

            if "Sort" in value:
                sort_key = value.split(": ")[1]

        items[category][sort_key] = obj

top = [
    {
        "label" : "正保琉球国絵図写",
        "id" : "shoho-0001",
        "children" : [
            "oshima",
            "kikai"
        ],
        "manifest" : "https://lab-hi.github.io/map/iiif/1/manifest.json",
        "curation" : prefix + "/iiif/curation/1.json",
        "thumbnail": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/hi/1.tif/full/200,/0/default.jpg"
    },
    {
        "label" : "正保琉球国悪鬼納島絵図写",
        "id" : "shoho-0002",
        "children" : [
            "aku"
        ],
        "manifest" : "https://lab-hi.github.io/map/iiif/3/manifest.json",
        "curation" : prefix + "/iiif/curation/3.json",
        "thumbnail": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/hi/3.tif/full/200,/0/default.jpg"
    },
    {
        "label" : "正保琉球国八山島絵図",
        "id" : "shoho-0003",
        "children" : [
            "yashima"
        ],
        "manifest" : "https://lab-hi.github.io/map/iiif/2/manifest.json",
        "curation" : prefix + "/iiif/curation/2.json",
        "thumbnail": "https://iiif.dl.itc.u-tokyo.ac.jp/iiif/tmp/hi/2.tif/full/200,/0/default.jpg"
    }
]

collections = []

for obj in top:

    key = obj["label"]

    collections2 = []

    collection = {
        "@id" : prefix + "/api/data/{}".format(obj["id"]),
        "label" : key,
        "collections" : collections2,
        "thumbnail" : obj["thumbnail"],
        "curation" : obj["curation"],
        "manifest": obj["manifest"]
    }

    for category in obj["children"]:
        category_uri = prefix + "/api/data/shoho-" + category
        members = items[category_uri]

        manifests = []

        collections3 = {
            "@id" : category_uri,
            "label": map[category_uri]["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"],
            "manifests" : manifests
        }
        collections2.append(collections3)

        for sort_key in sorted(members):

            m = members[sort_key]

            member_uri = m["@id"]

            uuid = member_uri.split("/")[-1]

            item = {
                "@id": member_uri,
                "label" : m["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]
            }

            if uuid in uuids:

                # curation_uri = "https://ryukyu-kuniezu.web.app/api/iiif/curation/top.json"

                # item["curation"] = curation_uri
                item["canvas"] = uuids[uuid]


            if "http://schema.org/description" in m:
                descriptions = m["http://schema.org/description"]

                for desc in descriptions:
                    aas = desc["@value"].split(": ")

                    item[aas[0]] = aas[1]

            if "http://schema.org/spatial" in m:
                spatial_id = m["http://schema.org/spatial"][0]["@id"]

                # Excelで複数行になっている場合の不具合
                if spatial_id in map:
                    spatial = map[spatial_id]
                    spatial_label = spatial["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]
                    hash = spatial["http://schema.org/geo"][0]["@id"]

                    item["spatial_label"] = spatial_label
                    item["spatial_hash"] = hash
                    item["google"] = "https://goo.gl/maps/" + spatial_id.split("/")[-1]

            manifests.append(item)

    

    collections.append(collection)

with open("/Users/nakamurasatoru/git/d_hi/okinawa/viewer/static/data/all.json", 'w') as outfile:
    json.dump(collections, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))