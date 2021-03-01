import requests
import os
import yfinance
bigvar='I LIKE BREAD'

#bigvar=str(os.urandom(1000000))
#hi=requests.get('http://184.56.71.178')
hi=requests.post('http://184.56.71.178',{'username':str(bigvar),'submin':'Submit'})
requests.get('http://184.56.71.178')
print(hi)

class muskTweets():
    def __init__(self,keywords,cp):
        self._keywords=keywords
        self.tweet=''
        self.checkStocksLater=[] #['name','timestamp','hour_ago','now_price','hour_later']
        self.currentStock
        self.psqlUsername=str(self.cp['SQL']['user'])
        self.psqlPassword=str(self.cp['SQL']['password'])
        self.psqlHost=str(self.cp['SQL']['host'])
        self.psqlDatabase=str(self.cp['SQL']['database'])

    def checkTweet(self):
        twitterApi=''

    def parseTweet(self):
        wordList=self.tweet.split(' ')
        for i in wordList:
            if i in self._keywords:
                stockNow=self.stockMarket(i,time.time())
                stockHourAgo=self.stockMarket(i,time.time()-3600)
                self.checkStocksLater.append([i,time.time(),stockHourAgo,stockNow])
                
                
                
    def stockMarket(self,what,when):
        ticketData=yfinance.Ticker(what)
        tickerDf=tickerData.history(period='1d',when)
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
                
    def sqlLogger(self,passedList)
        conn=psycopg2.connect(self.psqlHost,self.psqlDatabase,self.psqlUser,self.psqlPassword)
        cur=conn.cursor()
        cmd=''
        for i in passedList:
            cmd+=i+','
        cmd=cmd[:-1]
        cur.execute('INSERT INTO '+where+'('+cmd+')')
        
    def run(self):
        while True:
            self.checkTweet()
            self.parseTweet()
            self.checkLater()
            
        
