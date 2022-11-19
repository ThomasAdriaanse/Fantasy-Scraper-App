from sys import maxsize
from espn_api.basketball import League
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint


lLeague = League(league_id=2027816442, year=2022, espn_s2='AECOM11%2FOes1p32ZKGjC3wfVCRNWO7xugbWPEtY8A9j1MFeexoupN2g6XkJP265N5lBgdTNAGHKxPGnwbhLQtjBYMmrkt8DRt1l9j%2BDvb0O19%2FX%2BXqWAo0uE6X6wS7nH9CXu62kY9dYVTtSCeNnv797iZmXl8GjAvwspZFvU4CH2VPzGj7Uj5DbseYM2%2BOA%2FS0k2zPXNzPlVrV2PaffrFeX2m7r5he5gdROQI8nBv25OzazETyWc1PvsKjLtc0dVLxmd5FqkEALjy4%2FRWjkvCCwhEZUn%2FB0S8Cash9sAjZbJCA%3D%3D', \
                                                    swid='{956E0B11-5D52-40DC-BDC7-2165266219D9}')

league = League(league_id=547530848, year=2023, espn_s2='AEAQt2d9QIN%2FNSX8LUGzWjCJjXeZGJ9dv%2B1ipZg6guQEPdYVylucTwuvCiF2Ddzl7BkAJ%2BaEe5fAn1%2Fq9dSixaaUuporz53HTgvrOZbprG9ciSF98wSKCoEUdXbfApwJPNMgcCPIB014tusrdJUPRWVozp0xHXpDCfs1LlxC1Ex65YV5fVFCNekgi%2FyVO9PnlNGbViyrSu8bXgEvncJCuSds4YRJsvni2QIACyhf%2F9i0GF6zEe%2BzEdcYMwqFLSvJG9hbyGHmYWBiV5nt2HU7fZ0SumkV%2Bf6Zp2P6227CVfG4Bg%3D%3D', \
                                                    swid='{956E0B11-5D52-40DC-BDC7-2165266219D9}')
#league = League(league_id=547530848, year=2023)
from Levenshtein import distance as lev
from Levenshtein import *

"""
injury_list = [] 
for team in range(len(league.teams)):
    team = league.teams[team]
    roster = team.roster
    for player in roster:
        if player.injured == True:
            injury_list.append(player.name)

f_a = []
for player in league.free_agents(2, 300):
    f_a.append(player)

f_a_stats = []
for player in f_a:
    f_a_stats.append(player.stats)"""


def getTeamRoster(teamNum):
    return league.teams[teamNum].roster
""" 
def get2Stats(stat1, stat2, averageOrTotal, team):#should probably change to getXStats later

    stats1Vals = []
    stats2Vals = []
    playedRoster = []

    if team == 0:# team 0 is all teams
        for j in range(len(league.teams)):
            for i in range(len(league.teams[team].roster)):
                if '022022' in league.teams[team].roster[i].stats.keys():
                    
                    stats1Vals.append(league.teams[team].roster[i].stats['022022'][averageOrTotal][stat1])
                    stats2Vals.append(league.teams[team].roster[i].stats['022022'][averageOrTotal][stat2])
                    playedRoster.append(league.teams[team].roster[i].name)
    else:
        for i in range(len(league.teams[team].roster)):
            if '022022' in league.teams[team].roster[i].stats.keys():
                
                stats1Vals.append(league.teams[team].roster[i].stats['022022'][averageOrTotal][stat1])
                stats2Vals.append(league.teams[team].roster[i].stats['022022'][averageOrTotal][stat2])
                playedRoster.append(league.teams[team].roster[i].name)
      
    return stats1Vals, stats2Vals, playedRoster
 """

#pprint(league.teams[0].roster[4].stats['2022_total'])
#pprint(league.teams[0].roster[0].name)
def getStatsTeamObj(team, averageOrTotal, *args):#same as get2Stats but uses team obj not team number

    statsLists = [[] for i in range(len(args))]
    #print(team)
    #print(averageOrTotal)
    #pprint(args)
    for index, ar in enumerate(args):
        
        for i in range(len(team.roster)):
            if '2022_total' in team.roster[i].stats.keys():
                if 'avg' in team.roster[i].stats['2022_total'].keys():
                    if ar == "name":
                        statsLists[index].append(team.roster[i].name)
                    else:
                        #print(statsLists[index].append(team.roster[i].stats['2022_total']))
                        statsLists[index].append(team.roster[i].stats['2022_total'][averageOrTotal][ar])
            elif '2023_total' in team.roster[i].stats.keys():
                if 'avg' in team.roster[i].stats['2023_total'].keys():
                    if ar == "name":
                        statsLists[index].append(team.roster[i].name)
                    else:
                        statsLists[index].append(team.roster[i].stats['2023_total'][averageOrTotal][ar])

    #pprint(statsLists)
    return statsLists 



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
    #playerArray = [0,0,0]
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



"""
PTS = PTSvals
MIN = MINvals

ser =  pd.Series(index = MIN, data = PTS)
df = ser.to_frame()

df.reset_index(inplace=True)
df.columns = ['MIN','PTS']
df.plot(kind='scatter',x='MIN',y='PTS',c='DarkBlue')
plt.show()


df = pd.DataFrame(
    [PTSvals,
    MINvals], 
    index=['points', 'minutes'],
    columns=playedRoster
    )

plt.plot(PTSvals, MINvals, 'ro')
print(df)
plt.axis([0, 36, 0, 50])

plt.show()
"""


"""

x = PTSvals
y = MINvals
names = np.array(playedRoster)
c = np.random.randint(1,5,size=len(names))

norm = plt.Normalize(1,4)
cmap = plt.cm.RdYlGn

fig,ax = plt.subplots()
sc = plt.scatter(x,y,c=c, cmap=cmap, norm=norm)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):

    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}, {}".format(" ".join([names[n] for n in ind["ind"]]), 
                               " ".join([str(x[n]) for n in ind["ind"]]),
                               " ".join([str(y[n]) for n in ind["ind"]]))
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)


def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = sc.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()"""