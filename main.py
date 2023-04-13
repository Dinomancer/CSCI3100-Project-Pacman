import sys
import pygame
#add
import PySimpleGUI as Message

from Setting import Setting
from DBControl import DBControl
import time

Message.theme = ('DarkAmber') # modify this to get other theme
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)

#add this is a function that input two string that can show the dialog

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
    pacmanFrame = 0

    score = 0
    life = 1
    coin = 0
    ghostSpeed = 1
    map = None
    pacmanGridPos = [0,0]
    pacmanRealPos = [0,0]
    pacmanDir = "right"
    pacmanMove = False
    ghosts = []     #[x,y,gridx,gridy,dir]
    stopped = False
    delayKeyInput = None

    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        #self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
        pygame.display.set_caption('Pacman')
        self.font = pygame.font.Font('Nunito-Medium.ttf',50)
        #add music
        self.music = pygame.mixer.Sound("music\\fight.mp3")
        #add button click sound
        self.clicksound = pygame.mixer.Sound("music\\click.mp3")
        #add eat sound need to further play when collision happen with pacman and pac
        self.eatsound = pygame.mixer.Sound("music\\coin.mp3")

        self.setStage("Setting")   #SHOP/EDITOR: to start stage in shop/editor, change this to "Editor"/"Shop"
        self.imgWall = pygame.image.load("Img\\defaultSkin\\wall.png").convert()
        self.imgPacman = pygame.image.load("Img\\defaultSkin\\pacman.png").convert()
        self.imgPacman.set_colorkey(BLACK)
        self.imgGhost = pygame.image.load("Img\\defaultSkin\\ghost.png").convert()
        self.imgGhost.set_colorkey(BLACK)
        self.gifPacman = []
        for i in range(10):
            img = pygame.image.load("Img\\defaultSkin\\pixil-frame-"+str(i)+".png").convert()
            img.set_colorkey(BLACK)
            pygame.transform.scale(img, (36,36))
            self.gifPacman.append(pygame.transform.scale(img, (36,36)))
        self.imgPacdot = pygame.image.load("Img\\defaultSkin\\pacdot.png").convert()
        self.imgWall = pygame.transform.scale(self.imgWall,(36,36))
        self.imgPacman = pygame.transform.scale(self.imgPacman,(36,36))
        self.imgPacdot = pygame.transform.scale(self.imgPacdot,(36,36))
        #add
        self.setting = Setting()
        self.DBControl = DBControl()

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
        if stage == "Menu":
            closeButton = Button((1010,1060,10,60),"Img\\defaultSkin\\closeButton.png", "quit")
            startButton = Button((600,680,320,400),"Img\\defaultSkin\\startButton.png", "MainGame")

            self.buttons = [closeButton, startButton]
        if stage == "Shop":     #SHOP: put all buttons in the shop here
            startButton = Button((600, 680, 320, 400), "Img\\defaultSkin\\startButton.png", "buff1")

        if stage == "Editor":   #EDITOR: put all buttons present in the editor here
            pass
        if stage == "MapEdit":
            closeButton = Button((1010,1060,10,60),"Img\\defaultSkin\\closeButton.png", "quit")

            #self.buttons = []
            for i in range(20):
                for j in range(20):
                    #Button = Button(())
                    block = Button((i,i + 32,j , j + 32), "Img\\defaultSkin\\startButton.png", "place")
                    self.buttons.append(block)
            self.buttons.append(closeButton)
        #add
        if stage == "Setting":
            #Important: below line is for test use
            self.setting = Setting()

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
            closeButton = Button((328,376,48,96),"Img\\defaultSkin\\closeButton.png", "backToMenu")
            self.buttons = [left, right, up, down, vol, leftbutton, rightbutton,upbutton,downbutton,volbutton, closeButton]
        #add
        if stage == "Login":
            #important: below line is for testing
            self.DBControl = DBControl()
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

        if stage == "MainGame":
            closeButton = Button((1010,1060,10,60),"Img\\defaultSkin\\closeButton.png", "quit")
            self.buttons = [closeButton]

    def drawScreen(self):
        if (not self.map == None) and self.stage=="MainGame":   #SHOP/EDITOR: modify this line to hide the game map
            self.drawMap(self.map)
        #add for setting
        if self.stage == "Setting":
            self.background()
        for b in self.buttons:
            b.draw(self.screen)

    def listen(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in self.buttons:
                if b.isClicked(event.pos):
                    #add sound
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


    def runOperation(self, operation):
        if operation == "MainGame":
            self.music.play()
            self.setStage("MainGame")
            self.mainGameInit("MainGame")

        #important: need a opeartion that back to menu

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

    def mainGameInit(self, mapPath):
        self.score = 0
        self.life = 1
        self.coin = 0
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
        for ghost in self.ghosts:
            self.screen.blit(self.imgGhost, (ghost[0],ghost[1]))
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
                elif c=="4": #ghost
                    line.append("0")
                    self.ghosts.append([280+36*j,36*i,i,j,"right"])
                else:
                    line.append(c)
            self.map.append(line)
        map.close()
    
    def saveMap(self, mapPath):
        s = ""
        for i in range(0,20):
            for j in range(0,20):
                if self.map[i][j]=="3":   #fill pacman pos with empty
                    s += "0"
                else:
                    s += str(self.map[i][j])
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

    def changeDir(self):
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
            if abs(self.pacmanRealPos[0]-ghost[0]) < 10 or abs(self.pacmanRealPos[1]-ghost[1]) < 10:
                return True
        return False

    def step(self):
        if self.stage == "MainGame":
            if self.paused == False:
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
                    self.changeDir()
                
                if self.stopped == True:
                        self.changeDir()
                
                if self.stopped == False:
                    self.pacmanFrame += 1
                    if self.pacmanFrame >= 7:
                        self.pacmanFrame = 0
            if self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] == "1":
                self.score += 10
                self.map[self.pacmanGridPos[0]][self.pacmanGridPos[1]] = "0"


class Button:
    img = None
    position = (0, 0, 0, 0)  # x1, x2, y1, y2
    operation = None
    text = None

    def __init__(self, position, imgPath=None, operation=None, text=None):
        if imgPath != None:
            imgToLoad = pygame.image.load(imgPath).convert()
            self.img = pygame.transform.scale(imgToLoad, (position[1] - position[0], position[3] - position[2]))
        self.position = position
        self.operation = operation
        self.text = text

    def draw(self, surface):
        if not self.img == None:
            surface.blit(self.img, (self.position[0], self.position[2]))
        if not self.text == None:
            # this line access pacman inside button
            t = pacman.font.render(self.text, True, WHITE)
            tRect = t.get_rect()
            tRect.center = ((self.position[1] + self.position[0]) // 2, (self.position[3] + self.position[2]) // 2)
            surface.blit(t, tRect)

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