# Textify
# Programming for quantitative Economics
# University of St. Gallen

## Load Packages

import io
import os

import tkinter as tk
from tkinter import filedialog
from typing import List

from google.cloud import vision
from google.cloud.vision import types as types_vision


from google.cloud import language

# Importing pandas and numpy packages
# These packages are used to create data frames
import pandas
import numpy

# Importing goslate packages.
# This package is used to translate words to german/english
import goslate




### Text Detection using Google Cloud Vision API


## Specify API Credentials
# apikey.json is currently not shared in github (is in plantify.gitignore)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey_Vision.json"

# Access Cloud Vision Functions
gvision_functions = vision.ImageAnnotatorClient()

# # Allows to open finder/explorer to choose a picture
# root = tk.Tk()
# root.withdraw()
#
# # Allows us to choose a picture via finder/explorer
# file_name = filedialog.askopenfilename()

# Allows us to choose a picture in the project directory
file_name = 'ShortStoryKidsTest.png'



with io.open(file_name,'rb') as image_file:
    content = image_file.read()

image = types_vision.Image(content=content)


response = gvision_functions.document_text_detection(image=image)
output_gvision = response.full_text_annotation

text_output_gvision = output_gvision.text


### Text Analysis using Google Cloud Natural Language API
## Specify API Credentials
# apikey.json is currently not shared in github (is in plantify.gitignore)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey_Language.json"

# Access Cloud Vision Functions
language_client = language.LanguageServiceClient()

# document = text which is going to be analyzed
document = language.types.Document(
    content= text_output_gvision,
    language= 'de',
    type='PLAIN_TEXT')

#automatische Language erkennung kann noch verbessert werden


# response =
response = language_client.analyze_sentiment(document=document, encoding_type='UTF32')


print(response)