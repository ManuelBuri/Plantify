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
