 ######## ######## ##     ## ######## #### ######## ##    ##
    ##    ##        ##   ##     ##     ##  ##        ##  ##
    ##    ##         ## ##      ##     ##  ##         ####
    ##    ######      ###       ##     ##  ######      ##
    ##    ##         ## ##      ##     ##  ##          ##
    ##    ##        ##   ##     ##     ##  ##          ##
    ##    ######## ##     ##    ##    #### ##          ##


 # Textify,
 # your image text extractor and analysis programme.
 # Extract text from your images, process a sentiment analysis, search through it and generate a .mp3 file out of it.
 # What is best, you can directly send the results to your mailbox.


 # University of St. Gallen
 # A "Programming for Quantitative Economics" project from:
 #   Patrick Buess, 16-606-089
 #   Manuel Buri, 16-606-188


 # Disclaimer:
 # This programme could only be tested for Mac OS environment.
 # Due to the fact that the two contributors do not have any access to windows environment.

 # Futhermore we would like to emphasize, that our programm is able to process an image with the following specifications:
     # Supported file formats:
     # -JPEG
     # -PNG8
     # -PNG24
     # -GIF
     # -Animiertes GIF (only first frame)
     # -BMP
     # -WEBP
     # -RAW
     # -ICO

     # Supported languages:
     # - Chinese (simple)
     # - Chinese (traditional)
     # - English
     # - French
     # - German
     # - Italian
     # - Japan
     # - Korean
     # - Portuguese
     # - Spanish

     # Image file size:
     # limited to a maximum of 4mb

     # Image format size:
     # For good results we recommend to use a format of 1.024 x 768.



 # Table of contents:
# - Import packages
# - Initialising API and Google Cloud Functions
# - Key Functions
#   - Analyze text in an image
#   - Add an additional image
#   - Send results to your mail
#   - Detect the language of the text
#   - Generate an .mp3 file
#   - Process the sentiment analysis



## Import packages
# You will find all necessary packages in textify_requirements.txt
import io
import os
from io import StringIO

import re

# tkinter GUI package
import tkinter as tk
from tkinter import *
from tkinter import filedialog

# Package to send mails with attachments
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
# Google Cloud Vision Functions
from google.cloud import vision
from google.cloud.vision import types as types_vision

# Google Cloud Natural Language Functions
from google.cloud import language

# Google Cloud Text-to-Speech Functions
from google.cloud import texttospeech

# Google Cloud Translation
from google.cloud import translate_v2



## Initialising API, Google Cloud Functions and tkinter
# Set Google Cloud API credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey.json"
# Please save "apikey.json" in your project folder.

# Initialize Google Cloud Functions
# Google Cloud Vision
gvision_functions = vision.ImageAnnotatorClient()
# Google Cloud Translation
gtranslate_functions = translate_v2.Client()
# Google Cloud Text-To-Speech
gtexttospeech_functions = texttospeech.TextToSpeechClient()

# Some tkinter stuff
root = tk.Tk()
root.withdraw()


## KEY FUNCTIONS

# Function for loading the image at the beginning
def loadimage():
    global text
    global text_output_original

    # Allows us to choose a picture via finder
    file_name = filedialog.askopenfilename()

    # Allows us to choose a picture in the project directory
    # file_name = 'Seiten aus Slides_Students.jpg'

    # Processes and defines the file_name as an image file
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read();

    # image = image which is going to be analyzed
    image = types_vision.Image(content=content);

    # We call the "document_text_detection"
    response_gvision = gvision_functions.document_text_detection(image=image);

    output_gvision = response_gvision.full_text_annotation;
    text_output_gvision = output_gvision.text

    # Store the initally stored text in a separate variable for later retrieving
    text_output_original = text_output_gvision

    # Option to remove line breaks from scanned text
    # text_output_gvision = text_output_gvision.replace('\n', ' ').replace('\r', '')

    if text_output_gvision is '':
        is_there_text = False
        text.delete(0.0, END)
        text.insert(END, 'Please choose another image. There is no text in this image')
    else:
        text.delete(0.0, END)
        text.insert(END, text_output_gvision)

# Add second/additional text from an image at the end of the first text
def addnew():
    global btnadd

    # Choose additional image for scanning
    file_name = filedialog.askopenfilename()

    # Opens the image and stores it in the variable "content"
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read();

    # image = image which is going to be analyzed
    image = types_vision.Image(content=content);

    response_gvision = gvision_functions.document_text_detection(image=image);

    output_gvision = response_gvision.full_text_annotation;


    text_output_gvision_new = output_gvision.text

    # Option to remove line breaks from scanned text
    # text_output_gvision_new = text_output_gvision_new.replace('\n', ' ').replace('\r', '')

    # Add additional text below the existing one and mark it
    text.insert(END, '\n #NEW SCAN\n')
    text.insert(END, text_output_gvision_new)


# Send Mail with text to address of choosing
def sendmail():
    global toaddr
    global mailinput
    global mailadress
    global varaudio

    # Open a pop-up window where the user can type in the address and choose an attachment
    mailinput = Tk()

    # Set variable for checkbutton to zero
    varaudio = 0

    # Checkbutton for audio attachment
    chk = Checkbutton(mailinput, text='Attach audio file', command=audiovariable)
    chk.grid(columnspan=2, row=1)

    # Label for instructions
    desc = Label(mailinput, text='Type in your recipient', font=('Arial Regular', 15))
    desc.grid(columnspan=2, row=0, pady=20)

    # Entry field for mailadress
    mailadress = Entry(mailinput, width=40)
    mailadress.grid(column=0, row=2, pady=20, padx=20)

    # Send button
    btnsend2 = Button(mailinput, text='Send', command=sendto)
    btnsend2.grid(column=1, row=2, padx=20, pady=20)

    mailinput.mainloop()

# Function keeping track of the checkbutton, necessary because native option did not work
def audiovariable():
    global varaudio
    if varaudio == 0:
        varaudio = 1
    else:
        varaudio = 0

# Function needed to close the pop up windows
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

    # Construct multipart message
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Textify Text Delivery"

    # Attach bodytext to mail
    body = text.get(0.0, END)
    msg.attach(MIMEText(body, 'plain'))

    # If checkbutton is checked, generate and add an audio file of the text
    if (varaudio == 1):
        savemp3formail()
        fileToSend = "Audio.mp3"
        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        # Attach audio file to message
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

    # Send mail from server
    server = smtplib.SMTP('patrickbuess.ch', 587)
    server.starttls()
    server.login(fromaddr, "PASSWORD")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    mailinput.destroy()

# Function creating a mp3 of the loaded text:
def tts():
    global mp3name
    global ttsinput

    # Open a pop-up window
    ttsinput = Tk()

    # Lavel with instructions
    desc = Label(ttsinput, text='Name your audio file', font=('Arial Regular', 15))
    desc.grid(columnspan=2, row=0, pady=20)

    # Entry field to enter the name of the file
    mp3name = Entry(ttsinput, width=40)
    mp3name.grid(column=0, row=1, padx=20, pady=20)

    # Save button
    btnsend3 = Button(ttsinput, text='Send', command=savemp3)
    btnsend3.grid(column=1, row=1, padx=20, pady=20)


# Function to detect the language of the text and
# generate a .mp3 file out of the text, specifically
# for the mail attachment as audio file name is fixed here
def savemp3formail():
    global text

    # Google Cloud Translation
    # Call gtranslate_functions to detect the language of our images
    output_gtranslate = gtranslate_functions.detect_language(text.get(0.0, END))
    # Extract the image code from output_gtranslate
    # We will use language_code_output_gtranslate further for Text-to-Speech and the Sentiment Analysis
    language_code_output_gtranslate = (output_gtranslate['language'])

    # Google Cloud Text-to-Speech
    # Define text which is going to be spoken
    input_text = texttospeech.types.SynthesisInput(text=text.get(0.0, END))

    # Define the voice, language and gender of the speaker which is going to read the text
    voice = texttospeech.types.VoiceSelectionParams(
        language_code=language_code_output_gtranslate,
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    # Define which data format is going to be created
    # We decided to go for a .mp3 format.
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Call gtexttospeech_functions to process the above defined parameters and produce a .mp3 file
    response_gtexttospeech = gtexttospeech_functions.synthesize_speech(input_text, voice, audio_config)

    # Name of Audio file is prefixed as it must be found by the mail send function
    nameyourtext = 'Audio'

    # saves the .mp3 file with the individual file name in the project directory folder.
    with open(nameyourtext + '.mp3', 'wb') as out:
        out.write(response_gtexttospeech.audio_content)

# Function to detect the language of the text and
# generate a .mp3 file out of the text.
def savemp3():
    global ttsinput
    global text
    global mp3name

    # Call google translate client to determine language of text
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

    # Close the pop-up window
    close_ttsinput()

# Function which generates a pop-up window for search terms
def searchwindow():
    global term

    # Open pop-up
    searchinput = Tk()

    # Label with instruction
    desc = Label(searchinput, text='Type in your search term', font=('Arial Regular', 15))
    desc.grid(columnspan=2, row=0, pady=20)

    # Entry field for search term
    term = Entry(searchinput, width=40)
    term.grid(column=0, row=1, padx=20, pady=20)

    # Submit button
    btnsend4 = Button(searchinput, text='Send', command=search)
    btnsend4.grid(column=1, row=1, padx=20, pady=20)

# Function which delivers the parameters to the search function
def searchterm():
    global term
    global text
    search(text, term, 'found')

# Search function
def search():
    global term

    # Start at beginning of text field
    pos = '1.0'
    # While position is not at the end, assess the text
    while True:
        idx = text.search(term.get(), pos, END)
        if not idx:
            break
        # If match is found, add a tag which adds a yellow
        pos = '{}+{}c'.format(idx, len(term.get()))
        text.tag_add('found', idx, pos)

    # Close pop-up window
    close_searchinput()

# Function adding textfacts and sentiment analysis results at the top
def getfacts():
    global text

    # Assess which language the text is written in, so the sentiment analysis works
    gtranslate_functions = translate_v2.Client()
    output_gtranslate = gtranslate_functions.detect_language(text.get(0.0, END))
    language_code_output_gtranslate = (output_gtranslate['language'])
    glanguage_functions = language.LanguageServiceClient()

    # document = text which is going to be analyzed
    document = language.types.Document(
        content=text.get(0.0, END),
        language=language_code_output_gtranslate,
        type='PLAIN_TEXT')

    # Analyze text with google sentiment analysis
    response_glanguage = glanguage_functions.analyze_sentiment(document=document, encoding_type='UTF32')
    sentiment_output_glanguage = response_glanguage.document_sentiment

    # Store relevant numbers in variables
    s_score = str(sentiment_output_glanguage.score)
    s_mag = str(sentiment_output_glanguage.magnitude)

    # Store text in more practical variable
    s = text.get(0.0, END)

    # Count the number of characters, words and phrases of text
    characters = str(len(s))
    words = str(len(re.findall(r'\w+', s)))
    phrases = str(len(re.split(r'[.!?]+', s)))

    # Insert infos at the beginning of the text
    text.insert(1.0, 'Textfacts \n\nCharacters: ' + characters + '\nWords: ' + words + '\nSentences: ' + phrases + '\n\nScore: ' + s_score + '\nThe score tells us the overall emotional sentiment in the text. 1 = very positive, -1 = very negative.\n\nMagnitude: ' + s_mag + '\nThe magnitude illustrates the amount of emotional (positive and negative) content in a text. The longer a text the higher its magnitude.\n\n')

# Function for undo button: Retrieving the text stored in a separate variable at the beginning
def undobtn():
    global text_output_original
    global text

    text.delete(0.0, END)
    text.insert(END, text_output_original)

# Application

# Create toplevel window, containing our application
window = Toplevel()
window.title("Welcome to Textify")
window.configure(background='#f2f2f2')

# Option to prevent resizing of window
window.resizable(width=False, height=False)

# Retrieve image with logo from assets folder
base_folder = os.path.dirname(__file__)
image_path = os.path.join(base_folder, 'assets/logo.png')
photo = PhotoImage(file=image_path)

# Title field contains logo
title = Label(window, image=photo, background="#f2f2f2")
title.grid(column=0, row=0, padx=20, pady=20)

# Button calling the function to load an initial image
btnload = Button(window, text='Load Image', command=loadimage, height=2, width=15)
btnload.grid(column=0, row=1)

# Textfield displaying the results
text = Text(window, font=('Arial Regular', 12))
text.insert(END, "Choose an image for analyis")
text.grid(column=1, row=0, rowspan=10, padx=20, pady=20)
# Tag added to the matching words from the search function highlighting them yellow
text.tag_config('found', background='yellow')

# Button to add an image
btnadd = Button(window, text='Add new', command=addnew, height=2, width=15)
btnadd.grid(column=0, row=2)

# Button that calls the pop up for sending an email
btnsend = Button(window, text='Send Mail', command=sendmail, height=2, width=15)
btnsend.grid(column=0, row=3)

# Button that calls the pop up to create an audio file
btnmp3 = Button(window, text='Create Audio', command=tts, height=2, width=15)
btnmp3.grid(column=0, row=4)

# Button that calls the pop up to enter search term
btnsearch = Button(window, text='Search Text', command=searchwindow, height=2, width=15)
btnsearch.grid(column=0, row=5)

# Button that calls the function which adds text facts at the beginning
btnfacts = Button(window, text='Text Facts', command=getfacts, height=2, width=15)
btnfacts.grid(column=0, row=6)

# Button that will exchange current textfield content with original one
btnfacts = Button(window, text='Undo', command=undobtn, height=2, width=15)
btnfacts.grid(column=0, row=7)

# End of toplevel window
window.mainloop()