
import random
import pygame

from flatData import *
from flatByte import *

      

class Board:
  def __init__(self,size,name="untitled"):
    self.name, self.size = name, size
    self.maxValue = 1
    self.squares = DataHandler([ByteHandler([2 for i in range(self.size[0])],name=self.name+"_squares_DH_"+str(ii)) for ii in range(self.size[1])],name=self.name+"_squaresDH")
    
  def set(self,pos,value):
    self.squares[pos[1]][pos[0]] = value
    self.bound(pos)
    
  def add(self,pos,value):
    self.bound(pos)
    self.squares[pos[1]][pos[0]] += value
    #self.squares[pos[1]][pos[0]]
    
  def bound(self,pos):
    self.squares[pos[1]][pos[0]] %= self.maxValue+1
    
  def preset(self,name="randomize",interval=(0,0)):
    print(self.name + ": setting preset to " + name)
    if interval==(0,0):
      interval = (0,self.maxValue) #read default from self
    for y in range(self.size[1]):
      for x in range(self.size[0]):
        if name=="randomize":
          self.squares[y][x] = random.randint(interval[0],interval[1])
        elif name=="rings":
          self.squares[y][x] = self.center(((self.size[0]/2 - x)**2 + (self.size[1]/2 - y)**2)**0.5, self.size[0]/2,8)
        elif name=="checkers":
          self.squares[y][x] = (y*x)%2
    print("here's a sample of the new pattern: " + str([self.squares[8][i] for i in range(8)]))
          
  def center(self,value,limit,width):
    return 1 if 2*abs(limit/2 - value) < width else 0

  def draw(self,target): #make it scrollable someday
    #print("drawing: " + str(self.squares)[0:256])
    for y in range(self.size[1]):
      for x in range(self.size[0]):
        pygame.draw.rect(target,self.colorAt(x,y),((x*8)+1,(y*8)+1,7,7),4)
      
  def colorAt(self,x,y):
    row = self.squares[y]
    square = row[x]
    return self.colorOf(square)
      
  def colorOf(self,id): #board colors
    c = (((256/(self.maxValue+1))*id)%256)
    return (c,c,c,255)
      