import pymysql
import random
import string


class DBControl:
    def __init__(self):
        self.login_flag = False  # the login_flag let the user to use login require function
        self.username = ""
        self.password = ""
        self.highscore = 0
        self.gold = 0
        self.buff = [0, 0, 0, 0, 0]  # 0-9 means level 1 to level 10
        self.skin = [0, 0, 0]  # 0 means skin not yet buy, 1 means skin is bought
        self.mapdata = ""
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


    # this a funtion that upload user info except the mapdata
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

    # this is a function, that save the self.mapdata to the database that relate to the current username and password
    # before call this function, the Interface is need to store mapdata in the class instance, self.mapdata
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

