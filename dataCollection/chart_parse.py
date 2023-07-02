import PyPDF2
import re
from collections import defaultdict
import data_extraction as de


def createPDFReaderObj(file):
    return PyPDF2.PdfFileReader(file)


def arrayifyRaces(pdfReaderObj) -> list:
    """ itemizes data in each line of parsed pdf and merges pages that have been incorrectly split by the pdf to
    text parsing """

    raceList = [[line for line in page.extractText().splitlines()] for page in pdfReaderObj.pages]  # itemize each line
    fullCard = []
    for i, val in enumerate(raceList):  # sew broken races back together
        if all(j.isupper() for j in val[0]):
            if i != len(raceList) - 1 and not all(k.isupper() for k in raceList[i + 1][0]):
                fullCard.append(val + raceList[i + 1])
            else:
                fullCard.append(val)
    return fullCard


def stringPartition(programNumber: str, startFirstCall: str, fieldSize: int) -> list[tuple]:
    """ partitions program number, start, and first call string and returns a list of tuples of potential combinations
    of values """

    if len(startFirstCall) == 2:
        return [(programNumber, startFirstCall[0], startFirstCall[1])]
    elif len(startFirstCall) == 3:
        return eliminateInvalids(fieldSize, [(programNumber, startFirstCall[0], startFirstCall[1:]),
                                             (programNumber, startFirstCall[:2], startFirstCall[2])])
    else:
        return eliminateInvalids(fieldSize, [(programNumber, startFirstCall[0:2], startFirstCall[2:])])


def eliminateInvalids(fieldsize: int, possibles: list[tuple]) -> list[tuple]:
    """ takes a list of tuples of potential combinations of values for the program number, start, and first call
    and returns a list of tuples after eliminating values that aren't logically sound """

    return [(tar1, tar2, tar3) for tar1, tar2, tar3, in possibles if
            all(i <= fieldsize for i in [int(tar2), int(tar3)]) and
            all(j[0] != '0' for j in [tar1, tar2, tar3])]


def getCertains(possibles: list[tuple]) -> list[list]:
    """ takes a list of tuples of potential combinations of values for the program number, start, and first call for
    every horse in the race and returns a list of two lists contains certain values and values that still need to be
    filtered down further to find the true value """

    certain = []
    toBeChecked = []
    for value in possibles:
        if len(value) == 1:
            certain.append(value[0])
        else:
            toBeChecked.append(value)
    return certain, toBeChecked


def storeKnownValues(certains: list[tuple]):
    """ takes a list containing the true program number, start, and first call of one or more horses and stores
    them in a dictionary """

    confirmed = defaultdict(set)
    for positions in certains:
        confirmed['number'].add(positions[0])
        confirmed['start'].add(positions[1])
        confirmed['firstCall'].add(positions[2])
    return confirmed

def addToCertainDict(certainDict: dict, numStartFirstcall: list) -> None:
    """ add string triplet to certain dict"""
    for key, i in zip(['number', 'start', 'firstCall'], numStartFirstcall):
        certainDict[key].add(i)

def removeFromCertainDict(certainDict: dict, numStartFirstcall: list) -> None:
    """ remove string triplet from certain dict """

    for key, i in zip(['number', 'start', 'firstCall'], numStartFirstcall):
        certainDict[key].remove(i)

def checkTripletInCertain(certainDict: dict, number: str, start: str, firstCall: str) -> bool:
    """ check if program number, start, and first call exist in certainDict"""

    if (number not in certainDict['number'] and start not in certainDict['start'] and
            firstCall not in certainDict['firstCall']):
        return True
    return False

def findTrueValue(fieldSize: int, certainDict: defaultdict, toBeChecked: list[tuple], idx: int) -> int:
    """ function recursively runs through all potential values for each entrant's program number, start, and first call,
        and runs until it finds a winner's values that don't conflict with the known values """

    if len(certainDict['number']) == fieldSize:  # all positions filled with no duplicates
        return True

    for number, start, firstCall in toBeChecked[idx]:
        # check for conflicts -- recursive call to next values to be checked if no conflicts
        if checkTripletInCertain(certainDict, number, start, firstCall):
            addToCertainDict(certainDict, [number, start, firstCall])
            if findTrueValue(fieldSize, certainDict, toBeChecked, idx + 1):
                return firstCall
            removeFromCertainDict(certainDict, [number, start, firstCall])


def findPossiblePositions(unparsedPositions: list, possiblePositions: list, fieldSize: int):
    entry = 'A'  # condition where there is an entry in the race, such as 1 1A or 2 2B
    usedProgramNumbers = set()

    for i, (programNumber, startFirstCall) in enumerate(unparsedPositions):

        # make adjustment to the program number if there is an entry such as 1 1A or 2 2B
        if programNumber in usedProgramNumbers:
            programNumber = programNumber + entry
            entry = chr(ord(entry) + 1)
        if i == 0:
            winnerPossibles = stringPartition(programNumber, startFirstCall, fieldSize)
            if len(winnerPossibles) == 1:
                return winnerPossibles[0][2]  # early exit if the winner's values are not in question
            else:
                possiblePositions.append(winnerPossibles)
        else:
            possiblePositions.append(stringPartition(programNumber, startFirstCall, fieldSize))
        usedProgramNumbers.add(programNumber)
    return False


def extractRaceData(race: list) -> dict:
    """ function iterates over a single race, extracting all relevant data.  Calls the findTrueValue function if
    the winners position at each call is uncertain"""

    findRunningLines = re.compile(r'^(?!\d+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|])\d+)(\d{1,'
                                  r'2}[a-zA-Zs\'.]{2,18}(\([A-Z]{2,6}\))?\d{1,4})$')
    raceDetail = {'maidens': False}
    unparsedPositions, possiblePositions = [], []
    winner = tenFurlongsPlus = False
    firstCallLengths = secondCallPosition = secondCallLengths = ''

    for i, val in enumerate(race):
        if i == 0:
            de.getTrackDateRace(race, raceDetail)
            if de.getMaidensCancelled(race[3], raceDetail):
                return {}  # return no data if race is canceled
        elif 'fieldSize' not in raceDetail and val == 'Trainers:':
            de.getFieldSize(race, raceDetail, i)
        elif 'surface' not in raceDetail and val in {"CurrentTrackRecord:", "Purse:"}:
            if de.filterHurdles(race, i):  #
                return {}  # return no data if race is for hurdlers
            tenFurlongsPlus = de.getSurfaceDistance(race, raceDetail, i)
        elif 'condition' not in raceDetail and val == 'Track:':
            de.getTrackCondition(race, raceDetail, i)
        elif bool(re.match(findRunningLines, val)):

            # if race is over ten furlongs, data is not corrupted and we can assign all the values from each call
            if tenFurlongsPlus and not winner:
                firstCallPosition = de.getProgramNumberStartFirstCall(val)[1]
                firstCallLengths, secondCallPosition, secondCallLengths = race[i + 1], race[i + 2], race[i + 3]
                de.assignPositionAtCalls(raceDetail, firstCallPosition, firstCallLengths, secondCallPosition,
                                         secondCallLengths)
                winner = True

            else:
                if not winner:
                    programNumber, startFirstCall = de.getProgramNumberStartFirstCall(val)
                    unparsedPositions.append([programNumber, startFirstCall])
                    firstCallLengths, secondCallPosition, secondCallLengths = race[i + 1], race[i + 2], race[i + 3]
                    winner = True
                else:
                    programNumberField, startFirstCallField = de.getProgramNumberStartFirstCall(val)
                    unparsedPositions.append([programNumberField, startFirstCallField])
        elif "CANCELLED" in val:
            return {}

    if tenFurlongsPlus:
        return raceDetail

    firstCallPosition = findPossiblePositions(unparsedPositions, possiblePositions, raceDetail['fieldSize'])

    if not firstCallPosition:
        certainTuples, toBeChecked = getCertains(possiblePositions)
        certainDict = storeKnownValues(certainTuples)
        firstCallPosition = findTrueValue(raceDetail['fieldSize'], certainDict, toBeChecked, 0)

    de.assignPositionAtCalls(raceDetail, firstCallPosition, firstCallLengths, secondCallPosition, secondCallLengths)
    return raceDetail
