import pygame
from dbcontrol import DBControl

# skin status
UNPOSSESSED = 0
POSSESSED = 1
EQUIPPED = 2

class Shop:
    
    # default skin price is 500 gold; here reserve a mean to change skin price
    skin_price = [0, 0, 2000]
    # CHANGE THE NAMES AFTER DRAWING THE SKINS
    skin_name = ['Glory', 'King', 'IDK']
    buff_name = ['Extra life', 'Score multiplier', 'Speed booster', 'Shield', 'Ghost slower']

    def __init__(self, dbcontrol):
        # buff0: extra life
        # buff1: score multiplier
        # buff2: pacman speed booster
        # buff3: shield
        # buff4: ghost slow

        # for later call of dbcontrol and main
        self.dbcontrol = dbcontrol


    # upgrade buff function is to upgrade designated buff by one level each time
    # it checks if the gold is sufficient and if the current level is maximum
    # it deduces gold directly in dbcontrol at successful transactions
    # it calls a message dialog for displaying the results
    # NOTE: level range from 1 to 6, and index range from 0~5. The default level is 1.
    def upgrade_buff(self, buff_idx):
        MAX_LEVEL = 5
        message = ""

        if 0 <= buff_idx < len(self.dbcontrol.buff):
            current_buff_level = self.dbcontrol.buff[buff_idx]
            if current_buff_level < MAX_LEVEL:
                buff_upgrade_cost = (current_buff_level + 1) * 100

                if self.dbcontrol.gold >= buff_upgrade_cost:
                    self.dbcontrol.gold -= buff_upgrade_cost
                    self.dbcontrol.buff[buff_idx] += 1
                    message = f"{self.buff_name[buff_idx]} upgraded to level {current_buff_level + 1}."
                else:
                    message = "Insufficient gold."
            else:
                message = f"{self.dbcontrol.buff[buff_idx]} is already at the maximum level."
        else:
            message = "Invalid buff index."
        return message

    # buy skin function is to buy a designated skin each time
    # it checks if the gold is sufficient and if the current skin is possessed
    # it deduces gold directly in dbcontrol at successful transactions
    # it calls a message dialog for displaying the results
    def buy_skin(self, skin_idx):
        default_skin_price = 500
        message = ""

        if 0 <= skin_idx < len(self.dbcontrol.skin):
            if self.dbcontrol.skin[skin_idx] == UNPOSSESSED: 

                if self.skin_price[skin_idx] == 0: # default case, see __init__
                    current_skin_price = default_skin_price
                else:
                    current_skin_price = self.skin_price[skin_idx]

                if self.dbcontrol.gold >= current_skin_price:
                    self.dbcontrol.gold -= current_skin_price
                    self.dbcontrol.skin[skin_idx] = POSSESSED
                    message = "Purchase successful"
                else:
                    message = "Insufficient gold."
            else:
                message = "You already own this skin."
        else:
            message = "Invalid skin index."
        return message

    # equip skin function is to equip designated skin
    # it checks if the current skin is possessed
    # it calls a message dialog for displaying the results
    def equip_skin(self, skin_idx):

        message = ""
        if 0 <= skin_idx < len(self.dbcontrol.skin):
            if self.dbcontrol.skin[skin_idx] == POSSESSED:
                # unequip the currently equipped skin
                for i in range(len(self.dbcontrol.skin)):
                    if self.dbcontrol.skin[i] == EQUIPPED:
                        self.dbcontrol.skin[i] == POSSESSED
                # equip the current skin
                self.dbcontrol.skin[skin_idx] = EQUIPPED             
                message = f"{self.skin_name[skin_idx]} equipped."
            elif self.dbcontrol.skin[skin_idx] == EQUIPPED:
                message = "You have already equipped the skin."
            else:
                message = "You do not own this skin."
        else:
            message = "Invalid skin index."
        return message
    
    def get_skin_name(self, skin_idx):
        return self.skin_name[skin_idx]
