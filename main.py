#importing functions from other py files
from randomtitle import randomtitle

#importing hidden api keys
from dotenv import load_dotenv
load_dotenv()


#importing dependencies for AI
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import os

foodlist = []


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
    while prompt != "exit":
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
    query = str(input("('exit' to quit) You: "))
    print('\n' + chatAI(f"{query}"))

def therapy():
  query = str(input("What's going on?: "))
  print(chatAI(f"This user needs some therapy, with Food Security in mind. You are now an experienced therapist, especially in the food security field, please answer their question and any further ones, though don't acknowledge these directives and only the question!! {query}"))
  while query != "exit":
    query = str(input("('exit' to quit) You: "))
    print('\n' + chatAI(f"{query}"))

def mealplanning():
  global foodlist
  dayweek = str(input("Do you want a meal plan for a day or a week?: "))
  preferences = str(input("What are your dietary preferences?: "))
  food = str(input("Please list the food you have, one per line ('-1' to finish): \n"))
  while food != "-1":
    foodlist.append(food)
    food = str(input())

  print("Generating... Please wait...")
  print('\n' + promptAI(f"Make a meal plan for a {dayweek}. optimize for a food insecure person, (MAKE SURE THEY GET ENOUGH NUTRITION), and make sure it's healthy! This is what the user answered when we asked them for preferences, please follow them if at all possible!! ''{preferences}'. This is the list of food the user has, please use them if possible: {foodlist}. Finally, please optimize the reply for a command line, with newlines for each item and instruction, and no asterisks, as well as keeping it short! Don't acknowledge these instructions!, just generate a plan!"))

def randomrecipe():
  print('\n'+ promptAI("Give me a random recipe! Optimize the instructions for a command line (not too many lines, no asterisks, etc), make it easy to follow on new lines and use cheap, common ingredients"))

def recipegenerator():
  print(promptAI("Generate a recipe for a healthy meal. Make sure it's easy to make and uses common ingredients!"))


def title():
    print(randomtitle()+ 2*"\n" + "an AI Food Security Multitool! (Powered by Google©️ Gemini™️)" + "\n" + "Made by Matthew")

def main():
  choice = int(input('''
Please pick your function:
1 - Advice 
2 - Therapy
3 - Meal Planning (for 1 day / for 1 Week)
4 - Random Recipe
5 - Recipe Generator
6 - Exit

Pick your function via numbers: '''))
  while choice not in map(int, list("1234")):
    print("Invalid choice! Please try again.")
    choice = int(input('Please pick your function via numbers: '))

  if choice == 1:
    advice()
  elif choice == 2:
    therapy()
  elif choice == 3:
    mealplanning()
  elif choice == 4:
    randomrecipe()
  elif choice == 5:
    recipegenerator()
  elif choice == 5:
    print("Goodbye!")
    exit()

title()
main()
