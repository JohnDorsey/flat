
from flatData import *

class ByteHandler(DataHandler):

  def __init__(self,source,name="unnIH",parent=None):
    DataHandler.__init__(self,source,name=name,parent=parent)
    
  def __str__(self):
    return "bh" + DataHandler.__str__(self)
    
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
    startType = type(self.source)
    self.changes.clear()
    self.source.clear()
    self.source = [int(refresh[i]) for i in range(len(self.refresh))]
    if not startType==type(self.source):
      print(self.name + ": ByteHandler.putRefresh type mismatch of source: " + str(startType) + " -> " + str(type(self.source)))
    #for i in range(len(self.source)):
    #  self.source[i] = int(refresh[i])
    #self.source = [refresh[i] for i in range(len(self.source))]
  

    
  def adopt(self): #adopt overridden because ByteHandlers have no non-primative children
    pass
    
    
   
  def putUpdate(self,update): #debugging only
    print(self.name + ": putUpdate is " + str(type(update)) + ": " + str(update))
    DataHandler.putUpdate(self,update)
    
  def getUpdate(self): #debugging only
    result = DataHandler.getUpdate(self)
    print(self.name + ": getUpdate is " + str(type(result)) + ": " + str(result))
    return result