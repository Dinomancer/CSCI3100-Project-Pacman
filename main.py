import sys
import pygame
import random
import time
from shop import Shop
from DBControl import DBControl
import PySimpleGUI as Message
from Setting import Setting
import os

#binding the color we want to use to color name
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
    ghostSpeed = 1
    map = None
    pacmanGridPos = [0,0]
    pacmanRealPos = [0,0]
    pacmanInitPos = [0,0]
    pacmanDir = "right"
    pacmanMove = False
    ghosts = []     #in the format of [x,y,gridx,gridy,dir,img]
    stopped = False
    delayKeyInput = None

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
    score_multiplier_duration = [2, 5, 7, 10, 12, 15]
    speed_boost_duration = [2, 5, 7, 10, 12, 15]
    repellant_shield_duration = [2, 5, 7, 10, 12, 15]
    ghost_slow_duration = [2, 5, 7, 10, 12, 15]
    # For future expansion: score_multiplier = [1.5, 1.5, 2.0, 2.0, 2.5, 2.5]
    # For future expansion: speed_boost_multiplier = [1.1, 1.1, 1.15, 1.2, 1.25, 1.3]
    # For future expansion: ghost_slow_multiplier = [0.9, 0.75, 0.7, 0.65, 0.6, 0.5]

    #initilize the pacman object
    def __init__(self):
        #Initilize level
        self.levelCount = "Easy"
        #Create setting object
        self.setting = Setting()
        #Create dbcontrol object
        self.DBControl = DBControl()
        #Create shop object
        self.shop = Shop(self.DBControl)
        #add button click sound
        self.clicksound = pygame.mixer.Sound("music\\click.mp3")
        #add eat sound
        self.eatsound = pygame.mixer.Sound("music\\coin.mp3")
        #initlize the screen the game use
        self.screen = pygame.display.set_mode((1280, 720))
        #the screen title
        pygame.display.set_caption('Pacman')
        #the game font
        self.font = pygame.font.Font('Nunito-Medium.ttf',25)
        #editMap is the map editor editing item is the tool user choose
        #item is the item place in map editor
        #pacplace is whether the pacman has been place
        self.editMap = []
        self.item = 0
        self.pacplace = False
        #equip is the number of skin, if equip == 0 means first skin is equipped
        self.equip = 0
        #view is the number of skin in skin shop, if view == 0, means player is viewing first skin in the skin shop
        self.view = 0
        # to indicate which button is running operation
        self.activeButton = None
        self.setStage("Menu")
        #img load
        self.imgWall = pygame.image.load("Img\\defaultSkin\\wall.png").convert()
        self.imgPacman = pygame.image.load("Img\\defaultSkin\\pacman.png").convert()
        self.imgPacman.set_colorkey(BLACK)
        self.imgGhost = pygame.image.load("Img\\defaultSkin\\ghost00.png").convert()
        self.imgGhost.set_colorkey(BLACK)
        self.imgGhost = pygame.transform.scale(self.imgGhost, (36,36))
        self.imgGhosts = []
        for i in range(4):
            self.imgGhosts.append(pygame.image.load("Img\\defaultSkin\\ghost"+str(i)+str(self.equip)+".png").convert())
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
        self.imgPlayLocal = pygame.image.load("Img\\defaultSkin\\playLocal.png").convert()

    # this function draws the background to the screen
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
    # this function set the stage (i.e. different window). Each stage has different buttons and layout. 
    def setStage(self, stage):
        self.stage = stage
        #to MENU
        if stage == "Menu":
            self.ghosts = []
            self.levelCount = "Easy"
            
            notice = Button((390,890,30,110),"Img\\defaultSkin\\notice.png", None)
            welcome = Button((465,815,110,250),"Img\\defaultSkin\\welcome.png", None)
            playLocalButton = Button((680,780,260,360),"Img\\defaultSkin\\playLocal.png", "MainGameLocal")#plays mapLocal.txt
            startButton = Button((500,600,260,360),"Img\\defaultSkin\\startButton.png", "MainGame")  #plays level easy
            shopButton = Button((480,800,500,580), "Img\\defaultSkin\\shop.png", "enter_shop")
            loginButton = Button((480,800,400,480), "Img\\defaultSkin\\login-logout.png", "Login")
            settingButton = Button((20,70,10,60), "Img\\defaultSkin\\setting.png", "Setting")
            downloadButton = Button((280,440,420,460),"Img\\defaultSkin\\download-user-data.png", "DownloadALL")
            uploadButton = Button((840,1000,420,460),"Img\\defaultSkin\\upload-user-data.png", "UploadData")
            editorButton = Button((480,800,600,680),"Img\\defaultSkin\\map-editor.png", "MainEditor")
            restartButton = Button((1150,1200,10,60),"Img\\defaultSkin\\restartButton.png", "Menu")
            closeButton = Button((1210,1260,10,60),"Img\\defaultSkin\\closeButton.png", "Quit")
            clearHighScoreButton = Button((1150,1260,70,100),"Img\\defaultSkin\\clear-high-score.png", "clearHighScore")
            self.buttons = [notice, welcome, closeButton, startButton, restartButton, shopButton, loginButton, settingButton, downloadButton, uploadButton, editorButton, playLocalButton, clearHighScoreButton]
        #to Shop Main Window
        if stage == "Shop":     
            quitButton = Button((20, 70, 10, 60), "Img\\defaultSkin\\return.png", 'exit_shop')
            buffShopButton = Button ((450, 830, 300, 420), "Img\\Button\\button_buff-shop.png", 'enter_buff_shop')
            skinShopButton = Button ((450, 830, 480, 600), "Img\\Button\\button_skin-shop.png", 'enter_skin_shop')
            restartButton = Button((1150, 1200, 10, 60), "Img\\defaultSkin\\restartButton.png", "Menu")
            closeButton = Button((1210, 1260, 10, 60), "Img\\defaultSkin\\closeButton.png", "Quit")
            clearHighScoreButton = Button((1150, 1260, 70, 100), "Img\\defaultSkin\\clear-high-score.png",
                                          "clearHighScore")
            self.buttons = [quitButton, buffShopButton, skinShopButton, restartButton, closeButton, clearHighScoreButton]
        # to Buff_Shop
        if stage == 'Buff_Shop' :
            quitButton = Button((20, 70, 10, 60), "Img\\defaultSkin\\return.png", 'return_to_shop_menu')
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
            restartButton = Button((1150, 1200, 10, 60), "Img\\defaultSkin\\restartButton.png", "Menu")
            closeButton = Button((1210, 1260, 10, 60), "Img\\defaultSkin\\closeButton.png", "Quit")
            clearHighScoreButton = Button((1150, 1260, 70, 100), "Img\\defaultSkin\\clear-high-score.png",
                                          "clearHighScore")
            lv = []
            for i in range(5): # blit the corresponding icon for each level
                lv.append(Button((340 + 125 * i, 440 + 125 * i, 160, 600), "Img\\Shop\\Lv{}.png".format(self.DBControl.buff[i]), None))
                
            self.buttons = [quitButton, buff0,icon0, buff1,icon1, buff2,icon2, buff3,icon3, buff4,icon4, lv[0],lv[1],lv[2],lv[3],lv[4], closeButton, restartButton, clearHighScoreButton]
        # to Skin_Shop 
        if stage == 'Skin_Shop':
            quitButton = Button((20, 70, 10, 60), "Img\\defaultSkin\\return.png", 'return_to_shop_menu')
            leftButton = Button((350, 400, 520, 560), "Img\\Button\\left_unclick.png", 'previous_skin')
            rightButton = Button((880, 930, 520, 560), "Img\\Button\\right_unclick.png", 'next_skin')
            buyButton = Button((540, 740, 480, 560), "Img\\Button\\button_buy.png", 'buy_skin')
            equipButton = Button((540, 740, 600, 680), "Img\\Button\\button_equip.png", 'equip_skin')
            restartButton = Button((1150, 1200, 10, 60), "Img\\defaultSkin\\restartButton.png", "Menu")
            closeButton = Button((1210, 1260, 10, 60), "Img\\defaultSkin\\closeButton.png", "Quit")
            clearHighScoreButton = Button((1150, 1260, 70, 100), "Img\\defaultSkin\\clear-high-score.png", "clearHighScore")

            self.buttons = [quitButton, leftButton, rightButton, buyButton, equipButton, restartButton, closeButton, clearHighScoreButton]
        # to MapEditor Main Window
        if stage == "MainEditor":  # EDITOR: put all buttons present in the editor here
            returnButton = Button((20, 70, 10, 60), "Img\\defaultSkin\\return.png", "Menu")
            editButton = Button((517, 817, 269, 349), "Img\\defaultSkin\\editMapButton.png", "gotoEdit")
            downloadButton = Button((517, 817, 400, 480), "Img\\defaultSkin\\downloadMapButton.png", "gotoDownload")
            restartButton = Button((1150, 1200, 10, 60), "Img\\defaultSkin\\restartButton.png", "Menu")
            closeButton = Button((1210, 1260, 10, 60), "Img\\defaultSkin\\closeButton.png", "Quit")
            clearHighScoreButton = Button((1150, 1260, 70, 100), "Img\\defaultSkin\\clear-high-score.png",
                                          "clearHighScore")
            self.buttons = [editButton, downloadButton, returnButton,closeButton, clearHighScoreButton, restartButton]
     
        # to editing view of map editor
        if stage == "Edit2":
            self.editMap = []
            self.pacplace = False
            for i in range(20):
                row = []
                for j in range(20):
                    if (i == 0 or j == 0 or i == 19 or j == 19):
                        row.append(2)
                    else:
                        row.append(0)
                self.editMap.append(row)
            # initialize buttons in this screen
            wallButton = Button((101, 162, 161, 217), "Assets\\Wall_Icon.png", "wall")
            ghostButton = Button((95, 170, 256, 332), "Assets\\Ghost_Icon.png", "ghost")
            pacmanButton = Button((109, 169, 371, 431), "Assets\\Pacman_Icon.png", "pacman")
            clearButton = Button((95, 170, 470, 546), "Img\\defaultSkin\\button_x.png", "clear")
            fillButton = Button((1080, 1250, 100, 150), "Img\\defaultSkin\\button_fill.png", "fillWithPac")
            uploadButton = Button((1080, 1250, 250, 300), "Img\\defaultSkin\\button_upload.png", "editMapUpload")
            saveButton = Button((1080, 1250, 400, 450), "Img\\defaultSkin\\button_save.png", "saveEditMap")
            exitButton = Button((1080, 1250, 550, 600), "Img\\defaultSkin\\button_exit.png", "Menu")

            self.buttons = [wallButton, ghostButton, pacmanButton, saveButton, clearButton, uploadButton, exitButton,
                            saveButton, fillButton]
            for i in range(20):
                for j in range(20):
                    if i == 0 or j == 0 or i == 19 or j == 19:
                        block = Button((j * 36 + 280, j * 36 + 280 + 36, i * 36, i * 36 + 36), "Assets\\Wall_Icon.png",
                                       "place", str(i) + "," + str(j), 1)
                    else:
                        block = Button((j * 36 + 280, j * 36 + 280 + 36, i * 36, i * 36 + 36), "Assets\\empty.png",
                                       "place", str(i) + "," + str(j), 1)

                    self.buttons.append(block)
        #toMainGame
        if stage == "MainGame":
            closeButton = Button((1210,1260,10,60),"Img\\defaultSkin\\closeButton.png", "Quit")
            pauseButton = Button((20,70,10,60),"Img\\defaultSkin\\pauseButton.png", "Pause")
            saveButton = Button((80,130,10,60),"Img\\defaultSkin\\download.png", "DBSaveMap")
            restartButton = Button((1150,1200,10,60),"Img\\defaultSkin\\restartButton.png", "Menu")
            clearHighScoreButton = Button((1150, 1260, 70, 100), "Img\\defaultSkin\\clear-high-score.png","clearHighScore")
            self.buttons = [closeButton, pauseButton, restartButton, saveButton, clearHighScoreButton]
        #toGameOver Animation Screen (an animation before static game over screen)
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
        # to Setting
        if stage == "Setting":
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
       
        #to login screen
        if stage == "Login":
            layout = [[Message.Text('UserName'), Message.InputText()],
                      [Message.Text('PassWord'), Message.InputText()],
                      [Message.Button('Login'), Message.Button('Signup'), Message.Button('Continue'), Message.Button('Log out')],
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

                if cause == 'Log out':
                    txt = open("highscore.txt", "w")
                    txt.write(str(self.DBControl.highscore))
                    txt.close()
                    self.DBControl = DBControl()
                    output = "Log out Success!"
                    window['OUTPUT'].update(value=output)
            window.close()
            self.setStage("Menu")
        # to GameOver screen 
        if stage == "GameOver":
            self.ghosts = []
            restartButton1 = Button((640-100,640+100,460-40,460+40),"Img\\defaultSkin\\buttonFrame.png", "Menu", "Back To Menu")
            restartButton = Button((1150, 1200, 10, 60), "Img\\defaultSkin\\restartButton.png", "Menu")
            closeButton = Button((1210, 1260, 10, 60), "Img\\defaultSkin\\closeButton.png", "Quit")
            clearHighScoreButton = Button((1150, 1260, 70, 100), "Img\\defaultSkin\\clear-high-score.png",
                                          "clearHighScore")
            text = Button((640,640,250,250),None,None,"Game Over")
            text1 = Button((640,640,300,300),None,None,"Score :"+str(self.score))
            self.buttons = [restartButton1, closeButton, restartButton, text, text1, clearHighScoreButton]
        #to Win Screen
        if stage == "Win":
            self.ghosts = []
            restartButton = Button((1150, 1200, 10, 60), "Img\\defaultSkin\\restartButton.png", "Menu")
            closeButton = Button((1210, 1260, 10, 60), "Img\\defaultSkin\\closeButton.png", "Quit")
            clearHighScoreButton = Button((1150, 1260, 70, 100), "Img\\defaultSkin\\clear-high-score.png",
                                          "clearHighScore")
            text = Button((640,640,250,250),None,None,"You Win")
            text1 = Button((640,640,300,300),None,None,"Score :"+str(self.score))
            self.buttons = [closeButton, restartButton, clearHighScoreButton, text, text1]
            if self.levelCount == "Easy":
                self.levelCount = "Medium"
                continueButton = Button((640-100,640+100,460-40,460+40),"Img\\defaultSkin\\next-level.png", "MainGameMedium")
                self.buttons.append(continueButton)
            elif self.levelCount == "Medium":
                self.levelCount = "Hard"
                continueButton = Button((640-100,640+100,460-40,460+40),"Img\\defaultSkin\\next-level.png", "MainGameHard")
                self.buttons.append(continueButton)
            elif self.levelCount == "Hard":
                self.levelCount = "Easy"
            
    #draw the set stage to the screen
    def drawScreen(self):
        if self.stage == "Setting":
            self.background()
        if (not self.map == None) and (self.stage=="MainGame" or self.stage=="GameOverAnimation"):   #SHOP/EDITOR: modify this line to hide the game map
            self.drawMap(self.map)
        # draw highscore and score [please double check not sure]
        for b in self.buttons:
            b.draw(self.screen)
        
    
        if self.stage == "Buff_Shop":
            imgToLoad = pygame.image.load("Img\\defaultSkin\\costlist.png")
            priceimg = pygame.transform.scale(imgToLoad, (220, 200))
            self.screen.blit(priceimg, (1000, 300))
        if self.stage == "Skin_Shop":
            if self.view == 0:
                t = self.font.render("Price: " + "FREE", True, WHITE)
            elif self.view > 0:
                t = self.font.render("Price: " + "$" + str(self.shop.skin_price[self.view]), True, WHITE)
            
            tRect = t.get_rect()
            tRect.center = (640, 440)
            self.screen.blit(t,tRect)
            imgPath = "Img\\defaultSkin\\ghost0"+ str(self.view) + ".png"
            imgToLoad = pygame.image.load(imgPath).convert()
            if self.view == 2: # To fix conversion error
                imgToLoad = pygame.image.load(imgPath)
            skinimg = pygame.transform.scale(imgToLoad, (360, 360))
            self.screen.blit(skinimg, (460, 60))
        if self.stage not in ["Edit2"]:
            if self.stage in ["MainGame"]:
                t = self.font.render("Score: "+str(self.score),True,WHITE)
            else:
                t = self.font.render("Gold: " + str(self.DBControl.gold), True, WHITE)
            tRect = t.get_rect()
            tRect.center = (100, 100)
            self.screen.blit(t,tRect)
            t = self.font.render("Highscore: "+str(self.DBControl.highscore),True,WHITE)
            tRect = t.get_rect()
            tRect.center = (100,150)
            self.screen.blit(t,tRect)
            t = self.font.render("Username: "+str(self.DBControl.username),True,WHITE)
            tRect = t.get_rect()
            tRect.center = (100,200)
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

        if (self.stage == "MainEditor"):
            self.background()
            TITLE_DISPLAY = pygame.image.load(os.path.join('Assets', 'title.png'))
            self.screen.blit(TITLE_DISPLAY, (495, 140))
        if (self.stage == "Edit2"):
            TITLE_DISPLAY = pygame.image.load(os.path.join('Assets', 'Tool Bar.png'))
            TOOL_BAR = pygame.image.load(os.path.join('Assets', 'Tool_Bar_Border.png'))
            self.screen.blit(TITLE_DISPLAY, (74, 36))
            self.screen.blit(TOOL_BAR, (48, 115))

    # this function is for listen to event
    def listen(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # for clicked button
            for b in self.buttons:
                if b.isClicked(event.pos):
                    self.clicksound.play()
                    self.activeButton = b
                    self.runOperation(b.operation)
                    self.activeButton = None
                    break
            if self.stage == "Editor":  
                pass
        # for clicked key on keyboard
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

    # this function is to run important operations based on the button user click, each button has an operation
    def runOperation(self, operation):
        #to quit the game 
        if operation == "Quit":
            txt = open("highscore.txt", "w")
            txt.write(str(self.DBControl.highscore))
            txt.close()
            pygame.quit()
            sys.exit()
        # when first starting the main game, difficulty is set to easy and main game stage is set
        if operation == "MainGame":
            self.levelCount = "Easy"
            self.setStage("MainGame")
            self.mainGameInit("Map\\easy.txt")
        # when passing first difficulty, difficulty is set to medium and main game stage is set
        if operation == "MainGameMedium":
            self.levelCount = "Medium"
            self.setStage("MainGame")
            self.mainGameInit("Map\\medium.txt")
        # when passing second difficulty, difficulty is set to hard and main game stage is set
        if operation == "MainGameHard":
            self.levelCount = "Hard"
            self.setStage("MainGame")
            self.mainGameInit("Map\\hard.txt")
        # play local created map
        if operation == "MainGameLocal":
            self.levelCount = "Custom"
            self.setStage("MainGame")
            self.mainGameInit("Map\\mapLocal.txt")
        # return to menu
        if operation == "Menu":
            self.score = 0
            self.setStage("Menu")
        # to pause the game
        if operation == "Pause":
            if self.paused == True:
                self.paused = False
            else:
                self.paused = True
        if operation == "clearHighScore":
            self.DBControl.highscore = 0

        """BELOW ARE SHOP RELATED FUNCTIONS"""
        #to enter the shop
        if operation == "enter_shop":
            self.setStage('Shop')

        #to enter buff shop in the shop
        if operation == "enter_buff_shop":
            self.setStage('Buff_Shop')

        #to enter skin shop in the shop
        if operation == "enter_skin_shop":
            self.setStage('Skin_Shop')

        # following two operations are for exit and return back to menu
        if operation == "exit_shop":
            self.setStage('Menu')
        
        if operation == "return_to_shop_menu":
            self.setStage('Shop')

        # Buff shop actions;
        #upgrade buff level
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
        # change skin selection
        if operation == 'previous_skin':
            self.view -= 1
            if self.view < 0:
                self.view = 2
            self.setStage('Skin_Shop')

        if operation == 'next_skin':
            self.view += 1
            if self.view > 2:
                self.view = 0
            self.setStage('Skin_Shop')
        #buy skin
        if operation == 'buy_skin':
            self.response(self.shop.buy_skin(self.view), "Notice")
            self.setStage('Skin_Shop')
            
        #if user decide to equip skin,the ghost would change the apperance
        if operation == 'equip_skin':
            self.response(self.shop.equip_skin(self.view), "Notice")
            if self.DBControl.skin[self.view] == 2:
                self.equip = self.view
            self.imgGhosts = []
            for i in range(4):
                if self.view == 2:
                    self.imgGhosts.append(
                        pygame.image.load("Img\\defaultSkin\\ghost" + str(i) + str(self.equip) + ".png"))
                else: # To fix conversion incompatibility
                    self.imgGhosts.append(
                        pygame.image.load("Img\\defaultSkin\\ghost" + str(i) + str(self.equip) + ".png").convert())
                self.imgGhosts[i].set_colorkey(BLACK)
                self.imgGhosts[i] = pygame.transform.scale(self.imgGhosts[i], (36, 36))

            self.setStage('Skin_Shop')
       
        """BELOW ARE SETTING RELATED FUNCTIONS"""
        #change the respective key to the user input by catching the userinput
        if operation == "cleft":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.setting.keyBinding("left", event.key)
                        self.buttons[5] = Button((700, 944, 144, 192), "Img\\defaultSkin\\button.png", "cleft",pygame.key.name(self.setting.left))
                        return
       
        if operation == "cright":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.setting.keyBinding("right", event.key)
                        self.buttons[6] = Button((700, 944, 240, 288), "Img\\defaultSkin\\button.png", "cright",pygame.key.name(self.setting.right))
                        return
        
        if operation == "cup":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.setting.keyBinding("up", event.key)
                        self.buttons[7] = Button((700, 944, 336, 384), "Img\\defaultSkin\\button.png", "cup", pygame.key.name(self.setting.up))
                        return
        
        if operation == "cdown":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.setting.keyBinding("down", event.key)
                        self.buttons[8] = Button((700, 944, 432, 480), "Img\\defaultSkin\\button.png", "cdown",pygame.key.name(self.setting.down))
                        return
        #for change volume
        if operation == "cvol":
            layout = [[Message.Text("Input a value between 0 to 100")],
                      [Message.Input()], [Message.Button("Confirm"), Message.Button("Cancel")]]
            window = Message.Window('Volume change', layout)
            while True:
                cause, values = window.read()
                if cause == Message.WIN_CLOSED or cause == 'Cancel':  # if user closes window or clicks cancel
                    break
                if cause == "Confirm":
                    try:
                        vol = int(values[0])
                        if 0 <= vol and vol <= 100:
                            self.setting.volumeChange(vol)
                            break
                        else:
                            continue
                    except:
                        continue
            window.close()
            self.buttons[9] = Button((700, 944, 528, 576), "Img\\defaultSkin\\button.png", "cvol", str(self.setting.vol))
            self.clicksound.set_volume(self.setting.vol/100)
            self.eatsound.set_volume(self.setting.vol / 100)
            return
    
        """BELOW ARE MAIN-MENU AND DATABASE RELATED FUNCTIONS"""
        #enter setting page
        if operation == "Setting":
            self.setStage("Setting")
        #enter login page
        if operation == "Login":
            self.setStage("Login")
        #the following 3 operations intearct with the DBControl Module to save, upload and download map
        #save to both local and server
        if operation == "DBSaveMap":
            self.paused = True
            self.DBControl.mapdata = self.saveMap("Map\\mapLocal.txt")
            successful = self.DBControl.save()
            if not successful:
                self.response("Save to local only. Login to save to database", "Failed")
            else:
                self.response("Saved to database and local, you may quit now.","Successful")
        if operation == "DownloadALL":
            self.downloadALL()
        if operation == "UploadData":
            successful = self.DBControl.upload()
            if not successful:
                self.response("Failed to upload to database, have you logged in?", "Failed")
            else:
                self.response("User data saved to database.","Successful")
                
        """BELOW ARE MAP EDITOR RELATED FUNCTIONS"""
        #enter maineditor page
        if operation == "MainEditor":
            self.setStage("MainEditor")
        #enter edit a map page
        if operation == "gotoEdit":
            self.setStage("Edit2")
        # set up the download window with the aid of PygameGUI and interact with the DBControl to print different messages.
        if operation == "gotoDownload":
            input = ""
            layout = [[Message.Text('Please Input a MapCode:'), Message.InputText()],
                      [Message.Button('Done'), Message.Button('Return')], [Message.Text("", key='-TEXT-')]]
            window = Message.Window("Download Window", layout)
            self.DBControl.login_flag = True
            while True:
                cause, values = window.read()
                if cause == Message.WIN_CLOSED or cause == "Return":
                    break
                input = values[0]
                if cause == "Done":
                    if (self.DBControl.downloadAMap(input) and self.DBControl.login_flag == True):
                        mapLocal = open("Map\\mapLocal.txt", "w")
                        mapLocal.write(self.DBControl.mapdata)
                        mapLocal.close()
                        #call map load function here
                        window['-TEXT-'].update("Download Success")
                    elif (self.DBControl.login_flag == True):
                        window['-TEXT-'].update("Download Failure")
                    else:
                        window['-TEXT-'].update("Please Login First")
            window.close()
            self.stage = "MainEditor"
        # following 5 operations are for placing different items e.g. wall and pacman or clearing
        if operation == "wall":
            self.item = 2
        if operation == "pac":
            # to check if valid place i.e. only one pacman is placed
            if self.pacplace == False:
                self.item = 1
                self.pacplace = True
            else:
                self.response("Can only place one pacman", "place fail")
        if operation == "clear":
            self.item = 0
        if operation == "pacman":
            self.item = 3
        if operation == "ghost":
            self.item = 4
        # for display when user places an item
        if operation == "place":
            imgToLoad = None
            if self.item == 0:
                imgToLoad = pygame.image.load("Assets\\empty.png").convert()
            elif self.item == 2:
                imgToLoad = pygame.image.load("Img\\defaultSkin\\wall.png").convert()
            elif self.item == 3:
                imgToLoad = pygame.image.load("Img\\defaultSkin\\pacman.png").convert()
            elif self.item == 4:
                imgToLoad = pygame.image.load("Img\\defaultSkin\\ghost.png").convert()
            if imgToLoad:
                self.activeButton.img = pygame.transform.scale(imgToLoad, (36, 36))
                text = self.activeButton.text.split(",")
                i = int(text[0])
                j = int(text[1])
                self.editMap[i][j] = self.item
        # to prefill with pacdots
        if operation == "fillWithPac":
            self.item = 1
            imgToLoad = pygame.image.load("Img\\defaultSkin\\pacdot.png").convert()
            for button in self.buttons:
                if button.text:
                    text = button.text.split(",")
                    i = int(text[0])
                    j = int(text[1])
                    if button.edit == 1 and self.editMap[i][j] == 0:
                        self.editMap[i][j] = 1
                        button.img = pygame.transform.scale(imgToLoad, (36, 36))
        #save map to db
        if operation == "editMapUpload":
            s = self.mapToString(self.editMap)
            pacmanCount = 0
            for c in s:
                if c=="3":
                    pacmanCount +=1
            if pacmanCount != 1:
                self.response("Upload Failed! Incorrect pacman number", "Upload")
            else:
                #save to db
                mapcode = self.DBControl.uploadAMap(s)
                if mapcode:
                    self.response("Upload Success! Your map code is %s" % (mapcode), "Upload")
                else:
                    self.response("Upload Failed! Have you logged in?", "Upload")

        #save map to local
        if operation == "saveEditMap":
            s = self.mapToString(self.editMap)
            pacmanCount = 0
            for c in s:
                if c=="3":
                    pacmanCount +=1
            if pacmanCount != 1:
                self.response("Upload Failed! Incorrect pacman number", "Upload")
            else:
                m = open("Map\\mapLocal.txt", "w")
                m.write(s)
                m.close()
                self.response("Save Success to local, you can play it at main menu now", "Save")


    # this function is for reading the input text of the pop up window until the user closes the window or press cancel
    def response(self, text, windowname):
        layout = [[Message.Text(text)],
                    [Message.Button('OK')]]
        window = Message.Window(windowname, layout)
        while True:
            cause, values = window.read()
            if cause == Message.WIN_CLOSED or cause == 'OK':  # if user closes window or clicks cancel
                break
        window.close()

    #initializes the game and all the buffs(powerups) then choose initial direction for ghosts. Pacman is set to be facing right.
    #This function is called when clicking play new game or play local game.
    def mainGameInit(self, mapPath):
        self.pacmanDir = "right"
        self.score = 0
        self.life = int(self.extra_life[int(self.DBControl.buff[0])])
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
        #let ghosts choose initial direction
        for ghost in self.ghosts:
            choices = []
            if self.map[ghost[0]][ghost[1]+1]!="2":
                choices.append("right")
            if self.map[ghost[0]][ghost[1]-1]!="2":
                choices.append("left")
            if self.map[ghost[0]-1][ghost[1]]!="2":
                choices.append("up")
            if self.map[ghost[0]+1][ghost[1]]!="2":
                choices.append("down")
            ghost[4] = random.choice(choices)

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
    # helper function

    #this function change a map that can recongize by the game to a string that can store in database
    def mapToString(self, map1):
        s = ""
        for i in range(0,20):
            for j in range(0,20):
                s += str(map1[i][j])
        return s


    #import local "mapPath"'s mapdata into Pacman.map
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

    # This function connect with DBControl to download all the user data include the past stop game map data.
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


    #save Pacman.map as a txt to local mapPath
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

    #check if pacman way is blocked
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
    #handle cases when path is not blocked and user decide to change direction
    def changePacmanDir(self):
        if not self.isBlocked(self.delayKeyInput):
            if self.pacmanDir == "right" or self.pacmanDir == "left":
                if self.delayKeyInput == "up" or self.delayKeyInput == "down":
                    self.pacmanDir = self.delayKeyInput
            if self.pacmanDir == "up" or self.pacmanDir == "down":
                if self.delayKeyInput == "left" or self.delayKeyInput == "right":
                    self.pacmanDir = self.delayKeyInput
        self.delayKeyInput = None
    #check if ghost is touched
    def isTouchingGhost(self):
        for ghost in self.ghosts:
            if abs(self.pacmanRealPos[0]-ghost[2]) < 30 and abs(self.pacmanRealPos[1]-ghost[3]) < 30:
                return True
        return False
    #check win
    def isWinning(self):
        for i in self.map:
            for j in i:
                if j=="1":
                    return False
        return True
    #function is to handle numerous main game events
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
                # pacman touches ghost
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
                #if user win
                if self.isWinning():
                        self.DBControl.highscore = max(self.score,self.DBControl.highscore)
                        self.DBControl.gold += self.score//10
                        self.setStage("Win")
            if self.paused == True:
                t = self.font.render("Press any key to start", True, WHITE)
                tRect = t.get_rect()
                tRect.center = (1140, 360)
                self.screen.blit(t,tRect)

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
                self.scoreMultiDuration = int(self.score_multiplier_duration[int(self.DBControl.buff[1])]) * 40
                self.eatsound.play()
                self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "0"
            #speedBoost
            if self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] == "6":
                self.speedBoost = True
                self.speedBoostDuration = int(self.speed_boost_duration[int(self.DBControl.buff[2])]) * 40
                self.eatsound.play()
                self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "0"
            #shield
            if self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] == "7":
                self.shield = True
                self.shieldDuration = int(self.repellant_shield_duration[int(self.DBControl.buff[3])]) * 40
                self.eatsound.play()
                self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "0"
            #ghostSlow
            if self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] == "8":
                self.ghostSlow = True
                self.ghostSlowDuration = int(self.ghost_slow_duration[int(self.DBControl.buff[4])]) * 40
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

    #This function spawn buff randomly on empty space in the map
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

    #initlize the button object, a button may or may not have a imgPath, if not, the button is empty; may or may not have a operation,
    #if not, the button will have not click effect; may or may not have a text, if have, the button will have a text on it's image;
    #the edit is only for mapeditor function, it is used to specify whether a button is a block in the map.
    def __init__(self, position, imgPath=None, operation=None, text=None, edit=None):
        if imgPath!=None:
            imgToLoad = pygame.image.load(imgPath).convert()
            self.img = pygame.transform.scale(imgToLoad,(position[1]-position[0],position[3]-position[2]))
        self.position = position
        self.operation = operation
        self.text = text
        self.edit = edit


    #draw the button on the surface
    def draw(self, surface):
        if not self.img == None:
            surface.blit(self.img, (self.position[0],self.position[2]))#FANG
        if not self.text == None and self.edit == None:
            # this line access pacman inside button
            t = pacman.font.render(self.text, True, WHITE)
            tRect = t.get_rect()
            tRect.center = ((self.position[1] + self.position[0]) // 2, (self.position[3] + self.position[2]) // 2)
            surface.blit(t, tRect)
    #check if button clicked
    def isClicked(self, mousePos):
        p = self.position
        if p[0] < mousePos[0] and p[1] > mousePos[0] and p[2] < mousePos[1] and p[3] > mousePos[1]:
            return True
        else:
            return False


#main function
pygame.init()
pacman = Pacman()
clock = pygame.time.Clock()

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
