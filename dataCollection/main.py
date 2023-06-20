from chart_scrape import downloadChart
from chart_parse import arrayifyRaces, createPDFReaderObj, extractRaceData
from post_race_data import postRace
from catalog_race import moveFiles, renameFiles
from pathlib import Path
from collections import namedtuple


def main(pathObj):
    chart = namedtuple('chart', 'date track')  # instantiate namedtuple to store the chart's date and track name
    chartData = None
    with open(pathObj, "rb") as fullCard:
        # create pdf reader object and arrayify each the data in each race
        fullCard = arrayifyRaces(createPDFReaderObj(fullCard))

        # extract needed data from each race and set the chart data to be returned for naming the file
        for race in fullCard:
            data = extractRaceData(race)
            if data:
                postRace(data)
                if not chartData:
                    chartData = chart(data['date'], data['track'].removesuffix('park'))
    return chartData


if __name__ == '__main__':
    downloadChart()  # download current day's Equibase chart
    sourceFolder = Path("C:\\Users\\User\\Charts\\NewChart")
    for sourceFile in sourceFolder.iterdir():
        chartData = main(sourceFile)

        # rename and move the downloaded charts into the correct directory corresponding to the track and year
        if chartData is not None:
            destinationFolder = f"C:\\Users\\User\\Charts\\{chartData.track}\\{chartData.track[:3] + chartData.date[:4]}"
            sourceFile = renameFiles(sourceFile, chartData.date)
            moveFiles(sourceFile, destinationFolder)
        else:
            sourceFile.unlink()  # delete file if it contains no data
