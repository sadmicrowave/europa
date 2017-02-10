#!/usr/local/bin/python3

from modules import items

class Serum(items.Usable):
    def __init__(self, name, classtype, description, cost, hp, level):
        self.hp = hp
        self.level = level
        super().__init__(name, classtype, description, cost, hp, level)
 