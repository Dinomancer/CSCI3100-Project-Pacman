########################
######## Pacman ########
########################

Pacman is a game created using pygame. It can be played local, but also supports login and upload/downloading user profile and making custom maps.
Basic gameplay is similar to the original pacman. In addition, player can buy skin and powerups in the shop.

##############################
######## Requirements ########
##############################

Pacman requires python 3.0 or above, pygame, pysimplegui and pysql.

Download python 3 here:	https://www.python.org/downloads/

install pygame by typing this in shell:
python3 -m pip install -U pygame==2.3.0 --user
or visit: https://www.pygame.org/

install pysimplegui by typing this in shell:
pip3 install pysimplegui
or visit this website: https://www.pysimplegui.org

install pymysql by typing this in shell:
python3 -m pip install PyMySQL
or try this website: https://pypi.org/project/pymysql/

################################
######## Execution #############
################################

Run main.py on python. A game window should popup.
WASD to move, or you can change key binding by clicking the tool icon on the upper left.
Press X to close game, the circle arrow to return to menu.
Make sure to be using english typing instead of chinese typing keyboard!

################################
######## Code Structure ########
################################

All the UI design and pacman game logic is inside main.py. Here are some sections that are important:

For UI design, check the Buttons class first. This class defines a button which has an image, a rectangle box and stores a string "operation".
It is made clickable so whenever the player clicks the button the corresponding operation will be executed. 
You may see all the operations written in the function runOperation() inside class Pacman. These lines of code will execute if a button is clicked.

Next, checkout the setStage() function in class Pacman. Every "stage" is a layout of buttons that the player sees when playing the game. For example
the menu, the setting screen and the pacman game screen are all "stages". Use setStage to switch between them.

Last thing to note is that the stage layout does not define everything on the screen. Especially for the main game, some drawing logic happens inside Pacman.drawScreen() function.
There, you can see other plain images that are drawn in each scene. pacman animation, ghosts and pacman buff icons are all drawn here.

For the game logic, look at the step() function in class Pacman. This is the logic of what the game does each game frame.
Basic logic is that pacman moves each frame, and when it is 36pixels(a grid) away from its starting position, it is considered to have reached a new grid location.
It then updates its grid location, eats the dot there, and make a turn if necessary. User's direction input is not immediately taken in, but it is stored in Pacman.delayedKeyInput.
The input is taken in when pacman reaches a grid location. Therefore, user can hit the direction key a bit earlier and still get the pacman to make a turn.

DBcontrol handles everything that requires internet connection. Login, download, upload map, etc.
#In order to view the database,
#access to http://www.phpmyadmin.co with following info or you can use terminal access
#Server: sql12.freemysqlhosting.net
#Name: sql12612119
#Username: sql12612119
#Password: uNQLBwFZZJ
#Port number: 3306

Shop manages the user's shop purchase data and their coins.

Settings deal with modifying key inputs and changing volumes.