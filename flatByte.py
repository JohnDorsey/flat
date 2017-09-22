
from flatData import *

class ByteHandler(DataHandler):

  def __init__(self,source,name="unnIH"):
    DataHandler.__init__(self,source,name=name)
    
  def getRefresh(self):
    print("getting refresh (direct) for " + self.name + ": "),
    #result = b''
    result = ""
    for item in self.source:
      #result += item.to_bytes(1,"little")
      result += str(item)
    print(result)
    return result
    
  def putRefresh(self,refresh):
    print("putting refresh (direct) for " + self.name)
    self.changes.clear()
    self.source = [int(refresh[i]) for i in range(len(self.source))]
    #for i in range(len(self.source)):
    #  self.source[i] = int(refresh[i])
    #self.source = [refresh[i] for i in range(len(self.source))]
    
  def getUpdate(self):
    result = DataHandler.getUpdate(self)
    print("the ByteHandler getUpdate is: " + str(result))
    return result
    
  def putUpdate(self,update):
    print("the ByteHandler putUpdate is: " + str(update))
    DataHandler.putUpdate(self,update)