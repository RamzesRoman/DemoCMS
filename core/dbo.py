import sqlite3
import threading
from core.config import Config

db_lock=threading.Lock()

class DBO:
  FETCH=0
  LASTID=1
  ROWCOUNT=2

  def __init__(self,table_name):
    self.__table_name=table_name

  def execute(self,sql,query=0):
    with db_lock:
      conn=sqlite3.connect(Config["db_file"])
      c=conn.cursor()
      print(sql)
      c.execute(sql)
      result=None
      if query==self.FETCH:
        result=c.fetchall()
      if query==self.LASTID:
        result=c.lastrowid
      if query==self.ROWCOUNT:
        result=c.rowcount
      conn.commit()
      conn.close()
    return result

  def create(self,data):
    sql="INSERT INTO \"" + self.__table_name + "\" "
    keys=[]
    values=[]
    for (key,value) in data.items():
      keys.append(key)
      values.append("'" + str(value) + "'")
    sql = sql + "(" + ",".join(keys) + ") VALUES(" + ",".join(values) + ");"
    self.id=self.execute(sql,self.LASTID)

  def read(self,id):
    sql="PRAGMA table_info(\"" + self.__table_name + "\");"
    res=self.execute(sql)
    fields=[]
    for indx,name,t,n,d,p in res:
      fields.append(name)
    sql="SELECT " + ",".join(fields) + " FROM \"" + self.__table_name + "\" WHERE id='" + str(id) + "'"
    res=self.execute(sql)
    if len(res)>0:
      result={}
      for f in range(len(fields)):
        result[fields[f]]=res[0][f]
      return result
    return None

  def enumerate_sql(self):
    sql="PRAGMA table_info(\"" + self.__table_name + "\");"
    res=self.execute(sql)
    fields=[]
    for indx,name,t,n,d,p in res:
      fields.append(name)
    sql="SELECT " + ",".join(fields) + " FROM \"" + self.__table_name + "\""
    return sql

  def enumerate(self, search=None, start=0, limit=25):
    sql=self.enumerate_sql()
    if not search is None:
      conditions=[]
      for key,value in search.items():
        conditions.append(key + "=\'" + str(value) +"'")
      sql = sql + " WHERE " + " AND ".join(conditions)
    if start is None:
      start=0
    if limit is None:
      limit=25
    sql = sql + " LIMIT " + str(start) + "," + str(limit)
    return self.execute(sql)

  def delete(self,id):
    sql="DELETE FROM \"" + self.__table_name + "\" WHERE id=" + str(id)
    res=self.execute(sql,self.ROWCOUNT)
    return None


  def update(self,id,data):
    sql="UPDATE \"" + self.__table_name + "\" SET "
    params=[]
    for (key,value) in data.items():
      params.append(key +"='" + value + "'")
    sql = sql + " " + ",".join(params) + " WHERE id=" + str(id)
    self.id=self.execute(sql,self.ROWCOUNT)

