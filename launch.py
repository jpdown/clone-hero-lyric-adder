# Programmed by Jaden D (PoisonedPanther)
# Takes in a .chart file and a text file with lyrics
# Outputs a new .chart file with lyrics intact

import os

def readFiles():
    #Store old working directory
    workingDir = os.getcwd()

    chartPath = input("Please drag the chart file into this window and press enter:")
    lyricsPath = input("Please drag the lyrics file into this window and press enter:")

    #Separate files from paths to allow changing directory (due to windows having drive letters :angery:)
    chartSplit = os.path.split(chartPath)
    lyricsSplit = os.path.split(lyricsPath)

    #Read chart file
    os.chdir(chartSplit[0])
    with open(chartSplit[1], "r") as chart:
        chartFile = chart.readlines()

    #Read lyric file
    os.chdir(lyricsSplit[0])
    with open(lyricsSplit[1], "r") as lyrics:
        lyricsFile = lyrics.readlines()

    #Change back to old working directory
    os.chdir(workingDir)

    #Return files and path to old chart file
    return chartFile, lyricsFile, 

def syllableGenerator(lyrics: list): #Takes in list of lines from lyric file, generates list of syllables
    syllables = [] 
    for line in lyrics:
        syllables += line.split()
    return syllables

def modifyChartFile(chart: list, syllables: list):
    pass

def main():
    readFiles()
    #syllables = syllableGenerator(lyrics)
    #for syllable in syllables:
    #    print(syllable)

if __name__ == "__main__":
    main()