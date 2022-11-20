import numpy as np
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from pprint import pprint


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

url = 'https://www.cbssports.com/nba/injuries/'



def getCurrentlyInjured():

    injList = []
    HTMLPage = getData(url)
    container = HTMLPage.find("div", {"class": "Page-shell"})
    content = container.find("div", {"class": "Page-content"})
    main = content.find("main", {"class": "PageLayout PageLayout--adRail"})
    col = main.find("div", {"class": "Page-colMain"})
    teams = col.find_all("div", {"class": "TableBaseWrapper"})

    for team in teams:
        base = team.find("div", {"id": "TableBase"})
        shadows = base.find("div", {"class": "TableBase-shadows"})
        overflow = shadows.find("div", {"class": "TableBase-overflow"})
        table = overflow.find("table", {"class": "TableBase-table"})
        body = table.find("tbody")

        rows = table.find_all('tr')
        for row in rows:
            cols=row.find_all('td')
            cols=[x.text.strip() for x in cols]
            injList.append(cols)
            #print(cols)
    
    cleanedList = [x for x in injList if x != []]
    pprint(cleanedList)  

    return cleanedList

getCurrentlyInjured()


#table = container.find('table')
#table_rows = table.find_all('tr')

#print(row)
