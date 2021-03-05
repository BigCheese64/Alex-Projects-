def deltaT(self):
  for i in range(len(self.twitterStamps)):
    if i!=len(self.twitterStamps):
      self.deltaTy.append(self.twitterStamps[i+1]-self.twitterStamps[i])
      self.deltaTx.append((self.twitterStamps[i+1]+self.twitterStamps[i])/2)
      
      
    
  
