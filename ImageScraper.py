import numpy as np
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import os
from os.path  import basename
import urllib.request

s = HTMLSession()



def getData(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser') 
    return soup

""" 
def getNextPage(soup):
    
    if not soup.find('a', string='Next')['href']:
        url = 'https://www.prosportstransactions.com/basketball'
        return url
    else:
        return soup.find('a', string='Next')['href'] """

url = 'https://www.nba.com/players'



def getCurrentlyInjured():

    injList = []
    HTMLPage = getData(url)
    container = HTMLPage.find("div", {"id": "__next"})
    content = container.find("div", {"class": "Layout_base__6IeUC Layout_withSubNav__ByKRF Layout_justNav__2H4H0"})
    main = content.find("div", {"class": "Layout_mainContent__jXliI"})
    parse1 = main.find("main")
    parse2 = parse1.find("div", {"class": "MaxWidthContainer_mwc__ID5AG"})
    parse3 = parse2.find("section", {"class": "Block_block__62M07"})
    parse4 = parse3.find("div", {"class": "Block_blockContent__6iJ_n"})
    parse5 = parse4.find("div", {"class": "PlayerList_content__kwT7z"})
    parse6 = parse5.find("div", {"class": "PlayerList_playerTable__Jno0k"})
    parse7 = parse6.find("div", {"class": "LeagueRoster_table__B1Zyz"})
    parse8 = parse7.find("div", {"class": "MockStatsTable_statsTable__V_Skx"})
    parse9 = parse8.find("div")
    parse10 = parse9.find("table", {"class": "players-list"})
    parse11 = parse10.find("tbody")
    parse12 = parse11.find("tr")
    parse13 = parse12.find("td", {"class": "primary text RosterRow_primaryCol__1lto4"})
    parse14 = parse13.find("a", {"class": "Anchor_anchor__cSc3P RosterRow_playerLink__qw1vG"})
    parse15 = parse14.find("div", {"class": "RosterRow_playerHeadshot__tvZOn"})
    parse16 = parse15.find("img")
    link = parse16["src"]
    imgname = parse16["alt"]+".png"

    imgContent = requests.get(link).content
    # Set the directory path
    directory = "C:/Users/thoma/OneDrive - Queen's University/Documents/Random Code Folders Crap/Pythion VS Code/Fantasy Scraper Folder/playerImages"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the image to a file in the directory
    with open(os.path.join(directory, imgname), "wb") as f:
        f.write(imgContent)

    #if "http" in link:
    #    with open(imgname, "wb") as f:
    #        f.write(requests.get(link).content)

    #directory = "C:/Users/thoma/OneDrive - Queen's University/Documents/Random Code Folders Crap/Pythion VS Code/Fantasy Scraper Folder/playerImages"


    #C:\Users\thoma\OneDrive - Queen's University\Documents\Random Code Folders Crap\Pythion VS Code\Fantasy Scraper Folder\playerImages
    return link

pprint(getCurrentlyInjured())