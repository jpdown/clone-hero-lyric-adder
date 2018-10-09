# Programmed by Jaden D (jpdown)
# Takes in a .chart file and a text file with lyrics
# Outputs a new .chart file with lyrics intact
# Contact me on Discord if you encounter any issues: jpdown#0001

import os
import traceback
import sys

def readFiles():
    chartPath = input("Please drag the chart file into this window and press enter:")
    lyricsPath = input("Please drag the lyrics file into this window and press enter:")

    #Get rid of surrounding quotes if path has spaces
    if chartPath.startswith("\"") and chartPath.endswith("\""):
        chartPath = chartPath[1:-1]
    if lyricsPath.startswith("\"") and lyricsPath.endswith("\""):
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

def modifyChartFile(chart: list, syllables: list): #For every line, add the syllable if line contains a lyric event
    #Count the number of syllables in the case of running out of syllables
    numSyllables = len(syllables)
    tooManyEvents = False

    newChart = []
    for line in chart:
        if "lyric " in line and not tooManyEvents:
            try:
                location = line.find("lyric")
                newLine = line[:location] + "lyric {0}\"\n".format(syllables.pop(0))
                newChart.append(newLine)
            except IndexError: #Too many lyric events, not enough syllables
                print("There were too many lyric events in the chart, I ran out of syllables.")
                #Count the number of lyric events in chart
                numLyrics = 0
                for line in chart:
                    if "lyric " in line:
                        numLyrics += 1
                print("{0} syllables, {1} lyric events".format(numSyllables, numLyrics))
                input("Press enter to continue writing the new chart, close me to skip writing the new file.")
                tooManyEvents = True #Allow program to write rest of chart
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
    newChart = modifyChartFile(chart, syllables)
    writeNewChart(chartPath, newChart)
    
    #Change back to old working directory
    os.chdir(workingDir)

    #End program
    print("Done! You'll find your new chart file in the same location as your old chart")
    input("Press enter to close...")

if __name__ == "__main__":
    try:
        main()
    except:
        printException()