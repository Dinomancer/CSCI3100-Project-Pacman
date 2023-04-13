import sys
import os
import pygame
from dbControl import DBControl
import PySimpleGUI as gui 

BLACK = (0, 0, 0)

WHITE = (255, 255, 255)

BLUE = (0, 0, 255)

GREEN = (0, 255, 0)

RED = (255, 0, 0)

YELLOW = (255, 255, 0)

PURPLE = (255, 0, 255)

SKYBLUE = (0, 191, 255)

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

[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0],

]





class Pacman:

    screen = None

    font = None

    buttons = []

    stage = ""

    paused = False



    imgWall = None

    imgPacman = None

    imgPacdot = None



    score = 0

    life = 1

    coin = 0

    ghostSpeed = 1

    map = None

    pacmanGridPos = [0,0]

    pacmanRealPos = [0,0]

    pacmanDir = "right"

    delayKeyInput = None
    



    def __init__(self):

        self.screen = pygame.display.set_mode((1280, 720))

        #self.screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)

        pygame.display.set_caption('Pacman')

        self.font = pygame.font.Font('Nunito-Medium.ttf',50)

        self.setStage("Main Editor")   #SHOP/EDITOR: to start stage in shop/editor, change this to "Editor"/"Shop"

        self.imgWall = pygame.image.load("Img\\defaultSkin\\wall.png").convert()

        self.imgPacman = pygame.image.load("Img\\defaultSkin\\pacman.png").convert()

        self.imgPacdot = pygame.image.load("Img\\defaultSkin\\pacdot.png").convert()

        self.imgWall = pygame.transform.scale(self.imgWall,(36,36))

        self.imgPacman = pygame.transform.scale(self.imgPacman,(36,36))

        self.imgPacdot = pygame.transform.scale(self.imgPacdot,(36,36))
        self.item = -1
        self.DBControl = DBControl()


    def setStage(self, stage):

        self.stage = stage

        if stage == "Menu":

            menu = Button((1010,1060,10,60),"Img\\defaultSkin\\closeButton.png", "quit")

            self.buttons = [menu]

        if stage == "Shop":     #SHOP: put all buttons in the shop here

            pass

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
        if stage == "Settings":

            pass

        if stage == "MainGame":

            pass



    def drawScreen(self):

        if (not self.map == None) and self.stage=="MainGame":   #SHOP/EDITOR: modify this line to hide the map
            self.drawMap(self.map)

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
        
        for b in self.buttons:
            b.draw(self.screen)
 

        



    def listen(self, event):

        
        if event.type == pygame.MOUSEBUTTONDOWN:

            for b in self.buttons:

                if b.isClicked(event.pos):

                    self.runOperation(b.operation)

                    break

            if self.stage == "Main Editor":
                pass  

                
            if self.stage == "Edit2":
                self.runOperation('edit')

           

        if event.type == pygame.KEYDOWN:
            pass


    def runOperation(self, operation):
        def CreateEditingMap(operation,newMap):
            if operation == "reset":
                with open('createdMap','w') as f:
                                for a in range(0,20):
                                    for b in range(0,20):
                                        f.write(str(newMap[a][b]))
            if operation == "place":
                for i,button in enumerate(self.buttons):
                    if i < 4:
                        if self.buttons[0].isClicked(event.pos):
                            self.item = 2
                        if self.buttons[1].isClicked(event.pos):
                            self.item = 4
                        if self.buttons[2].isClicked(event.pos):
                            self.item = 3
                        if self.buttons[3].isClicked(event.pos):
                            with open('createdMap','w') as f:
                                for a in range(0,20):
                                    for b in range(0,20):
                                        f.write(str(newMap[a][b]))
                    elif button.isClicked(event.pos) and self.item == 2 :
                
                        """ calculation for button position on map: (tested)
                        ipos = -1
                        for k in range(i+1):
                            if (k-4) % 20 == 0: 
                                ipos +=1
                        jpos = (i-4) % 20 """
                        ipos = -1
                        for k in range(i+1):
                            if (k-4) % 20 == 0: 
                                ipos +=1
                        jpos = (i-4) % 20
                    
                        newMap[ipos][jpos] = 2
                        imgToLoad = pygame.image.load("Img\\defaultSkin\\wall.png").convert()
                        button.img = pygame.transform.scale(imgToLoad, (36,36) )
                    elif button.isClicked(event.pos) and self.item == 3:
                        ipos = -1
                        for k in range(i+1):
                            if (k-4) % 20 == 0: 
                                ipos +=1
                        jpos = (i-4) % 20
                    
                        newMap[ipos][jpos] = 3
                        imgToLoad = pygame.image.load("Img\\defaultSkin\\pacman.png").convert()
                        button.img = pygame.transform.scale(imgToLoad, (36,36) )
                    elif button.isClicked(event.pos) and self.item == 4:
                        ipos = -1
                        for k in range(i+1):
                            if (k-4) % 20 == 0: 
                                ipos +=1
                        jpos = (i-4) % 20
                    
                        newMap[ipos][jpos] = 4
                        imgToLoad = pygame.image.load("Img\\defaultSkin\\ghost.gif").convert()
                        button.img = pygame.transform.scale(imgToLoad, (36,36) )

                    

        def get_user_input(context):
            gui.theme('DarkAmber')
            input = ""
            layout = [[gui.Text(context + " Window")],[gui.Text('Your Input:'),gui.InputText()],[gui.Button('Done'),gui.Button('Return')],[gui.Text("", key='-TEXT-')]]
            window = gui.Window(context,layout) 

            while True:
                event,values = window.read()
                if event == gui.WIN_CLOSED or event == "Return":
                    break
                input += values[0]
                if event == "Done":
                    if context == "Upload":
                         self.DBControl = DBControl()

                         if(self.DBControl.uploadAMap(input)):
                            window['-TEXT-'].update("Upload Success")
                         else:
                            window['-TEXT-'].update("Upload Failure")

                    if context == "Download":
                        self.DBControl = DBControl()
                        if(self.DBControl.downloadAMap(input)):
                            window['-TEXT-'].update("Download Success")
                        else:
                            window['-TEXT-'].update("Download Failure")
            window.close()
  
      
        if operation == "quit":
            pygame.quit()
            sys.exit()

        if operation == "MainGame":

            self.mainGameInit("MainGame")

        #SHOP: you can put operations you need here, for example operation=="buyBuff1", buff1 += 1
        if operation == "gotoEdit":
            self.setStage("Edit2")
            CreateEditingMap("replace",newMap)
            CreateEditingMap("place", newMap)

        if operation == "gotoDownload":
            get_user_input("Download")

        if operation == "gotoUpload":
            get_user_input("Upload")

            
    def mainGameInit(self, mapPath):

        self.score = 0

        self.life = 1

        self.coin = 0

        self.importMap(mapPath)

        self.drawMap(map)

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

        self.screen.blit(self.imgPacman, (self.pacmanRealPos[0],self.pacmanRealPos[1]))

                    



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



    def step(self):

        if self.stage == "MainGame":

            if self.paused == False:

                if self.pacmanDir == "right":

                    self.pacmanRealPos[0] += 1  #move to the right



class Button:

    img = None

    position = (0,0,0,0)        #x1, x2, y1, y2

    operation = None

    text = None

    

    def __init__(self, position, imgPath=None, operation=None):

        imgToLoad = pygame.image.load(imgPath).convert()

        self.img = pygame.transform.scale(imgToLoad,(position[1]-position[0],position[3]-position[2]))

        self.position = position

        self.operation = operation



    def draw(self, surface):

        if not self.img == None:

            surface.blit(self.img, (self.position[0],self.position[2]))



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

    clock.tick(10)