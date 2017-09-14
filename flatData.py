

#changing items updates change dict.
#getting items shows the local value from the change dict or objects dict.
#getting updates implies that the update will be sent to everyone, so change dict is cleared.
#getting refresh implies filling someone in when they join, so it does not influence change dict
#use putUpdate to put refreshes



class DataHandler:
  def __init__(self,objects,name="unnDH"):
    self.objects = objects
    self.changes = {}
    self.name = name
    self.contains = (lambda datkey: self.objects.__contains__(datkey)) if type(objects)==dict else (lambda datkey: datkey > 0 and datkey < len(self.objects))

  def __setitem__(self,key,value): #change something
    if not (self.changes.__contains__(key) and self.changes[key]==value):
      self.changes[key] = value

  def __getitem__(self,key): #shows unapplied changes
    try:
      return self.changes[key] if self.changes.__contains__(key) else self.objects[key]
    except KeyError as ke:
      print(self.name + " KeyError: " + str(ke) )
      return "keyerrorinsert"
      
  #removes all changes that don't contain a value that's actually new
  def cleanChanges(self): 
    for key in self.changes:
      if self.contains(key) and self.objects[key] == self.changes[key]:
        self.changes.delitem(key)     

  #apply changes and empty changes dictionary
  def applyChanges(self):
    for key in self.changes:
      self.objects[key] = self.changes[key]
    self.changes = {}

  #encodes changes, also applies them locally
  def getUpdate(self):
    self.cleanChanges()
    sendableChanges = {}
    for key in self.changes:
      sendableChanges[key] = encodeUpdate(self.changes[key])
    result = str(sendableChanges).replace(" ","").encode()
    self.applyChanges()
    return result


  #encodes all data without emulating or applying changes
  def getRefresh(self):
    sendableChanges = {}
    for key in self.objects:
      sendableChanges[key] = encodeRefresh(self.objects[key])
    result = str(sendableChanges).replace(" ","").encode()
    return result

  def putUpdate(self,stream): #recieving data
    try:
      if type(stream)==DataHandler:
        updates = stream
      elif type(stream)==bytes:
        if len(stream) > 0:
          #updates = eval(stream.decode())
          updates = {}
          decodeUpdate(updates,stream)
        else:
          return
      else: 
        print(self.name + " putUpdate: unknown update type " + str(type(stream)) + " " + str(stream))
      #chumble spuzz
      for key in updates:
        if type(self.objects[key])==DataHandler: #assume that if the held object is a dataHandler, its update  must be a dataHandler update dictionary.
          self.objects[key].putUpdate(updates[key]) #updates are recursive, to change only parts of parts
        else:
          self.objects[key] = updates[key] #put regular update
      if len(self.changes) > 0:
        print(self.name + "flatData was given update while tracking changes. (bad things may happen now)")
    except KeyError as ke:
      print(self.name + ": key error in putUpdate: " + ke)

  def putRefresh(self,stream):
    print(self.name + ": putRefresh defaulting to putUpdate because everything is broken all the time")
    self.putUpdate(stream)
      
      

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

def decodeUpdate(object,stream):
  try:
    object.putUpdate(stream)
  except AttributeError:
    object = eval(stream.decode())
    
def decodeRefresh(object,stream):
  pass
