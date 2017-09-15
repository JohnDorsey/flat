




class DataHandler:
  def __init__(self,source,name="unnDH"):
    self.source, self.name = source, name
    self.changes = {}
    
  def __getitem__(self,key,value):
    try:
      return self.changes[key]
    except:
      try:
        return self.sources[key]
      except:
        print("self.name: " + str(key) + " does not exist")
    
  def __setitem__(self,key):
    if not (self.source.__contains__(key)):
      self.source[key] = value
      self.changes[key] = value
      return
    if not (self.changes.__contains__(key) and self.changes[key]==value):
      self.changes[key] = value
      
  def getUpdate(self):
    result = self.changes
    self.changes = {}
    return result
    
  def putUpdate(self,update):
    for key in update:
      pass
      
  def getRefresh(self):
    pass
    
  def putRefresh(self):
    pass

def encodeUpdate(object):
  pass
  
def decodeUpdate(object,input):
  pass
  
def encodeRefresh(object):
  pass
  
def decodeRefresh(object,input):
  pass
    
  