

    
    
def encodeUpdate(object): #these methods allow recursion where __str__ would break it.
  try:
    return object.getUpdate()
  except AttributeError:
    return str(object).encode()
    
def encodeRefresh(object):
  try:
    return type(object).getRefresh(object)
  except AttributeError:
    return str(object).encode()

def decodeUpdate(object,input):
  try:
    object.putUpdate(input)
    return True
  except AttributeError:
    return False
    
def decodeRefresh(object,input):
  try:
    type(object).putRefresh(object,input)
    return True
  except AttributeError:
    return False
    
    
    
def toStream(object):
  return str(object).replace(" ","").encode()
  
def toData(object):
  return eval(object.decode())