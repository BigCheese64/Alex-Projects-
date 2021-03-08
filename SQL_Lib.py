#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 09:29:31 2020

@author: alex
"""

class change():
    def __init__(self):
        self.comma=','
        self.singleQuote="'"
        
    def toString(self,v):#where v is any postgresql object that just needs quotes around it such as a string or an ip address
        v=self.singleQuote+str(v)+self.singleQuote
        return(v)
    def toBool(self,v):#where v is either the python type bool or a string that makes sense ex: true
        v=str(v).upper()
        return(v)
    def toInt(self,v):#where v is any type of number
        return(str(v))
    def toFloat(self,v):#where v is any type of number
        return(str(v))
    def toHex(self,v):
        #stuffs
        print()
    def toDateTime(self,v):#where v is any string the user wants classified as a datetime psql object
        v=self.singleQuote+str(v)+self.singleQuote+"::datetime"
        return(v)
    def toPoint(self,v):#where v is a tuple of x,y 
        v="("+str(v[0])+self.self.comma+str(v[1])+")"
        return(v)
    def toLineSeg(self,v):#where v is a tuple of tuples ex: [[-3,8],[5,2]]
        v="(("+str(v[0][0])+self.comma+str(v[0][1])+")"+self.comma+"("+str(v[0][0])+self.comma+str(v[0][1])+"))"
        return(v)
    def toBox(self,v):#where v is a tuple of tuples ex: [[-3,8],[5,2]]
        v="(("+str(v[0][0])+self.comma+str(v[0][1])+")"+self.comma+"("+str(v[0][0])+self.comma+str(v[0][1])+"))"
        return(v)
    def toPath(self,v):#where v is a list of tuples ex: [[-3,8],[5,2],[2,12]]
        v1="("
        for i in v:
            v1+="("+i[0]+self.comma+i[1]+")"+self.comma
        v1=v1[:-1]+")"
        return(v1)
    def toPolygon(self,v):#where v is a list of x,y tuples ex: [[1,2],[5,8],[10,-2]]
        v1="("
        for i in v:
            v1+="("+i[0]+self.comma+i[1]+")"+self.comma
        v1=v1[:-1]+")"
        return(v1)
    def toCircle(self,v):#where v is a tuple with the first element is a tuple containing the x,y of the center of the circle and the last element is the radius
        #ex: [[0,0],10] 
        v="<("+v[0][0]+self.comma+v[0][1]+")"+self.comma+v[1]+">"
        return(v)
    def toBitString(self,v):#where v is bytes 
        v=v[0].upper()+v[1:]
        return(v)
    def toList(self,v,listType):   #where v is any list where all objects types are the same and psql compatable excluding lists and listType is the SQL_Lib.py function you want to use on them
        #ex toList(['hi',['hi2','hi3'],'hello'],"toString")
        return(self.__toList2(v,listType)[:-1])
    def __toList2(self,v,listType):#Private function required to convert lists
        formatedList=""
        if isinstance(v, list):
            formatedList+="{"
            for i in v:
                formatedList+=self.__toList2(i,listType)
            if formatedList[-1]==self.comma:
                formatedList=formatedList[:-1]
            formatedList+="},"
        else:
            v=eval("self."+listType+"(v)")+self.comma
            formatedList+=v
        return formatedList
    def multiLists(self,v,listType): #where v is any list with any number inner lists. Returns psql string that allows for inserting multiple rows at once. Ex: [[1,2,3],[3,2,1]] --> (1,3),(2,2),(3,1); If lists are not the same len None values will be added until they are the same
        longest_list = max(len(elem) for elem in v)
        for i in range(len(v)):
            diff=longest_list-len(v[i])
            for j in range(diff):
                v[i].append('NULL')
        v2=''
        for i in range(len(v[0])):
            v1='('
            for j in range(len(v)):
                v1+=self.__toList2(v[j][i],listType)
            v1=v1[:-1]+'),'
            v2+=v1
        v2=v2[:-1]
        return(v2)
            
class revert():
    def toString(self,v):
        return str(v)
    def toInt(self,v):
        return int(v)
    def toBool(self,v):
        return bool(str(v).lower())
    def toFloat(self,v):
        return(float(v))
    def toHex(self,v):
        return(hex(v)) ##Dont know if this will work?
    def toDateTime(self,v):
        print() ##Not sure
                    
            
if __name__=='__main__':
    v=[[5,6,[4,5],8],[8,7,6,5]]
        
    print(change().multiLists(v,'toFloat'))
    

    
