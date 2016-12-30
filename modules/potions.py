#!/usr/local/bin/python3

from modules import items
from res.bgcolors import BgColors

class Potion(items.Usable):
    def __init__(self, name, classtype, description, cost, hp, level):
        self.hp = hp
        self.level = level
        super().__init__(name, classtype, description, cost, hp, level)
 
   # def __str__(self):
   #     #return "{} | Value:{}, HP:{} \n{}{}{}".format(self.name, self.cost, self.hp, BgColors.WARNING, self.description, BgColors.ENDC)
   #     return "{} | Value:{}, HP:{} | {}{}{}".format(self.name, self.cost, self.hp, BgColors.WARNING, self.description, BgColors.ENDC)
