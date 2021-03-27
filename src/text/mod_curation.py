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

      marker = "http://codh.rois.ac.jp/edo-maps/icons/icon-1.png#xy=11,27"
      if category == "村":
        marker = "https://cdn.mapmarker.io/api/v1/pin?size=25&background=%23F44E3B&icon=fa-star&color=%23FFFFFF&voffset=0&hoffset=1#xy=12,22"

      url = "https://ryukyu-kuniezu.web.app/item/" + uuid

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
                "chars": "[ <a href=\"/{}\">{}</a> ]<br/>{}".format(url, uuid, "<br/>".join(arr)),
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

curation["viewingHint"] = "annotation"
with open("data/curation.json", 'w') as outfile:
    json.dump(curation, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))
