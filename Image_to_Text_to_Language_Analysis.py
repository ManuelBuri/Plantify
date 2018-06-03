# Textify
# Programming for quantitative Economics
# Manuel Buri and Patrick Buess
# University of St. Gallen

## Load Packages
import io
import os

import tkinter as tk
from tkinter import filedialog

# Import Google libraries
# For Google Cloud Vision Functions
from google.cloud import vision
from google.cloud.vision import types as types_vision
# For Google Natural Language Functions
from google.cloud import language
# For Google Text-to-Speech Functions
from google.cloud import texttospeech

#from google.cloud import translate



### Text Detection using Google Cloud Vision API

## Specify API Credentials
# apikey_Vision.json is currently not shared in github
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey_Vision.json"

# Access Google Cloud Vision Functions
# We can then run any function which is supported from the ImageAnnotatorClient
# via gvision_functions.
gvision_functions = vision.ImageAnnotatorClient()


# Here we can run different functions from Google Cloud Vision
# We can get an overview of the different functions via:
# dir(gvision_functions)
# We have chosen document_text_detection which allows us to analyze the picture for texts.
# The output is then stored in response_gvision.
# We extract the text and save it as text_output_gvision

# Supported files:
# -JPEG
# -PNG8
# -PNG24
# -GIF
# -Animiertes GIF (nur erster Rahmen)
# -BMP
# -WEBP
# -RAW
# -ICO

is_there_text=True
while True:
    # Allows to open finder/explorer to choose a picture
    #root = tkinter.Tk()
    #root.withdraw()
    # Allows us to choose a picture via finder/explorer
    #file_name = filedialog.askopenfilename()

    # Allows us to choose a picture in the project directory
    file_name = 'Seiten aus Slides_Students.jpg'

    # Opens the @patrick was bedeutet dies?
    with io.open(file_name,'rb') as image_file:
        content = image_file.read();

    # image = image which is going to be analyzed
    image = types_vision.Image(content=content);

    response_gvision = gvision_functions.document_text_detection(image=image);

    output_gvision = response_gvision.full_text_annotation;

    text_output_gvision = output_gvision.text

    if text_output_gvision is '':
        is_there_text=False
        print('Please choose another image. There is no text in this image')
    else:
        is_there_text=True
        break


## Analysis of text_output_gvision
# to get an overview about the facts of the text such as amount of characters or words.

# Amount of words in text_output_gvision
text_output_gvision_splitted = text_output_gvision.split
amount_words_in_text_output_gvision = len(text_output_gvision_splitted())

# Amout of characters in text_output_gvision
amount_characters_in_text_output_gvision = len(text_output_gvision)

# The user can ask for the text facts via input function.
is_there_a_wrong_input = True
while True:

    user_question_text_facts = input('Which fact about the text would you like to know? \n A = Amount of words \n B = Amount of Characters \n C = I do not want to know any facts about the text \n Please input your choice: ')

    if user_question_text_facts is 'A':
        # We print the total amout of words in text_output_gvision.
        # To print it in a nice way we need show the integers as a string with str()
        print('There are ' + str(amount_words_in_text_output_gvision) + ' words in the text.')
        is_there_a_wrong_input = False

    elif user_question_text_facts is 'B':
        # We print the total amout of characters in text_output_gvision.
        # To print it in a nice way we need show the integers as a string with str()
        print('There are '+ str(amount_characters_in_text_output_gvision) + ' characters in the text.')
        is_there_a_wrong_input = False

    elif user_question_text_facts is 'C':
        print('As you wish. If you change your mind, please run the whole program again')

    else:
        #print('not included')
        is_there_a_wrong_input = True
        user_question_text_facts = input('Which fact about the text would you like to know? \n A = Amount of words \n B = Amount of Characters \n C = I do not want to know any facts about the text \n Please input your choice: ')
    break

# print(text_output_gvision)





### Text Analysis using Google Cloud Natural Language API

## Specify API Credentials
# apikey_Language.json is currently not shared in github
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey_Language.json"

# Access Google Cloud Natural Language Functions
# We can then run any function which is supported from the LanguageServiceClient
# via glanguage_functions.
glanguage_functions = language.LanguageServiceClient()

# document = text which is going to be analyzed
document = language.types.Document(
    content= text_output_gvision,
    language= 'en',
    type='PLAIN_TEXT')

#automatische Language erkennung kann noch verbessert werden


# Response which includes the sentiment analysis.
# @Manuel are there any other functions?
response_glanguage = glanguage_functions.analyze_sentiment(document=document, encoding_type='UTF32')


sentiment_output_glanguage = response_glanguage.document_sentiment

user_question_sentiment = input('Would you like to know the details about the sentiment analysis of your text? \n Y = Yes \n N = No : \n Please input your choice:  ')
if user_question_sentiment is 'Y':
    print('The total sentiment score of your text is '+ str(sentiment_output_glanguage) + '.')
else:
    print('As you wish. If you change your mind, please run the whole program again')



### Text-to-Speech using Google Cloud Text-to-Speech

## Specify API Credentials
# apikey_TextToSpeech.json is currently not shared in github
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apikey_TextToSpeech.json"

# Access Google Cloud Text-to-Speech Functions
# We can then run any function which is supported from the TextToSpeechClient
# via gtexttospeech_functions.
gtexttospeech_functions = texttospeech.TextToSpeechClient()

# text = text which is going to be spoken
text = text_output_gvision

# define text which is going to be spoken
input_text = texttospeech.types.SynthesisInput(text=text)

# define the voice which is going to read the text
voice = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

# define which data format is going to be created
audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)


response_gtexttospeech = gtexttospeech_functions.synthesize_speech(input_text, voice, audio_config)

# Here you can change the name of your .mp3 file
nameyourtext= input('Please enter the name of your .mp3 file: ')

# saves the .mp3 file with the individual file name in the project directory folder.
with open(nameyourtext+'.mp3', 'wb') as out:
    out.write(response_gtexttospeech.audio_content)
    print('Your .mp3 audio file was created and stored in your project directory folder as '+nameyourtext+'.mp3')

print('The program is fully executed. Please start again with another file.')