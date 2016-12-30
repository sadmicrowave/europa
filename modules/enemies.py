#!/usr/local/bin/python3

#from modules import items
from res.bgcolors import BgColors

class Enemy:	
	#def __init__(self, name, description, hp, damage, items=[]):
	def __init__(self, name, classtype, description, hp, damage, dead_message, level):
		self.name 		 = name
		self.description = description
		self.hp 		 = hp
		self.damage 	 = damage
		self.classtype	 = classtype
		self.dead_message  = dead_message
		self.level		 = level
		self.objects 	 = []
		self.looted	 	 = False
		
	def intro_text(self):
		if self.is_alive():
			return self.alive_message
		else:
			return self.dead_message
 
	def is_alive(self):
		return self.hp > 0

	def been_looted(self):
		return self.looted
    
	def get_items(self):
		return self.objects
        
#################################################################################################################################
# DEFINE VARIOUS ENEMIES - EXTENDING BASE CLASS ENEMY

# class GiantPlant(Enemy):
#     def __init__(self):
#         super().__init__(name="Giant Plant", description="A giant man-eating plant", hp=5, damage=1)
#     
#     def intro_text(self):
#         if self.is_alive():
#             return """
#             A giant man-eating plant lies in your path!
#             """
#         else:
#             return """
#             The wilting corpse of a giant plant lies motionless on the ground.
#             """
# 
# class GiantSpider(Enemy):
#     def __init__(self):
#         super().__init__(name="Giant Spider", description="A vicious looking giant spider", hp=10, damage=2)
#     
#     def intro_text(self):
#         if self.is_alive():
#             return """
#             A giant spider jumps down from its web in front of you!
#             """
#         else:
#             return """
#             The corpse of a dead spider rots on the ground.
#             """
# 
# class Snake(Enemy):
#     def __init__(self):
#         super().__init__(name="Snake", description="A large poisonous snake.", hp=15, damage=5)
#     
#     def intro_text(self):
#         if self.is_alive():
#             return """
#             You've stumbled into a snake pit.  You are met by a ferocious snake with large fangs!
#             """
#         else:
#             return """
#             The corpse of a dead snake rots on the ground.
#             """ 
#   
# class Ogre(Enemy):
#     def __init__(self):
#         super().__init__(name="Giant Spider", description="A nasty smelling cave Ogre", hp=30, damage=15)
#     
#     def intro_text(self):
#         if self.is_alive():
#             return """
#             A towering and terrifying ogre emerges from the dark!
#             """
#         else:
#             return """
#             The corpse of a dead ogre rots on the ground.
#             """ 
#         
# class SkeletonSoldier(Enemy):
#     def __init__(self):
#         items = [armor.WoodenShield(), weapons.Sword()]
#         super().__init__(name="Skeleton Soldier", description="A skeleton soldier raised from the dead", hp=55, damage=25, items=items)
#     
#     def intro_text(self):
#         if self.is_alive():
#             return """
#             A ragged and boney skeleton soldier, with a sword and shield, crawls out of the gravel.
#             """
#         else:
#             return """
#             The bones of a skeleton soldier lie scattered on the ground.
#             """ 

