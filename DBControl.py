import pymysql
import random
import string

#This class control the database of the game

class DBControl:
    #Initlize the object
    def __init__(self):
        # the login_flag flag denote whether user is login or not
        self.login_flag = False
        # The username, password is empty at first
        self.username = ""
        self.password = ""
        # The gold is 0 at first
        self.gold = 0
        # The buff level is all 0 at first
        self.buff = [0, 0, 0, 0, 0]  # 0-9 means level 1 to level 10
        # The skin is 2,0,0 at first means that ghost is equip default skin
        self.skin = [2, 0, 0]  # 0 means skin not yet buy, 1 means skin is bought
        # The mapdata stores the pause game map data
        # By default is empty
        self.mapdata = ""
        # There is a highscore.txt in the folder to store the local highscore of the player
        self.txt = open("highscore.txt", "r")
        self.highscore = int(self.txt.readline())
        self.txt.close()
        # The db is the connect with the database, if connect, we can use db.operation() to access and modify the database.
        self.db = None

    # this function start the database connection, it must be call once before every other function is use.
    def connect(self):
        try:
            self.db = pymysql.connect(host='sql12.freemysqlhosting.net',
                                      user='sql12612119',
                                      password='uNQLBwFZZJ',
                                      database='sql12612119')
            return True
        except:
            return None

    # the register function check if the username is exists, if so it should reject the user register request
    # else it create a new tuple in the db
    def register(self, username, password):
        if self.connect():
            cursor = self.db.cursor()
            sql = "SELECT username FROM Pacman WHERE BINARY username='" + username + "';"
            cursor.execute(sql)
            if (cursor.rowcount == 0):
                self.username = username
                self.password = password
                self.login_flag = True
                buff = ''.join(str(i) for i in self.buff)
                skin = ''.join(str(i) for i in self.skin)
                sql = "INSERT INTO Pacman VALUES ('%s', '%s', %d, %d, '%s', '%s', '%s')" % (
                    self.username, self.password, self.highscore, self.gold, buff, skin, self.mapdata)
                try:
                    cursor.execute(sql)
                    self.db.commit()
                except:
                    self.db.rollback()
                return True
            else:
                return False

    # this function check if the username and password exists in the db, if so, the user is login.
    def login(self, username, password):
        if self.connect():
            cursor = self.db.cursor()
            sql = "SELECT username FROM Pacman WHERE BINARY username='" + username + "' AND password='" + password + "';"
            cursor.execute(sql)
            if cursor.rowcount:
                self.username = username
                self.password = password
                self.login_flag = True
                return True
            else:
                return False

    # This function pull the user data to replace the local data
    def download(self):
        if self.login_flag and self.connect:
                sql = "SELECT * FROM Pacman WHERE BINARY username='" + self.username + "' AND password='" + self.password + "';"
                cursor = self.db.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                for rows in result:
                    self.highscore = int(rows[2])
                    self.gold = int(rows[3])
                    buff = rows[4]
                    self.buff[0] = int(buff[0])
                    self.buff[1] = int(buff[1])
                    self.buff[2] = int(buff[2])
                    self.buff[3] = int(buff[3])
                    self.buff[4] = int(buff[4])
                    skin = rows[5]
                    self.skin[0] = int(skin[0])
                    self.skin[1] = int(skin[1])
                    self.mapdata = rows[6]
                return True
        return False


    # This a funtion that upload user info except the local mapdata
    def upload(self):
        if self.login_flag and self.connect():
                buff = ''.join(str(i) for i in self.buff)
                skin = ''.join(str(i) for i in self.skin)
                sql = "UPDATE Pacman SET highscore = %d, gold = %d, buff = '%s', skin = '%s' WHERE BINARY username='" % (
                    self.highscore, self.gold, buff, skin) + self.username + "' AND password='" + self.password + "';"
                cursor = self.db.cursor()
                try:
                    cursor.execute(sql)
                    self.db.commit()
                    return True
                except:
                    return False
        return False

    # This is a function, that save the self.mapdata to the database that relate to the current username and password
    # before call this function, the Interface is need to store local mapdata in the class instance, self.mapdata
    def save(self):
        if self.login_flag and self.connect():
                sql = "UPDATE Pacman SET mapdata = '%s' WHERE BINARY username='" % (
                    self.mapdata) + self.username + "' AND password='" + self.password + "';"
                cursor = self.db.cursor()
                try:
                    cursor.execute(sql)
                    self.db.commit()
                    return True
                except:
                    return False
        return False

    # this is a function that generate the map code
    def codeGenerate(self):
        return ''.join(random.choice(string.digits) for _ in range(6))

    # this function will upload a map given the map data, it will random generate a code for the map,
    # then check if the code exists in the map, if so, it generate the code again, until the code does not exist
    # then it will insert the mapcode and mapdata to the database
    def uploadAMap(self, mapdata):
        if self.login_flag and self.connect():
                cursor = self.db.cursor()
                while (1):
                    mapcode = self.codeGenerate()
                    sql = "SELECT mapcode FROM Map WHERE mapcode='%s'" % (mapcode)
                    cursor.execute(sql)
                    if (cursor.rowcount == 0):
                        sql = "INSERT INTO Map VALUES ('%s', '%s')" % (mapcode, mapdata)
                        cursor.execute(sql)
                        self.db.commit()
                        return mapcode
        return None

    # this function take a mapcode as input, it will search the mapcode in the database
    # if the map exist, it will return the map
    # else it will return false, the interface should present a "map does not exist" message for the user
    def downloadAMap(self, mapcode):
        if self.login_flag and self.connect():
                cursor = self.db.cursor()
                sql = "SELECT mapdata FROM Map WHERE mapcode='%s'" % (mapcode)
                cursor.execute(sql)
                if (cursor.rowcount):
                    results = cursor.fetchall()
                    self.mapdata = results[0][0]
                    return True
        else:
            return False

    # This is a function that delete the userdata in the database. It should not be use expect for testing use.
    def deleteProfile(self):
        if self.connect():
            cursor = self.db.cursor()
            sql = "DELETE FROM Pacman WHERE BINARY username='" + self.username + "' AND password='" + self.password + "';"
            cursor.execute(sql)
            self.db.commit()
    # This is a function that delete the mapdata in the database by a mapcode. It should not be use expect for testing use.
    def deleteAMap(self, mapcode):
        if self.connect():
            cursor = self.db.cursor()
            sql = "DELETE FROM Map WHERE mapcode='%s'" % (mapcode)
            cursor.execute(sql)
            self.db.commit()

#Test
#In order to view the database,
#access to http://www.phpmyadmin.co with following info or you can use terminal access
#Server: sql12.freemysqlhosting.net
#Name: sql12612119
#Username: sql12612119
#Password: uNQLBwFZZJ
#Port number: 3306
#Uncommented the following lines to test
'''
test = DBControl()
print(test.connect()) # This will print True if connect success
print(test.login("test", "test")) # This will print false since the tuple is not exist in the database
print(test.register("test","test")) # This will print true since we now insert this tuple to the database
print(test.login("test", "test")) # This will print true since now the tuple exist in the database
test.mapdata = "2222222222222222222220000000000000000002200000000000000000022000222200000000000220002042000000000002200020420000000000022000222222222222000220000002000001120002200000020212021200022000000201110112000220000002021202120002200000020111011200022000000202120212000220000002003001120002200000022222222200022000000000000000000220000000000000000002200000000000000000022000000000000000000222222222222222222222"
print(test.save()) # THis will save the mapdata to the database and output true
input("Delete?") #This will let tester see the result before delete the profile, tester can check the website to see the result of above test
test.deleteProfile() # This will delete this tuple in the database

print(test.login("gold", "8888")) # This will print true since the tuple is exist in the database.
print(test.download()) # This will print true and we download all the data from the database
print(test.gold)
print(test.highscore) #This two will print 8888 and number larger than 1000  if so, that means we successly download the data
test.highscore += 100 # this will increase the highscore in the local
print(test.upload()) #This will upload the userdata to the database now if you check the database, the highscore of this profile is 1100
input("Replace?") #This will let tester see the result before replace the change data, tester can check the website to see the result of above test
test.highscore -= 100
test.upload()

map1 = test.mapdata # This map data is from account gold 8888
print(test.downloadAMap("342938")) #This will print true if it success download a map from the map database
map2 = test.mapdata
if (map1 != map2): #Check whether we success download a map
    print("success")
else:
    print("fail")
testmap = "1234" # we change the map data to test uploadAMap function
mapcode = test.uploadAMap(testmap) # The mapcode will be return and we can use it to find the map in the database
print(mapcode)
input("Remember?") # Now tester can find the mapcode and mapdata in the database
print(test.downloadAMap(mapcode)) # we use the mapcode to download the map from the database
print(test.mapdata) # if mapdata is the data of testmap, then the function is work well
test.deleteAMap(mapcode)
'''