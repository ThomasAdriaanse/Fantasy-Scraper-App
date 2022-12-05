import scraper
from pprint import pprint
import heapq


playerDict2023 = scraper.createPlayerDict('2023_total')
scraper.addFPTS('2023_total')
scraper.roundStats('2023_total')
proTeamDict2023 = scraper.splitByProTeam(playerDict2023)


#TO DO:
#sort into real teams DONE
#get average fpts per top 6 on each team DONE
#get who was on which team last year
#get availability score per player by adding fpts of other players on the team
#get change in availability score
#calculate change in expected ftps with help of change in availability score

def addContestedScore(playerDict2023, proTeamDict2023):
    #get average fpts of top 6 players on each team
    for i in proTeamDict2023:
        FPTSList = []
        for j in proTeamDict2023[i]:
            FPTSList.append(proTeamDict2023[i][j]['FPTS'])

        top6 = heapq.nlargest(6, FPTSList)
        avgFPTS = sum(top6)/len(top6)

        proTeamDict2023[i].update({'FPTS':avgFPTS})
        #print(avgFPTS) 


    #take away players own FPTS score from their team's top 6 and use that as their contested score
    for i in playerDict2023:

        team = playerDict2023[i]["PTEAM"]
        contestedScore = proTeamDict2023[team]['FPTS']*6 - playerDict2023[i]['FPTS']
        
        proTeamDict2023[team][i].update({'CONT':contestedScore})
        #print(proTeamDict2023[team]['FPTS'], "MINUS", playerDict2023[i]['FPTS'], "EQUALS", contestedScore)
        #print(i, " " ,contestedScore)

scraper.league = scraper.lLeague
playerDict2023 = scraper.createPlayerDict('2022_total')
proTeamDict2023 = scraper.splitByProTeam(playerDict2023)
addContestedScore(playerDict2023, proTeamDict2023)
