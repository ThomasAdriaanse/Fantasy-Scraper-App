from sys import maxsize
from espn_api.basketball import League
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint


lLeague = League(league_id=2027816442, year=2022, espn_s2='AECOM11%2FOes1p32ZKGjC3wfVCRNWO7xugbWPEtY8A9j1MFeexoupN2g6XkJP265N5lBgdTNAGHKxPGnwbhLQtjBYMmrkt8DRt1l9j%2BDvb0O19%2FX%2BXqWAo0uE6X6wS7nH9CXu62kY9dYVTtSCeNnv797iZmXl8GjAvwspZFvU4CH2VPzGj7Uj5DbseYM2%2BOA%2FS0k2zPXNzPlVrV2PaffrFeX2m7r5he5gdROQI8nBv25OzazETyWc1PvsKjLtc0dVLxmd5FqkEALjy4%2FRWjkvCCwhEZUn%2FB0S8Cash9sAjZbJCA%3D%3D', \
                                                    swid='{956E0B11-5D52-40DC-BDC7-2165266219D9}')

Cleague = League(league_id=547530848, year=2023, espn_s2='AEAQt2d9QIN%2FNSX8LUGzWjCJjXeZGJ9dv%2B1ipZg6guQEPdYVylucTwuvCiF2Ddzl7BkAJ%2BaEe5fAn1%2Fq9dSixaaUuporz53HTgvrOZbprG9ciSF98wSKCoEUdXbfApwJPNMgcCPIB014tusrdJUPRWVozp0xHXpDCfs1LlxC1Ex65YV5fVFCNekgi%2FyVO9PnlNGbViyrSu8bXgEvncJCuSds4YRJsvni2QIACyhf%2F9i0GF6zEe%2BzEdcYMwqFLSvJG9hbyGHmYWBiV5nt2HU7fZ0SumkV%2Bf6Zp2P6227CVfG4Bg%3D%3D', \
                                                    swid='{956E0B11-5D52-40DC-BDC7-2165266219D9}')
#league = League(league_id=547530848, year=2023)
from Levenshtein import distance as lev
from Levenshtein import *
league = Cleague


#print(league.scoreboard())


def createPlayerDict(year):
    #year = '2023_total'
    playerDict = {}
    for j in range(len(league.teams)):
        for i in range(len(league.teams[j].roster)):
            if year in league.teams[j].roster[i].stats.keys():
                    if 'avg' in league.teams[j].roster[i].stats[year].keys():
                        pstats = league.teams[j].roster[i].stats[year]['avg']
                        pstats.update({'FPTS': pstats['FGM']*2-pstats['FGA']+pstats['FTM']-pstats['FTA']+pstats['3PTM']+pstats['REB']+2*pstats['AST']+3*pstats['STL']+3*pstats['BLK']-2*pstats['TO']+pstats['PTS']})
                        pstats.update({"PTEAM": league.teams[j].roster[i].proTeam})
                        pstats.update({"FTEAM": league.teams[j]})
                        #playerDict[league.teams[j].roster[i].name] =  league.teams[j].roster[i].stats[year]['avg']
                        playerDict[league.teams[j].roster[i].name] = pstats


    for i in league.free_agents(size = 200):
        if year in i.stats.keys():
            if 'avg' in i.stats[year].keys():
                pstats = i.stats[year]['avg']
                pstats.update({'FPTS': pstats['FGM']*2-pstats['FGA']+pstats['FTM']-pstats['FTA']+pstats['3PTM']+pstats['REB']+2*pstats['AST']+3*pstats['STL']+3*pstats['BLK']-2*pstats['TO']+pstats['PTS']})
                pstats.update({"PTEAM": i.proTeam})
                #playerDict[i.name] = i.stats[year]['avg']
                playerDict[i.name] = pstats

    return playerDict

def roundStats(year):
    for j in range(len(league.teams)):
        for i in range(len(league.teams[j].roster)):
            if year in league.teams[j].roster[i].stats.keys():
                    if 'avg' in league.teams[j].roster[i].stats[year].keys():
                        pstats = league.teams[j].roster[i].stats[year]['avg']
                        for i in pstats:
                            if isinstance(pstats[i], float)==True:
                                #print("Pstats")
                                #pprint(pstats[i])
                                #pprint(pstats)

                                pstats[i] = round(pstats[i], 2)
                                #pprint(pstats[i])
    
    for i in league.free_agents():
        if year in i.stats.keys():
            if 'avg' in i.stats[year].keys():
                    pstats = i.stats[year]['avg']
                    #print(pstats)
                    for j in pstats:
                        if isinstance(pstats[j], str)==False:
                            pstats[j] = round(pstats[j], 2)

def splitByProTeam(playerDict):
    proTeamDict = {}
    #print(playerDict["Dejounte Murray"]['FPTS'])
    for i in playerDict:
        #print(playerDict[i]["FPTS"])
        #pprint(playerDict[i]["PTEAM"])
        if playerDict[i]["PTEAM"] not in proTeamDict:
            proTeamDict[playerDict[i]["PTEAM"]] = {}
        
        #print(i)
        proTeamDict[playerDict[i]["PTEAM"]].update({i:playerDict[i]})
            

    return proTeamDict

def addFPTS(year):
    for team in league.teams:
        for i in range(len(team.roster)):
            #needed so no error occurs when player has not played a game yet
            if year in team.roster[i].stats.keys():
                if 'avg' in team.roster[i].stats[year].keys():
                    pstats =  team.roster[i].stats[year]['avg']
                    pstats.update({'FPTS': pstats['FGM']*2-pstats['FGA']+pstats['FTM']-pstats['FTA']+pstats['3PTM']+pstats['REB']+2*pstats['AST']+3*pstats['STL']+3*pstats['BLK']-2*pstats['TO']+pstats['PTS']})
                    pstats.update({'PTEAM': team.roster[i].proTeam})

#dict = createPlayerDict('2023_total')
#proTeamDict = splitByProTeam(dict)
#pprint(proTeamDict)
#pprint(league.free_agents(size = 200))
#pprint(playerDict)

def getTeamRoster(teamNum):
    return league.teams[teamNum].roster

def getStatsTeamObj(team, year, averageOrTotal, *args):#same as get2Stats but uses team obj not team number

    statsLists = [[] for i in range(len(args))]
    for index, ar in enumerate(args):
        for i in range(len(team.roster)):
            #needed so no error occurs when player has not played a game yet
            if year in team.roster[i].stats.keys():
                if 'avg' in team.roster[i].stats[year].keys():
                    if ar == "name":
                        statsLists[index].append(team.roster[i].name)
                    else:
                        statsLists[index].append(team.roster[i].stats[year][averageOrTotal][ar])
           
    return statsLists 

def getAllPlayerStats(player, playerDict):
    if player.name in playerDict:
        return playerDict[player.name]
    else:
        return None

def getAllPlayerStatsByName(player, playerDict):
    if player in playerDict:
        return playerDict[player]
    else:
        return None

def getPlayerStatsByName(player, playerDict, *args):
    tempList = []
    if player in playerDict:
        for i in args:
            tempList.append(playerDict[player][i])
        return tempList
    else:
        return None

def getPlayerInfo(nameinput, xAxis, yAxis):
    #playerName
    cleanNameinput = cleanseString(nameinput)
    playerArray=[]
    for j in range(len(league.teams)):
        if lev(cleanNameinput, cleanseString(league.teams[j].team_name))<=2:
            return [league.teams[j],0,0]
        for i in range(len(league.teams[j].roster)):
            #print(league.teams[j].roster[i].stats.keys())
            if '2022_total' in league.teams[j].roster[i].stats.keys():
                if lev(cleanNameinput, cleanseString(league.teams[j].roster[i].name))<=2:
                    playerArray.append(league.teams[j].roster[i].stats['2022_total']['avg'][xAxis])
                    playerArray.append(league.teams[j].roster[i].stats['2022_total']['avg'][yAxis])
                    playerArray.append(league.teams[j].roster[i].name)
                    return playerArray
            elif '2023_total' in league.teams[j].roster[i].stats.keys():
                if lev(cleanNameinput, cleanseString(league.teams[j].roster[i].name))<=2:
                    playerArray.append(league.teams[j].roster[i].stats['2023_total']['avg'][xAxis])
                    playerArray.append(league.teams[j].roster[i].stats['2023_total']['avg'][yAxis])
                    playerArray.append(league.teams[j].roster[i].name)
                    return playerArray

    print("No Player Found")
    return [0,0,0]

def cleanseString(string):
    cleanString0 = string.lower()
    cleanString1 = cleanString0.replace("-","")
    cleanString2 = cleanString1.replace(".", "")
    cleanString = cleanString2.replace(" ", "")
    return cleanString

def getMaxRosterSize():
    maxSize=0
    for i in range(len(league.teams)):
        if len(league.teams[i].roster)>maxSize:
            maxSize = len(league.teams[i].roster)

    return maxSize;


def getAvgStats(playerDict):
    avgStatsDict = {}
    avgStatsDict.update({'FPTS':0, 'FGM':0, 'FGA':0, 'FTM':0, 'FTA':0, '3PTM':0, 'REB':0, 'AST':0, 'STL':0, 'BLK':0, 'TO':0, 'PTS':0})
    statsNeeded = {'FPTS', 'FGM', 'FGA', 'FTM', 'FTA', '3PTM', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PTS'}
    #avg stats overall:
    #try:
    for ind, val in enumerate(playerDict):
        if 'FTEAM' in playerDict[val].keys():
            pprint(playerDict[val])
            for j in statsNeeded:
                avgStatsDict[j]+= int(playerDict[val][j])

    for j in statsNeeded:
        avgStatsDict[j]/= len(playerDict)
    return avgStatsDict

"""     #avg stats for rostered players
    except Exception as e:
        for k in playerDict:
            print(k.roster)
            for ind, val in enumerate(k.roster):
                for j in statsNeeded:
                    avgStatsDict[j]+= int(k[val][j])
        
                for j in statsNeeded:
                    avgStatsDict[j]/= len(k)
                return avgStatsDict
        
 """


#pprint(league.teams)


#pprint(getAvgStats(dict))