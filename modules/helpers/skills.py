#!/usr/local/bin/python3

from modules.bgcolors import BgColors

class aSkills(object):
	
	@classmethod
	def check_skills(cls, **kwargs) :
		print("{}Skills:{}".format(BgColors.CADETBLUE, BgColors.ENDC))
		for k, v in kwargs['player'].skills.items():
			print("{}{:<10}:{}% - {}{}".format(BgColors.OKGREEN, v['name'], v['value'], v['desc'], BgColors.ENDC))
	
	
