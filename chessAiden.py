"""
Chess programme
"""
import Tkinter as tk
import time
import copy
import pickle

class track(object):
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C
    def retX(self, y):
        if self.A == 0:
            return y
        else:
            return -(self.B*y + self.C)/self.A
        
    def retY(self, x):
        if self.B == 0:
            return x
        else:
            return -(self.A*x + self.C)/self.B
        
    @staticmethod
    def twoPoints(pos1, pos2):
        [a, b] = pos1 - pos2
        if a == 0:
            return track(1, 0, -pos1.getX())
        else:
            m = b/a
            return track(-m, 1, (m*pos1.getX() - pos1.getY()))
            
    
    
class board(object):
    """
    Defines a board as a set of initial conditions
    __init__ should take in optional argument which is a list
    of pieces (also objects, with square location programmed in)
    """
    def __init__(self, pieces):
        self.livePieces = pieces
        self.deadPieces = []
        self.scrapPieces = []
        self.boardSaves = []
        self.updateBoardSave()
    
    def rePosBoard(self, pcs):
        # cycle through pcs and set the piece positions of board pieces
        tempLivePieces = []
        tempDeadPieces = []
        currentPieces = self.livePieces + self.deadPieces
        for oldPc in currentPieces:
            for pc in pcs[0]: #cycle through live pcs
                if pc.ID == oldPc.ID:
                    oldPc.setPos(pc.getPos())
                    tempLivePieces.append(oldPc)
            for pc in pcs[1]: #cycle through dead pcs
                if pc.ID == oldPc.ID:
                    oldPc.setPos(pc.getPos())
                    tempDeadPieces.append(oldPc)
        self.livePieces = tempLivePieces
        self.deadPieces = tempDeadPieces
        # check result
        return (len(self.livePieces) + len(self.deadPieces)) == 32
                        
                
                        
        
    def undoChange(self):
#        self.livePieces = self.boardSaves[-1][0]
#        self.deadPieces = self.boardSaves[-1][1]
        self.rePosBoard(self.boardSaves[-1])
        
    def goToTurn(self, turn):
        # returns the game state to that at turn
        maxTurn = len(self.boardSaves)
#        print 'TURN, MAXTURN', turn, maxTurn
#        self.livePieces = self.boardSaves[turn - maxTurn][0]
#        self.deadPieces = self.boardSaves[turn - maxTurn][1]
        print self.rePosBoard(self.boardSaves[turn - maxTurn])
    
    def truncateBoardSaves(self, size):
        # splits the self.boardSaves variable - avoiding problems with playing
        # after navigating game
        self.boardSaves = self.boardSaves[:size+1]
        
    def getBoardSaveForm(self):
        # returns a savable form of board
        tempSaveBoard = []
        tempSaveBoard.append(copy.deepcopy(self.livePieces))
        tempSaveBoard.append(copy.deepcopy(self.deadPieces))
        return tempSaveBoard
        
    def saveBoard(self, turn, filename = 'savedBoard.dat'):
        # Saving the objects:
        self.updateBoardSave()
        with open(filename, 'w') as f:
            pickle.dump([self.boardSaves, turn], f)
    
    def loadBoard(self, filename):
        # sets the pieces according to filename
        with open(filename) as f:
            boardSaved, turn = pickle.load(f)
        self.livePieces = boardSaved[-1][0]
        self.deadPieces = boardSaved[-1][1]
        return turn
            
    def updateBoardSave(self):
        self.boardSaves.append(self.getBoardSaveForm())

        
    def getLivePieces(self):
        return self.livePieces
    
    def getDeadPieces(self):
        return self.deadPieces
    
    def getSideDead(self, side):
        # returns [n, score, valid], where n is the number of dead
        # pieces, and score is the sides score and valid is test of game
        scoreDict = {'pawn':1, 'knight':3, 'bishop':3, 'castle':6, 'queen':9}
        n_dead = 0
        n_live = 0
        score = 0
        typDeadPieces = []
        for pc in self.deadPieces:
            if pc.getSide() == side:
                n_dead += 1
                score = score + scoreDict[pc.typ()]
                typDeadPieces.append(pc.typ())
        for pc in self.livePieces:
            if pc.getSide() == side:
                n_live += 1
        
        return [n_dead, score, n_live + n_dead == 16, typDeadPieces]
    
    def addPiece(self, piece):
        self.livePieces.append(piece)
        
    def takePiece(self, piece):
        tempLivePieces = []
        for i in range(len(self.livePieces)):
            if self.livePieces[i] == piece:
                self.deadPieces.append(self.livePieces[i])
            else:
                tempLivePieces.append(self.livePieces[i])
        self.livePieces = tempLivePieces
        
    def scrapPiece(self, piece):
        tempLivePieces = []
        for i in range(len(self.livePieces)):
            if self.livePieces[i] == piece:
                self.scrapPieces.append(self.livePieces[i])
            else:
                tempLivePieces.append(self.livePieces[i])
        self.livePieces = tempLivePieces
    
    def selectPiece(self, x, y):
        # returns piece in board.livePieces at pos x, y
        for pc in self.livePieces:
            if (pc.getPos().getX() == x) and (pc.getPos().getY() == y):
                return pc
        return None
    
    def isPiece(self, x, y):
        for pc in self.livePieces:
            if (pc.getPos().getX() == x) and (pc.getPos().getY() == y):
                return True
        return False
    
    def inCheck(self):
        """
        runs through all pieces in board to determine check and for who
        """
#        print 'Now here'
        for pc in self.livePieces:
            takes = pc.allTakes(self)
#            print pc.typ(), pc.getSide(), takes
            for i in takes:
                if i.typ() == 'king':
#                    print 'in Check!!'
                    return [True, i.getSide()]
#                else:
#                    return [False, 0]
        return [False, 0]
    
    def inCheckMate(self, side):
        # checks to see if Check Mate for one side
        simBoard = copy.deepcopy(self)
        check = simBoard.inCheck()
        if (check[0]) and (check[1] == side):
            # loop through all pieces on side and move them to all legal positions
            for pc in simBoard.livePieces:
                # check if piece is black or white
                if pc.getSide() == side:
#                    print 'side ', pc.getSide()
#                    print 'pos ', pc.getPos()
#                    print 'type ', pc.typ()
                    mvDict = pc.allMoves(simBoard)
                    # simulate each move
                    for pos in mvDict:
#                        simBoard.updateBoardSave()
#                        print 'new pos ', pos
                        if pc.movePiece(pos, simBoard):
                            if not simBoard.inCheck()[0]:
                                return False
#                            simBoard.undoChange()
            return True
        else:
            return False
          
    def inStaleMate(self, side):
        # checks to see if Check Mate for one side
        simBoard = copy.deepcopy(self)
#        check = simBoard.inCheck()
            # loop through all pieces on side and move them to all legal positions
        for pc in simBoard.livePieces:
            # check if piece is black or white
            if pc.getSide() == side:
#                    print 'side ', pc.getSide()
#                    print 'pos ', pc.getPos()
#                    print 'type ', pc.typ()
                mvDict = pc.allMoves(simBoard)
                # simulate each move
                for pos in mvDict:
#                    simBoard.updateBoardSave()
#                        print 'new pos ', pos
                        if pc.movePiece(pos, simBoard):
                            if not simBoard.inCheck()[0]:
                                return False
#                            simBoard.undoChange()
        return True
        
    def castling(self, side, castle, king):
        # returns False if we are castling and unsuccessful
        # implements a castling rule:
        # - must not be in check
        # - must have free track between king and castle
        # - king must not pass through check
        if castle == None:
            return True
        elif not king.typ() == 'king':
            return True
#        elif self.inCheck()[1] == side: # moved into check
#            return False
        else:
            simBoard = copy.deepcopy(self)
            x = castle.getPos().getX()
            y = castle.getPos().getY()
            
            if x == 0:
                x = 3
                x2 = 1
                xTest = 1
            elif x == 7:
                x = 5
                x2 = None
                xTest = -1
            else:
                raise ValueError('something wrong with castling')
            
            #check if king is in check anywhere along path (already checked final destination p0)
            p0 = square(king.getPos().getX(), king.getPos().getY())
            p1 = p0.add(square(xTest, 0))
            p2 = p1.add(square(xTest, 0))
            
            simKing = simBoard.selectPiece(p0.getX(), p0.getY())
            simKing.setPos(p1)
            if simBoard.inCheck()[1] == side: # moved into check
                return False
            simKing.setPos(p2)
            if simBoard.inCheck()[1] == side: # moved into check
                return False
            # check if castle neighbour square is occupied (not checked by freeTrack for king)
            if (x2 == 1) and (self.isPiece(x2, y)):
                return False
            else: # success condition
                castle.setPos(square(x, y))
                return True
                
    
#    for pc in self.board.getLivePieces():
##                print pc
##                print board
#        out = pc.allTakes(self.board)
#        for i in out:
##                    print 'i, iSide, iPos, pc, pcSide, pcPos', i.typ(), i.getSide(), i.getPos(), pc.typ(), pc.getSide(), pc.getPos()
#            if not i == None:
##                        print '---------------------------------'
#                x, y = self._map_coords(i.getPos().getX(), i.getPos().getY())
#                self.text2.append(self.canvas.create_text(x + 28, y - 28, text='dead', fill = 'red'))
    
class square(object):
    """
    is a square on the board
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getPosList(self):
        # returns the piece position in ordinary notation
        #return chr(ord('a') + self.x) + str(self.y)
        return [self.x, self.y]
        
    def getPosNot(self):
        # returns the piece position in ordinary notation
        return chr(ord('a') + self.x) + str(self.y + 1)
        
    def getX(self):
        return self.x
        
    def getY(self):
        return self.y
    
    def setStdSquare(self, stdPos):
        # sets the x and y from stdPos (a string)
        # PROBABLY UNECCESSARY
        self.x = ord(stdPos[0]) - ord('a')
        self.y = int(stdPos[1])
        
    def __add__(self, other):
        return [self.x + other.getX(), self.y + other.getY()]
        
    def add(self, other):
        # returns instance of square
        return square(self.x + other.getX(), self.y + other.getY())
        
    def __sub__(self, other):
        return [self.x - other.getX(), self.y - other.getY()]
    
    def __repr__(self):
        return str([self.x, self.y])
      
        
class piece(object):
    """
    piece on the board
    """
    _all = set()
    def __init__(self, square, side):
        # square -> square object
        # side -> 'b' or 'w'
        self.__class__._all.add(self)
        self.hasMoved = False
        self.ID = len(piece._all)
        if not (side == 1 or side == -1):
            raise ValueError('side must be either -1 or 1')
        self.square = square
        self.side = side
    
    def typ(self):
        if type(self) == pawn:
            return 'pawn'
        elif type(self) == knight:
            return 'knight'
        elif type(self) == bishop:
            return 'bishop'
        elif type(self) == castle:
            return 'castle'
        elif type(self) == queen:
            return 'queen'
        elif type(self) == king:
            return 'king'
        else:
            raise ValueError('not an acceptable piece type')
        
    def getPos(self):
        return self.square
        
    def getSide(self):
        return self.side
        
    def isLegalMove(self, pos, board):
        #returns True if piece can move to pos (a square)
        raise NotImplementedError
        
    def allTakes(self, board):
        # returns a dictionary of all possible pieces self can take
        out = {}
        for i in range(8):
            for j in range(8):
                pos = square(i, j)
                if self.isLegalMove(pos, board)[0] and (not self.freeTrack(board, pos)[1] == None):
                    victimPc = self.freeTrack(board, pos)[1]
                    out[victimPc] = True
        return out
        
    def allMoves(self, board):
        # returns a dictionary of all possible moves self can make
        out = {}
        for i in range(8):
            for j in range(8):
                pos = square(i, j)
                if self.isLegalMove(pos, board)[0] and self.freeTrack(board, pos)[0] == True:
                    out[pos] = True
        return out
    
    def setPos(self, pos):
        # forces new position
        self.square = pos
        
    def movePiece(self, pos, board):
        # returns True if successful - should save these move states
#        lastPos = self.square
        freeTemp = self.freeTrack(board, pos)
        legal = self.isLegalMove(pos, board)
        if legal[0] and freeTemp[0]:
            board.updateBoardSave()
            if not freeTemp[1] == None:
                # save board state
                board.takePiece(freeTemp[1])
            self.square = pos
            
            check = board.inCheck()
            if (check[0]) and (self.side == check[1]):
                board.undoChange()
                return False
            elif not board.castling(self.side, legal[1], self):
                board.undoChange()
                return False
            else:
                # pawn conversion
                if (self.square.getY() == (8 - self.side)%9) and (type(self) == pawn): # check for pawn conversion
                    board.addPiece(queen(self.square, self.side))
                    board.scrapPiece(self)
                self.hasMoved = True
                # castling
#                if not legal[1] == None:
#                    # get current position of castle
#                    x = legal[1].getPos().getX()
#                    y = legal[1].getPos().getY()
#                    # set x values for new position
#                    if x == 0:
#                        x = 3
#                    elif x == 7:
#                        x = 5
#                    else:
#                        raise ValueError('something wrong with castling')
#                    legal[1].setPos(square(x, y))
                return True
        else:
            return False
    
    def freeTrack(self, board, pos):
        # returns True if no pieces on board lie on piece's track
        # if the board piece lies on last square of piece's track, then
        # returns True and deletes the victim piece (if it's on the other side)
            
        origPos = self.getPos()
        [a, b] = pos - origPos
        path = track.twoPoints(origPos, pos)
        trk = []
        
        if [a, b] == [0, 0]:
            return [False, None]
        elif a == 0:
            for y in genRange(origPos.getY(), origPos.getY() + b + sign(b)):
                x = path.retX(y)
                trk.append([x, y])
#        elif b == 0:
#            
        else:
            for x in genRange(origPos.getX(), origPos.getX() + a + sign(a)):
                y = path.retY(x)
                trk.append([x, y])
        
        for pc in board.getLivePieces():
            if pc.getPos().getPosList() == trk[-1]:
                take = pc
            if pc.getPos().getPosList() in trk[1:-1]:
                return [False, None]
        
        try:#if take in locals():
            if take.getSide() == -self.getSide():
#                board.takePiece(take)
                return [True, take]
            else:
                return [False, None]
        except UnboundLocalError:
            return [True, None]
    
#    def takePiece(self):
#        self.live = False

def genRange(a, b):
    # general implementation of range. If b < a, returns reversed list
    if b >= a:
        return range(a, b)
    else:
        return list(reversed(range(b + 1, a + 1)))

def sign(a):
    #returns sign of a
    return (a>0) - (a<0)

class pawn(piece):
    """
    pawn
    """
#    def __init__(self, square, side):
#        super(pawn, self).__init__(square, side)
        
    def isLegalMove(self, pos, board):
        # first return false if move isn't possible for piece
        rel = [i * self.side for i in pos - self.square]
        rel2 = [i for i in pos - self.square]
        if self.square.getY() == (7 + self.side)%7 and rel == [0, 2]:# if starting pos and relative dist is 2
            return [True, None]
        elif rel == [0, 1]:# if rel distance is 1
            return [True, None]
        elif (rel[1] > 1) or (rel[1] < 0):
            return [False, None]
#        elif (rel[1] < 0):
#            return False
        elif board.isPiece(rel2[0] + self.square.getX(), rel2[1] + self.square.getY()):# if rel distance is 1
            return [True, None]
        else:
            return [False, None]
    
    def freeTrack(self, board, pos):
        origPos = self.getPos()
        [a, b] = pos - origPos
        path = track.twoPoints(origPos, pos)
        trk = []
        rel = [abs(i) for i in self.square - pos]
        
        if [a, b] == [0, 0]:
            return [False, None]
        elif a == 0:
            for y in genRange(origPos.getY(), origPos.getY() + b + sign(b)):
                x = path.retX(y)
                trk.append([ x, y])
        else:
            for x in genRange(origPos.getX(), origPos.getX() + a + sign(a)):
                y = path.retY(x)
                trk.append([x, y]) 
        for pc in board.getLivePieces():
            if pc.getPos().getPosList() == trk[-1]:
                take = pc
            if pc.getPos().getPosList() in trk[1:-1]:
#                print 'pc.typ() ', pc.typ()
#                print 'pc.getPos().getPosList() ', pc.getPos().getPosList()
                return [False, None]
                
        try:#if take in locals():
            if (take.getSide() == -self.getSide()) and (rel == [1, 1]):
#                board.takePiece(take)
                return [True, take]
            else:
                return [False, None]
        except UnboundLocalError:
            return [True, None]

class knight(piece):
    """
    knight
    """
#    def __init__(self, square, side):
#        super(knight, self).__init__(square, side)
        
    def isLegalMove(self, pos, board):
        # first return false if move isn't possible for piece
#        rel = [abs(i) for i in self.square - pos]
        rel = [abs(i) for i in pos - self.square]
        if rel == [1, 2] or rel == [2, 1]:# if starting relative dist is L shaped
            return [True, None]
        else:
            return [False, None]
    
    def freeTrack(self, board, pos):
        # returns True if no pieces on board lie on piece's track
        # if the board piece lies on last square of piece's track, then
        # returns True and deletes the victim piece (if it's on the other side)
        for pc in board.getLivePieces():
            if pc.getPos().getPosList() == [pos.getX(), pos.getY()]:
                take = pc
        
        try:#if take in locals():
            if take.getSide() == -self.getSide():
#                board.takePiece(take)
                return [True, take]
            else:
                return [False, None]
        except UnboundLocalError:
            return [True, None]
    
class bishop(piece):
    """
    bishop
    """
#    def __init__(self, square, side):
#        super(bishop, self).__init__(square, side)
        
    def isLegalMove(self, pos, board):
        # first return false if move isn't possible for piece
#        rel = [abs(i) for i in self.square - pos]#[((i>0) - (i<0)) for i in self.square - pos]
        rel = [abs(i) for i in pos - self.square]#[((i>0) - (i<0)) for i in self.square - pos]
        if (rel[0] == rel[1]):# if starting relative dist is L shaped
            return [True, None]
        else:
            return [False, None]


class castle(piece):
    """
    castle
    """
#    def __init__(self, square, side):
#        super(castle, self).__init__(square, side)
        
    def isLegalMove(self, pos, board):
        # first return false if move isn't possible for piece
#        rel = [abs(i) for i in self.square - pos]
        rel = [abs(i) for i in pos - self.square]
        if (rel[0] == 0) or (rel[1] == 0):# if starting relative dist is L shaped
            return [True, None]
        else:
            return [False, None]
            
            
class queen(piece):
    """
    queen
    """
#    def __init__(self, square, side):
#        super(queen, self).__init__(square, side)
        
    def isLegalMove(self, pos, board):
        # first return false if move isn't possible for piece
#        rel = [abs(i) for i in self.square - pos]
        rel = [abs(i) for i in pos - self.square]
        if (rel[0] == 0) or (rel[1] == 0) or (rel[0] == rel[1]):# if starting relative dist is L shaped
            return [True, None]
        else:
            return [False, None]


class king(piece):
    """
    king
    """
#    def __init__(self, square, side):
#        super(king, self).__init__(square, side)
        
    def isLegalMove(self, pos, board):
        # first return false if move isn't possible for piece
        rel = [abs(i) for i in pos - self.square]
        rel2 = [i for i in pos - self.square]
        if (rel == [1, 1]) or (rel == [1, 0]) or (rel == [0, 1]):
            return [True, None]
        elif (rel == [2, 0]) and (not self.hasMoved):
            if rel2[0] > 0:
                x = 0
#                cx = pos.getX() - 1
            else:
                x = 7
#                cx = pos.getX() + 1
            y = self.square.getY()
            pc = board.selectPiece(x, y) # select castle for castling
            if (not pc == None) and (pc.typ() == 'castle') and (not pc.hasMoved):
#                pc.setPos(square(cx, y))
                return [True, pc]
            else:
                return [False, None]
        else:
            return [False, None]



#------------------------------------------------------------------------------------------------

class Example(tk.Frame):
    def __init__(self, parent, board):
        self.board = board
        self.textDebug = []
        
        self.check = False
        self.checkmate = False
        self.stalemate = False
        
        self.timeStep = 0
        self.timeStepPos = None
        
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.bind("<Button-1>", self.callback)
        self.start_button = tk.Button(self, text="show threats", command=self.on_start)
        self.stop_button = tk.Button(self, text="hide threats", command=self.on_stop)
        self.save_button = tk.Button(self, text="save", command=self.on_save)
        self.load_button = tk.Button(self, text="load", command=self.on_load)
        self.fwd_button = tk.Button(self, text=">", command=self.on_fwd)
        self.back_button = tk.Button(self, text="<", command=self.on_back)
        
        self.fwd_button.pack(side='bottom', padx=10)
        self.back_button.pack(side='bottom', padx=10)
        
        self.save_button.pack(side='top', padx=10)
        self.load_button.pack(side='top', padx=10)
        self.start_button.pack(side='top', padx=10)
        self.stop_button.pack(side='top', padx=10)
        self.canvas.pack(fill="both", expand=True)
        
        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(8, 8)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill = "white")

        # Initialise board
        for j in range(8):
            for i in range(8):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                if (i%2 == 0 and j%2 == 0) or (i%2 == 1 and j%2 == 1):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill = "grey")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill = "white")
        self.side = 1
        self.selected = None

        
        self.setBoard()
        
        # Draw gridlines
        for i in range(9):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, 8)
            self.canvas.create_line(x1, y1, x2, y2)
        for i in range(9):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(8, i)
#            print x1, x2
            self.canvas.create_line(x1, y1, x2, y2)

        # text
        self.text = self.canvas.create_text(40, 10, text='turn: white')
        self.textSel = self.canvas.create_text(150, 10, text='selected: ')
        self.textScoreWhite = self.canvas.create_text(350, 487, text='score: ')
        self.textScoreBlack = self.canvas.create_text(350, 10, text='score: ')
        self.textCheck = self.canvas.create_text(150, 10, text='-')
        
        # call on_stop to initialize the state of the buttons
        self.on_stop()
        self.draw_one_frame()
    
    def setBoard(self):
        try: # delete existing representations of pieces
            for pc in self.pcs:
                self.canvas.delete(self.pcs[pc])
        except:
            pass
        try:
            self.canvas.delete(self.text)
            if self.side == 1:
                txt = 'turn: white'
            elif self.side == -1:
                txt = 'turn: black'
            self.text = self.canvas.create_text(40, 10, text=txt)
        except:
            print 'failed in setBoard'
        
        checkcheck = self.board.inCheck()
        if checkcheck[1] == 1:
            sideTxt = 'White'
        else:
            sideTxt = 'Black'
        
        if self.side == 1:
            sideTxt2 = 'White'
        else:
            sideTxt2 = 'Black'
        
        try:
            self.canvas.delete(self.textCheck)
        except:
            pass
            
        if checkcheck[0]:
            if self.board.inCheckMate(checkcheck[1]):
                self.textCheck = self.canvas.create_text(80, 487, text=sideTxt+' IN CHECK MATE!!')
                self.checkmate = True
            else:
                self.textCheck = self.canvas.create_text(80, 487, text=sideTxt+' IN CHECK!!')
                self.check = True
        else:
            if self.board.inStaleMate(self.side):
                self.textCheck = self.canvas.create_text(80, 487, text=sideTxt2+' IN STALE MATE!!')
                self.stalemate = True
            else:
                self.textCheck = self.canvas.create_text(80, 487, text='-')
                self.check = False
            
        self.pcs = {}
        livePieces = self.board.getLivePieces()
        for i in range(len(livePieces)):
            xc = livePieces[i].getPos().getX()
            yc = livePieces[i].getPos().getY()
            xx, yy = self._map_coords(xc, yc)
            txt = self.unicChess(livePieces[i].typ(), livePieces[i].getSide())
            self.pcs[livePieces[i]] = self.canvas.create_text(xx+28, yy-28, text=txt, font=("Arial", 40))
        try:
            self.showScore()
        except:
            print 'no textScore'
    
    
    def showScore(self):
        self.canvas.delete(self.textScoreWhite)
        self.canvas.delete(self.textScoreBlack)
        scoreWhite = self.board.getSideDead(1)
        scoreBlack = self.board.getSideDead(-1)
        if scoreWhite[2] and scoreBlack[2]:
            txtWhite = 'score: ' + str(scoreWhite[1]) + ' / ' 
            txtBlack = 'score: ' + str(scoreBlack[1]) + ' / '
            for ty in scoreWhite[3]:
                txtWhite = txtWhite + self.unicChess(ty, 1)
            for ty in scoreBlack[3]:
                txtBlack = txtBlack + self.unicChess(ty, 1)
        else:
            raise ValueError('the game isnt adding up')
        self.textScoreBlack = self.canvas.create_text(350, 487, text=txtWhite)
        self.textScoreWhite = self.canvas.create_text(350, 10, text=txtBlack)
        
    def unicChess(self, pcType, pcSide):
        # returns the unicode string for a certain pcType of colour pcSide
        if pcType == 'king':
            codeW = u"\u2654"
            codeB = u"\u265A"
        elif pcType == 'queen':
            codeW = u"\u2655"
            codeB = u"\u265B"
        elif pcType == 'castle':
            codeW = u"\u2656"
            codeB = u"\u265C"
        elif pcType == 'bishop':
            codeW = u"\u2657"
            codeB = u"\u265D"
        elif pcType == 'knight':
            codeW = u"\u2658"
            codeB = u"\u265E"
        elif pcType == 'pawn':
            codeW = u"\u2659"
            codeB = u"\u265F"
        else:
            raise ValueError('pcType not in List')
        
        if pcSide == 1:#(white)
            return codeW
        elif pcSide == -1:
            return codeB
        else:
            raise ValueError('pcSide not in List')
        
            
    def callback(self, event):
        if self.checkmate or self.stalemate:
            return False
        # define click point on board in squares
        self.clickx, self.clicky = self._map_pixel(event.x, event.y)
        # check if already selected, if not, make click selection 
        # (if click is valid selection)        
        if self.selected == None:
            tempselected = self.board.selectPiece(self.clickx, self.clicky)
            try:
                tempSide = tempselected.getSide()
                self.canvas.delete(self.textSel)
                txt = 'selected: ' + tempselected.getPos().getPosNot()
                self.textSel = self.canvas.create_text(150, 10, text=txt)
            except AttributeError:
                tempSide = None
            if tempSide == self.side:
                self.selected = tempselected
            else:
                print 'select piece from correct side'
        elif self.selected == self.board.selectPiece(self.clickx, self.clicky):
            print 'cancelling move'
            self.selected = None
#        elif self.selected.getSide() == self.side:
#            self.selected = self.board.selectPiece(self.clickx, self.clicky)
        else:
            # try to move the piece and check if successful
            if self.selected.movePiece(square(self.clickx, self.clicky), self.board):
                # check for Check Mate
                if self.board.inCheckMate(-self.side):
                    if self.side == 1:
                        print 'WHITE WINS!!!'
                    else:
                        print 'BLACK WINS!!!'
                # clear global selected variable and switch sides
                self.selected = None
                self.side = -self.side
                # count step
                if not ((self.timeStep == self.timeStepPos) or (self.timeStepPos == None)):
                    self.timeStep = self.timeStepPos
                    self.board.truncateBoardSaves(self.timeStepPos + 1)
                else:
                    self.timeStep += 1
                # reinstance the board
                self.setBoard()
            else:
                print 'not legal move'
                self.selected = None
    
    
        
    def on_start(self):
        """Start the animation"""
#        self.canvas.delete("all")
#        self.rect_id = self.canvas.create_rectangle(0,0,1,20, fill="blue")
#
        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.draw_one_frame()

    def on_stop(self):
        """Stop the animation"""
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        for n in self.textDebug:
            self.canvas.delete(n)
        self.running = False
        
    def on_save(self):
        self.board.saveBoard(self.side)
    
    def on_load(self):
        self.side = testBoard.loadBoard('savedBoard.dat')
        self.setBoard()
        self.checkmate = False
        self.stalemate = False
        
    def on_fwd(self):
        print self.timeStepPos, self.timeStep
        if (self.timeStepPos == None) or (self.timeStepPos == self.timeStep):
            # not moved yet
            self.timeStepPos = self.timeStep
            print 'cant go beyond now'
        else:
            self.board.goToTurn(self.timeStepPos + 1)
            self.timeStepPos = self.timeStepPos + 1
            self.side = -self.side
        # switch sides
        
        self.setBoard()
    
    def on_back(self):
        print self.timeStepPos, self.timeStep
        if self.timeStepPos == 0:
            # right back at beginning
            print 'cant go beyond starting position'
        elif self.timeStepPos == None:
            self.timeStepPos = self.timeStep
            self.board.goToTurn(self.timeStepPos - 1)
            self.timeStepPos = self.timeStepPos - 1
            
            self.side = -self.side
        else:
            self.board.goToTurn(self.timeStepPos - 1)
            self.timeStepPos = self.timeStepPos - 1
            
            self.side = -self.side
        # switch sides
        self.setBoard()

    def draw_one_frame(self):
        """Main control function for game"""
        if self.running:
            self.after(100, self.draw_one_frame)
            for n in self.textDebug:
                self.canvas.delete(n)
            self.text2 = []
#            try:
#                self.playGame()
#            test = []
            for pc in self.board.getLivePieces():
#                print pc
#                print board
                out = pc.allTakes(self.board)
                for i in out:
#                    print 'i, iSide, iPos, pc, pcSide, pcPos', i.typ(), i.getSide(), i.getPos(), pc.typ(), pc.getSide(), pc.getPos()
                    if not i == None:
#                        print '---------------------------------'
                        x, y = self._map_coords(i.getPos().getX(), i.getPos().getY())
                        self.textDebug.append(self.canvas.create_text(x + 28, y - 28, text='dead', fill = 'red'))
                        
#                test.append(out)
#                print self.clickx, self.clicky
#            except:
#                print 'not got it'
#            i, j = self._map_coords(6, 7)
#            j, k = self._map_pixel(i, j)
#            print 'test 1,2 = ' + str((i, j)) + str((j, k))
    
#    def playGame(self):
#        """
#        Main Control function for game
#        """
#        # 1st take in selection of piece
#        self.pc = self.board.selectPiece(self.clickx, self.clicky)
#        
#        # use self.selected as state to control mode of GUI (selecting or moving)
#        self.canvas.delete(self.text)
#        txt = str(self.clickx) + ',' + str(self.clicky)
#        self.text = self.canvas.create_text(40, 10, text=txt)
#        self.canvas.delete(self.pcs[self.board.selectPiece(self.clickx, self.clicky)])
        
        
    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
#        print 'from func' + str(250 + 450 * ((x - 8 / 2.0) / 8)), str(250 + 450 * ((8 / 2.0 - y) / 8))
        return (250 + 450 * ((x - 8 / 2.0) / 8),
                250 + 450 * ((8 / 2.0 - y) / 8))
    
    def _map_pixel(self, xp, yp):
        "opposite of _map_coords"
        return int(((float(xp - 250)/450) * 8) + 4), int(-((float(yp - 250)/450) * 8) + 4)

if __name__ == "__main__":
    root = tk.Tk()
    pieces = []
    for i in range(8):
        pieces.append(pawn(square(i, 1), 1))
        pieces.append(pawn(square(i, 6), -1))
    
#    print 'whats going on'
    pieces.append(castle(square(0, 0), 1))
    pieces.append(castle(square(7, 0), 1))
    pieces.append(castle(square(0, 7), -1))
    pieces.append(castle(square(7, 7), -1))

    pieces.append(knight(square(1, 0), 1))
    pieces.append(knight(square(6, 0), 1))
    pieces.append(knight(square(1, 7), -1))
    pieces.append(knight(square(6, 7), -1))
    
    pieces.append(bishop(square(2, 0), 1))
    pieces.append(bishop(square(5, 0), 1))
    pieces.append(bishop(square(2, 7), -1))
    pieces.append(bishop(square(5, 7), -1))
    
    pieces.append(queen(square(3, 0), 1))
    pieces.append(queen(square(3, 7), -1))
    
    pieces.append(king(square(4, 0), 1))
    pieces.append(king(square(4, 7), -1))
    
    testBoard = board(pieces)
    
    
    Example(root, testBoard).pack(fill="both", expand=True)
    root.mainloop()
    
#    testBoard.saveBoard()
#    b = testBoard.loadBoard('savedBoard.dat')
    
#    print a == b