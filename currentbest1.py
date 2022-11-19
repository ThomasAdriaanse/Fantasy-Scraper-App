import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import *
#from ttkwidgets.autocomplete import AutocompleteEntryListbox
from pprint import pprint

from PIL import ImageTk, Image

import urllib
import json

import pandas as pd
import numpy as np

import scraper

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
            xar, yar, namear=scraper.getStatsTeamObj(team, 'avg', xAxis, yAxis, "name")
            a.plot(xar,yar, 'ro')
                

        if playerHighlight[1] != 0 and playerHighlight[2] != 0:
            a.plot(playerHighlight[0], playerHighlight[1], 'ro', color = 'Yellow')
            if showNames == True: 
                a.annotate(playerHighlight[2], (playerHighlight[0], playerHighlight[1]))
            #print(playerHighlight[2], playerHighlight[0], playerHighlight[1])
        elif playerHighlight[0]!=0:
            for team in scraper.league.teams:
                if playerHighlight[0] == team:
                    xar, yar, namear=scraper.getStatsTeamObj(team, 'avg', xAxis, yAxis, "name")
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
        for F in (StartPage, GroupAnalysisPage, StatsPage, InjuryPage, MyTeamPage):
            
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
        
        #self.configure(background='green')
        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(GroupAnalysisPage))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                            command=quit)
        button2.pack()

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

class InputFrame(ttk.Frame):
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
        options = ['MIN','FGM','FGA','FTM','FTA','REB','AST','STL', 'BLK', 'TO', 'PTS']#3PM should be here but does not work for some reason
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

class GraphFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # setup the grid layout manager

        canvas = FigureCanvasTkAgg(playerGraphFigure, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

class StatsPage(tk.Frame):

    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Stats Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        table_frameL = TableFrame(self, scraper.league.teams[4])
        #button_frame.grid(column=1, row=0)
        table_frameL.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        table_frameR = TableFrame(self, scraper.league.teams[5])
        #button_frame.grid(column=1, row=0)
        table_frameR.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

class TableFrame(ttk.Frame):
    def __init__(self, container, team):
        super().__init__(container)
        

        #print(team.team_id)
        teamNameLabel = tk.Label(self, text=team.team_name, font=LARGE_FONT)
        teamNameLabel.pack(side = "top") 

        table=ttk.Treeview(self)

        #table["columns"] = ("Player", "PTS", "MIN")
        table["columns"] = ("Player", "MIN",'FGM','FGA','FTM','FTA','REB','AST','STL', 'BLK', 'TO', 'PTS')

        #MIN,FGM,FGA,FTM,FTA,3PM,REB,AST,STL, BLK, TO, PTS,

        #columns = scraper.getStatsTeamObj(team, 'avg', "name", 'PTS', 'MIN')
        columns = scraper.getStatsTeamObj(team, 'avg', "name",'MIN','FGM','FGA','FTM','FTA','REB','AST','STL', 'BLK', 'TO', 'PTS')#missing 3pm
        """ 
        table.column('#0', width=0, stretch=NO)
        table.column('Player', anchor=CENTER, width=100)
        table.column('PTS', anchor=CENTER, width=100)
        table.column('MIN', anchor=CENTER, width=100)

        table.heading('#0', text='', anchor=CENTER)
        table.heading('Player', text='Player', anchor=CENTER)
        table.heading('PTS', text='PTS', anchor=CENTER)
        table.heading('MIN', text='MIN', anchor=CENTER)

        for i in range(len(team.roster)):
            table.insert(parent='', index=i, iid=i, text='', values=(columns[0][i], columns[1][i], columns[2][i]))

        """
        

        def createTable(rows1, table):
            table.column('#0', width=0, stretch=NO)
            table.heading('#0', text='', anchor=CENTER)
            #print(len(table["columns"]))
            for ind, i in enumerate(table["columns"]):
               
                table.column(i, anchor=CENTER, width=50, minwidth = 40)
                table.heading(i, text=i, anchor=CENTER)
                #print(ind)

                
            for inj, j in enumerate(rows1):
                table.insert(parent='', index = inj, text ='', values = (rows1[:][inj]))
         

        #for i in range(scraper.getMaxRosterSize()):
            #row=DataRow(self)
            #image1 = ImageTk.PhotoImage(Image.open(folderLocation+"tableRowImage.png"))
            #label1 = tk.Label(self, image =image1)
            #label1.image = image1
            #row.pack(side = "top", padx=50)

        #convert columns list to rows
        rows = list(zip(*columns))[::-1]
        #pprint(rows)
        createTable(rows, table)
        table.pack(fill = X)
        
class DataRow(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

       
        #row.image = rowOutline
        #label1.image = rowOutline
        #label1.grid(column=0, row=rowNum, padx=100)
        rowOutline = ImageTk.PhotoImage(Image.open(folderLocation+"tableRowImage2.png"))
        row = tk.Label(self, image =rowOutline)
        row.pack(side = "top", fill=tk.x)

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, text=col, command=lambda _col=col: \
                 treeview_sort_column(tv, _col, not reverse))
  
class InjuryPage(tk.Frame):

    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)
        
        
        #Injury page to do:
        #get who is currehntly injured
        #get all past injury data
        #calculate average length of injury basesd on: age during injury, type of injury
        label = tk.Label(self, text="Injury Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

class MyTeamPage(tk.Frame):

    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="My Team", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        table_frameL = TableFrame(self, scraper.league.teams[0])
        #button_frame.grid(column=1, row=0)
        table_frameL.pack(fill=tk.BOTH, expand=True)

        



app = FantasyScraperApp()
ani = animation.FuncAnimation(playerGraphFigure, animate, interval=300)
#ani2 = animation.FuncAnimation(teamGraphFigure, animate2, interval=1000)
teamGraphFigure
app.mainloop()