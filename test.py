import ijson
from bs4 import BeautifulSoup
import urllib.error
from urllib.request import urlopen
import json
import os
import shutil
import pandas

column_names = ["GamePk", "Season", "Date/Time", "Away Team", "Home Team", "Players"]
gamesDF = pandas.DataFrame(columns=column_names)
#gamesDF.set_index({"GamePk", "Season", "Date/Time"})
os.chdir("2014")
gamesDF['GamePk'] = gamesDF.GamePk.astype(int)
with open("2014020001.json", 'r') as f:
    iterJson = ijson.parse(f)
    values = dict()
    players = dict()
    for prefix, event, value in iterJson:
        if prefix == 'gamePK':
            values['GamePk'] = value
        elif prefix == "gameData.game.season":
            values['Season'] = value
        elif prefix == "gameData.datetime.dateTime":
            values['Date/Time'] = value
        elif prefix == "gameData.teams.away.name":
            values["Away Team"] = value
        elif prefix == "gameData.teams.home.name":
            values["Home Team"] = value
        elif prefix.startswith("gameData.players"):
                parts = prefix.split('.', maxsplit=3)
                if len(parts) > 3:
                    if parts[2] not in players:
                        players[parts[2]] = {'fullName': None, 'rosterStatus': None, 'active': None,
                                             'currentTeam.name': None}
                    if parts[3] in players[parts[2]]:
                        players[parts[2]][parts[3]] = value
        else:
            if prefix.startswith("gameData.boxscore.teams.away.players"):
                parts = prefix.split('.')
                if len(parts) > 6:
                    if parts[5] not in players:
                        players[parts[5]] = {"timeOnIce": None, "powerPlayTimeOnIce": None,
                                             "shortHandedTimeOnIce": None}
                    if parts[6] in players[parts[5]]:
                        players[parts[5]][parts[6]] = value

    playerList = [(v['fullName'], v['rosterStatus'], v['active'], v['currentTeam.name'], v['timeOnIce'],
                   v['powerPlayTimeOnIce'], v['shortHandedTimeOnIce']) for k, v in players.items()]
    values["Players"] = playerList

    gamesDF = gamesDF.append(values, ignore_index=True)
    print(gamesDF)