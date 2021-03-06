

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
    self.baseResult = lambda: {} if type(self.source)==dict else list(0 for i in range(len(source))) if type(self.source)==list else None
    self.has = lambda check: self.source.__contains__(check) if type(self.source)==dict else check < len(self.source)
    
  def __getitem__(self,key):
    result = None
    try:
      result = self.changes[key]
    except KeyError:
      try:
        result = self.source[key]
        if hasattr(result, "getUpdate"):
          self.changes[key] = result
      except KeyError:
        print(self.name + ": " + str(key) + " does not exist")
      except IndexError:
        print(self.name + ": " + str(key) + " is out of bounds, try the range (0," + str(len(self.source)) + ")")
        pass
    return result
        
    
  def __setitem__(self,key,value):
    startType = type(self.source[key])
    if not (self.has(key)): #any item modified must be made part of the source
      self.source[key] = value
      print(self.name + ": adding new item to source: " + str(key) + ":" + str(value))
    self.changes[key] = value #the emulated value, either original or changed, must be made equal to value
    if self.source[key] == self.changes[key]: #after adding the change, maybe remove it.
      self.changes.__delitem__(key)
    if not startType == type(self.source[key]):
      print(self.name + ": setitem type mismatch for [" + str(key) + "]: " + str(startType) + " -> " + str(type(self.source[key])))
      
  def __str__(self):
    stringSource = {}
    stringChanges = {}
    for key in self.gen:
      stringSource[key] = str(type(self.source[key])) + type(self.source[key]).__str__(self.source[key])
    for key in self.changes:
      stringChanges[key] = type(self.changes[key]).__str__(self.changes[key])
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
      try:
        startType = type(self.source[key])
      except KeyError:
        print(self.name + ": putUpdate key [" + str(key) + "] doesn't exist in " + str(type(self.source)) + " source of length " + str(len(self.source)) + ", putting primative <- VERY BAD IF INCORRECT")
        startType = None
        self.source[key] = update[key]
      except IndexError:
        print(self.name + ": putUpdate index [" + str(key) + "] doesn't exist in " + str(type(self.source)) + " source of length " + str(len(self.source)) + ", stopping")
        return
      if self.changes.__contains__(key): #don't hold onto any changes that are remotely overwritten
        self.changes.__delitem__(key)
      if not decodeUpdate(self.source[key],update[key]):
        self.source[key] = update[key]
      if not startType == type(self.source[key]):
        print(self.name + ": putUpdate type mismatch for [" + str(key) + "]: " + str(startType) + " -> " + str(type(self.source[key])))

  def getRefresh(self):
    result = self.baseResult() #the refresh should be the same type as the content?????????????
    for key in self.gen: #review whether this should be avoided
      result[key] = encodeRefresh(self.source[key])
    return result
    
  def putRefresh(self,refresh):
    for key in self.gen:
      startType = type(self.source[key])
      if not decodeRefresh(self.source[key],refresh[key]):
        print(self.name + ": overwriting [" + str(key) + "]")
        self.source[key] = refresh[key]
      if not startType == type(self.source[key]):
        print(self.name + ": putRefresh type mismatch for [" + str(key) + "]: " + str(startType) + " -> " + str(type(self.source[key])))
    self.changes.clear() #whatever you have been doing with your local data, you are wrong.

