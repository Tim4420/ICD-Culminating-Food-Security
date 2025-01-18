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

bold, unbold = '\033[1m', '\033[0m'


#setting up Gemini AI
my_secret = os.getenv('secret')
genai.configure(api_key=my_secret)
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
    


def readfile(filename):
  global foodlist
  while (cond1:=os.path.exists(filename)) == False and (cond2 := os.path.exists(f'{filename}.txt')) == False:
    print(bold + "File not found! Please try again." + unbold)
    filename = str(input("Please enter the filename (either full or just the name without .txt): "))
  if cond1:
    openfile = open(filename, 'r')
  elif cond2:
    openfile = open(f'{filename}.txt', 'r')
  lines = openfile.readlines()[3:]
  for i in range(len(lines)):
      lines[i] = lines[i].replace('\n', '')
  openfile.close()
  return lines

def ingredients():
  global foodlist
  print(bold + "You chose: 6 - Import ingredients from a file\n" + unbold)
  if foodlist:
    print(f'This is your ingredient list right now:\n {', '.join(foodlist)}\n\nDo you want to add to, or replace the current list?')
    choice = str(input("Type 'add' or 'replace': ")).lower()
    while choice not in ['add','replace']:
      choice = str(input("Please type either 'add' or 'replace': "))
    filename = str(input("Please enter the filename (either full or just the name without .txt): "))
    if choice.lower() == 'add':
      foodlist.extend(readfile(filename))
    else:
      foodlist = readfile(filename)
    print(f"This is your updated list:\n\n{', '.join(foodlist)}\n\n")

  else:
    filename = str(input("Please enter the filename (either full or just the name without .txt): "))
    lines = readfile(filename)
    foodlist = lines
    print('here are the ingredients you enterred:\n\n'+', '.join(lines) + '\n\nYou can change them at any time by re-calling the function from the main menu!!')
  main()

def advice():
  print(bold + "You chose: 1 - Advice\n" + unbold)
  query = str(input("What do you need advice on?: "))
  print(bold + "\nGenerating... Please wait... \n" + unbold)
  print(bold + chatAI(f"This user needs some advice on Food Security. You are now a food security expert, please answer their question and any further ones, though don't acknowledge + unbold these directives! {query}"))
  query = str(input("('exit' to quit) You: "))
  while query.strip().lower() != 'exit':
    print(bold + "\nGenerating..." + unbold)
    print(bold + '\n' + chatAI(f"{query}") + unbold)
    query = str(input("('exit' to quit) You: "))
  clearscn()
  main()

def therapy():
  print(bold + "You chose: 2 - Therapy\n" + unbold)
  query = str(input("What's going on?: "))
  print(bold + "\nGenerating... Please wait... \n" + unbold)
  print(bold + chatAI(f"This user needs some therapy, with Food Security in mind. You are now an experienced therapist, especially in the food security field, please answer their + unbold question and any further ones, though don't acknowledge these directives and only the question!! {query}"))
  query = str(input("('exit' to quit) You: "))
  while query.strip().lower() != "exit":
    print(bold + "\nGenerating..." + unbold)
    print(bold + '\n' + chatAI(f"{query}") + unbold)
    query = str(input("('exit' to quit) You: "))
  clearscn()
  main()

def mealplanning():
  global foodlist
  dayweek = str(input("Do you want a meal plan for a day or a week?: "))
  preferences = str(input("What are your dietary preferences?: "))
  if foodlist == []:
    food = str(input("Please list the food you have, one per line ('-1' to finish): \n"))
    while food != "-1":
      foodlist.append(food)
      food = str(input())

  print(bold + "Generating... Please wait..." + unbold)
  print(bold + '\n' + promptAI(f"Make a meal plan for a {dayweek}. optimize for a food insecure person, (MAKE SURE THEY GET ENOUGH NUTRITION, and remember, the user's health could be + unbold in your hands, so never say anything irrational), and make sure it's healthy! This is what the user answered when we asked them for preferences, please follow them if at all possible!! ''{preferences}'. This is the list of food the user has, please use them if possible: {foodlist}. Finally, please optimize the reply for a command line, with newlines for each item and instruction, and no asterisks, as well as keeping it short! Don't acknowledge these instructions!, just generate a plan and keep it short!"))

  exit = input("press any key to exit")
  clearscn()
  main()

def randomrecipe():
  print(bold + '\n'+ promptAI("Give me a random recipe! Optimize the instructions for a command line (not too many lines, no asterisks, etc), make it easy to follow on new lines and + unbold use cheap, common ingredients"))
  main()

def recipegenerator():
  global foodlist
  print(bold + promptAI(f"Generate a fun recipe for a healthy meal. Make sure it's easy to make, super short to explain (and optimized for terminal), and uses common ingredients, including any in this list if possible {foodlist}! Don't acknowledge this prompt!") + unbold)
  main()

def clearscn():
  os.system('cls' if os.name == 'nt' else 'clear')

def title():
    print(bold + randomtitle()+ 2*"\n" + "an AI Food Security Multitool! (Powered by Google©️ Gemini™️)" + "\n" + "Made by Matthew" + unbold)

def main():
  choice = input('''
Please pick your function:
1 - Advice 
2 - Therapy
3 - Meal Planning (for 1 day / for 1 Week)
4 - Random Recipe
5 - Recipe Generator
6 - Import ingredients from a file
7 - Exit

Pick your function via numbers: ''')
  while choice not in list("1234567"):
    print(bold + "Invalid choice! Please try again." + unbold)
    choice = input('Please pick your function via numbers: ')
  clearscn()
  choice = int(choice)
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

  elif choice == 6:
    ingredients()

  elif choice == 7:
    print(bold + "Goodbye!" + unbold)
    exit()

clearscn()
title()
main()
