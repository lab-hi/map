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

from bs4 import BeautifulSoup

f = open("settings.yml", "r+")
prefix = yaml.load(f, Loader=yaml.SafeLoader)["prefix"]

json_open = open("data/all.json", 'r')
metadata = json.load(json_open)

metadata_map = {}

for obj in metadata:
  id = obj["@id"]
  metadata_map[id.split("/")[-1]] = obj

json_open = open("/Users/nakamurasatoru/git/d_omeka/omekac_hi/docs/iiif/curation/all.json", 'r')
curation = json.load(json_open)

selections = curation["selections"]

for selection in selections:
  members = selection["members"]

  for member in members:
    uuid = BeautifulSoup(member["label"], "lxml").text

    print(uuid)

    if uuid in metadata_map:
      obj = metadata_map[uuid]

      member["label"] = uuid

      arr = [obj["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]]

      category = ""

      for desc in obj["http://schema.org/description"]:
        value = desc["@value"]
        arr.append(value)

        if "分類" in value:
          category = value.split(" ")[1]

      
      if category == "村":
        marker = "https://cdn.mapmarker.io/api/v1/pin?size=25&background=%230062B1&color=%23FFFFFF&voffset=0&hoffset=1&icon=fa-circle#xy=12,22"
      elif category == "山":
        marker = "https://cdn.mapmarker.io/api/v1/pin?size=25&background=%234D4D4D&color=%23FFFFFF&voffset=0&hoffset=1&icon=fa-circle#xy=12,22"
      elif category == "崎":
        marker = "https://cdn.mapmarker.io/api/v1/pin?size=25&background=%23999999&color=%23FFFFFF&voffset=0&hoffset=1&icon=fa-circle#xy=12,22"
      else:
        marker = "https://cdn.mapmarker.io/api/v1/pin?size=25&background=%23D33115&color=%23FFFFFF&voffset=0&hoffset=1&icon=fa-circle#xy=12,22"

      url = prefix + "/item/" + uuid

      member["metadata"] = [
        {
          "value": [
            {
              "on": member["@id"],
              "motivation": "sc:painting",
              "resource": {
                "marker": {
                  "@id": marker,
                  "@type": "dctypes:Image"
                },
                "chars": "[ <a href=\"{}\">{}</a> ]<br/>{}".format(url, uuid, "<br/>".join(arr)),
                "format": "text/html",
                "@type": "cnt:ContentAsText"
              },
              "@type": "oa:Annotation",
              "@id": "http://codh.rois.ac.jp/edo-maps/owariya/15/1852/ndl/{}".format(uuid)
            }
          ],
          "label": "Annotation"
        }
      ]

selections = curation["selections"]

for selection in selections:

  id = selection["@id"].split("/")[5]

  curation_new = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@id": "https://nakamura196.github.io/omekac_hi/iiif/curation/{}.json".format(id),
    "@type": "cr:Curation",
    "label": selection["label"],
    "selections" : [selection],
    "viewingHint": "annotation"
  }

  curation["viewingHint"] = "annotation"
  with open("/Users/nakamurasatoru/git/d_hi/okinawa/viewer/static/iiif/curation/{}.json".format(id), 'w') as outfile:
      json.dump(curation_new, outfile, ensure_ascii=False,
                  indent=4, sort_keys=True, separators=(',', ': '))

# 計算用に、全部入りのcuration
with open("data/curation.json", 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
