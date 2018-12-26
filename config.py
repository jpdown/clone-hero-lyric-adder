# Config helper file for lyricAdder.py
# Programmed by Jaden D (jpdown)
# Contact me on Discord if you encounter any issues: jpdown#0001

#Imports
from enum import Enum
from configparser import ConfigParser

import os
import menu

#GLOBALS
class ChartTypes(Enum):
    Guitar = "Single"
    GuitarCoop = "DoubleGuitar"
    Bass = "DoubleBass"
    Rhythm = "DoubleRhythm"
    Keys = "Keyboard"
    Drums = "Drums"
    GHLGuitar = "GHLGuitar"
    GHLBass = "GHLBass"

class Difficulties(Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"
    Expert = "Expert"

class FiveFretInstruments(Enum):
    Guitar = "Single"
    GuitarCoop = "DoubleGuitar"
    Bass = "DoubleBass"
    Rhythm = "DoubleRhythm"
    Keys = "Keyboard"

class FiveFretNotes(Enum):
    Green = 0
    Red = 1
    Yellow = 2
    Blue = 3
    Orange = 4
    Open = 7

class DrumFiveNotes(Enum):
    Red = 1
    Yellow = 2
    Blue = 3
    Orange = 4
    Green = 5
    Kick = 0

class DrumFourNotes(Enum):
    Red = 1
    Yellow = 2
    Blue = 3
    Green = 4
    Kick = 0

class SixFretInstruments(Enum):
    GHLGuitar = "GHLGuitar"
    GHLBass = "GHLBass"

class SixFretNotes(Enum):
    Black1 = 3
    Black2 = 4
    Black3 = 8
    White1 = 0
    White2 = 1
    White3 = 2
    Open = 7

#Imported config class
class Config:
    def __init__(self):
        self.config = ConfigParser()
        self._checkConfig()
    
    def _checkConfig(self):
        if not os.path.exists("config.ini"):
            self.generateConfig()
        else:
            self.config.read("config.ini")
            if("Lyric Event Generators" not in self.config.sections()):
                print("Invalid config, regenerating")
                self.generateConfig()
    
    def generateConfig(self):
        self.config["Lyric Event Generators"] = {}
        self.config["Lyric Event Generators"]["Enabled"] = str(menu.getBooleanAnswer("Would you like to use signalling notes in a chart as lyric events? y/n: "))
        if(self.lyricEventGeneratorsEnabled):
            lyricEventConfig = self.config["Lyric Event Generators"]
            #ChartTypes
            instrumentOptions = ["{0}".format(instrument.name) for instrument in ChartTypes]
            prompt = "Please pick the instrument you would like to use. Valid values are:\n" + ", ".join(instrumentOptions)
            lyricEventConfig["Instrument"] = menu.getValidEnumInput(prompt + " ", ChartTypes)

            #Difficulties
            difficultyOptions = ["{0}".format(difficulty.name) for difficulty in Difficulties]
            prompt = "Please pick the difficulty you would like to use. Valid values are:\n" + ", ".join(difficultyOptions)
            lyricEventConfig["Difficulty"] = menu.getValidEnumInput(prompt + " ", Difficulties)

            #Notes
            #Decide which notes are valid for given instrument
            validNotes = self._determineValidNotes(lyricEventConfig["Instrument"])
            if(validNotes == "Drums"):
                fourOrFiveLane = menu.getValidListInput("Are you using 4 or 5 lane drums? 4/5: ", ["4", "5"])
                if(fourOrFiveLane == "4"):
                    validNotes = DrumFourNotes
                    lyricEventConfig["Four Lane Drums"] = "True"
                else:
                    validNotes = DrumFiveNotes
                    lyricEventConfig["Four Lane Drums"] = "False" 

            
            #Prompt user for note to use
            noteOptions = ["{0}".format(notes.name) for notes in validNotes]
            prompt = "Please select the note you would like to use. Valid values are:\n" + ", ".join(noteOptions)
            lyricEventConfig["Note"] = str(menu.getValidEnumInput(prompt + " ", validNotes))

            #Delete chart for instrument after?
            prompt = "Would you like to delete the chart for this instrument and difficulty after? y/n: "
            lyricEventConfig["Delete After"] = str(menu.getBooleanAnswer(prompt))
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)
    
    def _determineValidNotes(self, chartType):
        #Decide which notes are valid for given instrument
        if(chartType in [instrument.value for instrument in FiveFretInstruments]):
            validNotes = FiveFretNotes
        elif(chartType == "Drums"):
            try:
                if(self.config["Lyric Event Generators"].getboolean("Four Lane Drums")):
                    validNotes = DrumFourNotes
                else:
                    validNotes = DrumFiveNotes
            except ValueError: #If value hasn't been set yet
                return("Drums")
        elif(chartType in [instrument.value for instrument in SixFretInstruments]):
            validNotes = SixFretNotes
        else:
            raise(AssertionError("Invalid instrument supplied"))
        return(validNotes)

    
    @property
    def lyricEventGeneratorsEnabled(self):
        return(self.config["Lyric Event Generators"].getboolean("Enabled"))
    
    @property
    def lyricEventChart(self):
        chartName = ""
        chartName += self.config["Lyric Event Generators"]["Difficulty"]
        chartName += self.config["Lyric Event Generators"]["Instrument"]
        return(chartName)
    
    @property
    def lyricEventNote(self):
        noteEvent = "N "
        noteEvent += self.config["Lyric Event Generators"]["Note"]
        noteEvent += " 0"
        return(noteEvent)
    
    @property
    def lyricEventDeleteAfter(self):
        deleteAfter = self.config["Lyric Event Generators"].getboolean("Delete After")
        return(deleteAfter)
    
    @property
    def humanReadableInstrument(self):
        instrument = self.config["Lyric Event Generators"]["Instrument"]
        return(ChartTypes(instrument).name)
    
    @property
    def humanReadableDifficulty(self):
        difficulty = self.config["Lyric Event Generators"]["Difficulty"]
        return(Difficulties(difficulty).name)
    
    @property
    def humanReadableNote(self):
        #Decide which notes are valid for given instrument
        noteType = self._determineValidNotes(self.config["Lyric Event Generators"]["Instrument"])
        note = self.config["Lyric Event Generators"].getint("Note")
        return(noteType(note).name)

    
