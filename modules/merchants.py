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


#################################################################################################################################
# # CREATE THE DIFFERENT MERCHANTS WITH THEIR MERCHANT BOOKS FOR BUYING ITEMS
# class Merchant1(Merchant):
#     def __init__(self):
#         inventory = [weapons.Dagger()
#         			,weapons.Knife()
#         			,items.SmallHealthPotion()
#         		]
#         super().__init__( inventory )
#     
#     def intro_text(self):            
#         return """
#         You found a merchant! See what items he has for sale!
#         """
# 
# class Merchant2(Merchant):
#     def __init__(self):
#         inventory = [weapons.Sword()
#         			,armor.WoodenShield()
#         			,weapons.Knife()	        		 
#         		]
#         super().__init__( inventory )
#     
#     def intro_text(self):            
#         return """
#         You found a merchant! See what items he has for sale!
#         """