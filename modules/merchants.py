#!/usr/local/bin/python3
		
#################################################################################################################################
class Merchant:
	def __init__(self, name, classtype, description, items):
		self.name = name
		self.description = description
		self.inventory = items
		self.classtype = classtype
		self.taken	= False
	
	# method to determine if the item has been picked up yet
	def is_taken(self):
		return False
