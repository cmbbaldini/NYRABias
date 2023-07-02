from datetime import datetime
import re

Nose = Neck = Head = 0.25

distances = {'FiveFurlongs': '5 Furlongs', "FiveAndOneHalfFurlongs": '5 1/2 Furlongs', 'SixFurlongs': '6 Furlongs',
             'SixAndOneHalfFurlongs': '6 1/2 Furlongs', 'SevenFurlongs': '7 Furlongs',
             'SevenAndOneHalfFurlongs': '7 1/2 Furlongs', 'OneMile': '1 Mile',
             'OneAndOneSixteenthMiles': '1 1/16 Miles',
             'OneAndOneEighthMiles': '1 1/8 Miles', 'OneAndThreeSixteenthMiles': '1 3/16 Miles'}

distanceExceptions = {'OneAndOneFourthMiles': '1 1/4 Miles', 'OneAndFiveSixteenthMiles': '1 5/16 Miles',
                      'OneAndThreeEighthMiles': '1 3/8 Miles', 'OneAndOneHalfMiles': '1 1/2 Miles',
                      'OneAndFiveEighthMiles': '1 5/8 Miles', 'OneAndThreeFourthMiles': '1 3/4 Miles',
                      'TwoMiles': "2 Miles"}


def getTrackDateRace(race: list, raceDetail: dict) -> None:
    """ assign track, date, and raceNumber """

    track, date, raceNumber = ''.join([race[0], race[2]]).split('-')
    date = (datetime.strptime(date, '%B%d,%Y')).strftime('%Y-%m-%d')  # convert to datetime object
    raceDetail["track"] = track.capitalize()
    raceDetail['date'] = date
    raceDetail['raceNumber'] = int(raceNumber[-1]) if not raceNumber[-2].isnumeric() else int(raceNumber[-2:])


def getMaidensCancelled(conditions: str, raceDetail: dict) -> bool:
    """ check if race is restricted to maidens or if the race was canceled """

    if conditions.startswith('MAIDEN'):
        raceDetail['maidens'] = True
    elif conditions.startswith("Cancelled"):
        return True


def getFieldSize(race: list, raceDetail: dict, i: int) -> None:
    """ assign field size """

    if not race[i + 1][-1].isalpha():
        raceDetail['fieldSize'] = len(''.join([race[i + 1], race[i + 2]]).split(';'))
    else:
        raceDetail['fieldSize'] = len(race[i + 1].split(';'))

def filterHurdles(race: list, i: int) -> bool:
    """ check if race is for hurdlers """

    return "Hurdle" in race[i - 1]

def getSurfaceDistance(race: list, raceDetail: dict, i: int) -> bool:
    """ assign surface and distance values """

    surface = race[i - 1][race[i - 1].index('OnThe') + 5:]
    if '-' in surface:
        surface = surface.split('-')[0]
    if raceDetail['track'] == "Aqueduct" and surface in {"Turf", "Outerturf"}:
        if surface == "Turf":
            raceDetail['surface'] = "Inner" + surface.lower()
        else:
            raceDetail['surface'] = "Turf"
    else:
        raceDetail['surface'] = surface
    distance = (race[i - 1][:race[i - 1].index('OnThe')]).removeprefix('About')
    raceDetail['distance'] = distances.get(distance) or distanceExceptions.get(distance)
    return distance in distanceExceptions


def getTrackCondition(race: list, raceDetail: dict, i: int) -> None:
    """ assign track condition """

    raceDetail['condition'] = race[i + 1]


def getProgramNumberStartFirstCall(val: str) -> list:
    """ splits up string into two parts containing the program number, and the start concatenated with the first call
    """

    programNumber, startFirstCall = re.split(r'\D+', val)
    return [programNumber, startFirstCall]


def convertLengths(position: str, lengths: str) -> int:
    """ function converts lengths in string form to float """

    if position == '1':
        return 0
    return (eval(lengths) if '/' not in lengths or len(lengths) < 4 else eval(lengths[:lengths.index('/') - 1]) +
            eval(lengths[lengths.index('/') - 1:]))

def assignPositionAtCalls(raceDetail: dict, firstCallPosition: str, firstCallLengths: str, secondCallPosition: str,
                          secondCallLengths: str):
    """ assigns firstCall and secondCall values """

    raceDetail['firstCall'] = int(firstCallPosition)
    raceDetail['secondCall'] = int(secondCallPosition)
    raceDetail['firstCallLengthsBehind'] = convertLengths(firstCallPosition, firstCallLengths)
    raceDetail['secondCallLengthsBehind'] = convertLengths(secondCallPosition, secondCallLengths)