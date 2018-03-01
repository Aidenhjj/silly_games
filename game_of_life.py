# Problem Set 6:
# Visualization code for simulated robots.
#
# See the problem set for instructions on how to use this code.

import math
import time
import string
import random

from Tkinter import *

class GameOfLife(object):
    """
    Class that implements game of life
    """

    
    # -----------------------------------
    # Helper code
    # (you don't need to understand this helper code)
    def load_words(self):
        """
        Returns a list of valid words. Words are strings of lowercase letters.
        
        Depending on the size of the word list, this function may
        take a while to finish.
        """
        print "Loading init file..."
        # inFile: file
        inFile = open(self.filename, 'r', 0)
        # line: list
        lines = inFile.readlines()
        self.width = len(lines[0].split(','))
        self.height = len(lines)
        init = [[0 for x in range(self.height)] for y in range(self.width)]
        
        for j in range(self.height):
            line = lines[j].split(',')
            for i in range(self.width):
                if int(line[i]) == 0:
                    init[i][j] = False
                    print "O",
                else:
                    init[i][j] = True
                    print "X",
#                print line[j],
            print ""
        print 'loaded'
        return init
    
    def __init__(self, filename = "init.dat"):
        self.filename = filename
        self.gameState = self.load_words()
#        print self.gameState
    
    def inGrid(self, i, j):
        return (0 <= i <= self.width - 1) and (0 <= j <= self.height - 1)
        
    def playgame(self, goround = 1):
        #1) display start conditions
        #2) run 1st iteration of rules
        #3) display conditions
        #4) rinse and repeat
        if goround == 1:
            self.anim = GameVisualization(self, self.width, self.height, self.gameState)
        
#        if self.anim.getRunning():
        self.gameState = self.gameRules()
#            print goround
        self.anim.update()
#        else:
#            while not self.anim.getRunning():
#            time.sleep(0.5)
        
        self.playgame(goround + 1)
#        self.anim.done()
        
        #    Any live cell with fewer than two live neighbours dies, as if caused by under-population.
        #    Any live cell with two or three live neighbours lives on to the next generation.
        #    Any live cell with more than three live neighbours dies, as if by over-population.
        #    Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        
    def setGameState(self, newState):
        self.gameState = newState
    
    def getGameState(self):
       return self.gameState
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def oneStep(self):
        self.gameState = self.gameRules()
                
    def isOn(self, i, j):
        return self.gameState[i][j]
        
    def gameRules(self):
        # returns newGameState
        neighbours = [(0,1), (1,0), (1,1), (-1,1), (1,-1), (-1,-1), (0,-1), (-1,0)]
        liveN = 0
        newGameState = [[False for x in range(self.height)] for y in range(self.width)]
        for j in range(self.height):
            for i in range(self.width):
                for x, y in neighbours:
                    if self.inGrid(i + x, 0):
                        a = i + x
                    elif (i + x) < 0:
                        a = self.width - 1
                    else:
                        a = 0
                    
                    if self.inGrid(0, j + y):
                        b = j + y
                    elif (j + y) < 0:
                        b = self.height - 1
                    else:
                        b = 0
                    
#                    if i == 3 and j == 3:
#                        print 'stop here'
#                        print '-------------'
#                        print self.width, self.height
#                        print i, j
#                        print x, y
#                        print a, b, self.isOn(a, b)
#                        print '-------------'
                    if self.isOn(a, b):
                        liveN += 1        
        
#                print i, j, liveN
#                try:
#                    self.isOn(i, j)
#                except:
#                    print "here!"
                if self.isOn(i, j):
                    if (liveN < 2) or (liveN > 3):
                        newGameState[i][j] = False
                    else:
                        newGameState[i][j] = True
                else:
                    if liveN == 3:
                        newGameState[i][j] = True
                liveN = 0
        
        return newGameState

#def key(event):
#    print "pressed", repr(event.char)



class GameVisualization(object):
    
    
    def __init__(self, gameInstance, width, height, init, delay = 0.2):
        """
        Class for visualising Game of Life.
        width -> integer
        height -> integer
        init -> 2D 'array' in nested lists (initial conditions)
        """
        # Number of seconds to pause after each frame
        self.delay = delay
        
        self.running = True

        self.max_dim = max(width, height)
        self.width = width
        self.height = height
        self.init = init
#        print init
        self.gameInstance = gameInstance

        # Initialize a drawing surface
        self.master = Tk()
        self.frame = Frame(self.master, bg='grey', width=400, height=40)
        self.frame.pack(fill='x')
        button1 = Button(self.frame, text='Stop', command = self.cmdStop)
        button1.pack(side='left', padx=10)
        button2 = Button(self.frame, text='Start', command = self.cmdStart)
        button2.pack(side='left', padx=10)
        self.w = Canvas(self.master, width=500, height=500)
#        self.w.bind = Button(self, text = "Quit", command = self.quit("<Key>", key)
        self.w.bind("<Button-1>", self.callback)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(self.width, self.height)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")

        # Initialise board
        self.tiles = {}
        for j in range(height):
            for i in range(width):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                if self.init[i][j]:
#                    print "X",
                    self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, fill = "black")
#                else:
#                    print "O",
#            print ""

        # Draw gridlines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.w.create_line(x1, y1, x2, y2)

        # Draw some status text
#        self.robots = None
#        self.text = self.w.create_text(25, 0, anchor=NW,
#                                       text=self._status_string(0, 0))
        self.time = 0
        self.master.update()
    
#    def 
        
    def getRunning(self):
        return self.running
    
    def setRunning(self, onoff):
        self.running = onoff
        
    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        mainloop()    
    
    def callback(self):
        print "clicked at", event.x, event.y
        
    def cmdStop(self):
        print "clicked at stop"
#        mainloop()
        self.running = False
        
    def cmdStart(self, event):
        print "clicked at start"
        self.running = True
        
    def _on_off(self, i, j, switch):
        """
        switches the square on or off
        """
#        print self.tiles
        x1, y1 = self._map_coords(i, j)
        x2, y2 = self._map_coords(i + 1, j + 1)
        if switch:
            self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, fill = "black")
        else:
            try:
#                self.w.delete(self.tiles[(i, j)])
#                print 'deleted'
                self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, fill = "white")
            except KeyError:
#                self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, fill = "white")
                return
#    def _status_string(self, time, num_clean_tiles):
#        "Returns an appropriate status string to print."
#        percent_clean = 100 * num_clean_tiles / (self.width * self.height)
#        return "Time: %04d; %d tiles (%d%%) cleaned" % \
#            (time, num_clean_tiles, percent_clean)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

#    def _draw_robot(self, position, direction):
#        "Returns a polygon representing a robot with the specified parameters."
#        x, y = position.getX(), position.getY()
#        d1 = direction + 165
#        d2 = direction - 165
#        x1, y1 = self._map_coords(x, y)
#        x2, y2 = self._map_coords(x + 0.6 * math.sin(math.radians(d1)),
#                                  y + 0.6 * math.cos(math.radians(d1)))
#        x3, y3 = self._map_coords(x + 0.6 * math.sin(math.radians(d2)),
#                                  y + 0.6 * math.cos(math.radians(d2)))
#        return self.w.create_polygon([x1, y1, x2, y2, x3, y3], fill="red")

    def update(self):
        "Redraws the visualization with the specified room and robot state."
#        # Removes a gray square for any tiles have been cleandela
        
        if self.running:
            self.w.delete("all")
            # Draw a backing and lines
            x1, y1 = self._map_coords(0, 0)
            x2, y2 = self._map_coords(self.width, self.height)
            self.w.create_rectangle(x1, y1, x2, y2, fill = "white")
            
            for j in range(self.height):
                for i in range(self.width):
                    self._on_off(i, j, self.gameInstance.isOn(i, j))
            
            self.master.update()
            time.sleep(self.delay)
        else:
            time.sleep(.1)
#        # Delete all existing robots.
#        if self.robots:
#            for robot in self.robots:
#                self.w.delete(robot)
#                self.master.update_idletasks()
#        # Draw new robots
#        self.robots = []
#        for robot in robots:
#            pos = robot.getRobotPosition()
#            x, y = pos.getX(), pos.getY()
#            x1, y1 = self._map_coords(x - 0.08, y - 0.08)
#            x2, y2 = self._map_coords(x + 0.08, y + 0.08)
#            self.robots.append(self.w.create_oval(x1, y1, x2, y2,
#                                                  fill = "black"))
#            self.robots.append(
#                self._draw_robot(robot.getRobotPosition(), robot.getRobotDirection()))
#        # Update text
#        self.w.delete(self.text)
#        self.time += 1
#        self.text = self.w.create_text(
#            25, 0, anchor=NW,
#            text=self._status_string(self.time, room.getNumCleanedTiles()))
        
def callback(event):
    print "clicked at", event.x, event.y
        
#class GameCreation(object):
#    
#    
#    def __init__(self, width, height, delay = 0.2):
#        """
#        Class for visualising Game of Life.
#        width -> integer
#        height -> integer
#        init -> 2D 'array' in nested lists (initial conditions)
#        """
#        # Number of seconds to pause after each frame
#        self.delay = delay
#
#        self.max_dim = max(width, height)
#        self.width = width
#        self.height = height
#
#        # Initialize a drawing surface
#        self.master = Tk()
#        self.frame = Frame(self.master, bg='grey', width=500, height=40)
#        self.frame.pack(fill='x')
#        button1 = Button(self.frame, text='Save', command = self.cmdSave)
#        button1.pack(side='left', padx=10)
#        button2 = Button(self.frame, text='Quit', command = self.cmdQuit)
#        button2.pack(side='left', padx=10)
#        self.w = Canvas(self.master, width=500, height=500)
##        self.w.bind = Button(self, text = "Quit", command = self.quit("<Key>", key)
#        self.w.bind("<Button-1>", callback(event))
#        self.w.pack()
#        self.master.update()
#
#        # Draw a backing and lines
#        x1, y1 = self._map_coords(0, 0)
#        x2, y2 = self._map_coords(self.width, self.height)
#        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")
#
#        # Initialise board
#        self.tiles = {}
#        for j in range(height):
#            for i in range(width):
#                x1, y1 = self._map_coords(i, j)
#                x2, y2 = self._map_coords(i + 1, j + 1)
##                if self.init[i][j]:
#                self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, fill = "black")
#
#        # Draw gridlines
#        for i in range(width + 1):
#            x1, y1 = self._map_coords(i, 0)
#            x2, y2 = self._map_coords(i, height)
#            self.w.create_line(x1, y1, x2, y2)
#        for i in range(height + 1):
#            x1, y1 = self._map_coords(0, i)
#            x2, y2 = self._map_coords(width, i)
#            self.w.create_line(x1, y1, x2, y2)
#
#        self.time = 0
#        self.master.update()
#        
#    def done(self):
#        "Indicate that the animation is done so that we allow the user to close the window."
#        mainloop()    
#        
##    def coord(self, x, y)
#    
#
#        
#    def cmdSave(self):
#        print "clicked at save"
##        mainloop()
#        self.running = False
#        
#    def cmdQuit(self, event):
#        print "clicked at start"
#        mainloop()
#        
#    def _on_off(self, i, j, switch):
#        """
#        switches the square on or off
#        """
##        print self.tiles
#        x1, y1 = self._map_coords(i, j)
#        x2, y2 = self._map_coords(i + 1, j + 1)
#        if switch:
#            self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, fill = "black")
#        else:
#            self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2, fill = "white")
#
#    def _map_coords(self, x, y):
#        "Maps grid positions to window positions (in pixels)."
#        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
#                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))
#
#    def update(self):
#        "Redraws the visualization with the specified room and robot state."
##        # Removes a gray square for any tiles have been cleandela
#        
#        if self.running:
#            self.w.delete("all")
#            # Draw a backing and lines
#            x1, y1 = self._map_coords(0, 0)
#            x2, y2 = self._map_coords(self.width, self.height)
#            self.w.create_rectangle(x1, y1, x2, y2, fill = "white")
#            
#            for j in range(self.height):
#                for i in range(self.width):
#                    self._on_off(i, j, self.gameInstance.isOn(i, j))
#            
#            self.master.update()
#            time.sleep(self.delay)
#        else:
#            time.sleep(.1)
#
##game = GameOfLife("test.dat")
##try:
##    game.playgame()
##except KeyboardInterrupt:
##    game.anim.done()
#
##def playGameVis(game, goround = 1, anim = GameVisualization(game, game.getWidth(), game.getHeight(), game.getGameState())):
##    if goround == 1:
##        self.anim = GameVisualization(game, game.getWidth(), game.getHeight(), game.getGameState())
##    
##    game.setGameState(game.gameRules())
##    self.anim.update()

def dispGame(game):
    for j in range(len(game.gameState)):
        for i in range(len(game.gameState[0])):
            if game.gameState[i][j]:
                print "X",
            else:
                print"O",
        print ""
    print "-------------"

# testGame(GameOfLife):
game = GameOfLife("gun.dat")
#print game.width
#print game.height
#print game.inGrid(1,1)
#print game.inGrid(0,0)
#print game.inGrid(26,26)

#dispGame(game)
#game.oneStep()
game.playgame()
#dispGame(game)
#game.oneStep()
#dispGame(game)
#game.oneStep()
#dispGame(game)
