#importing functions from other py files
from randomtitle import randomtitle

#importing hidden api keys
from dotenv import load_dotenv
load_dotenv()


#importing dependencies for AI
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import os

#setting up Gemini AI
my_secret = os.getenv('shhhhhhhhhhhhhhhh')
genai.configure(api_key=my_secret)
basic, advanced = genai.GenerativeModel(
    "gemini-1.5-flash"), genai.GenerativeModel("gemini-2.0-flash-exp")


#setting up the prompt function
def promptAI(prompt):
  error_logged = False
  try:
    response = advanced.generate_content(prompt)
    error_logged = False
    return response.text
  except ResourceExhausted:
    if not error_logged:
      print(
          "Error! Gemini bandwidth reached :(, give it a few seconds and it'll work again! :)"
      )
      error_logged = True
  except Exception as error:
    if not error_logged:
      print(f"An unexpected error occurred: {error}")
      error_logged = True


def main():
  print(randomtitle()+ "\n")
  choice = int(input('''an AI Food Security Multitool! (Powered by Google©️ Gemini™️)
Made by Matthew

Please pick your function:
1 - Advice 
2 - Therapy
3 - Meal Planning (for 1 day / for 1 Week)
4 - Recipe Generator'
'''))


main()
