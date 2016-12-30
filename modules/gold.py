#!/usr/local/bin/python3

from modules import items
from res.bgcolors import BgColors

class Gold(items.Chest):
	def __init__(self, name, classtype, description, amt, interaction_item=[]):
		self.amt = amt
		hp = None
		super().__init__(name, classtype, description, amt, hp, interaction_item)

	def __str__(self):
		return "{}You picked up {} {} coins!{}".format(BgColors.OKGREEN, self.cost, self.name, BgColors.ENDC)