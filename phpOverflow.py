import yfinance
import time
import psycopg2
import configparser as cp
import tweepy
class muskTweets():
    def __init__(self,conf):
        self.tweet=''
        self.checkStocksLater=[] #['name','timestamp','hour_ago','now_price','hour_later']
        self.currentStock
        _database=str(conf['SQL']['database'])
        _user=str(conf['SQL']['user'])
        _password=str(conf['SQL']['password'])
        _host=str(conf['SQL']['host'])
        _port=str(conf['SQL']['port'])
        self.table=str(conf['SQL']['table'])        
        self.conn=psycopg2.connect(database=_database,user=_user,password=_password,host=_host,port=_port)
        self.cur=self.conn.cursor()
        _consumer_key=str(conf['TWITTER']['consumer_key'])
        _consumer_secret=str(conf['TWITTER']['consumer_secret'])
        _access_token=str(conf['TWITTER']['access_token'])
        _access_token_secret=str(conf['TWITTER']['access_token_secret'])
        self.id=str(conf['TWITTER']['access_token_secret'])
        self.auth = tweepy.OAuthHandler(_consumer_key, _consumer_secret)
        self.auth.set_access_token(_access_token, _access_token_secret)
        self.api = tweepy.API(self.auth)
        self.keywords=[]
        self.ticker=[]
        self.tweet=''
        
    def checkTweet(self):
        self.tweet=self.api.user_timeline(id=self.id,count=1)
        if self.tweet==self.lastTweet:
            return False
        else:
            return True
        
    def getKeyword(self):
        self.cur.execute('SELECT keywords FROM '+self.table)
        self.keywords=self.cur.fetchall()
        self.cur.execute('SELECT tickers FROM '+ self.table)
        self.tickers=self.cur.fetchall()
              

        
    def parseTweet(self):
        wordList=self.tweet.split(' ')
        for i in wordList:
            if i in self.keywords:
                ticker=self.tickers[self.keywords.index(i)]
                stockNow=self.stockMarket(i,time.time())
                stockHourAgo=self.stockMarket(i,time.time()-3600)
                self.checkStocksLater.append([ticker,i,time.time(),stockHourAgo,stockNow])
                
                
                
    def stockMarket(self,what,when):
        tickerData=yfinance.Ticker(what)
        tickerDf=tickerData.history(when,period='1d')
        return(tickerDf)
        #check price at time

    def checkLater(self):
        now=time.time()
        removeList=[]
        for i in range(len(self.checkStocksLater)):
            if now-self.checkStocksLater[i][1]>3600:
                self.checkStocksLater[i].append(self.stockMarket(self.checkStocksLater[i][0],time.time()))
                self.sqlLogger(self.checkStocksLater[i])
                removeList.append(i)
        for i in removeList:
            self.checkStocksLater.remove(i)
                
    def sqlLogger(self,passedList):
        cmd=''
        for i in passedList:
            cmd+=i+','
        cmd=cmd[:-1]
        self.cur.execute('INSERT INTO '+self.table+'('+cmd+')')
        
    def run(self):
        while True:            
            if(self.checkTweet()):
                self.parseTweet()
                self.checkLater()
                
        
