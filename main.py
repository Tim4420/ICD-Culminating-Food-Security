#importing functions from other py files
from randomtitle import randomtitle

#importing hidden api keys
from dotenv import load_dotenv
load_dotenv()

#importing dependencies for AI
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import os

#initializing an empty list for food ingredients that the user has access to
foodlist = []

#bold and unbold ANSI escape characters
bold, unbold = '\033[1m', '\033[0m'


#setting up Gemini AI
my_secret = os.getenv('secret')
genai.configure(api_key=my_secret)
basic, advanced = genai.GenerativeModel(
    "gemini-1.5-flash"), genai.GenerativeModel("gemini-2.0-flash-exp")
chat = basic.start_chat()

#setting up the prompt function
def promptAI(prompt):
  '''function for prompting AI for one single question'''
  error_logged = False
  try:
    response = advanced.generate_content(prompt)
    error_logged = False
    return response.text
  #try except block to preserve flow instead of stopping everything with an error
  except ResourceExhausted:
    if not error_logged:
      error_logged = True
      return "Error! Gemini bandwidth reached :(, give it a few seconds and it'll work again! :)"
  except Exception as error:
    if not error_logged:
      error_logged = True
      #in case of any other errors
      return f"An unexpected error occurred: {error}"


def chatAI(prompt):
  '''Function for starting a  chat with gemini AI, and returns the replies until the user says 'exit' '''
  error_logged = False
  try:
    while prompt != "exit":

      #sending a message to the AI
      response = chat.send_message(prompt)

      error_logged = False

      #returning the response
      return response.text
    
  except ResourceExhausted:
    #error handling as per usual
    if not error_logged:
      error_logged = True
      return "Error! Gemini bandwidth reached :(, give it a few seconds and ask again, and it'll work! :)"
  except Exception as error:
    if not error_logged:
      error_logged = True
      return f"An unexpected error occurred: {error}"
    

def readfile(filename):
  '''Function for reading user-specified files for ingredient lists'''

  #global keyword
  global foodlist
  #Input validation (seeing if the file exists or not, and if not, keeps prompting the user until they enter a 'valid' file, meaning either the name without the txt, or just the name)
  while (cond1:=os.path.exists(filename)) == False and (cond2 := os.path.exists(f'{filename}.txt')) == False:
    print(bold + "File not found! Please try again." + unbold)
    filename = str(input("Please enter the filename (either full or just the name without .txt): "))
    #if the path exists with the full filename they enterred, open it
  if cond1:
    openfile = open(filename, 'r')
    #if the path exists with .txt added to the end of it, open it
  elif cond2:
    openfile = open(f'{filename}.txt', 'r')

    #string slicing, to ignore the 3 first lines of the test list as they contain instructions
  lines = openfile.readlines()[3:]
  
  #removing the newline character from each list element (ex: 'Carrots\n' to just 'Carrots')
  for i in range(len(lines)):
      lines[i] = lines[i].replace('\n', '')

  openfile.close()
  return lines


def ingredients():
  '''Function for taking in ingredients, using the previous readfile function. '''
  global foodlist
  print(bold + "You chose: 6 - Import ingredients from a file\n" + unbold)
  #checking to see if the list has elements in it, if so, seeing if the user wants to append to or replace it entirely

  if foodlist:
    print(f'This is your ingredient list right now:\n {', '.join(foodlist)}\n\nDo you want to add to, or replace the current list?')
    choice = str(input("Type 'add' or 'replace': ")).lower()
    #more input validation
    while choice not in ['add','replace']:
      choice = str(input("Please type either 'add' or 'replace': "))

    filename = str(input("Please enter the filename (either full or just the name without .txt): "))
    #if the user wants to append, add elements to the end
    if choice.lower() == 'add':
      foodlist.extend(readfile(filename))
    else:
      #otherwise, redefine the file entirely
      foodlist = readfile(filename)
    print(f"This is your updated list:\n\n{', '.join(foodlist)}\n\n")

  else:
    #if no foodlist exists, create one
    filename = str(input("Please enter the filename (either full or just the name without .txt): "))
    lines = readfile(filename)
    foodlist = lines
    print('here are the ingredients you enterred:\n\n'+', '.join(lines) + '\n\nYou can change them at any time by re-calling the function from the main menu!!')
    #re-call main
  main()

def advice():
  '''Function for a user to chat to the AI and get advice'''
  print(bold + "You chose: 1 - Advice\n" + unbold)
  query = str(input("What do you need advice on?: "))
  print(bold + "\nGenerating... Please wait... \n" + unbold)

  #prints the reply of the AI to this query
  print(bold + chatAI(f"This user needs some advice on Food Security. You are now a food security expert, please answer their question and any further ones, though don't acknowledge + unbold these directives! {query}"))
  query = str(input("('exit' to quit) You: "))

  #keep the chat loop going until the user wants to exit
  while query.strip().lower() != 'exit':
    print(bold + "\nGenerating..." + unbold)
    print(bold + '\n' + chatAI(f"{query}") + unbold)
    query = str(input("('exit' to quit) You: "))

  #clears the screen, executes main again
  clearscn()
  main()

def therapy():
  '''Function like advice, but the AI acts as a therapist. Same structure as Advice, but with advice'''
  print(bold + "You chose: 2 - Therapy\n" + unbold)
  query = str(input("Hi! I'm your AI therapist for today, so do you mind telling me what's going on?: "))
  print(bold + "\nGenerating... Please wait... \n" + unbold)

  #prints the AI's response to the prompt
  print(bold + chatAI(f"This user needs some therapy, with Food Security in mind. You are now an experienced therapist, especially in the food security field, please answer their + unbold question and any further ones, though don't acknowledge these directives and only the question!! {query}"))
  query = str(input("('exit' to quit) You: "))

  #loops through until the user enters 'exit' and then quits
  while query.strip().lower() != "exit":
    print(bold + "\nGenerating..." + unbold)
    print(bold + '\n' + chatAI(f"{query}") + unbold)
    query = str(input("('exit' to quit) You: "))

  clearscn()
  main()

def mealplanning():
  '''Function to prompt the AI to plan meals for the user.'''

  global foodlist

  #asking user for some parameters, including length of the mealplan, dietary preferences, and a list of foods available unless foodlist already has foods.
  dayweek = str(input("Do you want a meal plan for a day or a week?: "))
  preferences = str(input("What are your dietary preferences?: "))

  if foodlist == []:
    food = str(input("Please list the food you have, one per line ('end' to finish): \n"))
    while food != 'end':
      foodlist.append(food)
      food = str(input())

  #prompting AI
  print(bold + "Generating... Please wait..." + unbold)
  print(bold + '\n' + promptAI(f"Make a meal plan for a {dayweek}. optimize for a food insecure person, (MAKE SURE THEY GET ENOUGH NUTRITION, and remember, the user's health could be + unbold in your hands, so never say anything irrational), and make sure it's healthy! This is what the user answered when we asked them for preferences, please follow them if at all possible!! ''{preferences}'. This is the list of food the user has, please use them if possible: {foodlist}(but don't exclusively limit the options to those foods, if they're unreasonably short). Finally, please optimize the reply for a command line, with newlines for each item and instruction, and no asterisks, as well as keeping it short! Don't acknowledge these instructions!, just generate a plan and keep it short!"))

  #once the user is done, they can press any key to exit. The input doesn't do anything, but nothing happens until the user does something, meaning they can note down ideas and such.
  _ = input("press enter to exit")

  #typical housekeeping
  clearscn()
  main()

def randomrecipe():
  '''Asks the AI for a completely random recipe, no matter the foods available at the moment'''
  print("Generating....")
  print(bold + '\n'+ promptAI("Give me a random recipe! Optimize the instructions for a command line (not too many lines, no asterisks, etc), make it easy to follow on new lines and use cheap, common ingredients. Lastly, don't acknowledge this prompt, only write it like you'd find online or in a book"))
  
  #givint the user time, and letting them exit when they're done
  _ = input("press enter to exit")

  #housekeeping
  clearscn()
  main()

def recipegenerator():
  '''generates a recipe, USING the user's food list.'''
  global foodlist
  if foodlist == []:
    #if the user doesn't have a foodlist yet, make one
    food = str(input("Please list the food you have, one per line ('end' to finish): \n"))
    while food != 'end':
      foodlist.append(food)
      food = str(input())
      
  print(bold + promptAI(f"Generate a fun recipe for a healthy meal. Make sure it's easy to make, super short to explain (and optimized for terminal), and uses common ingredients, including any in this list if possible {foodlist}! Don't acknowledge this prompt!") + unbold)
  _ = input("Press enter to quit back to menu! ")
  clearscn()
  main()

def clearscn():
  '''quick function for cleanliness, clearing the terminal to make it easy to read and avoid clutter'''
  #nt means running on windows, which of course has a different clearing function name 'cls', rather than 'clear' on mac
  os.system('cls' if os.name == 'nt' else 'clear')

def title():
    '''Function to print a random BITEWISE logo font,, followed by a short blurb'''
    #only runs once
    print(bold + randomtitle()+ 2*"\n" + "an AI Food Security Multitool! (Powered by Google©️ Gemini™️)" + "\n" + "Made by Matthew" + unbold)

def main():
  '''Main menu system, asks the user what function they want to call'''
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
  
  #again, input validation
  while choice not in list("1234567"):
    print(bold + "Invalid choice! Please try again." + unbold)
    choice = input('Please pick your function via numbers: ')

  #Making a dictionary of every choice, and their corresponding functions
  choices = {
    1: advice,
    2: therapy,
    3: mealplanning,
    4: randomrecipe,
    5: recipegenerator,
    6: ingredients,
    #quick function for number 7, as it executes two different lines instead of one
    7: lambda: (print(bold + "Goodbye!" + unbold), exit())}
  
  #clears screen  
  clearscn()
  choice = int(choice)
  choices[choice]()

clearscn()
title()
main()
