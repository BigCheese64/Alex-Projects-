def deltaT(self):
  for i in range(len(self.twitterStamps)):
    if i!=len(self.twitterStamps):
      self.deltaTy.append(self.twitterStamps[i+1]-self.twitterStamps[i])
      self.deltaTx.append((self.twitterStamps[i+1]+self.twitterStamps[i])/2)
      
      
def ytYvalues(self):
  for i in self.youtubeStamps:
    self.youtubeY.append(0)

def coorilation(self):
  for i in range(len(self.deltaTx)):
    #delta T * avg tweettime = %closerToNext vid
  
