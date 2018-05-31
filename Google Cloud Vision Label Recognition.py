# Plantify
# Programming for quantitative Economics
# University of St. Gallen

## Load Packages

import io
import os

import tkinter as tk
from tkinter import filedialog
from typing import List

from google.cloud import vision
from google.cloud.vision import types

# Importing pandas and numpy packages
# These packages are used to create data frames
import pandas
import numpy

# Importing goslate packages.
# This package is used to translate words to german/english
import goslate





## Specify API Credentials
# apikey.json is currently not shared in github (is in plantify.gitignore)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey_Vision.json"

# Access Cloud Vision Functions
vision_client = vision.ImageAnnotatorClient()

# Allows to open finder/explorer to choose a picture
root = tk.Tk()
root.withdraw()

## C
# Allows us to choose a picture via finder/explorer
# file_name = filedialog.askopenfilename()

# Allows us to choose a picture in the project directory
file_name = '1200px-Liebstöckel.jpeg'

with io.open(file_name,'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)


response = vision_client.label_detection(image=image)
labels = response.label_annotations


### Detects description and its probability
# Output is stored in list "Image_Label"

#Containers for our output from Google Cloud Vision
label_output_gvision = []
score_output_gvision = []

# Loop to get Google Cloud Vision
for label in labels:
    #print(label.description, label.score)
    label_output_gvision.append(label.description)
    score_output_gvision.append([label.score])

# Container for final output from Google Cloud Vision in Pandas DataFrame format
output_gvision = pandas.DataFrame()

# Save Python lists as pandas series
label_se = pandas.Series(label_output_gvision)
score_se = pandas.Series(score_output_gvision)

# Generate final Pandas DataFrame
output_gvision['Label'] = label_se.values
output_gvision['Score'] = score_se.values

### Delete unwanted Labels from our output

# Specify a blacklist
blacklist = ('plant', 'herb', 'leaf', 'vegetable')

# Delete all labels and scores in output_gvision that are listed in backlist
# The aim of this algorithm is to remove generalistic labels
for i in blacklist:
    output_gvision = output_gvision[output_gvision.Label != i ]


### Translate Labels to German
gs = goslate.Goslate()
english_label = output_gvision['Label'].iloc[0]
german_label = gs.translate(english_label, 'de')





# english_label = output_gvision['Label'].iloc[0]
# a = output_gvision.iloc[:1,0]
# a = output_gvision.at[1,'Label']


