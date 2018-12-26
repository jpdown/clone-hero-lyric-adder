# Menu helper file to only accept given valid values and return given answer
# Programmed by Jaden D (jpdown)
# Contact me on Discord if you encounter any issues: jpdown#0001

from enum import Enum

def getValidEnumInput(prompt: str, validVals: Enum):
    inputGiven = False
    while(not inputGiven):
        userInput = input(prompt)
        try:
            return(validVals[userInput].value)
        except ValueError:
            print("Invalid input given, please try again")

def getBooleanAnswer(prompt: str):
    inputGiven = False
    while(not inputGiven):
        userInput = input(prompt)
        if(userInput.lower().startswith("y")):
            return(True)
        elif(userInput.lower().startswith("n")):
            return(False)
        else:
            print("Invalid input given, please try again")

def getValidListInput(prompt: str, validInputs):
    inputGiven = False
    while(not inputGiven):
        userInput = input(prompt)
        if(userInput in validInputs):
            return(userInput)
        else:
            print("Invalid input given, please try again")