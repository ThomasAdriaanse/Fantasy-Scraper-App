import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, PhotoImage
from tkinter import *
#from ttkwidgets.autocomplete import AutocompleteEntryListbox
from pprint import pprint
import customtkinter
import heapq

from PIL import ImageTk, Image

import urllib
import json
 
import pandas as pd
import numpy as np

import InjuryScraper
import scraper
import advPlayerStats

from tkintertable import TableCanvas, TableModel




LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

playerGraphFigure = Figure(figsize=(5,5), dpi=100)
a = playerGraphFigure.add_subplot(111)
teamGraphFigure = Figure(figsize=(5,5), dpi=100)
a2 = teamGraphFigure.add_subplot(111)

playerHighlight=[0,0,0]#x, y, name
showNames=True
xAxis = ''
yAxis = ''
folderLocation = "C:/Users/thoma/OneDrive - Queen's University/Documents/Random Code Folders Crap/Pythion VS Code/Fantasy Scraper Folder/"

scraper.league = scraper.lLeague
playerDict2022 = scraper.createPlayerDict('2022_total')
proTeamDict2022 = scraper.splitByProTeam(playerDict2022)
scraper.addFPTS('2022_total')
scraper.roundStats('2022_total')
advPlayerStats.addContestedScore(playerDict2022, proTeamDict2022)

scraper.league = scraper.Cleague
playerDict2023 = scraper.createPlayerDict('2023_total')
proTeamDict2023 = scraper.splitByProTeam(playerDict2023)
scraper.addFPTS('2023_total')
scraper.roundStats('2023_total')
advPlayerStats.addContestedScore(playerDict2023, proTeamDict2023)



################# TO DO #################
#fix graph
#add advanced stats
#trade analyzer
#previous years stats
#contested score (kinda DONE) b 
    # - FPTS of other players on team
    # - FPTS of other players on same position on team
    # - age of players?
#player pictures behind team stats
#player stats window
#nba team pages

#########################################


def animate(i):
    global showNames
    global playerHighlight
    global xAxis
    global yAxis
    xar=[]#data arrays
    yar=[]
    namear = []
    a.clear()

    #MIN,FGM,FGA,FTM,FTA,3PM,REB,AST,STL, BLK, TO, PTS,
    if xAxis != '' and yAxis != '':

        for team in scraper.league.teams:#plot all players in league
            xar, yar, namear=scraper.getStatsTeamObj(team, '2023_total', 'avg', xAxis, yAxis, "name")
            a.plot(xar,yar, 'ro')
                

        if playerHighlight[1] != 0 and playerHighlight[2] != 0:
            a.plot(playerHighlight[0], playerHighlight[1], 'ro', color = 'Yellow')
            if showNames == True: 
                a.annotate(playerHighlight[2], (playerHighlight[0], playerHighlight[1]))
            #print(playerHighlight[2], playerHighlight[0], playerHighlight[1])
        elif playerHighlight[0]!=0:
            for team in scraper.league.teams:
                if playerHighlight[0] == team:
                    xar, yar, namear=scraper.getStatsTeamObj(team, '2023_total', 'avg', xAxis, yAxis, "name")
                    a.plot(xar,yar, 'ro', color = "Green")
                    if showNames==True:
                        for i, txt in enumerate(namear):
                            a.annotate(txt, (xar[i], yar[i]))
                    else:
                        a.plot(xar,yar, 'ro')
        
        a.set_xlabel(xAxis)
        a.set_ylabel(yAxis)
        a.set_title(yAxis +'/'+ xAxis)

""" def animate2(i):
    xar=[]#data arrays
    yar=[]
    namear = []
    a2.clear()
    #a.plot()

    for teamNum in range(len(scraper.league.teams)):
        xar, yar, namear=scraper.getStats('PTS', 'MIN', 'avg', teamNum)
        
        if teamNum == 3:
            a2.plot(xar,yar, 'ro', color = "Green")
            for i, txt in enumerate(namear):
                a.annotate(txt, (xar[i], yar[i]))
            
        else:
            a2.plot(xar,yar, 'ro')

    a2.set_xlabel('PTS')
    a2.set_ylabel('MIN')
    a2.set_title('MIN/PTS')
 """

class FantasyScraperApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default=folderLocation+"FantasyScraperIcon.ico")
        tk.Tk.wm_title(self, "Fantasy Scraper")
        
        #Settings so that frame will take up whole window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        

        self.frames = {}
        for F in (StartPage, GroupAnalysisPage, StatsPage, InjuryPage, MyTeamPage, MatchupPage):
            
            frame = F(container, self)
            self.frames[F] = frame
            #frame.pack(expand=TRUE)
            frame.grid(row=0, column=0, sticky="nsew")


        menubar = tk.Menu(container)
        self.config(menu = menubar)

        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        #filemenu.add_command(label="Save settings", command=lambda: popupmsg('Not supported just yet!'))
        #filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        
        changePageMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Change Page", menu=changePageMenu)
        #changePageMenu.add_separator()
        changePageMenu.add_command(label="Start Page",  command=lambda:self.show_frame(StartPage))
        changePageMenu.add_command(label="Group Analysis Page", command=lambda:self.show_frame(GroupAnalysisPage))
        changePageMenu.add_command(label="Stats Page", command=lambda:self.show_frame(StatsPage))
        changePageMenu.add_command(label="Injury Page", command=lambda:self.show_frame(InjuryPage))
        changePageMenu.add_command(label="My Team Page", command=lambda:self.show_frame(MyTeamPage))
        changePageMenu.add_command(label="Matchup Page", command=lambda:self.show_frame(MatchupPage))


        self.show_frame(StartPage)
        #self.show_frame(SelectPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
  
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=("""Enter app?"""), font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.configure(background='green')

        #self.configure(background='green')
        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(GroupAnalysisPage))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                            command=quit)
        button2.pack()

        # add a pop up to enter team details
        label1 = tk.Label(self, text=("Enter League Details:"), font=LARGE_FONT)
        label1.pack(pady=10,padx=10)

        label2 = tk.Label(self, text=("Enter Team Name"), font=LARGE_FONT)
        label2.pack(pady=10,padx=10)

class GroupAnalysisPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #self.configure(background='red')

        # create the input frame
        input_frame = InputFrame(self)
        #input_frame.grid(column=0, row=0)
        input_frame.pack(side = LEFT)

        # create the button frame
        graph_frame = GraphFrame(self)
        #button_frame.grid(column=1, row=0)
        graph_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

class InputFrame(tk.Frame): 
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager
        self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)

        # Find player entry
        ttk.Label(self, text='Find Player or Team:').grid(column=0, row=0, sticky=tk.W)
        playerEntry = ttk.Entry(self, width=30)
        #playerEntry = ttk.AutocompleteEntry(self, width=30)
        playerEntry.focus()
        playerEntry.grid(column=1, row=0, sticky=tk.W)

        # X Axis
        ttk.Label(self, text='X Axis:').grid(
            column=0, row=1, sticky=tk.W)
        options = ['MIN','FGM','FGA','FTM','FTA', '3PTM', 'REB','AST','STL', 'BLK', 'TO', 'PTS', 'FPTS', 'CONT']
        xAxisInput = StringVar(self)
        xAxisInput.set(options[0])
        xAxisSelect = OptionMenu(self, xAxisInput, *options)
        xAxisSelect.grid(column=1, row=1, sticky=tk.W)

        # Y Axis
        ttk.Label(self, text='Y Axis:').grid(
            column=0, row=2, sticky=tk.W)
        """yAxisEntry = ttk.Entry(self, width=30)
        yAxisEntry.grid(column=1, row=2, sticky=tk.W)"""
        yAxisInput = StringVar(self)
        yAxisInput.set(options[0])
        yAxisSelect = OptionMenu(self, yAxisInput, *options)
        yAxisSelect.grid(column=1, row=2, sticky=tk.W)
        
        # Show Highlighted Player  
        showHighlightedBox = tk.StringVar()
        highlightChecked = IntVar()
        showHighlightedBox = ttk.Checkbutton(
            self,
            text='Show Highlight',
            variable=highlightChecked,
            command=lambda: changeHighlightPlayer(playerEntry.get(), highlightChecked.get()))
        showHighlightedBox.grid(column=0, row=3, sticky=tk.W)

        # Show Names checkbox
        showNamesBox = tk.StringVar()
        namesChecked = IntVar()
        showNamesBox = ttk.Checkbutton(
            self,
            variable=namesChecked,
            text='Show Names?',
            command=lambda: changeNameShowing(namesChecked.get()))
        showNamesBox.grid(column=0, row=4, sticky=tk.W)

        goButton = ttk.Button(self, text="Go!",
                            command=lambda: changeAxes(xAxisInput.get(), yAxisInput.get()))
        goButton.grid(column=0, row=5, sticky=tk.W)

        for widget in self.winfo_children():
            widget.grid(padx=0, pady=5)

        def changeHighlightPlayer(player, checked):
            global playerHighlight
            if checked == 1:
                playerHighlight=scraper.getPlayerInfo(player, xAxis, yAxis)
            else:
                playerHighlight=[0,0,0]

        def changeNameShowing(checked):
            global showNames
            if checked==0:
                showNames=True
            elif checked==1:
                showNames=False
        
        def changeAxes(x, y):
            global xAxis 
            xAxis= x
            global yAxis 
            yAxis = y

class GraphFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager

        canvas = FigureCanvasTkAgg(playerGraphFigure, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

class StatsPage(tk.Frame):

    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)
        
        #code for scroll:-----------------------
        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)#

        # Create a scrollbar and attach it to the frame
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Attach the scrollbar to the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame to hold the scrollable content
        scrollable_frame = tk.Frame(canvas)

        # Bind the scrollable frame to the scrollbar
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)

        # Set the size of the scrollable region
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
        #---------------------------------

        for i in range(6):
            col = StatPageColFrame(scrollable_frame, scraper.league.teams[i*2], scraper.league.teams[i*2+1])
            col.pack()
    
class StatPageColFrame(tk.Frame):
    def __init__(self, parent, team1, team2):  
        tk.Frame.__init__(self, parent)
        self.configure(background='yellow')

        #table_frameL = TableFrame(self, scraper.league.teams[i*2])
        table_frameL = MyTeamPage(self, team1)
        #button_frame.grid(column=1, row=0)
        table_frameL.pack(side = LEFT)

        #table_frameR = TableFrame(self, scraper.league.teams[i*2+1])
        table_frameR = MyTeamPage(self, team2)
        #button_frame.grid(column=1, row=0)
        table_frameR.pack(side = RIGHT)

class TableFrame(tk.Frame):
    def __init__(self, container, team):
        super().__init__(container)

        #print(team)
        if team not in scraper.league.teams:
            team = scraper.league.teams[0]
        #master = self
        """ table = TableCanvas(self, 
			cellwidth=60, cellbackgr='#e3f698',
			thefont=('Arial',12),rowheight=18, rowheaderwidth=30,
			rowselectedcolor='yellow', read_only=True)
        table.show()  """
        self.configure(background='green')
        #self.height = 20
        #print(team.team_id)
        teamNameLabel = tk.Label(self, text=team.team_name, font=LARGE_FONT)
        teamNameLabel.pack(side = "top") 

        self.table=ttk.Treeview(self, height=13, selectmode="extended")

        #table["columns"] = ("Player", "PTS", "MIN")
        self.table["columns"] = ("Player", "MIN",'FGM','FGA','FTM','FTA', '3PTM', 'REB','AST','STL', 'BLK', 'TO', 'PTS',  'FPTS')

        #MIN,FGM,FGA,FTM,FTA,3PM,REB,AST,STL, BLK, TO, PTS,

        #columns = scraper.getStatsTeamObj(team, 'avg', "name", 'PTS', 'MIN')
        columns = scraper.getStatsTeamObj(team, '2023_total', 'avg', "name",'MIN','FGM','FGA','FTM','FTA', '3PTM', 'REB','AST','STL', 'BLK', 'TO', 'PTS',  'FPTS')#missing 3pm
        

        def createTable(rows1, table):
            table.column('#0', width=0, stretch=NO)
            table.heading('#0', text='', anchor=CENTER)
            #print(len(table["columns"]))
            for ind, i in enumerate(table["columns"]):
                if ind == 0:
                    table.column(i, anchor=CENTER, width=130, minwidth = 50)
                    table.heading(i, text=i, anchor=CENTER)
                else: 
                    table.column(i, anchor=CENTER, width=55, minwidth = 35)
                    table.heading(i, text=i, anchor=CENTER)
                #print(ind)

                
            for inj, j in enumerate(rows1):
                #print(rows1[:][inj])
                table.insert(parent='', index = inj, text ='', values = (rows1[:][inj]))

        #convert columns list to rows
        rows = list(zip(*columns))[::-1]
        #pprint(rows)
        rows = sorted(rows,key=lambda l:l[13], reverse=True)

        createTable(rows, self.table)
        #table.pack(fill = X) 
        self.table.pack(expand = True) 
        self.table.bind("<Double-1>", self.OnDoubleClick)

    def OnDoubleClick(self, event):
        item = self.table.selection()[0]
        playerName = self.table.item(item,"values")[0]
        print("you clicked on", playerName)
        
        new_window = tk.Toplevel(self, width=1600, height=1600)
        new_window.resizable(False, False)
        PlayerPage(new_window, playerName).pack()

class PlayerPage(tk.Frame):
    def __init__(self, parent, playerName):  
        tk.Frame.__init__(self, parent)
        self.configure(background='green')

        #code for scroll:-----------------------
        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)#

        # Create a scrollbar and attach it to the frame
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Attach the scrollbar to the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame to hold the scrollable content
        scrollable_frame = tk.Frame(canvas)

        # Bind the scrollable frame to the scrollbar
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)

        # Set the size of the scrollable region
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        #canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1*(event.delta//120), "units"))
        
        #---------------------------------

        label = tk.Label(scrollable_frame, text=playerName, font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        playerStats = scraper.getAllPlayerStatsByName(playerName, playerDict2023)
        pprint(playerStats)
        for k, v in playerStats.items():
            if k.isnumeric() == False:
                tempLabel = PlayerPageStatRowFrame(scrollable_frame, k, v)
                tempLabel.pack(pady=10,padx=10)

      
     
        #get file path
        imageName = "C:/Users/thoma/OneDrive - Queen's University/Documents/Random Code Folders Crap/Pythion VS Code/Fantasy Scraper Folder/playerImages/"
        imageName += playerName
        imageName += ' Headshot.png'

        #open image
        image = Image.open(imageName)
        #convert to correct type to support transparency
        image = image.convert("RGBA")
        image.mode = "RGBA"
        #create photoimage object
        photoImage = ImageTk.PhotoImage(image)
        panel = Label(self, image=photoImage)
        panel.photo = photoImage
        panel.pack()

class PlayerPageStatRowFrame(tk.Frame):

    def __init__(self, parent, leftCol, rightCol):  
        tk.Frame.__init__(self, parent)
        self.configure(background='purple')
        averageText = tk.Label(self, text=leftCol + ": ", font=LARGE_FONT)
        averageText.pack(side = LEFT)
        averageText2 = tk.Label(self, text=rightCol, font=LARGE_FONT)
        averageText2.pack(side = RIGHT)

class InjuryPage(tk.Frame):

    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)
        
        #Injury page to do:
        #get who is currently injured
        #get all past injury data
        #calculate average length of injury basesd on: age during injury, type of injury

        label = tk.Label(self, text="Injury Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        table_frameL = InjuryTableFrame(self)
        table_frameL.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

class InjuryTableFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        
        #print(team.team_id)
        teamNameLabel = tk.Label(self, text="Injuries", font=LARGE_FONT)
        teamNameLabel.pack(side = "top") 

        table=ttk.Treeview(self, height=25, selectmode="extended")
        table["columns"] = ("Player", "Position",'Date Updated','Injury','Injury Status', 'Fantasy Points')

        rows = InjuryScraper.getCurrentlyInjured()
        for i in rows:
            temp = scraper.getPlayerStatsByName(i[0], playerDict2023, "FPTS")
            if temp == None:
                i.append(0)
            else:
                i.append(temp[0])



        def createTable(rows1, table):
            table.column('#0', width=0, stretch=NO)
            table.heading('#0', text='', anchor=CENTER)
            #print(len(table["columns"]))
            for ind, i in enumerate(table["columns"]):
                if ind == 4 or ind == 0:
                    table.column(i, anchor=CENTER, width=100, minwidth = 40)
                else:
                    table.column(i, anchor=CENTER, width=50, minwidth = 40)

                table.heading(i, text=i, anchor=CENTER)
                #print(ind)

                
            for inj, j in enumerate(rows1):
                #print(rows1[:][inj])
                #print(len(rows1))
                table.insert(parent='', index = inj, text ='', values = (rows1[:][inj]))
         
        rows = sorted(rows,key=lambda l:l[5], reverse=True)
        createTable(rows, table)
        table.pack(fill = BOTH)

class MyTeamPage(tk.Frame):

    def __init__(self, parent, myTeam):  
        tk.Frame.__init__(self, parent)
        #My Team page to Do:
        #add projected points
        #extra stats such as injury percentage, fantasy points, fantasy points per min, 
        #myTeam = team
        if myTeam == None:
            myTeam = scraper.league.teams[0]
        #print(myTeam)
        self.configure(background='blue')

        label = tk.Label(self, text="My Team", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        table_frame = TableFrame(self, myTeam)
        table_frame.pack()

        stats = StatsFrame(self, myTeam)
        stats.pack()

class StatsFrame(tk.Frame):

    def __init__(self, parent, team):  
        tk.Frame.__init__(self, parent)
        self.configure(background='yellow')

        FPTSList = []
        #print(team)
        if team not in scraper.league.teams:
            team = scraper.league.teams[0]

        for i in team.roster:
            temp = scraper.getPlayerStatsByName(i.name, playerDict2023, "FPTS")
            if temp != None:
                FPTSList.append(temp[0])
        
        top10 = heapq.nlargest(10, FPTSList)
        avgFPTS = sum(top10)/len(top10)
        
        col1 = StatColFrame(self, "Top 10 Average FPTS:", avgFPTS)
        col1.pack()

class StatColFrame(tk.Frame):

    def __init__(self, parent, leftCol, rightCol):  
        tk.Frame.__init__(self, parent)
        self.configure(background='purple')

        averageText = tk.Label(self, text=leftCol, font=LARGE_FONT)
        averageText.pack(pady=10,padx=10, side = LEFT)
        averageText2 = tk.Label(self, text=rightCol, font=LARGE_FONT)
        averageText2.pack(pady=10,padx=10, side = RIGHT)
        
class MatchupPage(tk.Frame):

    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)
        
        box = scraper.league.box_scores()

        label = tk.Label(self, text="Week x Matchup", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        table_frameL = MyTeamPage(self, box[3].home_team)
        table_frameL.pack(fill=tk.BOTH, side = tk.LEFT, expand=True)

        #table frame before
        table_frameR = MyTeamPage(self, box[3].away_team)
        table_frameR.pack(fill=tk.BOTH, side = tk.RIGHT, expand=True)

app = FantasyScraperApp()
ani = animation.FuncAnimation(playerGraphFigure, animate, interval=300)
#ani2 = animation.FuncAnimation(teamGraphFigure, animate2, interval=1000)
teamGraphFigure
app.mainloop()