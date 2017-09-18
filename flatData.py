

#DataHandler tracks changes made by its owner, it emulates these changes when the owner accesses it.
#DataHandler.getUpdate() gets relevant changes for remote applications, also applying the changes locally.
#DataHandler.getRefresh() gets all data to send to remote applications, without applying changes.

#what's new after the rewrite:
#DataHandler's recursive calls to getRefresh and getUpdate yeild nested primatives all the way back up, which are encoded into bytes only at the last possible second, in the socket send statement.
#DataHandler's recursive calls to putUpdate [or putRefresh] accept nested primatives, which have been decoded from recieved bytes, stripped of their signal phrases/terminators.


class DataHandler:
  def __init__(self,source,name="unnDH"):
    self.source, self.name = source, name
    self.changes = {}
    self.gen = range(0,len(self.source)) if type(self.source)==list else iter(self.source)
    self.baseResult = lambda: {} if type(self.source)==dict else list(0 for i in range(len(source)))
    
  def __getitem__(self,key):
    try:
      return self.changes[key]
    except KeyError:
      try:
        return self.source[key]
      except KeyError:
        print("self.name: " + str(key) + " does not exist")
    
  def __setitem__(self,key,value):
    if not (self.source.__contains__(key)): #any item modified must be made part of the source
      self.source[key] = value
    self.changes[key] = value #the emulated value, either original or changed, must be made equal to value
    if self.source[key] == self.changes[key]: #after adding the change, maybe remove it.
      self.changes.delitem(key)
      
  def applyChanges(self):
    for key in self.changes:
      self.source[key] = self.changes[key]
      self.changes.delitem[key]

  def getUpdate(self):
    result = {}
    for item in self.changes: #review whether this should be avoided
      result[item] = encodeUpdate(self.changes[item])
    self.changes = {}
    return result
    
  def putUpdate(self,update):
    for key in update:
      if self.changes.__contains__(key): #don't hold onto any changes that are remotely overwritten
        self.changes.delitem(key)
      decodeUpdate(self.source[key],update[key])

  def getRefresh(self):
    result = self.baseResult() #the resfresh should be the same type as the content?????????????
    for key in self.gen: #review whether this should be avoided
      try:
        result[key] = encodeRefresh(self.changes[key])
      except KeyError:
        result[key] = encodeRefresh(self.source[key])
    return result
    
  def putRefresh(self,refresh):
    self.source = refresh
    self.changes = {} #whatever you have been doing with your local data, you are wrong.

    
    
    
    
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
    
    
    
def toStream(object):
  return str(object).replace(" ","").encode()
  
def toData(object):
  return eval(object.decode())