import time

class db_manager():
  def __init__(self,conf):
    self._conf=conf
    _database=str(conf['SQL']['database'])
    _user=str(conf['SQL']['user'])
    _password=str(conf['SQL']['password'])
    _host=str(conf['SQL']['host'])
    _port=str(conf['SQL']['port'])
    self.table=str(conf['SQL']['table'])        
    self.conn=psycopg2.connect(database=_database,user=_user,password=_password,host=_host,port=_port)
    self.cur=self.conn.cursor()
  
  def manage_temp_table(self):
    timeout=self._conf['TEMP']['TIMEOUT']
    self.cur.execute('SELECT username,timestamp FROM temp_users;')
    temp_users=self.cur.fetchall()
    old_users=[]
    for i in range(len(temp_users)):
      now=time.now()#will have to convert psql timestamp
      verification_time=temp_users[i][1]
      if((verification_time-now)>=timeout):
        self.cur.execute('DELETE FROM temp_users WHERE timestamp='+verification_time+';')
    
