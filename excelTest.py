import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import psycopg2
from apiclient.discovery import build
from selenium import webdriver


class youTubeInfo():
    def __init__(self,channelId):
        DEVELOPER_KEY = "AIzaSyCnPFkCPEDypwWcpkYCztNosU0-kGFwKoE"
        self.youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
        self._channelId=channelId
        self.dates=[]
        self.timeStamps=[]
    def getDates(self):
        uploads=self.youtube.channels().list(part="contentDetails",id=self._channelId).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        uploadItems=self.youtube.playlistItems().list(part="snippet",maxResults=50,playlistId=uploads).execute()['items']
        for i in uploadItems:
            self.dates.append(i['snippet']['publishedAt'])
    def parseDates(self):
        newDates=[]
        pattern='%Y-%m-%dT%H:%M:%SZ'
        for i in self.dates:
            date=datetime.datetime.strptime(i,pattern)
            newDates.append(date)
            self.timeStamps.append(datetime.datetime.timestamp(date))
        self.dates=newDates

class twitterInfo():
    def __init__(self):
        self.tweetDates=[]
        self.driver=webdriver.Firefox()
        self.timeStamps=[]
        self.timeout=15
        self.loadTime=30
    def getTweets(self):
        SCROLL_PAUSE_TIME = 0.5
        self.driver.get('https://twitter.com/michaelreeves')
        time.sleep(self.loadTime)
                    
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            timeElements=self.driver.find_elements_by_tag_name("time")
            for i in timeElements:
                try:
                    self.tweetDates.append(i.text)
                except:
                    print('Missed Tweet')
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                time.sleep(self.timeout)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height==last_height:              
                    break
            last_height = new_height
        print(len(self.tweetDates))
        self.driver.close()
        
    def parseDates(self):
        monthAbb=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        newDates=[]
        pattern='%m %d, %Y'
        for i in self.tweetDates:
            for j in range(len(monthAbb)):
                if i[:3]==monthAbb[j]:
                    i=str(j+1)+i[3:]
                    break
                
            if ',' not in i:
                i=i+', 2021'
            date=datetime.datetime.strptime(i,pattern)
            newDates.append(date)
            self.timeStamps.append(datetime.datetime.timestamp(date))
        self.tweetDates=newDates
            

class sqlLogger():
    def __init__(self,_database,_user,_password,_host,_port):
        self.conn=psycopg2.connect(database=_database,user=_user,password=_password,host=_host,port=_port)
        self.cur=con.cursor()
    def log(self,table,items):
        query=''
        for i in items:
            query+= i + ','
        query=query[:-1]
        self.cur.execute('INSERT INTO '+table+ ' VALUES ('+query+');')
        self.conn.commit()
    def close(self):
        conn.close()
        
        
def graphData(y1,x2,y2):
    graph1=plt.plot(range(len(y1)),y1)
    print((x2))
    print((y2))
    videoGraphs=plt.scatter(x2,y2)
    plt.gcf()
    plt.show()
        

            
def parseData(twitterStamps,youtubeStamps):
    twitterStamps.sort()
    youtubeStamps.sort()
    slicedLists={}
    lastDate=0
    for i in youtubeStamps:
        slicedLists[i]=[]
        for j in twitterStamps:
            if j<=i:
                slicedLists[i].append(j)
                lastDate=j
        if lastDate!=0:
            print('hi')
            twitterStamps=twitterStamps[twitterStamps.index(lastDate)+1:]
            lastDate=0            
    return(slicedLists)

def findDeltaT(slicedLists):
    deltaT=[]
    x=-1
    for i in slicedLists:
        x+=1
        slicedLists[i].sort()
        deltaT.append([])
        for j in range(len(slicedLists[i])-1):
            deltaT[x].append(slicedLists[i][j+1]-slicedLists[i][j])
    return(deltaT)

def findDeltaDeltaT(deltaT):
    deltaDeltaT=[]
    x=-1
    for i in deltaT:
        x+=1
        deltaDeltaT.append([])
        for j in range(len(i)-1):
            deltaDeltaT[x].append(i[j+1]-i[j])
    return(deltaDeltaT)
            
            


        

yTi=youTubeInfo('UCtHaxi4GTYDpJgMSGy7AeSw')
yTi.getDates()
yTi.parseDates()


tI=twitterInfo()
tI.getTweets()
tI.parseDates()

slicedLists=parseData(tI.timeStamps,yTi.timeStamps)
deltaT=findDeltaT(slicedLists)
deltaDeltaT=findDeltaDeltaT(deltaT)
print(len(slicedLists))
print(slicedLists)
print(deltaT)
print(deltaDeltaT)
joinedSlope=[]
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
