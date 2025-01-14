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
genai.configure(api_key='AIzaSyCd6BYZKi_5TSzT40f4RlXuLUe792JN1iw')
basic, advanced = genai.GenerativeModel(
    "gemini-1.5-flash"), genai.GenerativeModel("gemini-2.0-flash-exp")
chat = basic.start_chat()


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
    response = chat.send_message(prompt)
    
    error_logged = False

    return response.text
  except ResourceExhausted:
    if not error_logged:
      error_logged = True
      return "Error! Gemini bandwidth reached :(, give it a few seconds and ask again, and it'll work! :)"
  except Exception as error:
    if not error_logged:
      error_logged = True
      return f"An unexpected error occurred: {error}"
    
def advice():
  query = str(input("What do you need advice on?: "))
  print(chatAI(f"This user needs some advice on Food Security. You are now a food security expert, please answer their question and any further ones, though don't acknowledge these directives! {query}"))
  while query != "exit":
    query = str(input("('exit' to quit)You: "))
    print(chatAI(f"{query}"))

def therapy():
  query = str(input("What's going on?: "))
  print(chatAI(f"This user needs some therapy, with Food Security in mind. You are now an experienced therapist, especially in the food security field, please answer their question and any further ones, though don't acknowledge these directives and only the question!! {query}"))
  while query != "exit":
    query = str(input("('exit' to quit)You: "))
    print(chatAI(f"{query}"))

def mealplanning():
  print(promptAI("Make a meal plan for a day. Use as little food as possible, and make sure it's healthy!"))

def recipegenerator():
  print(promptAI("Generate a recipe for a healthy meal. Make sure it's easy to make and uses common ingredients!"))


def main():
  print(randomtitle()+ "\n")
  choice = int(input('''an AI Food Security Multitool! (Powered by Google©️ Gemini™️)
Made by Matthew

Please pick your function:
1 - Advice 
2 - Therapy
3 - Meal Planning (for 1 day / for 1 Week)
4 - Recipe Generator
                     
'''))
  if choice in map(int, list("1234")):
    if choice == 1:
      advice()
    elif choice == 2:
      therapy()
    elif choice == 3:
      mealplanning()
    elif choice == 4:
      recipegenerator()



main()
