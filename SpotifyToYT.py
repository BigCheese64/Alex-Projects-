from selenium import webdriver
import time
class spotifyToYoutube():
    def __init__(self,playlist,d):
        self.spotifyPlaylist=playlist
        self.driver=d
        self.driver.get(self.spotifyPlaylist)
    def getStuff(self):
        self.names=[]
        self.artists=[]
        for i in range(len(self.driver.find_element_by_class_name('react-contextmenu-wrapper'))-10):
            self.names.append(self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[4]/div[1]/div/div[2]/div/div/div[2]/section[1]/div[4]/section/ol/div['+str(i)+']/div/li/div[2]/div/div[1]').getText())
            self.artists.append(self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[4]/div[1]/div/div[2]/div/div/div[2]/section[1]/div[4]/section/ol/div['+str(i)+']/div/li/div[2]/div/div[2]/span[1]/span/span/a').getText())
    def getLinks(self):
        self.links=[]
        for i in range(len(self.names)):
            self.driver.get("https://www.youtube.com/results?search_query="+self.names[i]+' by '+self.artists[i])
            self.links.append(self.driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[3]/div[1]/div/div[1]/div/h3/a').get_attribute("href"))  
            
    def downloadLinks(self):
        for i in self.links:
            self.driver.get('https://ytmp3.cc/en13/')
            self.driver.find_element_by_id('input').send_keys(i)
            self.driver.find_element_by_id('submit').click()
            while len(self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/a[1]').get_attribute("href"))<1:
                time.sleep(.5)
            self.driver.get(self.driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div[3]/a[1]').get_attribute("href"))
    def waitUntilDone(self):
        while dl_wait:
            time.sleep(1)
            dl_wait = False
            files = os.listdir(directory)
            if nfiles and len(files) != nfiles:
                dl_wait = True

            for fname in files:
                if fname.endswith('.crdownload'):
                    dl_wait = True
        self.driver.close()
        print('Done!')


STY=spotifyToYoutube(input('Spotify Playlist>'),webdriver.Firefox())
STY.getStuff()
STY.getLinks()
STY.downloadLinks()
STY.waitUntilDone()
