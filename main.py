import sys
import pygame
import random
import time
from shop import Shop
from DBControl import DBControl
import PySimpleGUI as Message
from Setting import Setting
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)
"""
newMap = [
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],

[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],

[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],

[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],
[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0]
]"""

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
        life = extra_life[self.DBControl.buff[0]]
        speed = speed_boost_multiplier[self.DBControl.buff[w]]
    # buff0: extra life
    # buff1: score multiplier
    # buff2: pacman speed booster
    # buff3: shield
    # buff4: ghost slow
    """
    scoreMulti = False
    scoreMultiDuration = 0
    speedBoost = False
    speedBoostDuration = 0
    shield = False
    shieldDuration = 0
    ghostSlow = False
    ghostSlowDuration = 0

    eatCount = 0
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
        #add music
        #pygame.mixer.init()
        self.setting = Setting()
        self.DBControl = DBControl()
        self.shop = Shop(self.DBControl)
        self.music = pygame.mixer.Sound("music\\fight.mp3")
        #add button click sound
        self.clicksound = pygame.mixer.Sound("music\\click.mp3")
        #add eat sound need to further play when collision happen with pacman and pac
        self.eatsound = pygame.mixer.Sound("music\\coin.mp3")

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

        self.imgScoreMulti = pygame.image.load("Img\\defaultSkin\\scoreMulti.png").convert()
        self.imgSpeedBoost = pygame.image.load("Img\\defaultSkin\\speedBoost.png").convert()
        self.imgShield = pygame.image.load("Img\\defaultSkin\\shield.png").convert()
        self.imgGhostSlow = pygame.image.load("Img\\defaultSkin\\ghostSlow.png").convert()
        self.imgScoreMulti = pygame.transform.scale(self.imgScoreMulti,(36,36))
        self.imgSpeedBoost = pygame.transform.scale(self.imgSpeedBoost,(36,36))
        self.imgShield = pygame.transform.scale(self.imgShield,(36,36))
        self.imgGhostSlow = pygame.transform.scale(self.imgGhostSlow,(36,36))
        self.imgScoreMulti.set_colorkey(BLACK)
        self.imgSpeedBoost.set_colorkey(BLACK)
        self.imgShield.set_colorkey(BLACK)
        self.imgGhostSlow.set_colorkey(BLACK)
        """
        AMENDMENT 2: introduction of DBControl
        This needs further modification to be able to read, save and upload
        DBControl and Shop already imported
        """
        """END OF AMENDMENT 2"""
    def background(self):
        i = 280
        while i <= 1000:
            if i != 664:
                dot = Button((i, i + 48, 672, 720),"Img\\defaultSkin\\pacdot.png", None)
                dot.draw(self.screen)
            else:
                dot = Button((i, i + 48, 672, 720), "Img\\defaultSkin\\ghost.png", None)
                dot.draw(self.screen)
            if i == 520:
                dot = Button((i, i + 48, 0, 48), "Img\\defaultSkin\\Pacman.png", None)
            else:
                dot = Button((i, i + 48, 0, 48), "Img\\defaultSkin\\pacdot.png", None)
            dot.draw(self.screen)
            i += 48
        i = 48
        while i < 720:
            dot = Button((280, 328, i, i + 48), "Img\\defaultSkin\\pacdot.png", None)
            dot.draw(self.screen)
            dot = Button((1000, 1048, i, i + 48), "Img\\defaultSkin\\pacdot.png", None)
            dot.draw(self.screen)
            i += 48
    def setStage(self, stage):
        self.stage = stage
        #toMENU
        if stage == "Menu":
            self.ghosts = []
            closeButton = Button((1010,1060,10,60),"Img\\defaultSkin\\closeButton.png", "Quit")
            startButton = Button((600,680,320,400),"Img\\defaultSkin\\startButton.png", "MainGame")
            restartButton = Button((1070,1120,10,60),"Img\\defaultSkin\\restartButton.png", "Menu")
            """
            AMENDMENT 3: SHOP STAGES
            """
            # Here is a temporary shop button 
            shopButton = Button((600,680,420,500), "Img\\defaultSkin\\shop.png", "enter_shop")
            loginButton = Button((600,680,520,600), "Img\\defaultSkin\\login.png", "Login")
            settingButton = Button((600,680,620,700), "Img\\defaultSkin\\setting.png", "Setting")
            downloadButton = Button((690,770,320,400),"Img\\defaultSkin\\download.png", "DownloadALL")
            uploadButton = Button((780,860,320,400),"Img\\defaultSkin\\upload.png", "UploadData")
            self.buttons = [closeButton, startButton, restartButton, shopButton, loginButton, settingButton, downloadButton, uploadButton]
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
                lv.append(Button((340 + 125 * i, 440 + 125 * i, 160, 600), "Img\\Shop\\Lv{}.png".format(self.DBControl.buff[i]), None))
                
            self.buttons = [quitButton, buff0,icon0, buff1,icon1, buff2,icon2, buff3,icon3, buff4,icon4, lv[0],lv[1],lv[2],lv[3],lv[4]]
            
        if stage == 'Skin_Shop':
            quitButton = Button((10, 60, 10, 60), "Img\\defaultSkin\\closeButton.png", 'return_to_shop_menu')
            leftButton = Button((350, 400, 520, 560), "Img\\Button\\left_unclick.png", 'previous_skin')
            rightButton = Button((880, 930, 520, 560), "Img\\Button\\right_unclick.png", 'next_skin')
            buyButton = Button((540, 740, 480, 560), "Img\\Button\\button_buy.png", 'buy_skin')
            equipButton = Button((540, 740, 600, 680), "Img\\Button\\button_equip.png", 'equip_skin')
            
            self.buttons = [quitButton, leftButton, rightButton, buyButton, equipButton]

            """END OF AMENDMENT 3"""
        if stage == "Main Editor":   #EDITOR: put all buttons present in the editor here
            editButton = Button((517,817,269,349),"Img\\defaultSkin\\editMapButton.png","gotoEdit")
            downloadButton = Button((517,817,400,480),"Img\\defaultSkin\\downloadMapButton.png", "gotoDownload")
            uploadButton = Button((517,817,530,610),"Img\\defaultSkin\\uploadMapButton.png", "gotoUpload")
            self.buttons = [editButton,downloadButton,uploadButton]

        if stage == "Edit2": 
            wallButton = Button((101,162,161,217),"Assets\\Wall_Icon.png","place")
            ghostButton = Button((95,170,256,332),"Assets\\Ghost_Icon.png","place")
            pacmanButton = Button((109,169,371,431),"Assets\\Pacman_Icon.png","place")
            saveButton = Button((1093,1263,649,700),"Assets\\Save_Button.png","save")
            
            self.buttons = [wallButton,ghostButton,pacmanButton,saveButton]
            for i in range(20):
                for j in range(20):
                    #Button = Button(())
                    block = Button((j*36+280,j*36+280 +36, i*36 , i*36+36), "Assets\\empty.png", "place")
                    self.buttons.append(block)
        if stage == "MainGame":
            closeButton = Button((1010,1060,10,60),"Img\\defaultSkin\\closeButton.png", "Quit")
            pauseButton = Button((1010,1060,70,120),"Img\\defaultSkin\\pauseButton.png", "Pause")
            saveButton = Button((1070,1120,70,120),"Img\\defaultSkin\\pauseButton.png", "DBSaveMap")
            restartButton = Button((1070,1120,10,60),"Img\\defaultSkin\\restartButton.png", "Menu")
            self.buttons = [closeButton, pauseButton, restartButton, saveButton]
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
        
        if stage == "Setting":
            #Important: below line is for test use

            left = Button((400,548,144,192),"Img\\defaultSkin\\left.png")
            right = Button((400,548,240,288),"Img\\defaultSkin\\right.png")
            up = Button((400,548,336,384),"Img\\defaultSkin\\up.png")
            down = Button((400,548,432,480),"Img\\defaultSkin\\down.png")
            vol = Button((400,548,528,576),"Img\\defaultSkin\\vol.png")
            leftbutton = Button((700, 944, 144, 192), "Img\\defaultSkin\\button.png", "cleft", pygame.key.name(self.setting.left))
            rightbutton = Button((700, 944, 240, 288), "Img\\defaultSkin\\button.png", "cright", pygame.key.name(self.setting.right))
            upbutton = Button((700, 944, 336, 384), "Img\\defaultSkin\\button.png","cup", pygame.key.name(self.setting.up))
            downbutton = Button((700, 944, 432, 480), "Img\\defaultSkin\\button.png", "cdown", pygame.key.name(self.setting.down))
            volbutton = Button((700, 944, 528, 576), "Img\\defaultSkin\\button.png","cvol", str(self.setting.vol))
            closeButton = Button((328,376,48,96),"Img\\defaultSkin\\closeButton.png", "Menu")
            self.buttons = [left, right, up, down, vol, leftbutton, rightbutton,upbutton,downbutton,volbutton, closeButton]
        #add
        if stage == "Login":
            #important: below line is for testing
            layout = [[Message.Text('UserName'), Message.InputText()],
                      [Message.Text('PassWord'), Message.InputText()],
                      [Message.Button('Login'), Message.Button('Signup'), Message.Button('Continue')],
                      [Message.Text("", size=(0, 1), key='OUTPUT')]]
            window = Message.Window('Login/Signup', layout)
            while True:
                cause, values = window.read()
                if cause == Message.WIN_CLOSED or cause == 'Continue':  # if user closes window or clicks cancel
                    break
                if cause == 'Login':
                    if self.DBControl.login(values[0], values[1]):
                        output = "Login Success! Press Continue to enjoy your game"
                        window['OUTPUT'].update(value=output)
                    else:
                        output = "Login Failed! :("
                        window['OUTPUT'].update(value=output)

                if cause == 'Signup':
                    if self.DBControl.register(values[0], values[1]):
                        output = "Sign up Success! Press Continue to enjoy your game"
                        window['OUTPUT'].update(value=output)
                    else:
                        output = "Signup Failed! :( The username exists"
                        window['OUTPUT'].update(value=output)
            window.close()
            self.setStage("Menu")
            
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
            

    def drawScreen(self):#add for setting
        if self.stage == "Setting":
            self.background()
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
            t = self.font.render("Highscore: "+str(self.DBControl.highscore),True,BLUE)
            tRect = t.get_rect()
            tRect.center = (100,150)
            self.screen.blit(t,tRect)
        #draw buff icon in maingame
        if self.stage == "MainGame":
            if self.scoreMulti == True:
                self.screen.blit(self.imgScoreMulti,(1010,670))
            if self.speedBoost == True:
                self.screen.blit(self.imgSpeedBoost,(1056,670))
            if self.shield == True:
                self.screen.blit(self.imgShield,(1102,670))
            if self.ghostSlow == True:
                self.screen.blit(self.imgGhostSlow,(1158,670))
        """
        AMENDMENT 4 Call draw gold while in shop
        """
        if self.stage == "Shop" or self.stage == 'Buff_Shop' or self.stage == 'Skin_Shop':
            self.draw_gold_balance()
        """END OF AMENDMENT 4"""
        if (self.stage == "Main Editor"):
            BACKGROUND_DISPLAY = pygame.image.load(os.path.join('Assets','background.PNG'))
            TITLE_DISPLAY = pygame.image.load(os.path.join('Assets','title.png'))
            self.screen.blit(BACKGROUND_DISPLAY,(0,0))
            self.screen.blit(TITLE_DISPLAY,(495,140))
        if (self.stage == "Edit2"):
            TITLE_DISPLAY = pygame.image.load(os.path.join('Assets','Tool Bar.png'))
            TOOL_BAR = pygame.image.load(os.path.join('Assets','Tool_Bar_Border.png'))
            self.screen.blit(TITLE_DISPLAY,(74,36))
            self.screen.blit(TOOL_BAR,(48,115))

    """
    AMENDMENT 5: draw gold function
    """
    def draw_gold_balance(self):
        gold_balance_text = f"Gold: {self.DBControl.gold}"
        gold_balance_font = pygame.font.Font(None, 20)
        gold_balance_surf = gold_balance_font.render(gold_balance_text, True, (255, 255, 255))
        gold_balance_rect = gold_balance_surf.get_rect(topright=(self.screen.get_width() - 20, 20))
        self.screen.blit(gold_balance_surf, gold_balance_rect)
    """END OF AMENDMENT 5"""
    def listen(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in self.buttons:
                if b.isClicked(event.pos):#add sound
                    self.clicksound.play()
                    self.runOperation(b.operation)
                    break
            if self.stage == "Editor":  #EDITOR section here
                pass
        #add change to the key
        if event.type == pygame.KEYDOWN:
            if self.stage == "MainGame":
                if event.key == self.setting.up:
                    self.delayKeyInput = "up"
                if event.key == self.setting.down:
                    self.delayKeyInput = "down"
                if event.key == self.setting.left:
                    self.delayKeyInput = "left"
                if event.key == self.setting.right:
                    self.delayKeyInput = "right"
                self.paused = False

    def runOperation(self, operation):
        if operation == "Quit":
            pygame.quit()
            sys.exit()
        if operation == "MainGame":
            self.setStage("MainGame")
            self.mainGameInit("Map\\test.txt")
        if operation == "MainGameLocal":
            self.setStage("MainGame")
            self.mainGameInit("Map\\mapLocal.txt")
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
        """    """Shop functions"""
    
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

        # Buff shop actions;             
        if operation == 'upgrade_buff0':
            self.response(self.shop.upgrade_buff(0), "Notice")
            self.setStage('Buff_Shop')
        if operation == 'upgrade_buff1':
            self.response(self.shop.upgrade_buff(1), "Notice")
            self.setStage('Buff_Shop')
        if operation == 'upgrade_buff2':
            self.response(self.shop.upgrade_buff(2), "Notice")
            self.setStage('Buff_Shop')
        if operation == 'upgrade_buff3':
            self.response(self.shop.upgrade_buff(3), "Notice")
            self.setStage('Buff_Shop')
        if operation == 'upgrade_buff4':
            self.response(self.shop.upgrade_buff(4), "Notice")
            self.setStage('Buff_Shop')

        # Skin shop actions               
        if operation == 'previous_skin':
            current_skin_idx = (current_skin_idx - 1) % len(self.dbcontrol.skin)
            self.setStage('Skin_Shop')
            # Missing: draw the icon of current_index-th skin

        if operation == 'next_skin':
            current_skin_idx = (current_skin_idx + 1) % len(self.dbcontrol.skin)
            self.setStage('Skin_Shop')
            # Missing: draw the icon of current_index-th skin

        if operation == 'buy_skin':
            self.response(self.shop.buy_skin(current_skin_idx), "Notice")
            self.setStage('Skin_Shop')

        if operation == 'equip_skin':
            self.response(self.shop.equip_skin(current_skin_idx), "Notice")
            self.setStage('Skin_Shop')
        #add
        if operation == "cleft":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.setting.keyBinding("left", event.key)
                        self.buttons[5] = Button((700, 944, 144, 192), "Img\\defaultSkin\\button.png", "cleft",pygame.key.name(self.setting.left))
                        return
        #add
        if operation == "cright":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.setting.keyBinding("right", event.key)
                        self.buttons[6] = Button((700, 944, 240, 288), "Img\\defaultSkin\\button.png", "cright",pygame.key.name(self.setting.right))
                        return
        #add
        if operation == "cup":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.setting.keyBinding("up", event.key)
                        self.buttons[7] = Button((700, 944, 336, 384), "Img\\defaultSkin\\button.png", "cup", pygame.key.name(self.setting.up))
                        return
        #add
        if operation == "cdown":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.setting.keyBinding("down", event.key)
                        self.buttons[8] = Button((700, 944, 432, 480), "Img\\defaultSkin\\button.png", "cdown",pygame.key.name(self.setting.down))
                        return
        #add
        if operation == "cvol":
            layout = [[Message.Text("Input a value between 0 to 100")],
                      [Message.Input()], [Message.Button("Confirm"), Message.Button("Cancel")]]
            window = Message.Window('Volume change', layout)
            while True:
                cause, values = window.read()
                if cause == Message.WIN_CLOSED or cause == 'Cancel':  # if user closes window or clicks cancel
                    break
                if cause == "Confirm":
                    self.setting.volumeChange(int(values[0]))
                    break
            window.close()
            self.buttons[9] = Button((700, 944, 528, 576), "Img\\defaultSkin\\button.png", "cvol", str(self.setting.vol))
            self.clicksound.set_volume(self.setting.vol/100)
            self.music.set_volume(self.setting.vol / 100)
            self.eatsound.set_volume(self.setting.vol / 100)
            return
        if operation == "Setting":
            self.setStage("Setting")
        if operation == "Login":
            self.setStage("Login")
        #save to both local and server
        if operation == "DBSaveMap":
            self.paused = True
            self.DBControl.mapdata = self.saveMap("Map\\mapLocal.txt")
            successful = self.DBControl.save()
            if not successful:
                self.response("Failed to save to database, have you logged in?", "Failed")
            else:
                self.response("Saved to database, you may quit now.","Successful")
        if operation == "DownloadALL":
            self.downloadALL()
        if operation == "UploadData":
            successful = self.DBControl.upload()
            if not successful:
                self.response("Failed to upload to database, have you logged in?", "Failed")
            else:
                self.response("User data saved to database.","Successful")


    def response(self, text, windowname):
        layout = [[Message.Text(text)],
                    [Message.Button('OK')]]
        window = Message.Window(windowname, layout)
        while True:
            cause, values = window.read()
            if cause == Message.WIN_CLOSED or cause == 'OK':  # if user closes window or clicks cancel
                break
        window.close()

    def mainGameInit(self, mapPath):
        self.score = 0
        self.life = self.extra_life[self.DBControl.buff[0]]
        self.ghost = []
        self.paused = True
        self.ghostSpeed = 2
        self.pacmanSpeed = 3
        self.scoreMulti = False
        self.scoreMultiDuration = 0
        self.speedBoost = False
        self.speedBoostDuration = 0
        self.shield = False
        self.shieldDuration = 0
        self.ghostSlow = False
        self.ghostSlowDuration = 0
        self.eatCount = 0
        self.importMap(mapPath)
        self.drawMap(self.map)

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
                elif map[i][j] == "5":  #scoreMulti
                    self.screen.blit(self.imgScoreMulti, (280+36*j,36*i))
                elif map[i][j] == "6": 
                    self.screen.blit(self.imgSpeedBoost, (280+36*j,36*i))
                elif map[i][j] == "7": 
                    self.screen.blit(self.imgShield, (280+36*j,36*i))
                elif map[i][j] == "8":  
                    self.screen.blit(self.imgGhostSlow, (280+36*j,36*i))

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

    def mapToString(self, map):
        s = ""
        for i in range(0,20):
            for j in range(0,20):
                s += str(self.map[i][j])
        return s
    
    def stringToMap(self, str):
        pass

    #import local "mapPath" into Pacman.map
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
    
    def downloadALL(self):
        successful = self.DBControl.download()
        if successful:
            self.shop = Shop(self.DBControl)
            self.response("Downloaded", "Successful")
            mapLocal = open("Map\\mapLocal.txt", "w")
            mapLocal.write(self.DBControl.mapdata)
            mapLocal.close()
        else:
            self.response("Not downloaded, have you logged in?", "Failed")


    #save Pacman.map to local mapPath
    def saveMap(self, mapPath):
        s = ""
        tempmap = []
        for i in range(0,20):
            line = []
            for j in range(0,20):
                line.append(self.map[i][j])
            tempmap.append(line)

        tempmap[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "3"
        for ghost in self.ghosts:
            tempmap[ghost[0]][ghost[1]] = "4"
        for i in range(0,20):
            for j in range(0,20):
                s += str(tempmap[i][j])
        map = open(mapPath, "w")
        map.write(s)
        map.close()
        return s    #this s is a 400 string


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
                tempSpeed = self.pacmanSpeed
                if self.speedBoost == True:
                    tempSpeed *= 2
                if self.pacmanDir == "right" and self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]+1]!="2":
                    self.pacmanRealPos[0] += tempSpeed
                    self.stopped = False
                elif self.pacmanDir == "left" and self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]-1]!="2":
                    self.pacmanRealPos[0] -= tempSpeed
                    self.stopped = False
                elif self.pacmanDir == "up" and self.map[self.pacmanGridPos[0]-1][self.pacmanGridPos[1]]!="2":
                    self.pacmanRealPos[1] -= tempSpeed
                    self.stopped = False
                elif self.pacmanDir == "down" and self.map[self.pacmanGridPos[0]+1][self.pacmanGridPos[1]]!="2":
                    self.pacmanRealPos[1] += tempSpeed
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
                    tempSpeed = self.ghostSpeed
                    if self.ghostSlow == True:
                        tempSpeed = 1
                    if ghost[4] == "right" and self.map[ghost[0]][ghost[1]+1]!="2":
                        ghost[2] += tempSpeed
                    elif ghost[4] == "left" and self.map[ghost[0]][ghost[1]-1]!="2":
                        ghost[2] -= tempSpeed
                    elif ghost[4] == "up" and self.map[ghost[0]-1][ghost[1]]!="2":
                        ghost[3] -= tempSpeed
                    elif ghost[4] == "down" and self.map[ghost[0]+1][ghost[1]]!="2":
                        ghost[3] += tempSpeed

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
                    if self.shield == False:
                        self.life -= 1
                        #loses
                        if self.life <= 0:
                            self.DBControl.highscore = max(self.score,self.DBControl.highscore)
                            self.DBControl.gold += self.score//10
                            self.setStage("GameOverAnimation")
                        else:
                            self.pacmanGridPos[0] = self.pacmanInitPos[0]
                            self.pacmanGridPos[1] = self.pacmanInitPos[1]
                            self.pacmanRealPos = [280+36*self.pacmanInitPos[1],36*self.pacmanInitPos[0]]
                            self.paused = True
                            self.pacmanDir = "right"
                if self.isWinning():
                        self.DBControl.highscore = max(self.score,self.DBControl.highscore)
                        self.DBControl.gold += self.score//10
                        self.setStage("Win")
            #eat pacdot and other objects
            if self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] == "1":
                if self.scoreMulti == True:
                    self.score += 20 
                else:
                    self.score += 10
                #spawn random buff after eating 20dots
                self.eatCount += 1
                if self.eatCount >= 20:
                    self.eatCount = 0
                    self.spawnBuff()
                self.eatsound.play()
                self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "0"
            #score multi
            if self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] == "5":
                self.scoreMulti = True
                self.scoreMultiDuration = self.score_multiplier_duration[self.DBControl.buff[1]] * 40
                self.eatsound.play()
                self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "0"
            #speedBoost
            if self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] == "6":
                self.speedBoost = True
                self.speedBoostDuration = self.speed_boost_duration[self.DBControl.buff[2]] * 40
                self.eatsound.play()
                self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "0"
            #shield
            if self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] == "7":
                self.shield = True
                self.shieldDuration = self.repellant_shield_duration[self.DBControl.buff[3]] * 40
                self.eatsound.play()
                self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "0"
            #ghostSlow
            if self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] == "8":
                self.ghostSlow = True
                self.ghostSlowDuration = self.ghost_slow_duration[self.DBControl.buff[4]] * 40
                self.eatsound.play()
                self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "0"

            #duration decrease
            if self.scoreMultiDuration>0:
                self.scoreMultiDuration-=1
                if self.scoreMultiDuration <= 0:
                    self.scoreMulti = False
            if self.speedBoostDuration>0:
                self.speedBoostDuration-=1
                if self.speedBoostDuration <= 0:
                    self.speedBoost = False
            if self.shieldDuration>0:
                self.shieldDuration-=1
                if self.shieldDuration <= 0:
                    self.shield = False
            if self.ghostSlowDuration>0:
                self.ghostSlowDuration-=1
                if self.ghostSlowDuration <= 0:
                    self.ghostSlow = False
    
    def spawnBuff(self):
        #spawn randomly on empty squares
        emptySpace = []
        for i in range(20):
            for j in range(20):
                if self.map[i][j] == "0":
                    if not(i==self.pacmanGridPos[0] and j==self.pacmanGridPos[1]):
                        emptySpace.append([i,j])
        chosenSpace = random.choice(emptySpace)
        self.map[chosenSpace[0]][chosenSpace[1]] = str(5+random.randint(0,3))   #a random buff

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
#use this to create new map
'''
pacman.map = [
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,4,0,0,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 3,1,1,1,1, 2,2,2,2,2],
    
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2],
    [2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2, 2,2,2,2,2]
]
pacman.saveMap("Map\\smalltest.txt")
pacman.importMap("Map\\smalltest.txt")
'''

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