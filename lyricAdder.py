# Programmed by Jaden D (jpdown)
# Takes in a .chart file and a text file with lyrics
# Outputs a new .chart file with lyrics intact
# Contact me on Discord if you encounter any issues: jpdown#0001

import os
import traceback
import sys

def readFiles():
    chartPath = input("Please drag the chart file into this window and press enter:").strip()
    lyricsPath = input("Please drag the lyrics file into this window and press enter:").strip()

    #Get rid of surrounding quotes if path has spaces
    if chartPath.startswith("\"") and chartPath.endswith("\"") or chartPath.startswith("'") and chartPath.endswith("'"):
        chartPath = chartPath[1:-1]
    if lyricsPath.startswith("\"") and lyricsPath.endswith("\"") or lyricsPath.startswith("'") and lyricsPath.endswith("'"):
       lyricsPath = lyricsPath[1:-1]

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
    option = input("Would you like to continue? (y/n)")
    if(option.lower().startswith("y")):
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

    chart, lyrics, chartPath = readFiles()
    syllables = syllableGenerator(lyrics)
    if(getConfirmation(chart, syllables)):
        newChart = modifyChartFile(chart, syllables)
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