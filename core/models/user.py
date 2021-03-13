from core.dbo import DBO
from hashlib import sha256

class User(DBO):
  def __init__(self):
    DBO.__init__(self,"Users")

  def enumerate_sql(self):
    return "SELECT u.id,u.name,u.email,a.name FROM \"Users\" as u left join \"Access\" as a on a.id=u.access_id"

  def login(self, email, password):
    crypted=self.make_pass(password.strip())
    sql="SELECT id,name FROM \"Users\" WHERE email='" + email.strip() +"' AND pass='" + crypted +"'"
    res=self.execute(sql)
    if len(res)>0:
      result={}
      for id,name in res:
        result={"id":id,"name":name}
      return result
    return None

  def create(self,data):
    if not data.get("pass") is None:
      data["pass"]=self.make_pass(data["pass"])
    return DBO.create(self,data)

  def update(self,id,data):
    if not data.get("pass") is None:
      data["pass"]=self.make_pass(data["pass"])
    return DBO.update(self,id,data)


  def make_pass(self,clear):
    return sha256(clear.strip().encode("utf-8")).hexdigest()
