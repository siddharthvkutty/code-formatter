import os,sys

def greet_user( name ):
    print( "Hello, "+name+"!" )

class   Person:
    def __init__(self,name,age):
        self.name=name
        self.age    = age
    def is_adult( self ):
        if self.age>=18:
            return True
        else:
            return False

def add(x,y):
 return x+y

data = { 'a':1,'b'  :2,'c': 3 }
