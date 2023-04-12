import sys
import pygame
import random
import time
from shop import Shop
from DBControl import DBControl

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)

class Pacman:
    screen = None
    font = None
    buttons = []
    stage = ""
    paused = False

    imgWall = None
    imgPacman = None
    imgPacdot = None
    gifPacman = None
    imgGhost = None
    imgGhosts = None
    pacmanFrame = 0
    gifPacmanDeath = None

    score = 0
    highscore = 0
    life = 1
    coin = 0
    ghostSpeed = 1
    map = None
    pacmanGridPos = [0,0]
    pacmanRealPos = [0,0]
    pacmanInitPos = [0,0]
    pacmanDir = "right"
    pacmanMove = False
    ghosts = []     #[x,y,gridx,gridy,dir,img]
    stopped = False
    delayKeyInput = None
    """
    AMENDMENT 1: BUFF from SHOP: Hugh
    This states the buff effect
    Call example:
        life = extra_life[self.dbcontrol.buff[0]]
        speed = speed_boost_multiplier[self.dbcontrol.buff[w]]
    # buff0: extra life
    # buff1: score multiplier
    # buff2: pacman speed booster
    # buff3: shield
    # buff4: ghost slow
    """
    # each buff has 6 levels, level 0 to level 5
    extra_life = [1,2,3,4,5,6]
    score_multiplier = [1.5, 1.5, 2.0, 2.0, 2.5, 2.5]
    speed_boost_multiplier = [1.1, 1.1, 1.15, 1.2, 1.25, 1.3]
    ghost_slow_multiplier = [0.9, 0.75, 0.7, 0.65, 0.6, 0.5]
    # for all durations, need a clock
    score_multiplier_duration = [2, 5, 7, 10, 12, 15]
    speed_boost_duration = [2, 5, 7, 10, 12, 15]
    repellant_shield_duration = [2, 5, 7, 10, 12, 15]
    ghost_slow_duration = [2, 5, 7, 10, 12, 15]
    '''END OF AMENDMENT 1'''

    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        #self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        pygame.display.set_caption('Pacman')
        self.font = pygame.font.Font('Nunito-Medium.ttf',25)
        self.setStage("Menu")   #SHOP/EDITOR: to start stage in shop/editor, change this to "Editor"/"Shop"
        self.imgWall = pygame.image.load("Img\\defaultSkin\\wall.png").convert()
        self.imgPacman = pygame.image.load("Img\\defaultSkin\\pacman.png").convert()
        self.imgPacman.set_colorkey(BLACK)
        self.imgGhost = pygame.image.load("Img\\defaultSkin\\ghost0.png").convert()
        self.imgGhost.set_colorkey(BLACK)
        self.imgGhost = pygame.transform.scale(self.imgGhost, (36,36))
        self.imgGhosts = []
        for i in range(4):
            self.imgGhosts.append(pygame.image.load("Img\\defaultSkin\\ghost"+str(i)+".png").convert())
            self.imgGhosts[i].set_colorkey(BLACK)
            self.imgGhosts[i] = pygame.transform.scale(self.imgGhosts[i], (36,36))
        self.gifPacman = []
        for i in range(10):
            img = pygame.image.load("Img\\defaultSkin\\pixil-frame-"+str(i)+".png").convert()
            img.set_colorkey(BLACK)
            img = pygame.transform.scale(img, (36,36))
            self.gifPacman.append(pygame.transform.scale(img, (36,36)))
        self.gifPacmanDeath = []
        for i in range(7):
            img = pygame.image.load("Img\\defaultSkin\\death"+str(i)+".png").convert()
            img.set_colorkey(BLACK)
            img = pygame.transform.scale(img, (36,36))
            self.gifPacmanDeath.append(img)
        self.imgPacdot = pygame.image.load("Img\\defaultSkin\\pacdot.png").convert()
        self.imgWall = pygame.transform.scale(self.imgWall,(36,36))
        self.imgPacman = pygame.transform.scale(self.imgPacman,(36,36))
        self.imgPacdot = pygame.transform.scale(self.imgPacdot,(36,36))
        """
        AMENDMENT 2: introduction of DBControl
        This needs further modification to be able to read, save and upload
        DBControl and Shop already imported
        """
        self.dbcontrol = DBControl()
        self.shop = Shop(self.dbcontrol)
        """END OF AMENDMENT 2"""

    def setStage(self, stage):
        self.stage = stage
        if stage == "Menu":
            closeButton = Button((1010,1060,10,60),"Img\\defaultSkin\\closeButton.png", "Quit")
            startButton = Button((600,680,320,400),"Img\\defaultSkin\\startButton.png", "MainGame")
            restartButton = Button((1070,1120,10,60),"Img\\defaultSkin\\restartButton.png", "Menu")
            """
            AMENDMENT 3: SHOP STAGES
            """
            # Here is a temporary shop button 
            shopButton = Button((500,780,440,520), "Img\\defaultSkin\\closeButton.png", "enter_shop")
            self.buttons = [closeButton, startButton, restartButton, shopButton]
        if stage == "Shop":     #SHOP: put all buttons in the shop here
            quitButton = Button((10, 60, 10, 60), "Img\\defaultSkin\\closeButton.png", 'exit_shop')
            buffShopButton = Button ((450, 830, 300, 420), "Img\\Button\\button_buff-shop.png", 'enter_buff_shop')
            skinShopButton = Button ((450, 830, 480, 600), "Img\\Button\\button_skin-shop.png", 'enter_skin_shop')

            self.buttons = [quitButton, buffShopButton, skinShopButton]

        if stage == 'Buff_Shop' :
            quitButton = Button((10, 60, 10, 60), "Img\\defaultSkin/closeButton.png", 'return_to_shop_menu')
            # All can be implemented using list in final code
            buff0 = Button((340, 440, 620, 660), "Img\\Button\\button_upgrade.png", 'upgrade_buff0')
            buff1 = Button((465, 565, 620, 660), "Img\\Button\\button_upgrade.png", 'upgrade_buff1')
            buff2 = Button((590, 690, 620, 660), "Img\\Button\\button_upgrade.png", 'upgrade_buff2')
            buff3 = Button((715, 815, 620, 660), "Img\\Button\\button_upgrade.png", 'upgrade_buff3')
            buff4 = Button((840, 940, 620, 660), "Img\\Button\\button_upgrade.png", 'upgrade_buff4')
            icon0 = Button((340, 440, 40, 140), "Img\\Shop\\life.png", None)
            icon1 = Button((465, 565, 40, 140), "Img\\Shop\\score_multiplier.png", None)
            icon2 = Button((590, 690, 40, 140), "Img\\Shop\\Speed.png", None)
            icon3 = Button((715, 815, 40, 140), "Img\\Shop\\Invincible.png", None)
            icon4 = Button((840, 940, 40, 140), "Img\\Shop\\ghost_slow.png", None)
            lv = []
            for i in range(5): # will call Lv6.png; I set Lv6.png as identical to Lv5.png
                lv.append(Button((340 + 125 * i, 440 + 125 * i, 160, 600), "Img\\Shop\\Lv{}.png".format(self.dbcontrol.buff[i]), None))
                
            self.buttons = [quitButton, buff0,icon0, buff1,icon1, buff2,icon2, buff3,icon3, buff4,icon4, lv[0],lv[1],lv[2],lv[3],lv[4]]
            
        if stage == 'Skin_Shop':
            quitButton = Button((10, 60, 10, 60), "Img\\defaultSkin\\closeButton.png", 'return_to_shop_menu')
            leftButton = Button((350, 400, 520, 560), "Img\\Button\\left_unclick.png", 'previous_skin')
            rightButton = Button((880, 930, 520, 560), "Img\\Button\\right_unclick.png", 'next_skin')
            buyButton = Button((540, 740, 480, 560), "Img\\Button\\button_buy.png", 'buy_skin')
            equipButton = Button((540, 740, 600, 680), "Img\\Button\\button_equip.png", 'equip_skin')
            
            self.buttons = [quitButton, leftButton, rightButton, buyButton, equipButton]

            """END OF AMENDMENT 3"""
        if stage == "Editor":   #EDITOR: put all buttons present in the editor here
            pass
        if stage == "Settings":
            pass
        if stage == "MainGame":
            closeButton = Button((1010,1060,10,60),"Img\\defaultSkin\\closeButton.png", "Quit")
            pauseButton = Button((1010,1060,70,120),"Img\\defaultSkin\\pauseButton.png", "Pause")
            restartButton = Button((1070,1120,10,60),"Img\\defaultSkin\\restartButton.png", "Menu")
            self.buttons = [closeButton, pauseButton, restartButton]
        if stage == "GameOverAnimation":
            pacman.screen.fill(BLACK)
            if self.pacmanDir == "right":
                angle = 0
            if self.pacmanDir == "left":
                angle = 180
            if self.pacmanDir == "up":
                angle = 90
            if self.pacmanDir == "down":
                angle = 270
            rotatedPacman = pygame.transform.rotate(self.gifPacmanDeath[0], angle)
            self.screen.blit(rotatedPacman, (self.pacmanRealPos[0],self.pacmanRealPos[1]))
            pygame.display.flip()
            time.sleep(1)
            pacman.screen.fill(BLACK)
            for frame in range(1,7):
                rotatedPacman = pygame.transform.rotate(self.gifPacmanDeath[frame], angle)
                self.screen.blit(rotatedPacman, (self.pacmanRealPos[0],self.pacmanRealPos[1]))
                pygame.display.flip()
                time.sleep(0.5)
                pacman.screen.fill(BLACK)
            self.setStage("GameOver")
            
        if stage == "GameOver":
            restartButton1 = Button((640-100,640+100,460-40,460+40),"Img\\defaultSkin\\buttonFrame.png", "Menu", "Back to Menu")
            closeButton = Button((1010,1060,10,60),"Img\\defaultSkin\\closeButton.png", "Quit")
            restartButton = Button((1070,1120,10,60),"Img\\defaultSkin\\restartButton.png", "Menu")
            text = Button((640,640,250,250),None,None,"Game Over")
            text1 = Button((640,640,300,300),None,None,"Score :"+str(self.score))
            self.buttons = [restartButton1, closeButton, restartButton, text, text1]
        if stage == "Win":
            restartButton1 = Button((640-100,640+100,460-40,460+40),"Img\\defaultSkin\\buttonFrame.png", "Menu", "Back to Menu")
            closeButton = Button((1010,1060,10,60),"Img\\defaultSkin\\closeButton.png", "Quit")
            restartButton = Button((1070,1120,10,60),"Img\\defaultSkin\\restartButton.png", "Menu")
            text = Button((640,640,250,250),None,None,"You Win")
            text1 = Button((640,640,300,300),None,None,"Score :"+str(self.score))
            self.buttons = [restartButton1, closeButton, restartButton, text, text1]
            

    def drawScreen(self):
        if (not self.map == None) and (self.stage=="MainGame" or self.stage=="GameOverAnimation"):   #SHOP/EDITOR: modify this line to hide the game map
            self.drawMap(self.map)
        for b in self.buttons:
            b.draw(self.screen)
        #draw highscore and score
        if self.stage in ["MainGame", "Menu"]:
            t = self.font.render("Score: "+str(self.score),True,BLUE)
            tRect = t.get_rect()
            tRect.center = (100,100)
            self.screen.blit(t,tRect)
            t = self.font.render("Highscore: "+str(self.highscore),True,BLUE)
            tRect = t.get_rect()
            tRect.center = (100,150)
            self.screen.blit(t,tRect)
        """
        AMENDMENT 4 Call draw gold while in shop
        """
        if self.stage == "Shop" or self.stage == 'Buff_Shop' or self.stage == 'Skin_Shop':
            self.draw_gold_balance()
        """END OF AMENDMENT 4"""

    """
    AMENDMENT 5: draw gold function
    """
    def draw_gold_balance(self):
        gold_balance_text = f"Gold: {self.dbcontrol.gold}"
        gold_balance_font = pygame.font.Font(None, 20)
        gold_balance_surf = gold_balance_font.render(gold_balance_text, True, (255, 255, 255))
        gold_balance_rect = gold_balance_surf.get_rect(topright=(self.screen.get_width() - 20, 20))
        self.screen.blit(gold_balance_surf, gold_balance_rect)
    """END OF AMENDMENT 5"""
    def listen(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in self.buttons:
                if b.isClicked(event.pos):
                    self.runOperation(b.operation)
                    break
            if self.stage == "Editor":  #EDITOR section here
                pass
        if event.type == pygame.KEYDOWN:
            if self.stage == "MainGame":
                self.paused = False
                if event.key == pygame.K_UP:
                    self.delayKeyInput = "up"
                if event.key == pygame.K_DOWN:
                    self.delayKeyInput = "down"
                if event.key == pygame.K_LEFT:
                    self.delayKeyInput = "left"
                if event.key == pygame.K_RIGHT:
                    self.delayKeyInput = "right"

    def runOperation(self, operation):
        if operation == "Quit":
            pygame.quit()
            sys.exit()
        if operation == "MainGame":
            self.setStage("MainGame")
            self.mainGameInit("MainGame")
        if operation == "Menu":
            self.score = 0
            self.setStage("Menu")
        if operation == "Pause":
            if self.paused == True:
                self.paused = False
            else:
                self.paused = True
        #SHOP: you can put operations you need here, for example operation=="buyBuff1", buff1 += 1
        """
        AMENDMENT 6: Shop functions
        NOTE: THIS IS NOT THE FINAL VERSION; SOME COMPONENTS ARE MISSING
        In shop, set stage after each action to refresh the appearance
        """
        MAIN_MENU = 0
        BUFF_SHOP = 1
        SKIN_SHOP = 2
        global current_skin_idx

        if operation == "enter_shop":
            self.setStage('Shop')

        if operation == "enter_buff_shop":
            self.setStage('Buff_Shop')

        if operation == "enter_skin_shop":
            self.setStage('Skin_Shop')
            current_skin_idx = 0
            # Missing: draw the icon of 0th skin

        if operation == "exit_shop":
            self.setStage('Menu')
        
        if operation == "return_to_shop_menu":
            self.setStage('Shop')

        # Buff shop actions;             # Now missing notification of transactions or actions
        if operation == 'upgrade_buff0':
            self.shop.upgrade_buff(0)
            self.setStage('Buff_Shop')
        if operation == 'upgrade_buff1':
            self.shop.upgrade_buff(1)
            self.setStage('Buff_Shop')
        if operation == 'upgrade_buff2':
            self.shop.upgrade_buff(2)
            self.setStage('Buff_Shop')
        if operation == 'upgrade_buff3':
            self.shop.upgrade_buff(3)
            self.setStage('Buff_Shop')
        if operation == 'upgrade_buff4':
            self.shop.upgrade_buff(4)
            self.setStage('Buff_Shop')

        # Skin shop actions               # Now missing notification of transactions or actions
        if operation == 'previous_skin':
            current_skin_idx = (current_skin_idx - 1) % len(self.dbcontrol.skin)
            self.setStage('Skin_Shop')
            # Missing: draw the icon of current_index-th skin

        if operation == 'next_skin':
            current_skin_idx = (current_skin_idx + 1) % len(self.dbcontrol.skin)
            self.setStage('Skin_Shop')
            # Missing: draw the icon of current_index-th skin

        if operation == 'buy_skin':
            self.shop.buy_skin(current_skin_idx)
            self.setStage('Skin_Shop')

        if operation == 'equip_skin':
            self.shop.equip_skin(current_skin_idx)
            self.setStage('Skin_Shop')
        """END OF AMENDMENT 6"""

    def mainGameInit(self, mapPath):
        self.score = 0
        self.life = 2
        self.ghost = []
        self.paused = True
        self.importMap("Map\\test.txt")
        self.drawMap(self.map)
        self.ghostSpeed = 1

    def drawMap(self, map):
        for i in range(0,20):
            for j in range(0,20):
                if map[i][j] == "0":    #empty
                    pass
                elif map[i][j] == "1":  #pacdot
                    self.screen.blit(self.imgPacdot, (280+36*j,36*i))
                elif map[i][j] == "2":  #wall
                    self.screen.blit(self.imgWall, (280+36*j,36*i))
                elif map[i][j] == "3":  #pacman
                    pass
                    #self.screen.blit(self.imgPacman, (280+36*j,36*i))
                    #self.pacmanGridPos = [i,j]
                    #self.pacmanRealPos = [280+36*j,36*i]
                elif map[i][j] == "4":  #ghost
                    pass
                    #self.screen.blit(self.imgGhost, (280+36*j,36*i))

        #draw ghost
        for i in range(len(self.ghosts)):
            self.screen.blit(self.imgGhosts[i%4], (self.ghosts[i][2],self.ghosts[i][3]))
        #draw pacman
        if self.pacmanDir == "right":
            angle = 0
        if self.pacmanDir == "left":
            angle = 180
        if self.pacmanDir == "up":
            angle = 90
        if self.pacmanDir == "down":
            angle = 270
        rotatedPacman = pygame.transform.rotate(self.gifPacman[self.pacmanFrame], angle)
        self.screen.blit(rotatedPacman, (self.pacmanRealPos[0],self.pacmanRealPos[1]))
        #draw life
        for i in range(self.life):
            self.screen.blit(self.imgPacman, (10+36*i, 670))


    def importMap(self, mapPath):
        self.map = []
        map = open(mapPath, "r")
        for i in range(0,20):
            line = []
            for j in range(0,20):
                c = map.read(1)
                if c=="3":   #pacman
                    line.append("0")
                    self.pacmanGridPos = [i,j]
                    self.pacmanRealPos = [280+36*j,36*i]
                    self.pacmanInitPos = [i,j]
                elif c=="4": #ghost
                    line.append("0")
                    self.ghosts.append([i,j,280+36*j,36*i,"right"])
                else:
                    line.append(c)
            self.map.append(line)
        map.close()
    

    def saveMap(self, mapPath):
        s = ""
        for i in range(0,20):
            for j in range(0,20):
                s += str(self.map[i][j])
        self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "3"
        for ghost in self.ghosts:
            self.map[ghost[0]][ghost[1]] = "4"
        map = open(mapPath, "w")
        map.write(s)
        map.close()

    def isBlocked(self,dir):
        if dir == "right" and self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]+1]=="2":
            return True
        if dir == "left" and self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]-1]=="2":
            return True
        if dir == "up" and self.map[self.pacmanGridPos[0]-1][self.pacmanGridPos[1]]=="2":
            return True
        if dir == "down" and self.map[self.pacmanGridPos[0]+1][self.pacmanGridPos[1]]=="2":
            return True
        return False

    def changePacmanDir(self):
        if not self.isBlocked(self.delayKeyInput):
            if self.pacmanDir == "right" or self.pacmanDir == "left":
                if self.delayKeyInput == "up" or self.delayKeyInput == "down":
                    self.pacmanDir = self.delayKeyInput
            if self.pacmanDir == "up" or self.pacmanDir == "down":
                if self.delayKeyInput == "left" or self.delayKeyInput == "right":
                    self.pacmanDir = self.delayKeyInput
        self.delayKeyInput = None

    def isTouchingGhost(self):
        for ghost in self.ghosts:
            if abs(self.pacmanRealPos[0]-ghost[2]) < 30 and abs(self.pacmanRealPos[1]-ghost[3]) < 30:
                return True
        return False
    def isWinning(self):
        for i in self.map:
            for j in i:
                if j=="1":
                    return False
        return True

    def step(self):
        if self.stage == "GameOverAnimation":
            pass
        if self.stage == "MainGame":
            if self.paused == False:
                #move pacman
                if self.pacmanDir == "right" and self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]+1]!="2":
                    self.pacmanRealPos[0] += 3
                    self.stopped = False
                elif self.pacmanDir == "left" and self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]-1]!="2":
                    self.pacmanRealPos[0] -= 3
                    self.stopped = False
                elif self.pacmanDir == "up" and self.map[self.pacmanGridPos[0]-1][self.pacmanGridPos[1]]!="2":
                    self.pacmanRealPos[1] -= 3
                    self.stopped = False
                elif self.pacmanDir == "down" and self.map[self.pacmanGridPos[0]+1][self.pacmanGridPos[1]]!="2":
                    self.pacmanRealPos[1] += 3
                    self.stopped = False
                else:
                    self.stopped = True

                #reached new grid location
                if abs(self.pacmanGridPos[0]*36-self.pacmanRealPos[1])>=36 or abs(self.pacmanGridPos[1]*36+280-self.pacmanRealPos[0])>=36:
                    self.pacmanGridPos[0] = (self.pacmanRealPos[1]+18)//36
                    self.pacmanGridPos[1] = (self.pacmanRealPos[0]+18-280)//36
                    self.pacmanRealPos = [280+36*self.pacmanGridPos[1],36*self.pacmanGridPos[0]]
                    #change direction
                    self.changePacmanDir()
                
                if self.stopped == True:
                        self.changePacmanDir()
                
                if self.stopped == False:
                    self.pacmanFrame += 1
                    if self.pacmanFrame >= 7:
                        self.pacmanFrame = 0

                #move ghost
                for ghost in self.ghosts:
                    if ghost[4] == "right" and self.map[ghost[0]][ghost[1]+1]!="2":
                        ghost[2] += 2
                    elif ghost[4] == "left" and self.map[ghost[0]][ghost[1]-1]!="2":
                        ghost[2] -= 2
                    elif ghost[4] == "up" and self.map[ghost[0]-1][ghost[1]]!="2":
                        ghost[3] -= 2
                    elif ghost[4] == "down" and self.map[ghost[0]+1][ghost[1]]!="2":
                        ghost[3] += 2

                    #reached new grid
                    if abs(ghost[0]*36-ghost[3])>=36 or abs(ghost[1]*36+280-ghost[2])>=36:
                        ghost[0] = (ghost[3]+18)//36
                        ghost[1] = (ghost[2]+18-280)//36
                        ghost[2] = 280+36*ghost[1]
                        ghost[3] = 36*ghost[0]
                        #change direction
                        choices = []
                        if self.map[ghost[0]][ghost[1]+1]!="2":
                            choices.append("right")
                        if self.map[ghost[0]][ghost[1]-1]!="2":
                            choices.append("left")
                        if self.map[ghost[0]-1][ghost[1]]!="2":
                            choices.append("up")
                        if self.map[ghost[0]+1][ghost[1]]!="2":
                            choices.append("down")
                        #only turn back if facing dead end
                        if len(choices)>=2:
                            try:
                                if ghost[4]=="up":
                                    choices.remove("down")
                                elif ghost[4]=="down":
                                    choices.remove("up")
                                elif ghost[4]=="left":
                                    choices.remove("right")
                                elif ghost[4]=="right":
                                    choices.remove("left")
                            except:
                                pass

                        ghost[4] = random.choice(choices)
                if self.isTouchingGhost():
                    self.life -= 1
                    #loses
                    if self.life <= 0:
                        self.highscore = max(self.score,self.highscore)
                        self.coin += self.score//10
                        self.setStage("GameOverAnimation")
                    else:
                        self.pacmanGridPos[0] = self.pacmanInitPos[0]
                        self.pacmanGridPos[1] = self.pacmanInitPos[1]
                        self.pacmanRealPos = [280+36*self.pacmanInitPos[1],36*self.pacmanInitPos[0]]
                        self.paused = True
                        self.pacmanDir = "right"
                if self.isWinning():
                        self.highscore = max(self.score,self.highscore)
                        self.coin += self.score//10
                        self.setStage("Win")

            if self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] == "1":
                self.score += 10
                self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "0"
        

class Button:
    img = None
    position = (0,0,0,0)        #x1, x2, y1, y2
    operation = None
    text = None
    
    def __init__(self, position, imgPath=None, operation=None, text=None):
        if imgPath!=None:
            imgToLoad = pygame.image.load(imgPath).convert()
            self.img = pygame.transform.scale(imgToLoad,(position[1]-position[0],position[3]-position[2]))
        self.position = position
        self.operation = operation
        self.text = text

    def draw(self, surface):
        if not self.img == None:
            surface.blit(self.img, (self.position[0],self.position[2]))
        if not self.text == None:
            #this line access pacman inside button
            t = pacman.font.render(self.text,True,BLUE)
            tRect = t.get_rect()
            tRect.center = ((self.position[1]+self.position[0])//2,(self.position[3]+self.position[2])//2)
            surface.blit(t,tRect)

    def isClicked(self, mousePos):
        p = self.position
        if p[0] < mousePos[0] and p[1] > mousePos[0] and p[2] < mousePos[1] and p[3] > mousePos[1]:
            return True
        else:
            return False
        

"""
text = font.render("Welcome to Pacman!Press Esc to quit.",True,(255,0,0),(0,0,0))

textRect =text.get_rect()
textRect.center = (640,360)
screen.blit(text,textRect)
pacmanIdle = pygame.image.load("Img\\defaultSkin\\pacman.png").convert()
pacmanIdle = pygame.transform.scale(pacmanIdle,(100,100))
screen.blit(pacmanIdle,(300,300))

b = 
w = Window((400,600,400,600),[b])
w.draw(screen)
"""

pygame.init()
pacman = Pacman()
clock = pygame.time.Clock()
#a simple maze
"""
pacman.map = [
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,2],
    [2,1,2,2,2, 2,2,1,2,2, 2,2,1,2,2, 2,2,2,1,2],
    [2,1,2,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,2,1,2],
    [2,1,2,1,2, 2,2,2,1,2, 2,1,2,2,2, 2,1,2,1,2],
    
    [2,1,2,1,2, 1,1,1,1,1, 1,1,1,1,1, 2,1,2,1,2],
    [2,1,2,1,2, 1,2,1,2,2, 2,2,1,2,1, 2,1,2,1,2],
    [2,1,1,1,2, 1,1,1,1,1, 1,1,1,1,1, 2,1,1,1,2],
    [2,1,2,1,1, 1,2,1,2,1, 1,2,1,2,1, 1,1,2,1,2],
    [2,1,2,1,2, 1,2,1,2,1, 1,2,1,2,1, 2,1,2,1,2],
    
    [2,1,2,1,2, 1,2,1,2,1, 1,2,1,2,1, 2,1,2,1,2],
    [2,1,2,1,1, 1,2,1,2,2, 2,2,1,2,1, 1,1,2,1,2],
    [2,1,1,1,2, 1,1,1,1,3, 1,1,1,1,1, 2,1,1,1,2],
    [2,1,2,1,2, 1,2,1,2,2, 2,2,1,2,1, 2,1,2,1,2],
    [2,1,2,1,2, 1,1,1,1,1, 1,1,1,1,1, 2,1,2,1,2],
    
    [2,1,2,1,2, 2,2,2,1,2, 2,1,2,2,2, 2,1,2,1,2],
    [2,1,2,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,2,1,2],
    [2,1,2,2,2, 2,2,1,2,2, 2,2,1,2,2, 2,2,2,1,2],
    [2,1,1,1,1, 1,1,1,1,1, 1,1,1,1,1, 1,1,1,1,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2]
]
pacman.saveMap("Map\\test.txt")
pacman.importMap("Map\\test.txt")
"""


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            pacman.listen(event)
    pacman.step()
    pacman.drawScreen()
    pygame.display.flip()
    pacman.screen.fill(BLACK)   #clear screen
    clock.tick(40)