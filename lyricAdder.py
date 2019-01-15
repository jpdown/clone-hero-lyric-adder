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

def findEvents(chart: list): #Finds the events section of chart file
    eventsFound = False
    for line in range(0, len(chart)): #Search for where to start manipulating things
        if("Events" in chart[line]):
            eventsStartLine = line
            eventsFound = True
        elif("}" in chart[line] and eventsFound):
            eventsEndLine = line
            eventsFound = False
    return eventsStartLine, eventsEndLine

def splitEvents(chart: list): #Finds events and returns a new list of just the events isolated
    eventsStartLine, eventsEndLine = findEvents(chart)
    events = []
    for line in range(eventsStartLine + 2, eventsEndLine): #Starts past the lines [Events] and {
        events.append(chart[line])
    return events

def convertNotesToLyrics(chart: list, configs): #Function to take notes given by config and convert to lyric events, returning new list
    newChart = []
    lyricChartFound = False
    for line in range(0, len(chart)): #Search for where to start manipulating things
        if(configs.lyricEventChart in chart[line]):
            lyricChartStartLine = line
            lyricChartFound = True
        elif("}" in chart[line] and lyricChartFound):
            lyricChartEndLine = line
            lyricChartFound = False
    
    eventsStartLine, eventsEndLine = findEvents(chart)
    
    #Start manipulating things when copying to new list
    for line in range(len(chart)):
        if(line == eventsStartLine + 2):
            for i in range(lyricChartStartLine + 2, lyricChartEndLine):
                newEvent = chart[i].replace(configs.lyricEventNote, "E \"lyric \"")
                newChart.append(newEvent)
        if(line >= lyricChartStartLine and line <= lyricChartEndLine and configs.lyricEventDeleteAfter):
            continue
        newChart.append(chart[line])
    
    #Organize events list
    newChart = organizeEvents(newChart)
    return(newChart)

def organizeEvents(chart: list): #Takes in a chart and makes sure the event list is organized
    events = []
    eventsStartLine, eventsEndLine = findEvents(chart)
    for i in range(eventsStartLine + 2, eventsEndLine): #Start past lines [Events] and {
        events.append(chart[i])
    
    events.sort(key=lambda x: int(x.split()[0]))

    #After events list sorted, return new chart file with sorted events list
    newChart = replaceEvents(events, chart)
    return newChart
    



#Manipulating lyric events from lyrics.txt
def phraseGenerator(lyrics: list): #Takes in a list of lines from lyric file, each line is a phrase
    phrases = []
    for line in lyrics:
        if line.strip() == "":
            continue
        phrases.append(_syllableGenerator(line))
    return phrases

def _syllableGenerator(lyrics: str): #Takes in string from file, generates a list of syllables
    syllables = lyrics.split()
    return syllables

#Manipulating lyrics from chart file
def getNumLyricEvents(chart: list): #Takes in chart file, returns number of lyric events
    numLyrics = 0
    for line in chart:
        if "lyric " in line:
            numLyrics += 1
    return numLyrics

def getNumSyllables(syllables: list): #Takes in syllables list, returns length of list
    return(len(syllables))

def getConfirmation(phrases: list, chartPhrases: list): #Prints number of syllables in each phrase, alerting user of potential errors
    if(len(phrases) > len(chartPhrases)):
        print("You have more phrases in the lyrics.txt than you do in the chart file")
        print("The following information is relating to the number of phrases in your chart file:")
        maxRange = len(chartPhrases)
    elif(len(chartPhrases) > len(phrases)):
        print("You have more phrases in the chart file than you do in the lyrics.txt")
        print("The following information is relating to the number of phrases in your lyrics file:")
        maxRange = len(phrases)
    else:
        print("You have the correct number of phrases in your chart and lyric file")
        maxRange = len(phrases)

    isOk = True
    for i in range(maxRange):
        phraseLen = len(phrases[i])
        chartPhraseLen = len(chartPhrases[i])
        s = "{0}: {1}, {2}: {3}".format(i+1, phraseLen, chartPhraseLen, phrases[i])
        if phraseLen != chartPhraseLen:
            if isOk:
                print("You have the following errors in your lyrics:")
                print("<phrase number>: <chart syllables>, <lyrics syllables>: <contents of phrase lyrics>")
                isOk = False
            print(s)
    
    if not isOk:
        print("Please fix the errors in your lyrics and try again.")
        return False
    
    print("You have no errors in your lyrics.")
    option = menu.getBooleanAnswer("Would you like to continue? (y/n) ")
    if(option):
        return True
    else:
        return False



def splitChartPhrases(events: list): #Splits events list into lyric events separated by phrase and all other events
    phrases = [] #Blank list to contain lists of all events associated with each phrase
    otherEvents = [] #List to contain all other events
    currentPhrase = -1 #All phrase_start's will increment this value, effectively starting at 0
    for line in events:
        if "phrase_start" in line:
            currentPhrase += 1
            phrases.append([]) #Create list for all events relating to this phrase
            otherEvents.append(line)
        elif "lyric " in line:
            phrases[currentPhrase].append(line)
        elif "phrase_end" in line:
            otherEvents.append(line)
        else: #not an event relating to lyrics
            otherEvents.append(line)
    return phrases, otherEvents


def modifyChartFile(chart: list, phrases: list, chartPhrases: list, chartOtherEvents: list): #For every line, add the syllable if line contains a lyric event
    # #Count the number of syllables in the case of running out of syllables
    # newChart = []
    # for line in chart:
    #     if "lyric " in line:
    #         try:
    #             location = line.find("lyric")
    #             newLine = line[:location] + "lyric {0}\"\n".format(syllables.pop(0))
    #             newChart.append(newLine)
    #         except IndexError: #Too many lyric events, not enough syllables
    #             newChart.append(line)
    #     else:
    #         newChart.append(line)
    # return newChart

    newEvents = []
    newChart = []

    newEvents = modifyLyrics(phrases, chartPhrases)
    newEvents = newEvents + chartOtherEvents
    newChart = replaceEvents(newEvents, chart)
    newChart = organizeEvents(newChart)

    return newChart

def modifyLyrics(phrases: list, chartPhrases: list): #Takes the lyrics phrases and chart phrases and combines them
    events = []
    for phrase in range(len(phrases)): #both lists are same length
        for syllable in range(len(phrases[phrase])): #both lists are same length
            event = chartPhrases[phrase][syllable]
            event.replace("lyric ", "lyric {0}".format(phrases[phrase][syllable]))
            events.append(event)
    return(events)

def replaceEvents(events: list, chart: list): #Replaces previous event list with new event list in chart
    eventsStartLine, eventsEndLine = findEvents(chart)

    newChart = []
    for line in range(len(chart)):
        if(line == eventsStartLine + 2):
            for event in events:
                newChart.append(event)
        if(line >= eventsStartLine and line < eventsEndLine):
            continue
        newChart.append(chart[line])
    
    return(newChart)


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
    phrases = phraseGenerator(lyrics)

    if(configs.lyricEventGeneratorsEnabled):
        lyricEventChart = convertNotesToLyrics(chart, configs)
    else:
        lyricEventChart = chart

    #Split lyric events in chart to phrases
    events = splitEvents(lyricEventChart)
    chartPhrases, otherEvents = splitChartPhrases(events)

    if(getConfirmation(chartPhrases, phrases)):
        newChart = modifyChartFile(lyricEventChart, phrases, chartPhrases, otherEvents)
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