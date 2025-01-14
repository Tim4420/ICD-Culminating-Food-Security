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
      error_logged = True
      return "Error! Gemini bandwidth reached :(, give it a few seconds and it'll work again! :)"
  except Exception as error:
    if not error_logged:
      error_logged = True
      return f"An unexpected error occurred: {error}"

def chatAI(prompt):
  error_logged = False
  try:
    if not chat:
      chat = basic.start_chat()

    response = chat.send_message(prompt)
    
    error_logged = False

    return chat.text
  except ResourceExhausted:
    if not error_logged:
      error_logged = True
      return "Error! Gemini bandwidth reached :(, give it a few seconds and ask again, and it'll work! :)"
  except Exception as error:
    if not error_logged:
      error_logged = True
      return f"An unexpected error occurred: {error}"

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
  if choice in list(1234):
    if choice == 1:
      advice()
    elif choice == 2:
      therapy()
    elif choice == 3:
      mealplanning()
    elif choice == 4:
      recipegenerator()



main()
