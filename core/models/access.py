from core.dbo import DBO
from hashlib import sha256

class Access(DBO):
  def __init__(self):
    DBO.__init__(self,"Access")
