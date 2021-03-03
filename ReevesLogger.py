import time
import datetime
import numpy as np
import psycopg2
from apiclient.discovery import build
from selenium import webdriver
import configparser as cp

class youTubeInfo():
    def __init__(self,channelId):
        DEVELOPER_KEY = "AIzaSyCnPFkconfEDypwWconfkYCztNosU0-kGFwKoE"
        self.youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)
        self._channelId=channelId
        self.dates=[]
        self.timeStamps=[]
    def getDates(self):
        uploads=self.youtube.channels().list(part="contentDetails",id=self._channelId).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads'] #Gets channel upload playlist id
        uploadItems=self.youtube.playlistItems().list(part="snippet",maxResults=50,playlistId=uploads).execute()['items'] #Gets all info on all videos in uploads playlist
        for i in uploadItems:
            self.dates.append(i['snippet']['publishedAt']) #Get date of each video
    def parseDates(self):
        newDates=[]
        pattern='%Y-%m-%dT%H:%M:%SZ'
        for i in self.dates:
            date=datetime.datetime.strptime(i,pattern)
            newDates.append(date)
            self.timeStamps.append(datetime.datetime.timestamp(date)) #Converts date into unix timestamp
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
    def __init__(self,conf):
        _database=str(conf['SQL']['database'])
        _user=str(conf['SQL']['user'])
        _password=str(conf['SQL']['password'])
        _host=str(conf['SQL']['host'])
        _port=str(conf['SQL']['port'])
        
        self.conn=psycopg2.connect(database=_database,user=_user,password=_password,host=_host,port=_port)
        self.cur=con.cursor()
    def log(self,table,column,items):
        query=''
        for i in items:
            query+= i + ','
        query=query[:-1]
        self.cur.execute('INSERT INTO '+table+' ('+column+') VALUES ('+query+');')
        self.conn.commit()
        
    def sqlGrabber(self,columnName):
        self.cur.execute('SELECT '+columnName.lower()+' FROM '+self.table)
        eval('self.'+columnName+'=self.cur.fetchall()')
        
    def close(self):
        self.cur.close()
        self.conn.close()


if __name__=="__main__":
    yTi=youTubeInfo('UCtHaxi4GTYDpJgMSGy7AeSw')
    tI=twitterInfo()
    
    config = cp.ConfigParser()
    config.read("ReevesSQL.ini")

    sql=sqlLogger(config)
    while True:
        yTi.getDates()
        newYTdates=yTi.parseDates()
        oldYTdates=sql.sqlGrabber('youtubeStamps')
        sql.log(list(set(newYTdates)-set(oldYTdates)).sort())
        
        tI.getTweets()
        newTdates=tI.parseDates()
        oldTdates=sql.sqlGrabber('twitterStamps')
        sql.log(list(set(newTdates)-set(oldTdates)).sort())
        time.sleep(config['SETTINGS']['sleeptime'])

