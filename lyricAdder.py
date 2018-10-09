# Programmed by Jaden D (PoisonedPanther)
# Takes in a .chart file and a text file with lyrics
# Outputs a new .chart file with lyrics intact
# Contact me on Discord if you encounter any issues: PoisonedPanther#0001

import os

def readFiles():
    chartPath = input("Please drag the chart file into this window and press enter:")
    lyricsPath = input("Please drag the lyrics file into this window and press enter:")

    #Get rid of surrounding quotes on Windows
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
    newChart = []
    for line in chart:
        if "lyric " in line:
            newLine = line.replace("lyric ", "lyric {0}".format(syllables.pop(0)))
            newChart.append(newLine)
        else:
            newChart.append(line)
    return newChart

def writeNewChart(path: tuple, chart: list): #Write a new chart file, prepending the name with LYRIC
    with open("LYRIC" + path[1], "w") as newChart:
        for line in chart:
            newChart.write(line)

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
    main()