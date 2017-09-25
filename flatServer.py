import socket
import _thread
from flatBoard import *
from flatPlayer import *
from flatData import *
from flatByte import *
from flatCodec import *
import time
import random



world = Board((64,64),name="server-world") #the server copy of the board
#boardHandler = BoardHandler(board) #translates instruction bytes and manipulates board
#worldBoardHandler = BoardHandler(world,name="serverWBH")
#worldDataHandler = DataHandler(world.squares,name="serverWDH")
world.preset(name="checkers")
dataHandler = DataHandler({},name="serverDH")
updateStream = b'' #store the current tick's updates here while distributing them to clients
world.squares.applyChanges()


print("initializing AF_INET SOCK_STREAM socket...")
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
hostName = socket.gethostname()
print("hostname is " + hostName)
port=25564 #default minecraft port minus 1
s.bind((hostName,port)) #reserve the port, now accessible through socket s
print("server running on port " + str(port))
s.setblocking(False) 
s.settimeout(0.1)




def clientThread(member): #this runs and handlers a player connection until disconnected
  print("new thread created for " + str(member[1]))
  member[0].send(b'#you_have_joined;')
  introduce(member)
  member[0].send(b'#you_have_been_introduced')
  print("waiting 5 seconds for member[0] to interpret introduction...")
  time.sleep(5.0)
  clientTick = 0
  while(True):
    clientTick += 1
    member[2]["debugData"]["serverSays"] = random.randint(1,100)
    try:
      result = interact(member)
      if result != 0:
        print(str(member[1])+": tick="+str(clientTick)+": quitting thread with code " + str(result))
        return
    except ConnectionResetError:
      print(str(member[1]) +": tick="+str(clientTick)+": connection reset, quitting thread")
      return

  
def serverThread(interval):
  print("server thread started with tick interval of " + str(interval))
  serverTick = 0
  while(True):
    serverTick += 1
    updateStream = toStream(dataHandler.getUpdate())
    #world.add((1,4),1)
    #worldDataHandler[1][4] = 
    time.sleep(interval)
  

def interact(member): #exchange data with specified player
  c = member[0] #connection
  ph = member[2] #player handler
  try:
    streamIn = c.recv(16384) #record client requests
  except socket.error as se:
    print(str(member[1]) + ": " + str(se))
    streamIn = b'#empty;'
  blocks = streamIn.split(b';')
  for block in blocks:
    if len(block) > 0:
      print(str(len(block)) + "B: ",end="")
    if block.startswith(b'#'):
      print(str(block))
      pass
    elif block.startswith(b'XX'): ##XX from client to server means disconnect me
      print("XX - the client will be disconnected")
      c.send(b'#xx_recieved_all_communications_end_instantly;')
      c.close()
      return 1
    elif block.startswith(b'PR'): #PR = player refresh
      print("PR - will put " + block.decode())
      ph.putUpdate(toData(block[2:])) #cut out the b'PR'. combine these selectors soon
      world.add((ph["pos"][0],ph["pos"][1]),1)
    elif block.startswith(b'PU'):
      print("PU - will put " + block.decode())
      ph.putUpdate(toData(block[2:])) #cut out the b'PU'. combine these selectors soon
      world.add((ph["pos"][0],ph["pos"][1]),1)
      ######NEEDS TO REGISTER CHANGE WITH THE WORLD DATA HANDLER
      pass
    elif len(block) >= 1:
      print("UNKNOWN - " + block.decode())
  if len(updateStream) > 0:
    c.send(b'DU'+updateStream+b';') #send this tick's data update to member
  #world.preset("randomize")
  c.send(b'BU'+toStream(world.squares.getUpdate())+b';') #send a board update to member
  return 0


  
  
  
def introduce(member):
  print("introducing member to the game")
  member[0].send(b'#intro;')
  member[0].send(b'BR'+toStream(world.squares.getRefresh())+b';')
  member[0].send(b'PR'+toStream(member[2].getRefresh())+b';') #send a player refresh to member
  member[0].send(b'DR'+toStream(dataHandler.getRefresh())+b';') #send a data refresh to member
  print("all introductions have been sent")
  


  
  
print("starting server thread...")
_thread.start_new_thread(serverThread,(0.125,))

print("waiting for first connection...")

while(True):
  try: #let new players join
    s.listen(5)
    c, address = s.accept()
    print("creating entry for " + str(address))
    member = [c,address,createPlayer(name="severMemberDH")]
    print("connection established with " + str(address))
    member[0].send(("#connected to " + hostName + ":" + str(port)).encode()+b';') #greet
    _thread.start_new_thread(clientThread,(member,))
  except socket.error:
    pass #the expected socket error is that nobody tried to connect
  
