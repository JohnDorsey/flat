import pygame
import random
from flatData import *

pygame.init()

def createPlayer(name="cpDH"):
  return DataHandler({"pos":(random.randint(0,32),random.randint(0,32)),"unchanging":"same"},name=name)
    
class Player:
  def move(data,direction):
    data["pos"] = (data["pos"][0]+direction[0],data["pos"][1]+direction[1])
    
  def draw(data,label,target,color=(255,0,255,255)): #call addFont before using this
    pygame.draw.circle(target,color,Player.screenPos(data["pos"]),4,2)
    target.blit(Player.font.render(str(label),True,(220,63,255,255)),Player.screenPos(data["pos"]))
    
  def screenPos(pos):
    return (pos[0]*8+4,pos[1]*8+4)
    

Player.font = pygame.font.SysFont("courier",14)