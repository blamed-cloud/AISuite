#!/usr/bin/env python

class TestClass:
	string = "I am a test class"
	
	def __init__(self, _name):
		self.name = _name
		
	def get_name(self):
		print str(self.name)

#testing if passing a class works as I hope it does.	
def try_stuff(classname):
	print classname.string
	x = classname("Bob")
	x.get_name()
	
try_stuff(TestClass)
#turns out it does. (or at least it seems too)
