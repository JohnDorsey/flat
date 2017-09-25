

from flatCodec import *

#DataHandler tracks changes made by its owner, it emulates these changes when the owner accesses it.
#DataHandler.getUpdate() gets relevant changes for remote applications, also applying the changes locally.
#DataHandler.getRefresh() gets all data to send to remote applications, without applying changes.

#what's new after the rewrite:
#DataHandler's recursive calls to getRefresh and getUpdate yeild nested primatives all the way back up, which are encoded into bytes only at the last possible second, in the socket send statement.
#DataHandler's recursive calls to putUpdate [or putRefresh] accept nested primatives, which have been decoded from recieved bytes, stripped of their signal phrases/terminators.


class DataHandler:
  def __init__(self,source,name="unnDH",parent=None):
    self.source, self.name = source, name
    self.changes = {}
    self.gen = range(0,len(self.source)) if type(self.source)==list else iter(self.source)
    self.baseResult = lambda: {} if type(self.source)==dict else list(0 for i in range(len(source)))
    self.has = lambda check: self.source.__contains__(check) if type(self.source)==dict else check < len(self.source)
    self.parent = parent
    self.adopt()
    
  def __getitem__(self,key):
    try:
      return self.changes[key]
    except KeyError:
      try:
        return self.source[key]
      except KeyError:
        print(self.name + ": " + str(key) + " does not exist")
    
  def __setitem__(self,key,value):
    if not (self.has(key)): #any item modified must be made part of the source
      self.source[key] = value
      print(self.name + ": adding new item to source: " + str(key) + ":" + str(value))
    self.changes[key] = value #the emulated value, either original or changed, must be made equal to value
    if self.source[key] == self.changes[key]: #after adding the change, maybe remove it.
      self.changes.__delitem__(key)
    self.register()
      
  def __str__(self):
    stringSource = {}
    stringChanges = {}
    for key in self.gen:
      stringSource[key] = str(self.source[key])
    for key in self.changes:
      stringChanges[key] = str(self.changes[key])
    return "{name:" + self.name + ",source:" + str(stringSource) + ",changes:" + str(stringChanges) + "}"
      
  def applyChanges(self):
    for key in self.changes:
      self.source[key] = self.changes[key]
    self.changes.clear()

  def getUpdate(self):
    result = {}
    for item in self.changes: #review whether this should be avoided
      result[item] = encodeUpdate(self.changes[item])
    self.applyChanges()
    #print(self.name + ": getUpdate result: " + str(result))
    return result
    
  def putUpdate(self,update):
    for key in update:
      if self.changes.__contains__(key): #don't hold onto any changes that are remotely overwritten
        self.changes.delitem(key)
      if not decodeUpdate(self.source[key],update[key]):
        self.source[key] = update[key]

  def getRefresh(self):
    result = self.baseResult() #the refresh should be the same type as the content?????????????
    for key in self.gen: #review whether this should be avoided
      result[key] = encodeRefresh(self.source[key])
    return result
    
  def putRefresh(self,refresh):
    for key in self.gen:
      if not decodeRefresh(key,refresh[key]):
        self.source[key] = refresh[key]
    self.changes.clear() #whatever you have been doing with your local data, you are wrong.

  def register(self,child=None):
    if not child==None:
      if type(self.source)!=list:
        print(self.name + ": cannot register child who asked, they are not stored in a list")
      else:
        index = self.source.index(child)
        self.changes[index] = child
    if not self.parent==None:
      self.parent.register(self)
    
  def adopt(self):
    tries = 0
    fails = 0
    for key in self.gen:
      tries += 1
      try:
        self.source[key].parent = self
      except AttributeError:
        fails += 1
    print(self.name + ": adopted " + str(tries-fails) + " of " + str(tries) + " children.")
        


  
'''
def toStream(object):
  if type(object)==dict:
    result = b'{'
    for key in object:
      result += str(object[key]).encode() + b':' + (str(object).encode() if not type(object)==bytes else object) + b','
    result = result[:-1] + b'}'
    return result.replace(b' ',b'')
  else:
    return str(object).replace(" ","").encode()
'''