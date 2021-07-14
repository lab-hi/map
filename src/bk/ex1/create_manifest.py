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


import requests
r = requests.get("https://clioimg.hi.u-tokyo.ac.jp/viewer/view/idata/0M0/_103ha_/185/00000001")

from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, 'lxml')

ids = str(soup).split("var jsonUrls = [")[1].split("]")[0].replace("\"", "").split(",")

canvases = []

prefix = "https://clioimg.hi.u-tokyo.ac.jp/viewer/view/idata/0M0/_103ha_/185/"

base = prefix.replace("/view/", "/api/image/")

for i in range(len(ids)):

    index = str(i + 1)

    id = ids[i]

    url = base+str(id)+".tif"

    r = requests.get(url+"/info.json").json()

    width = r["width"]
    height = r["height"]

    canvas_id = prefix + "canvas/p"+index

    canvas = {
        "@type": "sc:Canvas",
        "@id": canvas_id,
        "label": "["+index+"]",
        "thumbnail": {
            "@id": url+"/full/200,/0/default.jpg",
            "service": r
        },
        "images": [
            {
                "@type": "oa:Annotation",
                "motivation": "sc:painting",
                "@id": prefix + "annotation/p"+index+"-image",
                "resource": {
                    "@type": "dctypes:Image",
                    "format": "image/jpeg",
                    "width" : width,
                    "height" : height,
                    "@id": url+"/full/full/0/default.jpg",
                    "service": r
                },
                "on": canvas_id
            }
        ],
        "width": width,
        "height": height
    }

    canvases.append(canvas)

manifest = {
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": "https://lab-hi.github.io/map/iiif/ex1/manifest.json",
  "@type": "sc:Manifest",
  "label": "琉球諸島図",
  "attribution": "東京大学史料編纂所",
  "sequences": [
    {
      "@id": url + "/sequence/normal",
      "@type": "sc:Sequence",
      "label": "Current Page Order",
      "viewingHint": "non-paged",
      "canvases": canvases
    }
  ]
}

f2 = open("../../docs/iiif/ex1/manifest.json", 'w')
json.dump(manifest, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
