import matplotlib.pyplot as plt
import psycopg2
import configparser as cp
class dataLearner():
    def __init__(self,conf):
        _database=str(conf['SQL']['database'])
        _user=str(conf['SQL']['user'])
        _password=str(conf['SQL']['password'])
        _host=str(conf['SQL']['host'])
        _port=str(conf['SQL']['port'])
        self.table=str(conf['SQL']['table'])        
        self.conn=psycopg2.connect(database=_database,user=_user,password=_password,host=_host,port=_port)
        self.cur=self.conn.cursor()

        self.twitterStamps=[]
        self.youtubeStamps=[]
        self.pairedLists=[]
        self.deltaTy=[]
        self.deltaTx=[]
        self.youtubeY=[]
        
    def sqlGrabber(self,columnName):
        self.cur.execute('SELECT '+columnName.lower()+' FROM '+self.table)
        if columnName.lower()=='youtubestamps':
            self.youtubeStamps = self.parseData(self.cur.fetchall())
        elif columnName.lower()=='twitterstamps':
            self.twitterStamps=self.parseData(self.cur.fetchall())
        self.youtubeStamps.sort()
        self.twitterStamps.sort()
    def parseData(self,sqlList):
        newList=[]
        for i in sqlList:
            if i[0]!=None:
                newList.append(float(i[0]))
        return newList
        
        
        
    def graphData(self):
        graph1=plt.plot(self.deltaTx,self.deltaTy)
        videoGraphs=plt.scatter(self.youtubeStamps,self.youtubeY)
        plt.gcf()
        plt.show()
            
    
    def deltaT(self):
      #print(self.youtubeStamps)
      for i in range(len(self.twitterStamps)):
        if i!=len(self.twitterStamps)-1:
          self.deltaTy.append(self.twitterStamps[i+1]-self.twitterStamps[i])
          self.deltaTx.append((self.twitterStamps[i+1]+self.twitterStamps[i])/2)

      #print(self.deltaTy)
          
          
    def ytYvalues(self):
      for i in self.youtubeStamps:
        self.youtubeY.append(0)

    def equationTest(self):
        t=0


    def close(self):
        self.cur.close()
        self.conn.close()            
            


        

if __name__=='__main__':
    config = cp.ConfigParser()
    config.read("ReevesSQL.ini")    
    dL=dataLearner(config)
    dL.sqlGrabber('twitterstamps')
    dL.sqlGrabber('youtubestamps')
    dL.deltaT()
    dL.ytYvalues()
    dL.graphData()
    dL.equationTest()
    dL.close()
    

