
from flatData import *

class ByteHandler(DataHandler):

  def __init__(self,source,name="unnIH"):
    DataHandler.__init__(self,source,name=name)
    
  def getRefresh(self):
    print(self.name + ": getting refresh (direct): "),
    #result = b''
    result = ""
    for item in self.source:
      #result += item.to_bytes(1,"little")
      result += str(item)
    print(result)
    return result
  
  def putRefresh(self,refresh):
    print(self.name + ": putting refresh (direct)")
    self.changes.clear()
    self.source = [int(refresh[i]) for i in range(len(self.source))]
    #for i in range(len(self.source)):
    #  self.source[i] = int(refresh[i])
    #self.source = [refresh[i] for i in range(len(self.source))]
  

    
  def adopt(self): #adopt overridden because ByteHandlers have no non-primative children
    pass
    
    
   
  def putUpdate(self,update): #debugging only
    print(self.name + ": putUpdate is: " + str(update))
    DataHandler.putUpdate(self,update)
    
  def getUpdate(self): #debugging only
    result = DataHandler.getUpdate(self)
    print(self.name + ": getUpdate is: " + str(result))
    return result