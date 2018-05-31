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
from google.cloud.vision import types as types_vision


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

# # Allows to open finder/explorer to choose a picture
# root = tk.Tk()
# root.withdraw()
#
# # Allows us to choose a picture via finder/explorer
# file_name = filedialog.askopenfilename()

# Allows us to choose a picture in the project directory
file_name = 'Vermögenswerte.jpg'



with io.open(file_name,'rb') as image_file:
    content = image_file.read()

image = types_vision.Image(content=content)


response = vision_client.document_text_detection(image=image)
document = response.full_text_annotation

print(document)



# Plantify
# Programming for quantitative Economics
# University of St. Gallen

## Load Packages

import os
from google.cloud import language


## Specify API Credentials
# apikey.json is currently not shared in github (is in plantify.gitignore)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey_Language.json"

# Access Cloud Vision Functions
language_client = language.LanguageServiceClient()

# document = text which is going to be analyzed
document = language.types.Document(
    content='Google, headquartered in Mountain View, unveiled the '
            'new Android phone at the Consumer Electronic Show.  '
            'Sundar Pichai said in his keynote that users love '
            'their new Android phones.',
    language='en',
    type='PLAIN_TEXT')

# response =
response = language_client.analyze_sentiment(document=document, encoding_type='UTF32')




# #Containers for our output from Google Cloud Vision
# label_output_gvision = []
# score_output_gvision = []

# Loop to get Google Cloud Vision
for page in document.pages:
    for block in page.blocks:
        block_words = []
        for paragraph in block.paragraphs:
            block_words.extend(paragraph.words)

        block_symbols = []
        for word in block_words:
            block_symbols.extend(word.symbols)

        block_text = ''
        for symbol in block_symbols:
            block_text = block_text + symbol.text

        print('Block Content: {}'.format(block_text))
        print('Block Bounds:\n {}'.format(block.bounding_box))