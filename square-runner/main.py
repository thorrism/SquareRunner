
import kivy
import random
kivy.require('1.0.6')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import *
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty, BooleanProperty, StringProperty
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.uix.image import Image
import os
Builder.load_file('mainscreen.kv')
Window.fullscreen = True

platform = platform()

###PC VERSION###

if platform == 'android':
    leaderboard_highscore = 'CgkIiJHrt9IREAIQAA'

#screen manager to handle all the screens
sm = ScreenManager(transition=NoTransition())  

##################
#Game over screen#
##################
class DeathScreen(Screen):
    #score labels text and positions
    finalScore = NumericProperty(0)
    highScore = NumericProperty(0)
    gameOver = ObjectProperty(None)
    playAgain = ObjectProperty(None)
    mainMenu = ObjectProperty(None)

    #check for clicking a button
    def bounds_check(self, touch, objX, objY, height, width):
        if touch.x >= objX and touch.x <= objX+width:
            if touch.y >= objY and touch.y <= objY+height:
                return True

    #all the action for the game
    def on_touch_down(self, touch):
        if self.bounds_check(touch, self.playAgain.getX(), self.playAgain.getY(), self.playAgain.getHeight(), self.playAgain.getWidth()):
            Clock.schedule_interval(game_screen.update, 1.0 / 60.0)
            game_screen.newGame()
            sm.current = 'game'

    def setHighScore(self, score):
        self.highScore = score

    def setScore(self, score):
        self.finalScore = score

    def getHighScore(self):
        return self.highScore

#Game over image
class GameOver(Widget):
    def __init__(self, **kwargs):
        super(GameOver, self).__init__(**kwargs)

#Class for the play again button
class PlayAgain(Widget):
    def __init__(self, **kwargs):
        super(PlayAgain, self).__init__(**kwargs)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width
##########################
#End of Game Over screen#
##########################

###################
#Arrow Key Widgets#
###################
class UpKey(Widget):
    def __init__(self, **kwargs):
        super(UpKey, self).__init__(**kwargs)

    #methods for when the user catches the powerup
    def invertImage(self):
        self.newSource = 'up2.png'

    def resetImage(self):
        self.newSource = 'up1.png'

class DownKey(Widget):
    def __init__(self, **kwargs):
        super(DownKey, self).__init__(**kwargs)

    #methods for when the user catches the powerup
    def invertImage(self):
        self.newSource = 'down2.png'

    def resetImage(self):
        self.newSource = 'down1.png'

class LeftKey(Widget):
    def __init__(self, **kwargs):
        super(LeftKey, self).__init__(**kwargs)

    #methods for when the user catches the powerup
    def invertImage(self):
        self.newSource = 'left2.png'

    def resetImage(self):
        self.newSource = 'left1.png'

class RightKey(Widget):
    def __init__(self, **kwargs):
        super(RightKey, self).__init__(**kwargs)

    #methods for when the user catches the powerup
    def invertImage(self):
        self.newSource = 'right2.png'

    def resetImage(self):
        self.newSource = 'right1.png'
####################
#End of key widgets#
####################

##############
#Game Objects#
##############
class PowerUp(Widget):
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(PowerUp, self).__init__(**kwargs)

    def setX(self, newX):
        self.x = newX

    def setY(self, newY):
        self.y = newY

    def getX(self):
        return self.x

    def getY(self):
        return self.y 

    #Place the power up object at a randomlocation on screen. Adjusted the bounds for randomness to be more centered
    def randomLocation(self):
        self.x = random.randint(200,Window.width-200)
        self.y = random.randint(200,Window.height-200)

        #ensure that the circle is on screen and able to be caught
        if self.x+self.width > Window.width:
            self.x -= (self.width+10)
        if self.x-self.width < 0:
            self.x += (self.width+10)
        if self.y < (Window.height/4):
            self.y += (self.width+10) + (Window.height/4)
        if self.y+self.height > Window.height:
            self.y -= (self.width+10)

#class for the scoring object
class ScoreBall(Widget):
    def __init__(self, **kwargs):
        super(ScoreBall, self).__init__(**kwargs)

    #pick a random location for the ball to spawn at on the screen
    def randomLocation(self):
        self.x = random.randint(200,Window.width-200)
        self.y = random.randint(200,Window.height-200)

        #ensure that the circle is on screen and able to be caught
        if self.x+self.width > Window.width:
            self.x -= (self.width+10)
        if self.x-self.width < 0:
            self.x += (self.width+10)
        if self.y < (Window.height/4):
            self.y += (self.width+10) + (Window.height/4)
        if self.y+self.height > Window.height:
            self.y -= (self.width+10)

#class for the zombie square objects
class Squares(Widget):
    def __init__(self, **kwargs):
        super(Squares, self).__init__(**kwargs)
        self.height = "25dp"
        self.width = "25dp"

    speed = NumericProperty(2)
    index = NumericProperty(0)
    velX = NumericProperty(0)
    velY = NumericProperty(0)

    def invertImage(self):
        self.newSource = 'badguy2.png'

    def resetImage(self):
        self.newSource = 'badguy1.png'

    def setX(self, newX):
        self.x = newX

    def setY(self, newY):
        self.y = newY

    #set the square blue if activated
    def setActive(self):
        pass

    #set the squares their zombie grey color
    def resetActive(self):
        pass

    #move the player based on the direction vectors
    def move(self):
        self.x += self.velX
        self.y += self.velY

        #pick a random location for the ball to spawn at on the screen
    def randomLocation(self):
        self.x = random.randint(50,Window.width-50)
        self.y = random.randint(50, (Window.height-Window.height/6)-100)

        
        if self.x+self.width > (Window.width-50):
            self.x -= (self.width+10)
        if self.x-self.width < 50:
            self.x += (self.width+10)
        if self.y < (Window.height/6-50):
            self.y += (self.width+10)
        if self.y+self.height > 50:
            self.y -= (self.width+10)

#class for the player object
class Player(Widget):

    score = NumericProperty(0)
    highScore = NumericProperty(0)
    countDown = NumericProperty(6)
    visible = NumericProperty(0)

    #this controls the color of the score on the screen
    red = NumericProperty(0)
    green = NumericProperty(0)
    blue = NumericProperty(0)

    #speed at which the player moves
    speed = NumericProperty(2)

    #vector propoerties controlling directional movement
    velX = NumericProperty(2)
    velY = NumericProperty(2)

    #to increment and reset for the powerup
    counter = NumericProperty(0)

    #boolean states for if the player has a powerup, and if the game has been started
    active = BooleanProperty(False)
    start = BooleanProperty(False)

    #high score text file and set the high score saved in the file
    score_file = open('highscore.txt', 'r+')
    highScore = score_file.read()
    score_file.close()

    #move the player based on vector velocity
    def move(self):
        if self.start:
            self.x += self.velX
            self.y += self.velY

    def reset(self):
        self.counter = 0
        self.active = False
        self.start = False
        self.x = self.width
        self.y = Window.height / 2
        self.velX = 0
        self.velY = 0
        self.speed = 2
        self.scoreBlack()
        self.countDown = 6
        self.score = 0
    
    def detect_collision(self, obj):
        pass

    def increaseScore(self):
        self.score += 1

    def getScore(self):
        return self.score

    def setHighScore(self, score):
        self.highScore = score

    def getHighScore(self):
        return self.highScore

    def resetScore(self):
        self.score = 0

    def resetCountDown(self):
        self.countDown = 6

    def performCountDown(self, dt):
        self.countDown -= 1
        if self.countDown <= 0:
            self.resetCountDown()
            return False 

    def fasterSpeed(self):
        self.speed = 3

    def resetSpeed(self):
        self.speed = 2

    #color the score label white
    def scoreWhite(self):
        self.red = .5
        self.green = .5
        self.blue = .5

    #color the score label black
    def scoreBlack(self):
        self.red = 0
        self.green = 0
        self.blue = 0

    #when the player hits a goal circle, set the spawned enemies direction
    def setEnemyDirection(self, newSquare):
        #player moving right
        if self.velX > 0: 
            #check to see if the enemy will be on screen
            if self.x - (self.width+5) > 0:
                newSquare.x = self.x - (self.width+5)
                newSquare.y = self.y
                newSquare.velX = -1
            #send the enemy square down if not
            else:
                newSquare.x = self.x
                newSquare.y = self.y - (self.height+5)
                newSquare.velY = -1
        #player moving left
        elif self.velX < 0:
            #again, checking if the new enemey will be on screen
            if self.x + (self.width+5)+self.width < Window.width:
                newSquare.x = self.x + (self.width+5)
                newSquare.y = self.y
                newSquare.velX = 1
            #send the new enemy down if not
            else:
                newSqaure.x = self.x
                newSquare.y = self.y - (self.height+5)
                newSquare.velY = -1
        #player moving up
        elif self.velY > 0:
            #if the new enemy square is not below the arrow keys line 
            if self.y - (self.height+5) > (Window.height/4):
                newSquare.x = self.x
                newSquare.y = self.y - (self.height+5)
                newSquare.velY = -1
            #otherwise, send it going left
            else:
                newSquare.x = self.x - (self.width+5)
                newSquare.y = self.y
                newSquare.velX = -1
        #player moving down
        elif self.velY < 0:
            #if the new enemy square is still on the screen, bellow window's height
            if self.y + ((self.height+5)+self.height) < Window.height:
                newSquare.x = self.x
                newSquare.y = self.y + (self.height+5)
                newSquare.velY = 1
            #otherwise, send it left like above's check
            else:
                newSquare.x = self.x - (self.width+5)
                newSquare.y = self.y
                newSquare.velX = -1
#####################
#End of Game Objects#
#####################

#############
#Game Screen#
#############
class Game(Screen):

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None



    #objects needed for the game
    ball = ObjectProperty(None)
    player = ObjectProperty(None)
    scoreLabel = ObjectProperty(None)
    powerUp = ObjectProperty(None)
    newSource = StringProperty(None)

    #arrow key objects
    upKey = UpKey()
    downKey = DownKey()
    leftKey = LeftKey()
    rightKey = ObjectProperty(None)

    #dead boolean
    dead = BooleanProperty(False)

    #deal with creating new squares upon player-to-ball collisions
    squares = {}
    numSquares = NumericProperty(0)

    def wall_bounce(self, obj):
        if obj.velY == 0:
            #adjust the x so that it cannot get the error where the square is stuck 
            if(obj.velX > 0):
                obj.x -= 10
            else:
                obj.x += 10
            obj.velX = obj.velX*-1
        else:
            #same as above, adjust the y location in order to avoid the going two directions bug
            if(obj.velY > 0):
                obj.y -= 10
            else:
                obj.y += 10
            obj.velY = obj.velY*-1

    def start_game(self):
        self.ball.randomLocation()

    def resetPowerup(self, dt):
        self.player.active = False

    #take an old dictionary and remove the square at it's index and update with a new dictionary of squares
    def removeSquare(self, key):
        copyDict = self.squares.copy()
        del copyDict[key]
        return copyDict

    #check for clicking a widget, created because of my dislike for kivy's buttons
    def bounds_check(self, touch, objX, objY, height, width):
        if touch.x >= objX and touch.x <= objX+width:
            if touch.y >= objY and touch.y <= objY+height:
                return True

     #check for hitting walls
    def wall_bounds(self, obj):                   
        #check for top or bottom wall bounds
        if(obj.y < self.y+Window.height / 4) or (obj.y+obj.width > (Window.height-10) ):
            return True

        #check for left or right wall bounds 
        if(obj.x < 10) or (obj.x+obj.height > (Window.width-10) ):
            return True

    def newGame(self):
        #remove all squares
        for square in self.squares.itervalues():
            square.setX(-100)
        self.squares = {}
        self.numSquares = 0
        self.powerUp.x = -100
        self.dead = False
        self.player.reset()
        self.ball.randomLocation()

    #activate everything we need when the player hit's the power up and start a timer to end it
    def activatePowerup(self):
        self.newSource = 'background2.png'
        self.powerUp.setX(-100)
        self.player.scoreWhite()
        self.player.visible = 1
        self.upKey.invertImage()
        self.downKey.invertImage()
        self.leftKey.invertImage()
        self.rightKey.invertImage()
        self.player.fasterSpeed()
        for square in self.squares.itervalues():
            square.invertImage()

    #reset everything we need to when the timer ends for the power up 
    def resetPowerup(self, dt):
        self.newSource = 'background1.png'
        self.player.active = False
        self.player.scoreBlack()
        self.player.visible = 0
        self.player.resetSpeed()
        self.upKey.resetImage()
        self.downKey.resetImage()
        self.leftKey.resetImage()
        self.rightKey.resetImage()
        for square in self.squares.itervalues():
            square.resetImage()
        return False

    #all the action for the game
    def update(self, dt):
        self.player.move()
        if self.player.collide_widget(self.ball):  #check for player catching the goal ball
            if not self.player.active:             #only when the player isn't active do we create new squares and increment the counter  
                with self.canvas:                  #add the new square to the canvas dynamically
                    newSquare = Squares()  
                newSquare.index = self.numSquares
                self.numSquares += 1 
                self.player.counter += 1    
                self.player.setEnemyDirection(newSquare)
                self.squares[newSquare.index] = newSquare
                
            #always do this when player hits the ball
            self.ball.randomLocation()
            self.player.increaseScore()

        if self.player.collide_widget(self.powerUp):
            self.player.active = True
            self.activatePowerup()
            Clock.schedule_once(self.resetPowerup, 6)
            Clock.schedule_interval(self.player.performCountDown, 1)

        #if the counter is at 10, show the powerup
        if self.player.counter == 10:
            self.powerUp.active = True
            self.powerUp.randomLocation()
            self.player.counter = 0   

        #iterate over every square in the dictionary of squares
        for square in self.squares.itervalues():
            square.move()
            if self.wall_bounds(square):
                self.wall_bounce(square)

            if self.player.collide_widget(square):
                if not self.player.active:
                    death_screen.setHighScore(int(self.player.getHighScore()))
                    death_screen.setScore(self.player.getScore())
                    if int(self.player.getHighScore()) < self.player.getScore():
                        self.player.score_file = open('highscore.txt', 'r+')
                        death_screen.setHighScore(self.player.getScore())
                        self.player.setHighScore(self.player.getScore())
                        self.player.score_file.truncate()
                        self.player.score_file.write(str(self.player.getScore()))
                        self.player.score_file.close()
                    sm.current = 'death'
                    self.newGame()            
                    return False
                    break
                else:
                    square.setX(-100)
                    self.player.increaseScore()
                    self.squares = self.removeSquare(square.index)

        #bounds checkings player to wall collision
        if self.wall_bounds(self.player):
            self.wall_bounce(self.player)

    #define movement for keyboard use as well (FOR PC / MAC OSX)
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        #WASD keys for up left down right respectivley
        if keycode[1] == 'w':
            self.player.start = True
            self.player.velY = self.player.speed
            self.player.velX = 0
        if keycode[1] == 'a':
            self.player.start = True
            self.player.velY = 0
            self.player.velX = self.player.speed*-1
        if keycode[1] == 's':
            self.player.start = True
            self.player.velY = self.player.speed*-1
            self.player.velX = 0
        if keycode[1] == 'd':
            self.player.start = True
            self.player.velY = 0
            self.player.velX = self.player.speed

        #up down left right for the arrow keys as well
        if keycode[1] == 'up':
            self.player.start = True
            self.player.velY = self.player.speed
            self.player.velX = 0
        if keycode[1] == 'left':
            self.player.start = True
            self.player.velY = 0
            self.player.velX = self.player.speed*-1
        if keycode[1] == 'down':
            self.player.start = True
            self.player.velY = self.player.speed*-1
            self.player.velX = 0
        if keycode[1] == 'right':
            self.player.start = True
            self.player.velY = 0
            self.player.velX = self.player.speed

    def on_touch_down(self, touch):
        #Check bounds of player's tap for each key, modify the range of checking for user's ease to tap
        if self.bounds_check(touch, self.upKey.x, self.upKey.y, self.upKey.height+80, self.upKey.width):
            self.player.start = True
            self.player.velY = self.player.speed
            self.player.velX = 0
        elif self.bounds_check(touch, self.downKey.x, self.downKey.y-80, self.downKey.height+80, self.downKey.width):
            self.player.start = True
            self.player.velY = self.player.speed*-1
            self.player.velX = 0
        elif self.bounds_check(touch, self.leftKey.x-80, self.leftKey.y, self.leftKey.height+160, self.leftKey.width+80):
            self.player.start = True
            self.player.velY = 0
            self.player.velX = self.player.speed*-1
        elif self.bounds_check(touch, self.rightKey.x, self.rightKey.y, self.rightKey.height+160, self.rightKey.width+80):
            self.player.start = True
            self.player.velY = 0
            self.player.velX = self.player.speed

        #These bounds checks are to make tapping the buttons easier!
        elif self.bounds_check(touch, self.rightKey.x, self.rightKey.y-80, self.rightKey.height+160, self.rightKey.width+80):
            self.player.start = True
            self.player.velY = 0
            self.player.velX = self.player.speed

        elif self.bounds_check(touch, self.leftKey.x, self.leftKey.y-80, self.leftKey.height+160, self.leftKey.width+80):
            self.player.start = True
            self.player.velY = 0
            self.player.velX = self.player.speed*-1

class ScoreLabel(Widget):
    def __init__(self, **kwargs):
        super(ScoreLabel, self).__init__(**kwargs)
####################
#End of Game Screen#
####################

#############
#Main Screen#
#############
class MenuScreen(Screen):
    playBtn = ObjectProperty(None)
    instructionsBtn = ObjectProperty(None)
    start = BooleanProperty(False)

    #create squares for an animation for the title screen
    squares = {}

    def wall_bounds(self, obj):                
        #check for top or bottom wall bounds
        if(obj.y < 10) or (obj.y+obj.width > ((Window.height-Window.height/6)-5) ):
            return True

        #check for left or right wall bounds 
        if(obj.x < 10) or (obj.x+obj.height > (Window.width-10) ):
            return True

    def wall_bounce(self, obj):
        if obj.velY == 0:
            #adjust the x so that it cannot get the error where the square is stuck 
            if(obj.velX > 0):
                obj.x -= 5
            else:
                obj.x += 5
            obj.velX = obj.velX*-1
        else:
            #same as above, adjust the y location in order to avoid the going two directions bug
            if(obj.velY > 0):
                obj.y -= 5
            else:
                obj.y += 5
            obj.velY = obj.velY*-1

    def createSquares(self):
        for i in range(10):
            with self.canvas:
                self.squares[i] = Squares()
            self.squares[i].randomLocation()

            #set direction
            direction = random.randint(0, 3)
            #right
            if direction == 0:
                self.squares[i].velX = 2
                self.squares[i].velY = 0
            #left
            if direction == 1:
                self.squares[i].velX = -2
                self.squares[i].velY = 0
            #down
            if direction == 2:
                self.squares[i].velX = 0
                self.squares[i].velY = 2
            #up
            if direction == 3:
                self.squares[i].velX = 0
                self.squares[i].velY = -2

    def update(self, dt):
        for square in self.squares.itervalues():
            square.move()
            if self.wall_bounds(square):
                self.wall_bounce(square)

    #check for clicking a button
    def bounds_check(self, touch, obj):
        if touch.x >= obj.x and touch.x <= obj.x+obj.width:
            if touch.y >= obj.y and touch.y <= obj.y+obj.height:
                return True

    def endAnimation(self):
        for square in self.squares.itervalues():
            square.setX(-100)
        self.squares = {}
        return False

    def on_touch_down(self, touch):
        if self.bounds_check(touch, self.playBtn):
            #start the game on click of play key
            sm.current = 'game'
            game_screen.start_game()
            Clock.schedule_interval(game_screen.update, 1.0 / 60.0)
            #clear the main screens squares dictionary and turn off the update interval
            self.endAnimation()

        if self.bounds_check(touch, self.instructionsBtn):
            self.endAnimation()
            sm.current = 'instructions'
            return False

#Buttons for either instructions or play
class Instructions(Widget):
    pass

class Play(Widget):
    pass
####################
#End of Main Screen#
####################

class SettingsScreen(Screen):
    pass

#####################
#Instructions Screen#
#####################
class ReturnBtn(Widget):
    def __init__(self, **kwargs):
        super(ReturnBtn, self).__init__(**kwargs)

class InstructionsScreen(Screen):
    returnBtn = ObjectProperty(None)

    #check for clicking a button
    def bounds_check(self, touch, obj):
        if touch.x >= obj.x and touch.x <= obj.x+obj.width:
            if touch.y >= obj.y and touch.y <= obj.y+obj.height:
                return True

    def on_touch_down(self, touch):
        if self.bounds_check(touch, self.returnBtn):
            sm.current = 'menu'
            main_menu.createSquares()


############################
#End of Instructions Screen#
############################

#Create screen objects to add to the screen manager.
game_screen = Game(name='game')
main_menu = MenuScreen(name='menu')
instructions_screen = InstructionsScreen(name='instructions')
death_screen = DeathScreen(name='death')

#add the screen objects
sm.add_widget(death_screen)
sm.add_widget(main_menu)
sm.add_widget(game_screen)
sm.add_widget(instructions_screen)

class SquareRunnerApp(App, GridLayout): 	
    def build(self):
        #establish the seed for true randomnize 
        random.seed()

        #start with the main menu
        sm.current = 'menu'
        #establish the main screen's animation squares
        main_menu.createSquares()
        Clock.schedule_interval(main_menu.update, 1.0 / 60.0)

        #return the screen manager to start the game
        return sm

if __name__ == '__main__':
    SquareRunnerApp().run()