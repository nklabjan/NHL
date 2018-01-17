############################################################
#
# File Name:    nhl_etl.py
#
# Author:       Nick Klabjan
#
# Description:  Uses Beautiful Soup to retrieve and download
#               data from each NHL game and saves that data
#               in directories.
#
############################################################

from bs4 import BeautifulSoup
import urllib.error
from urllib.request import urlopen
import json
import os
import shutil
import params
import ijson
import requests

"""
Creates an NHL object that allows one to 
create directories and download NHL files.
"""
class NHL:
    # saves current directory
    startingDir = os.getcwd()

    """Constructs new NHL object."""
    def __init__(self):
        pass

    """Creates directories for each NHL season."""
    @staticmethod
    def makedir():
        # traverses through NHL season
        for x in params.seasons:
            # if directory for that NHL season doesn't already exist
            if not os.path.exists(str(x)):
                # makes directory for that NHL season
                os.mkdir(str(x))
            else:
                # removes directory if it already exists
                shutil.rmtree(str(x))
                # makes directory for that NHL season
                os.mkdir(str(x))

    """Downloads .json files from the NHL server."""
    def transferfiles(self):
        # traverses through NHL seasons
        for x in params.seasons:
            # changes directory to that NHL season
            os.chdir(str(x))
            # counter to count number of files downloaded
            counter = 0
            # traverses through each game in a season
            for y in range(0, params.maxGames):
                try:
                    # saves URL address that contains game's data to variable 'url'
                    url = params.url1 + str(x) + "02" + str("%04d" % y) + params.url2
                    # grabs the game's data from the url
                    jsonString = urllib.request.urlopen(url).read().decode()
                    data = json.loads(jsonString)
                    # creates a new .json file as an outfile
                    with open(str(x) + "02" + str("%04d" % y) + ".json", "w") as outfile:
                        # copies the game's data from the url to the .json file
                        json.dump(data, outfile)
                        # increment counter after file has been downloaded
                        counter = counter + 1
                # throws exception if url doesn't exist (ie no NHL game)
                except urllib.error.HTTPError:
                    pass
            # prints out number of files downloaded for each season
            print("Season " + str(x) + ": " + str(counter) + " games downloaded")
            # returns back to starting directory
            os.chdir(self.startingDir)