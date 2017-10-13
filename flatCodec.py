

    
    
def encodeUpdate(object): #these methods allow recursion where __str__ would break it.
  if hasattr(object, "getUpdate"):
    return object.getUpdate()
  else:
    return object
    
def encodeRefresh(object):
  if hasattr(object, "getRefresh"):
    return type(object).getRefresh(object)
  else:
    return object

def decodeUpdate(object,input):
  if hasattr(object, "putUpdate"):
    object.putUpdate(input)
    return True
  else:
    return False
    
def decodeRefresh(object,input):
  if hasattr(object, "putRefresh"):
    type(object).putRefresh(object,input)
    return True
  else:
    print("codec: " + str(object) + " does not have a putRefresh method")
    return False
    
    
    
def toStream(object):
  return str(object).replace(" ","").encode()
  
def toData(object):
  return eval(object.decode())
