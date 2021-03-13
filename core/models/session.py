from core.dbo import DBO
import uuid

class Session(DBO):
  def __init__(self):
    DBO.__init__(self,"Sessions")


  def create(self,data):
    data["id"]=uuid.uuid4()
    DBO.create(self,data)
    return data