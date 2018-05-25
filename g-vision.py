# Load Packages

import io
import os

import tkinter as tk
from tkinter import filedialog

from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey.json"

vision_client = vision.ImageAnnotatorClient()

root = tk.Tk()
root.withdraw()

file_name = filedialog.askopenfilename()
#file_name = '28.jpg'

with io.open(file_name,'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

response = vision_client.label_detection(image=image)
labels = response.label_annotations

for label in labels:
    print(label.description)

