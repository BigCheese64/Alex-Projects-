import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import psycopg2
import configparser as cp

class dataLearner():
    def __init__(self,conf):
        _database=str(conf['SQL']['database'])
        _user=str(conf['SQL']['user'])
        _password=str(conf['SQL']['password'])
        _host=str(conf['SQL']['host'])
        _port=str(conf['SQL']['port'])
        _table=str(conf['SQL']['table'])
        self.conn=psycopg2.connect(database=_database,user=_user,password=_password,host=_host,port=_port)
        self.cur=con.cursor()

        self.twitterStamps=[]
        self.youtubeStamps=[]
        self.pairedLists=[]
        self.deltaTime=[]
    def sqlGrabber(self,columnName):
        self.cur.execute('SELECT '+columnName+' FROM '+self.table)
        eval('self.'+columnName+'=self.cur.fetchall()')   #Ask likith if there is a less gross way of doing this


        
    def graphData(self,y1,x2,y2):
        graph1=plt.plot(range(len(y1)),y1)
        print((x2))
        print((y2))
        videoGraphs=plt.scatter(x2,y2)
        plt.gcf()
        plt.show()
            

                
    def parseData(self,):
        self.twitterStamps.sort()
        self.youtubeStamps.sort()
        _twitterStamps=self.twitterStamps
        _youtubeStamps=self.twitterStamps
        slicedLists={}
        lastDate=0
        for i in _youtubeStamps:
            slicedLists[i]=[]
            for j in _twitterStamps:
                if j<=i:
                    slicedLists[i].append(j)
                    lastDate=j
            if lastDate!=0:
                print('hi')
                _twitterStamps=_twitterStamps[_twitterStamps.index(lastDate)+1:]
                lastDate=0
                
        self.pairedLists=slicedLists

    def findDeltaT():
        x=-1
        for i in self.pairedLists:
            x+=1
            self.pairedLists[i].sort()
            self.deltaT.append([])
            for j in range(len(self.pairedLists[i])-1):
                self.deltaT[x].append(self.pairedLists[i][j+1]-self.pairedLists[i][j])
        return(deltaT)


    def close(self):
        self.cur.close()
        self.conn.close()            
            


        

if __name__=='__main__':

    c

    xvalue=[]
    for i in deltaT:
        joinedSlope=joinedSlope+i
        xvalue.append(5)
    tweetsBetweenVids=[]
    vidPlacement=0
    for i in slicedLists:
        vidPlacement+=len(slicedLists[i])
        tweetsBetweenVids.append(vidPlacement)  





        
    graphData(joinedSlope,tweetsBetweenVids,xvalue)
