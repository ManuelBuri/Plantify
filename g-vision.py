# Load Packages

import io
import os

import tkinter as tk
from tkinter import filedialog

from google.cloud import vision
from google.cloud.vision import types

# Specify API Credentials
# apikey.json is currently not shared in github (is in plantify.gitignore)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey.json"

# Access Cloud Vision Functions
vision_client = vision.ImageAnnotatorClient()

# Allows to open finder/explorer to choose a picture
root = tk.Tk()
root.withdraw()

file_name = filedialog.askopenfilename()


with io.open(file_name,'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

response = vision_client.label_detection(image=image)
labels = response.label_annotations

# Prints labels and its probability
for label in labels:
    print(label.description, label.score)
