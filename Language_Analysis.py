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


print(response)