#!/usr/local/bin/python3

import math

#################################################################################################################################
class Repair:
	def __init__(self, name, classtype, description, level=None):
		self.name = name
		self.description = description
		self.classtype = classtype
		self.taken	= False
		self.level	= level
	
	# method to determine if the item has been picked up yet
	def is_taken(self):
		return False

	# determine if the item can be repaired, if the level of the repair vendor is greater or equal to the level of the item
	def can_repair(self, item):
		return item.level <= self.level

	# determine the cost of repairing the item, based on how damaged it is
	def repair_cost(self, item):
		repair_hp = item.orig_hp - item.hp
		cost = 0
		if repair_hp == 0 :
			cost = None
		else :
			cost = math.ceil(repair_hp * (1+(item.level/10)))
			
		return cost
	
	def __str__(self):
		return self.description