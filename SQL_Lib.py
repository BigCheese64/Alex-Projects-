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
        
    def toString(self,v):
        v=self.singleQuote+str(v)+self.singleQuote
        return(v)
    def toBool(self,v):
        v=str(v).upper()
        return(v)
    def toInt(self,v):
        return(str(v))
    def toFloat(self,v):
        return(str(v))
    def toHex(self,v):
        #stuffs
        print()
    def toDateTime(self,v):
        v=self.singleQuote+str(v)+self.singleQuote+"::datetime"
        return(v)
    def toPoint(self,v):
        v="("+str(v[0])+self.self.comma+str(v[1])+")"
        return(v)
    def toLineSeg(self,v):
        v="(("+str(v[0][0])+self.comma+str(v[0][1])+")"+self.comma+"("+str(v[0][0])+self.comma+str(v[0][1])+"))"
        return(v)
    def toBox(self,v):
        v="(("+str(v[0][0])+self.comma+str(v[0][1])+")"+self.comma+"("+str(v[0][0])+self.comma+str(v[0][1])+"))"
        return(v)
    def toPath(self,v):
        v1="("
        for i in v:
            v1+="("+i[0]+self.comma+i[1]+")"+self.comma
        v1=v1[:-1]+")"
        return(v1)
    def toPolygon(self,v):
        v1="("
        for i in v:
            v1+="("+i[0]+self.comma+i[1]+")"+self.comma
        v1=v1[:-1]+")"
        return(v1)
    def toCircle(self,v):
        v="<("+v[0][0]+self.comma+v[0][1]+")"+self.comma+v[1]+">"
        return(v)
    def toBitString(self,v):
        v=v[0].upper()+v[1:]
        return(v)
    def toList(self,v,listType):    
        return(self.toList2(v,listType)[:-1])
    def toList2(self,v,listType):
        formatedList=""
        if isinstance(v, list):
            formatedList+="{"
            for i in v:
                formatedList+=self.toList2(i,listType)
            if formatedList[-1]==self.comma:
                formatedList=formatedList[:-1]
            formatedList+="},"
        else:
            v=eval("self.to"+listType+"(v)")+self.comma
            formatedList+=v
        return formatedList
            
            
stuff=['hi',['hi','hi','hi'],['hi','hi']]
print(change().toList(stuff,"String"))
    
