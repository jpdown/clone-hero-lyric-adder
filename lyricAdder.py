# Programmed by Jaden D (jpdown)
# Takes in a .chart file and a text file with lyrics
# Outputs a new .chart file with lyrics intact
# Contact me on Discord if you encounter any issues: jpdown#0001

import os
import traceback
import sys

import config
import menu

def readFiles():
    chartPath = input("Please drag the chart file into this window and press enter:").strip()
    lyricsPath = input("Please drag the lyrics file into this window and press enter:").strip()

    #Get rid of surrounding quotes if path has spaces
    if chartPath.startswith("\"") and chartPath.endswith("\"") or chartPath.startswith("'") and chartPath.endswith("'"):
        chartPath = chartPath[1:-1]
    if lyricsPath.startswith("\"") and lyricsPath.endswith("\"") or lyricsPath.startswith("'") and lyricsPath.endswith("'"):
       lyricsPath = lyricsPath[1:-1]
    
    #Replace '\ ' with just a space
    chartPath = chartPath.replace(r"\ ", " ")
    lyricsPath = lyricsPath.replace(r"\ ", " ")

    #Separate files from paths to allow changing directory (due to windows having drive letters :angery:)
    chartSplit = os.path.split(chartPath)
    lyricsSplit = os.path.split(lyricsPath)

    #Read lyric file
    os.chdir(lyricsSplit[0] + "/")
    with open(lyricsSplit[1], "r") as lyrics:
        lyricsFile = lyrics.readlines()

    #Read chart file
    os.chdir(chartSplit[0] + "/")
    with open(chartSplit[1], "r") as chart:
        chartFile = chart.readlines()

    #Return files and path to old chart file
    return chartFile, lyricsFile, chartSplit

#Adding lyric events from signalling value
def confirmConfig(configs): #Confirms current config values with user
    print("Your current config values are:")
    lyricGenEnabled = configs.lyricEventGeneratorsEnabled
    print("Generating lyric events from chart notes: {0}".format(lyricGenEnabled))
    if(lyricGenEnabled):
        try:
            instrument = configs.humanReadableInstrument
            difficulty = configs.humanReadableDifficulty
            note = configs.humanReadableNote
            deleteAfter = str(configs.lyricEventDeleteAfter)
        except ValueError:
            print("Invalid config, regenerating")
            configs.generateConfig()
            return(False)
        print("Instrument: " + instrument)
        print("Difficulty: " + difficulty)
        print("Note: " + note)
        print("Delete After: {0}".format(deleteAfter))

    if(menu.getBooleanAnswer("Are these settings correct? y/n: ")):
        return(True)
    else:
        return(False)

def convertNotesToLyrics(chart: list, configs): #Function to take notes given by config and convert to lyric events, returning new list
    newChart = []
    lyricChartFound = False
    eventsFound = False
    for line in range(0, len(chart)): #Search for where to start manipulating things
        if(configs.lyricEventChart in chart[line]):
            lyricChartStartLine = line
            lyricChartFound = True
        elif("}" in chart[line] and lyricChartFound):
            lyricChartEndLine = line
            lyricChartFound = False
        if("Events" in chart[line]):
            eventsStartLine = line
            eventsFound = True
        elif("}" in chart[line] and eventsFound):
            eventsEndLine = line
            eventsFound = False
    
    #Start manipulating things when copying to new list
    for line in range(len(chart)):
        if(line == eventsStartLine + 2):
            for i in range(lyricChartStartLine + 2, lyricChartEndLine):
                newEvent = chart[i].replace(configs.lyricEventNote, "E \"lyric \"")
                newChart.append(newEvent)
        if(line >= lyricChartStartLine and line <= lyricChartEndLine and configs.lyricEventDeleteAfter):
            continue
        newChart.append(chart[line])
    
    numLyricEvents = lyricChartEndLine - 1 - (lyricChartStartLine + 2)
    
    #Organize events list
    newChart = organizeEvents(newChart, eventsStartLine, eventsEndLine, numLyricEvents, chart)
    return(newChart)

def organizeEvents(chart: list, eventsStartLine: int, eventsEndLine: int, numLyricEvents, oldChart: list): #Takes in a chart and makes sure the event list is organized
    events = []
    newEventsStart = eventsStartLine + 2
    newEventsEnd = eventsEndLine + numLyricEvents - 1
    for line in range(newEventsStart, newEventsEnd + 1):
        events.append(chart[line])
    
    events.sort(key=lambda x: int(x.split()[0]))

    #After events list sorted, return new chart file with sorted events list
    newChart = []
    for line in range(len(chart)):
        if(line == newEventsStart):
            for event in events:
                newChart.append(event)
        if(line >= newEventsStart and line <= newEventsEnd):
            continue
        newChart.append(chart[line])
    
    return(newChart)
    



#Manipulating lyric events
def syllableGenerator(lyrics: list): #Takes in list of lines from lyric file, generates list of syllables
    syllables = [] 
    for line in lyrics:
        syllables += line.split()
    return syllables

def getNumLyricEvents(chart: list): #Takes in chart file, returns number of lyric events
    numLyrics = 0
    for line in chart:
        if "lyric " in line:
            numLyrics += 1
    return numLyrics

def getNumSyllables(syllables: list): #Takes in syllables list, returns length of list
    return(len(syllables))

def getConfirmation(chart: list, syllables: list):
    print("Number of lyric events: " + str(getNumLyricEvents(chart)))
    print("Number of syllables: " + str(getNumSyllables(syllables)))
    option = menu.getBooleanAnswer("Would you like to continue? (y/n) ")
    if(option):
        return True
    else:
        return False

def modifyChartFile(chart: list, syllables: list): #For every line, add the syllable if line contains a lyric event
    #Count the number of syllables in the case of running out of syllables
    newChart = []
    for line in chart:
        if "lyric " in line:
            try:
                location = line.find("lyric")
                newLine = line[:location] + "lyric {0}\"\n".format(syllables.pop(0))
                newChart.append(newLine)
            except IndexError: #Too many lyric events, not enough syllables
                newChart.append(line)
        else:
            newChart.append(line)
    return newChart

def writeNewChart(path: tuple, chart: list): #Write a new chart file, prepending the name with LYRIC
    with open("LYRIC" + path[1], "w") as newChart:
        for line in chart:
            newChart.write(line)

def printException():
    traceback.print_exc()
    print("Please make an issue on the GitHub repo or message jpdown#0001 on Discord with this error message.")
    input("Press enter to close...")

def main():
    #Store old working directory
    workingDir = os.getcwd()

    configs = config.Config()
    #Confirm config values are correct
    configCorrect = False
    while(not configCorrect):
        configCorrect = confirmConfig(configs)
        if(not configCorrect):
            configs.generateConfig()
    


    chart, lyrics, chartPath = readFiles()
    syllables = syllableGenerator(lyrics)
    if(configs.lyricEventGeneratorsEnabled):
        lyricEventChart = convertNotesToLyrics(chart, configs)
    else:
        lyricEventChart = chart


    if(getConfirmation(lyricEventChart, syllables)):
        newChart = modifyChartFile(lyricEventChart, syllables)
        writeNewChart(chartPath, newChart)
        print("Done! You'll find your new chart file in the same location as your old chart")
    else:
        print("Cancelling, no new file will be written.")
    
    #Change back to old working directory
    os.chdir(workingDir)

    #End program
    input("Press enter to close...")

if __name__ == "__main__":
    try:
        main()
    except:
        printException()