
import time
import socket
from flatBoard import *
from flatPlayer import *
from flatData import *
from flatByte import *
import pygame

print("initializing pygame...")
pygame.init()
print("initializing display...")
screen = pygame.display.set_mode((512,512))

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
#hostName = socket.gethostname() #get hostname for creating connection, assuming it is on this host
hostName = "192.168.56.1"
port=25564

def connect():
  s.connect((hostName,port)) #connect to server
  print("tentative connection")
  s.setblocking(False)
  s.settimeout(5)
  intro = s.recv(4320)
  terpStream(intro)
  s.settimeout(0.1)
  print("introducing myself as " + hostName + ":" + str(port) + " through notes")
  s.send(b'#hello_I_am_' + hostName.encode() + b':' + str(port).encode()+b';') #greet with note
  
def stop():
  print("Sending Disconnect signal...")
  s.send(b'XX;')
  print("disconnecting...")
  s.close()
  print("closing display...")
  pygame.display.quit()
  print("quitting...")
  quit()
  


def frame(t=0.125):
  time.sleep(t)
  pygame.display.flip()
  for ev in pygame.event.get():
    if ev.type == pygame.QUIT:
      s.send(b'#goodbye;')
      stop()
    if ev.type == pygame.KEYDOWN:
      Player.move(me,keyToDirection(ev.key))
      s.send(b'PR'+toStream(me.getUpdate())+b';')
  try:
    streamIn = s.recv(4320) #recieve data from server
  except socket.error:
    return
  terpStream(streamIn)
      

def keyToDirection(key): #keycode -> axis touple
  return (1,0) if key==pygame.K_RIGHT else (-1,0) if key==pygame.K_LEFT else (0,-1) if key==pygame.K_UP else (0,1) if key==pygame.K_DOWN else (0,0)
  
def terpStream(stream):
  blocks = stream.split(b';')
  for block in blocks:
      terpBlock(block)
    
def terpBlock(block):
  if len(block) <= 0:
    print("received empty block")
  elif block.startswith(b'#'):
    print(str(block))
  elif block.startswith(b'BR'): #board refresh
    print("BR")
    worldDataHandler.putRefresh(block[2:]) ###Just replaced wbh with wdh
  elif block.startswith(b'BU'):
    print("BU - will put " + block[2:].decode())
    worldDataHandler.putUpdate(toData(block[2:]))
  elif block.startswith(b'PR'): #player refresh
    print("PR - will put " + block[2:].decode())
    me.putUpdate(toData(block[2:])) #give bytes to handler
  elif block.startswith(b'DU'): #data update
    print("DU - will put " + block[2:].decode())
    dataHandler.putUpdate(toData(block[2:])) #give bytes to handler
  elif block.startswith(b'DR'):
    print("DR - will put " + block[2:].decode())
    dataHandler.putRefresh(toData(block[2:])) #give bytes to handler
  else:
    print("UNKNOWN (" + str(len(block)) + " bytes): " + block.decode())
  
     
     

    

world = Board((64,64),name="client-world")
#worldBoardHandler = BoardHandler(world)
worldDataHandler = DataHandler(world.squares)

me = createPlayer()
me.name = "clientPlayerDH"


#players = []
dataHandler = DataHandler({},name="clientDH")



connect()


while(True):
  world.draw(screen)
  Player.draw(me,str(me["pos"]),screen)
  #for item in dataHandler:
  #  if item.__contains__("pos"):
  #    Player.draw(item,str(item["pos"]),screen,color=(255,255,0,255))
  frame(t=0.125)

      