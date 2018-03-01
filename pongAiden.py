# -*- coding: utf-8 -*-
"""
PONG GAME
"""

import time
import Tkinter as tk
import random

def sign(a):
    #returns sign of a
    return (a>0) - (a<0)

class Equipment(object):
    """
    Base class for Ball and Paddle
    """
    def __init__(self, pos, vel, size, side = 0):
        self.pos = pos
        self.vel = vel
        self.size = size
        self.side = side
    
    def getPos(self):
        return self.pos
        
    def getSize(self):
        return self.size
    
    def getVel(self):
        return self.vel
    
    def updatePos(self, step):
        self.pos.newPos(self.vel, step)
    
    def getEdge(self):
        raise NotImplementedError
        
    def onCourt(self, Court):
        CourtSize = Court.getBounds()
        edge = self.getEdge()
        if min(edge[1]) <= min(CourtSize[1]):
            return [False, 'y-']
        elif max(edge[1]) >= max(CourtSize[1]):
            return [False, 'y+']
        elif min(edge[0]) <= min(CourtSize[0]):
            return [False, 'x1']
        elif max(edge[0]) >= max(CourtSize[0]):
            return [False, 'x0']
        else:
            return [True, '--']
        
    def typ(self):
        if type(self) == Ball:
            return 'Ball'
        elif type(self) == Paddle:
            return 'Paddle'
        return False
    

class Position(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def newPos(self, vel, step):
        self.x = self.x + (vel.getVelX() * step)
        self.y = self.y + (vel.getVelY() * step)
    
    def __repr__(self):
        return str([self.x, self.y])
        
        
class Velocity(object):
    
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy
    
    def getVelX(self):
        return self.vx
    
    def getVelY(self):
        return self.vy
    
    def setVel(self, vx, vy):
        self.vx = vx
        self.vy = vy
        
    def __repr__(self):
        return str([self.vx, self.vy])


class Paddle(Equipment):
    """
    Paddle is the Paddle
    """
    
    def getEdge(self):
        # returns coordinates that define Paddle
        x = self.pos.getX()
        y = self.pos.getY()
        return [[x - 20, x + 20], [y - self.size, y + self.size]]
    
    def getSide(self):
        # returns whether paddle is on left or right
        return self.side
        
    def up(self, speed, Court):
        if self.onCourt(Court)[0]:
            self.vel.setVel(0, speed)
        elif (self.onCourt(Court)[1] == 'y+'):
            self.vel.setVel(0, 0)
        elif (self.onCourt(Court)[1] == 'y-'):
            self.vel.setVel(0, speed)
        else:
            raise ValueError('oops Paddle.up()')
            
    
    def down(self, speed, Court):
        if self.onCourt(Court)[0]:
            self.vel.setVel(0, -speed)
        elif (self.onCourt(Court)[1] == 'y-'):
            self.vel.setVel(0, 0)
        elif (self.onCourt(Court)[1] == 'y+'):
            self.vel.setVel(0, -speed)
        else:
            raise ValueError('oops Paddle.down()')
        
    def rest(self):
        self.vel.setVel(0, 0)
        
    def inPaddle(self, x, y):
        edge = self.getEdge()
        
        if (edge[1][0] <= y <= edge[1][1]) and (edge[0][0] <= x <= edge[0][1]):
            return [True, 'x']
        else:
            return [False, '']
    
class Ball(Equipment):
    
    def getEdge(self):
        x = self.pos.getX()
        y = self.pos.getY()
        return [[x - self.size, x + self.size], [y - self.size, y + self.size]]
            
    def reflectX(self):
        self.vel.setVel(-self.vel.getVelX(), self.vel.getVelY())
    
    def reflectY(self):
        self.vel.setVel(self.vel.getVelX(), -self.vel.getVelY())

    def genBall(self, x, y):
        self.pos = Position(x, y)
        self.vel = Velocity((int(10 * random.random()) + 5) * sign(random.random() - 0.5), (int(10 * random.random()) + 5) * sign(random.random() - 0.5))
    
    def hit(self, Court):
        hitCourt = self.onCourt(Court)
        if not hitCourt[0]:
            if hitCourt[1][0] == 'x':
                Court.updateScore(int(hitCourt[1][1]))
                self.genBall(500, 500)
                time.sleep(1)
                return True
            elif hitCourt[1][0] == 'y':
                self.reflectY()
                return True
        edge = self.getEdge()
        for Paddle in Court.Paddles:
            for x in edge[0]:
                for y in edge[1]:
                    hitPaddle = Paddle.inPaddle(x, y)
                    if hitPaddle[0]:
                        if hitPaddle[1] == 'x':
                            self.reflectX()
                            return True
                        elif hitPaddle[1] == 'y':
                            self.reflectY()
                            return True
                        else:
                            raise ValueError('something wrong with hitPaddle part of hit()')
        return False

class RoomBall(Ball):
    """
    Ordinary ball that reflects off surfaces as expected
    """
    
    def hit(self, Court):
        hitCourt = self.onCourt(Court)
        if not hitCourt[0]:
            if hitCourt[1][0] == 'x':
                self.reflectX()
                return True
            elif hitCourt[1][0] == 'y':
                self.reflectY()
                return True
        return False
        
class RandBall(Ball):
    """
    Ball that reflects off surfaces as expected with randomness in the direction
    of reflaction (max 10% random deflection)
    """
    def reflectX(self):
        dx = (self.vel.getVelX() * 0.2) * (random.random() - 0.5)
        dy = (self.vel.getVelY() * 0.2) * (random.random() - 0.5)
        self.vel.setVel(-self.vel.getVelX() + dx, self.vel.getVelY() + dy)
    
    def reflectY(self):
        dx = (self.vel.getVelX() * 0.2) * (random.random() - 0.5)
        dy = (self.vel.getVelY() * 0.2) * (random.random() - 0.5)
        self.vel.setVel(self.vel.getVelX() + dx, -self.vel.getVelY() + dy)
            

class Court(object):
    """
    Court contains all other game objects
    note - ony currently works with 2 Paddles
    """
    
    def __init__(self, height, width, Balls, Paddles, win = 10):
                
        self.Balls = Balls
        self.Paddles = Paddles
        self.width = width
        self.height = height
        self.score = [0, 0]
        self.win = win

    def getBounds(self):
        return [[0, self.width], [0, self.height]]
        
    def updateScore(self, winner):
        # winner is 0 or 1
        self.score[winner] += 1
    
    def getScore(self):
        return self.score
        
    def getBalls(self):
        return self.Balls
        
    def getPaddles(self):
        return self.Paddles
    
    def getPaddleSide(self, side):
        for pad in self.Paddles:
            if pad.getSide() == side:
                return pad
        return None
        
    def getWin(self):
        if self.score[0] > self.win:
            return [True, 0]
        elif self.score[1] > self.win:
            return [True, 1]
        else:
            return [False, None]
    
    def updateCourt(self, stepSize):
        equip = self.Balls + self.Paddles
        for eq in equip:
            eq.updatePos(stepSize)
        

class Widget(tk.Frame):
    """
    Main app UI class
    """
    def __init__(self, parent, Court, gameSpeed, sensitivity = 20):
        self.Court = Court

        self.width = Court.getBounds()[0][1]
        self.height = Court.getBounds()[1][1]
        self.running = False
        self.gameSpeed = gameSpeed
        self.sensitivity = sensitivity
        
        self.max_dim = max(self.width, self.height)
        
        self.rightPaddle = Court.getPaddleSide(1)
        self.leftPaddle = Court.getPaddleSide(0)
        
        self.t = 0
        
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.start_button = tk.Button(self, text="start", command=self.on_start)
        self.stop_button = tk.Button(self, text="stop", command=self.on_stop)
        
        self.bind("<KeyPress-Up>", self.pressupR)
        self.bind("<KeyRelease-Up>", self.relupR)
        
        self.bind("<KeyPress-Down>", self.pressdownR)
        self.bind("<KeyRelease-Down>", self.reldownR)
        
        self.bind("<KeyPress-w>", self.pressupL)
        self.bind("<KeyRelease-w>", self.relupL)
        
        self.bind("<KeyPress-s>", self.pressdownL)
        self.bind("<KeyRelease-s>", self.reldownL)

        self.start_button.pack(side='top', padx=10)
        self.stop_button.pack(side='top', padx=10)
        self.canvas.pack()
        
        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(self.width, self.height)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill = "white")
        
        # text
        self.textScore = self.canvas.create_text(40, 0, text='score: ')
        
        # Initialise board
        self.contents = []
        self.playGame()
        self.focus_set()

        # call on_stop to initialize the state of the buttons
        self.on_stop()
        self.draw_one_frame()
    
    def playGame(self):
        """
        Main game logic
        """
        self.canvas.delete("all")
        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(self.width, self.height)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill = "white")
        
        # set textScore - displayed by tKinter
        self.textScore = self.canvas.create_text(40, 0, text='score: ')
        
        # PRINT RESULTS
        equipList = self.Court.getBalls() + self.Court.getPaddles()
        for equip in equipList:
            edge = equip.getEdge()
            i1 = edge[0][0]
            i2 = edge[0][1]
            j1 = edge[1][0]
            j2 = edge[1][1]
            x1, y1 = self._map_coords(i1, j1)
            x2, y2 = self._map_coords(i2, j2)
            if equip.typ() == 'Ball' or type(equip) == RoomBall or type(equip) == RandBall:
                self.contents.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill = "black"))
            elif equip.typ() == 'Paddle':
                self.contents.append(self.canvas.create_rectangle(x1, y1, x2, y2, fill = "green"))
        
        self.showScore()
        for Ball in self.Court.getBalls():
            Ball.hit(self.Court)
            
        self.Court.updateCourt(1)
    
    def showScore(self):
        self.canvas.delete(self.textScore)
        score = str(self.Court.getScore())
        self.textScore = self.canvas.create_text(40, 10, text=score)
        
    def pressupR(self, event):
        self.rightPaddle.up(self.sensitivity, self.Court)
        
    def relupR(self, event):
        self.rightPaddle.rest()
        
    def pressdownR(self, event):
        self.rightPaddle.down(self.sensitivity, self.Court)
        
    def reldownR(self, event):
        self.rightPaddle.rest()
        
    def pressupL(self, event):
        self.leftPaddle.up(self.sensitivity, self.Court)
        
    def relupL(self, event):
        self.leftPaddle.rest()
        
    def pressdownL(self, event):
        self.leftPaddle.down(self.sensitivity, self.Court)
        
    def reldownL(self, event):
        self.leftPaddle.rest()
    
    def on_start(self):
        """Start the animation"""
        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.draw_one_frame()

    def on_stop(self):
        """Stop the animation"""
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.running = False

    def draw_one_frame(self):
        """Main control function for game"""
        if self.running:
            self.after(self.gameSpeed, self.draw_one_frame)
            self.playGame()
            
    def _map_coords(self, x, y):
        "Maps grid Positions to window Positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))
    
    def _map_pixel(self, xp, yp):
        "opposite of _map_coords"
        return int(((float(xp - 250)/450) * 8) + 4), int(-((float(yp - 250)/450) * 8) + 4)

if __name__ == "__main__":
    # Initialise Tk
    root = tk.Tk()
    
    blls = [RandBall(Position(500, 500), Velocity(10, 5), 10)]
    pddls = [Paddle(Position(50, 500), Velocity(0, 0), 100, 0), Paddle(Position(950, 500), Velocity(0, 0), 100, 1)]
    crt = Court(1000, 1000, blls, pddls)
    
    # start main game Object and run mainloop:
    Widget(root, crt, 10).pack(fill="both", expand=True)
    root.mainloop()