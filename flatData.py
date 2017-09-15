




class DataHandler:
  def __init__(self,source,name="unnDH"):
    self.source, self.name = source, name
    self.changes = {}
    
  def __getitem__(self,key,value):
    try:
      return self.changes[key]
    except KeyError:
      try:
        return self.sources[key]
      except KeyError:
        print("self.name: " + str(key) + " does not exist")
    
  def __setitem__(self,key,value):
    if not (self.source.__contains__(key)):
      self.source[key] = value
      self.changes[key] = value
      return
    if not (self.changes.__contains__(key) and self.changes[key]==value):
      self.changes[key] = value
    if self.source[key] == self.changes[key]:
      self.changes.delitem(key)
      
  def applyChanges(self):
    for key in self.changes:
      self.source[key] = self.changes[key]
      self.changes.delitem[key]

  def getUpdate(self):
    result = self.changes
    self.changes = {}
    return result
    
  def putUpdate(self,update):
    for key in update:
      if self.changes.__contains__(key):
        self.changes.delitem(key)
      self.source[key] = update[key]
      #self.changes[key] = update[key]
      
    
  def getRefresh(self):
    result = {}
    for key in self.source:
      try:
        result[key] = self.changes[key]
      except KeyError:
        result[key] = self.source[key]
    
  def putRefresh(self,refresh):
    self.source = refresh

    
    
    
    
def encodeUpdate(object): #these methods allow recursion where __str__ would break it.
  try:
    return object.getUpdate()
  except AttributeError:
    return str(object).encode()
    
def encodeRefresh(object):
  try:
    return object.getRefresh()
  except AttributeError:
    return str(object).encode()

def decodeUpdate(object,input):
  try:
    object.putUpdate(input)
  except AttributeError:
    object = input
    
def decodeRefresh(object,input):
  try:
    object.putRefresh(input)
  except AttributeError:
    object = input