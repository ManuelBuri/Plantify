## Load Packages
import io
import os
from io import StringIO

import re

import tkinter as tk
from tkinter import *
from tkinter import filedialog

import smtplib
import mimetypes
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email import encoders
from email.mime.base import MIMEBase
from email.utils import COMMASPACE, formatdate


# Import Google libraries
# For Google Cloud Vision Functions
from google.cloud import vision
from google.cloud.vision import types as types_vision
# For Google Natural Language Functions
from google.cloud import language
# For Google Text-to-Speech Functions
from google.cloud import texttospeech
from google.cloud import translate_v2

# Initialising

# Set Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey.json"
gvision_functions = vision.ImageAnnotatorClient()

# Some tkinter stuff
root = tk.Tk()
root.withdraw()


# KEY FUNCTIONS

# Function for loading the image at the beginning
def loadimage():
    global text
    global text_output_original

    # Allows us to choose a picture via finder/explorer
    file_name = filedialog.askopenfilename()

    # Allows us to choose a picture in the project directory
    # file_name = 'Seiten aus Slides_Students.jpg'

    # Opens the @patrick was bedeutet dies?
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read();

    # image = image which is going to be analyzed
    image = types_vision.Image(content=content);

    response_gvision = gvision_functions.document_text_detection(image=image);

    output_gvision = response_gvision.full_text_annotation;

    text_output_gvision = output_gvision.text
    text_output_original = text_output_gvision

    # text_output_gvision = text_output_gvision.replace('\n', ' ').replace('\r', '')

    if text_output_gvision is '':
        is_there_text = False
        text.delete(0.0, END)
        text.insert(END, 'Please choose another image. There is no text in this image')
    else:
        text.delete(0.0, END)
        text.insert(END, text_output_gvision)

    return(text)



# Add second text at the end
def addnew():
    global btnadd

    btnadd = Button(window, text='Add new', command=addnew, height=2, width=20)
    file_name = filedialog.askopenfilename()

    # Allows us to choose a picture in the project directory
    # file_name = 'Seiten aus Slides_Students.jpg'

    # Opens the @patrick was bedeutet dies?
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read();

    # image = image which is going to be analyzed
    image = types_vision.Image(content=content);

    response_gvision = gvision_functions.document_text_detection(image=image);

    output_gvision = response_gvision.full_text_annotation;

    text_output_gvision_new = output_gvision.text
    text_output_gvision_new = text_output_gvision_new.replace('\n', ' ').replace('\r', '')
    text.insert(END, '\n #NEW SCAN\n')
    text.insert(END, text_output_gvision_new)

# Send Mail with text to address of choosing
def sendmail():
    global toaddr
    global mailinput
    global mailadress
    global varaudio

    mailinput = Tk()

    varaudio = 0
    chk = Checkbutton(mailinput, text='Attach audio file', command=audiovariable)
    chk.grid(columnspan=2, row=1)
    desc = Label(mailinput, text='Type in your recipient', font=('Arial Regular', 15))
    desc.grid(columnspan=2, row=0, pady=20)
    mailadress = Entry(mailinput, width=40)
    mailadress.grid(column=0, row=2, pady=20, padx=20)
    btnsend2 = Button(mailinput, text='Send', command=sendto)
    btnsend2.grid(column=1, row=2, padx=20, pady=20)

    mailinput.mainloop()

def audiovariable():
    global varaudio
    if varaudio == 0:
        varaudio = 1
    else:
        varaudio = 0

# Function needed to close the pop up window for the mailadress
def close_mailinput():
    global mailinput
    mailinput.destroy()

def close_ttsinput():
    global ttsinput
    ttsinput.destroy()

def close_searchinput():
    global searchinput
    searchinput.destroy()

# Function executing the sending of the mail
def sendto():
    global text
    global toaddr
    global mailadress
    global varaudio

    toaddr = mailadress.get()
    fromaddr = 'mail@patrickbuess.ch'

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Textify Text Delivery"

    body = text.get(0.0, END)
    msg.attach(MIMEText(body, 'plain'))

    if (varaudio == 1):
        savemp3formail()
        fileToSend = "Audio.mp3"
        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        # List of attachments
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

    server = smtplib.SMTP('patrickbuess.ch', 587)
    server.starttls()
    server.login(fromaddr, "JoGVakPsQ2ffk8a$*")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    mailinput.destroy()

# Function creating a mp3 of the loaded text:
def tts():
    global mp3name
    global ttsinput

    ttsinput = Tk()
    desc = Label(ttsinput, text='Name your audio file', font=('Arial Regular', 15))
    desc.grid(columnspan=2, row=0, pady=20)
    mp3name = Entry(ttsinput, width=40)
    mp3name.grid(column=0, row=1, padx=20, pady=20)
    btnsend3 = Button(ttsinput, text='Send', command=savemp3)
    btnsend3.grid(column=1, row=1, padx=20, pady=20)


def savemp3formail():
    global text

    gtranslate_functions = translate_v2.Client()

    output_gtranslate = gtranslate_functions.detect_language(text.get(0.0, END))

    language_code_output_gtranslate = (output_gtranslate['language'])

    # Access Google Cloud Text-to-Speech Functions
    # We can then run any function which is supported from the TextToSpeechClient
    # via gtexttospeech_functions.
    gtexttospeech_functions = texttospeech.TextToSpeechClient()

    # define text which is going to be spoken
    input_text = texttospeech.types.SynthesisInput(text=text.get(0.0, END))

    # define the voice which is going to read the text
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=language_code_output_gtranslate,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    # define which data format is going to be created
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response_gtexttospeech = gtexttospeech_functions.synthesize_speech(input_text, voice, audio_config)

    # Here you can change the name of your .mp3 file
    nameyourtext = 'Audio'

    # saves the .mp3 file with the individual file name in the project directory folder.
    with open(nameyourtext + '.mp3', 'wb') as out:
        out.write(response_gtexttospeech.audio_content)


def savemp3():
    global ttsinput
    global text
    global mp3name

    gtranslate_functions = translate_v2.Client()

    output_gtranslate = gtranslate_functions.detect_language(text.get(0.0, END))

    language_code_output_gtranslate = (output_gtranslate['language'])

    # Access Google Cloud Text-to-Speech Functions
    # We can then run any function which is supported from the TextToSpeechClient
    # via gtexttospeech_functions.
    gtexttospeech_functions = texttospeech.TextToSpeechClient()

    # define text which is going to be spoken
    input_text = texttospeech.types.SynthesisInput(text=text.get(0.0, END))

    # define the voice which is going to read the text
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=language_code_output_gtranslate,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    # define which data format is going to be created
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response_gtexttospeech = gtexttospeech_functions.synthesize_speech(input_text, voice, audio_config)

    # Here you can change the name of your .mp3 file
    nameyourtext = mp3name.get()

    # saves the .mp3 file with the individual file name in the project directory folder.
    with open(nameyourtext + '.mp3', 'wb') as out:
        out.write(response_gtexttospeech.audio_content)

    close_ttsinput()

def searchwindow():
    global term

    searchinput = Tk()
    desc = Label(searchinput, text='Type in your search term', font=('Arial Regular', 15))
    desc.grid(columnspan=2, row=0, pady=20)
    term = Entry(searchinput, width=40)
    term.grid(column=0, row=1, padx=20, pady=20)
    btnsend4 = Button(searchinput, text='Send', command=search)
    btnsend4.grid(column=1, row=1, padx=20, pady=20)

def searchterm():
    global term
    global text
    search(text, term, 'found')

def search():
    global term

    pos = '1.0'
    while True:
        idx = text.search(term.get(), pos, END)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(term.get()))
        text.tag_add('found', idx, pos)

    close_searchinput()

def getfacts():
    global text

    s = text.get(0.0, END)

    characters = str(len(s))
    words = str(len(re.findall(r'\w+', s)))
    phrases = str(len(re.split(r'[.!?]+', s)))

    text.insert(1.0, 'Textfacts \n\nCharacters: ' + characters + '\nWords: ' + words + '\nSentences: ' + phrases + '\n\n')

def undobtn():
    global text_output_original
    global text

    text.delete(0.0, END)
    text.insert(END, text_output_original)

# Application

window = Toplevel()
window.title("Welcome to Textify")
window.configure(background='#f2f2f2')
# window.resizable(width=False, height=False)

base_folder = os.path.dirname(__file__)
image_path = os.path.join(base_folder, 'assets/logo.png')
photo = PhotoImage(file=image_path)

title = Label(window, image=photo, background="#f2f2f2")
title.grid(column=0, row=0, padx=5, pady=5)

btnload = Button(window, text='Load Image', command=loadimage, height=2, width=15)
btnload.grid(column=0, row=1)

text = Text(window, font=('Arial Regular', 12))
text.insert(END, "Choose an image for analyis")
text.grid(column=1, row=0, rowspan=8, padx=20, pady=20)
text.tag_config('found', background='yellow')

btnadd = Button(window, text='Add new', command=addnew, height=2, width=15)
btnadd.grid(column=0, row=2)

btnsend = Button(window, text='Send Mail', command=sendmail, height=2, width=15)
btnsend.grid(column=0, row=3)

btnmp3 = Button(window, text='Create Audio', command=tts, height=2, width=15)
btnmp3.grid(column=0, row=4)

btnsearch = Button(window, text='Search Text', command=searchwindow, height=2, width=15)
btnsearch.grid(column=0, row=5)

btnfacts = Button(window, text='Text Facts', command=getfacts, height=2, width=15)
btnfacts.grid(column=0, row=6)

btnfacts = Button(window, text='Undo', command=undobtn, height=2, width=15)
btnfacts.grid(column=0, row=7)


window.mainloop()

print(text_output_gvision)