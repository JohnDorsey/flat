


class ByteHandler(DataHandler):

  def __init__(self,source,name="unnIH"):
    DataHandler.__init__(self,source,name=name)
    
  def getRefresh(self):
    print("getting refresh (direct) for " + self.name)
    return self.source
    
  def putRefresh(self,refresh):
    print("putting refresh (direct) for " + self.name)
    self.changes.clear()
    self.source = refresh