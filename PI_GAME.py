#######################################################################################
#Name= Marcus Garner
#Date= 4/8/2018
#Description= Final PI PROJECT [SNAKE]
#######################################################################################
# WE DO NOT OWN SNAKE!!!! JUST A SCHOOL PROJECT. 

#BASE GAME IMPLEMENTED ON 4/11/2018 BY: Marcus G
# 5/11/2018 UPDATED ADDED: Joystick Axes and Joystick buttons  BY: Marcus G
#5/13/18 UPDATED ADDED: Music,power ups, increasing speed and color changes BY:James Wilson
#________ UPDATED ADDED:...... BY:______
#________ UPDATED ADDED:...... BY:______
#________ UPDATED ADDED:...... BY:______
#________ UPDATED ADDED:...... BY:______

from pygame.locals import *
from pygame.joystick import *
from random import randint
import pygame
import time
r = 0
g = 0
b = 0
x = 50

########################################
#### REMOVED BECAUSE NO WAV ON MY END

pygame.mixer.init()
pygame.mixer.music.load("Haunted Chase.wav")
pygame.mixer.music.play(loops=-1)


##### NUM ROCKS #####
NUM_ROCKS = 20

# window and grid dimensions
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 850
CELL_SIZE = 32

MAX_CELL_X = WINDOW_WIDTH / CELL_SIZE -1
MAX_CELL_Y = WINDOW_HEIGHT / CELL_SIZE -1

# joystick axes
AXIS_X = 0
AXIS_Y = 1

# joystick buttons
TOP_BLUE = 10
BOT_BLUE = 8
TOP_GREEN = 4
BOT_GREEN = 6
TOP_RED = 0
BOT_RED = 2

# image files
APPLE_IMG = "apple.png"
PLAYER_IMG = "snake.png"
power_IMG = "Boost.png"
rock_IMG = "rock.png"



def does_collide(x1, y1, x2, y2):
    return (x1 == x2 and y1 == y2)

# thing snake eats to get thiccer
class Apple:

    apple_surf = None
    
    def __init__(self,x,y):
        # create apple image
        if self.apple_surf is None:
            self.apple_surf = pygame.image.load(APPLE_IMG).convert()
            
        # scale coords by CELL_SIZE
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE

    # draw to screen
    def draw(self, surface):
        surface.blit(self.apple_surf,(self.x, self.y))
#power-ups
class Power:

    power_surf = None
    
    def __init__(self,x,y):
        # create power up image
        if self.power_surf is None:
            self.power_surf = pygame.image.load(power_IMG).convert()
            
        # scale coords by CELL_SIZE
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE

    # draw to screen
    def draw(self, surface):
        surface.blit(self.power_surf,(self.x, self.y))



# obstacle
class Rock:
    rock_surf = None
    
    
    def __init__(self,x,y):
        # create rock image
        if self.rock_surf is None:
            self.rock_surf = pygame.image.load(rock_IMG).convert()

        self.x = x
        self.y = y
        

    # draw to screen
    def draw(self, surface):
        surface.blit(self.rock_surf,(self.x, self.y))
    

# the snake
class Player:

    player_surf = None

    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3

    def __init__(self, length):
        # create player image
        if self.player_surf is None:
            self.player_surf = pygame.image.load(PLAYER_IMG).convert()

        # create position lists
        self.x = []
        self.y = []
        
        # fill in initial cells
        for i in range(0, -length, -1):
            self.x.append(i * CELL_SIZE)
            self.y.append(0)

        # set length and direction
        self.length = length
        self.direction = self.RIGHT

        # update timers
        self.updateCount = 0
        self.updateCountMax = 2

    def update(self):
        # check if it's time to update
        self.updateCount = self.updateCount + 1

        # actually update
        if self.updateCount > self.updateCountMax:
            # update rest of body
            for i in range(self.length - 1, 0, -1):
                #print "self.x[" + str(i) + "] = self.x[" + str(i - 1) + "]"
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # update head
            if self.direction == self.RIGHT:
                self.x[0] = self.x[0] + CELL_SIZE
            if self.direction == self.LEFT:
                self.x[0] = self.x[0] - CELL_SIZE
            if self.direction == self.UP:
                self.y[0] = self.y[0] - CELL_SIZE
            if self.direction == self.DOWN:
                self.y[0] = self.y[0] + CELL_SIZE

            # reset update timer
            self.updateCount = 0

    # add a new cell to body
    def addCell(self):
        # add new cell at head coords
        self.x.append(self.x[1])
        self.y.append(self.y[1])

        # update length
        self.length += 1

        

    # movement methods
    def moveRight(self):
        if self.direction is not self.LEFT:
            self.direction = self.RIGHT
    
    def moveLeft(self):
        if self.direction is not self.RIGHT:
            self.direction = self.LEFT

    def moveUp(self):
        if self.direction is not self.DOWN:
            self.direction = self.UP

    def moveDown(self):
        if self.direction is not self.UP:
            self.direction = self.DOWN

    # draw snake body
    def draw(self, surface):
        for i in range(0, self.length):
            surface.blit(self.player_surf,(self.x[i], self.y[i]))

# Main game class
class App:
    def __init__(self):
        self.running = False
        
        self.display_surf = None
        self.power = None
        self.player = None
        self.apple = None
        
      
        self.rocks = []
        
        
    def on_init(self):
        pygame.init()
        pygame.display.set_caption('SNAKE RELOADED')

        
       
        pygame.joystick.init()
        self.joystick = Joystick(0)
        self.joystick.init()
        
        
        # create main surface with window dimensions 
        self.display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE)

        # create game objects
        self.player = Player(3)
        self.apple = Apple(5, 5)
        self.power = Power(6,6)
        
        
       
        for i in range(NUM_ROCKS):
            x = randint(0, MAX_CELL_X) * CELL_SIZE
            y = randint(1, MAX_CELL_Y) * CELL_SIZE
            rock = Rock(x, y)
            print rock.x, rock.y
            self.rocks.append(rock)
        

        self.running = True

    def on_event(self, event):
        print "Probably never called"
        if event.type == QUIT:
            self.running = False

    def on_loop(self):
        # update player's body
        self.player.update()

        # does snake eat the apple?
        for i in range(0, self.player.length):
            if does_collide(self.apple.x, self.apple.y, self.player.x[i], self.player.y[i]):
                #color change
                r = randint(0, 255)
                g = randint(0, 255)
                b = randint(0, 255)
                
                #increases speed
                if(x < 10):
                    x = 10
                else:
                    x= x-(randint(0,3))
                global r,g,b,x
                # increase length of player
                #self.player.length = self.player.length + 1
                self.player.addCell()
                # reposition apple and power up
                self.power.x = randint(0, MAX_CELL_X) * CELL_SIZE
                self.power.y = randint(0, MAX_CELL_Y) * CELL_SIZE
                self.apple.x = randint(0, MAX_CELL_X) * CELL_SIZE
                self.apple.y = randint(0, MAX_CELL_Y) * CELL_SIZE
                
                ### COMMENTED THIS PART OUT ENTIRELY, TEMP FIX ###

                # prevents apple from spawning in other objects
                if(does_collide(self.apple.x, self.apple.y, self.power.x, self.power.y)):
                    self.apple.x = randint(0, MAX_CELL_X) * CELL_SIZE
                    self.apple.y = randint(0, MAX_CELL_Y) * CELL_SIZE
                
                    
                if(does_collide(self.apple.x, self.apple.y, self.power.x, self.power.y)):
                    self.power.x = randint(0, MAX_CELL_X) * CELL_SIZE
                    self.power.y = randint(0, MAX_CELL_Y) * CELL_SIZE
                
                    
                if(does_collide(self.apple.x, self.apple.y, self.power.x, self.power.y)or does_collide(self.apple.x, self.apple.y, self.rock.x, self.rock.y) ):
                    self.apple.x = randint(0, 24) * CELL_SIZE
                    self.apple.y = randint(0, 12) * CELL_SIZE
                
                
          
            for rock in self.rocks:
                if does_collide(rock.x, rock.y, self.player.x[i], self.player.y[i]):
                        print "Your final length was {}.".format(self.player.length)
                        self.running = False
       
                          
            if does_collide(self.power.x, self.power.y, self.player.x[i], self.player.y[i]):
                #power up slows dowm the game
                x = x+1
                global x 
                self.power.x = randint(0, MAX_CELL_X) * CELL_SIZE
                self.power.y = randint(0, MAX_CELL_Y) * CELL_SIZE
                self.apple.x = randint(0, MAX_CELL_X) * CELL_SIZE
                self.apple.y = randint(0, MAX_CELL_Y) * CELL_SIZE
        # does snake collide with itself? 
        for i in range(2, self.player.length):
            if does_collide(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i]):
                # rub it in
                #print("YOU LOSE!!! Collision: ")
                #print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                #print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                # quit
                print "Your final length was {}.".format(self.player.length)
                self.running = False

        # does snake go out of bounds?
        if self.player.x[0] >= WINDOW_WIDTH or self.player.x[0] < 0 or self.player.y[0] >= WINDOW_HEIGHT or self.player.y[0] < 0:
            print "Your final length was {}.".format(self.player.length)
            self.running = False

    def on_render(self):
        # fill with black
        self.display_surf.fill((r,g,b))

                   
        # draw everything
        self.player.draw(self.display_surf)
        self.apple.draw(self.display_surf)
        self.power.draw(self.display_surf)

        ###################################
        for rock in self.rocks:
            rock.draw(self.display_surf)
        ####################################
        
        # update screen
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        pygame.event.get()
        
##################################################################################

        # Main loop
        while(self.running):
            # get joystick axis input
            for event in pygame.event.get():

                # Move Player (With Joystick) 
                if event.type == JOYAXISMOTION:
                    if event.axis == AXIS_Y:
                        print "Axis Y {}".format(event.value)
                        if event.value > 0:
                            self.player.moveDown()
                        else:
                            self.player.moveUp()
                    elif event.axis == AXIS_X:
                        print "Axis X {}".format(event.value)
                        if event.value > 0:
                            self.player.moveRight()
                        else:
                            self.player.moveLeft()

                # Joystick Buttons
                if event.type == JOYBUTTONDOWN:
                    if event.button == TOP_BLUE:
                        print "Top blue pressed"
                    elif event.button == BOT_BLUE:
                        print "Bottom blue pressed"
                    elif event.button == TOP_GREEN:
                        print "Top green pressed"
                    elif event.button == BOT_GREEN:
                        print "Bottom green pressed"
                    elif event.button == TOP_RED:
                        print "Top red pressed"
                    elif event.button == BOT_RED:
                        print "Bottom red pressed"
                    

                if event.type == QUIT:
                    self.running = False
                

            
            keys = pygame.key.get_pressed()
            
            
            # Move Player (With Keyboard)
            if(keys[K_RIGHT]):
                self.player.moveRight()
            if(keys[K_LEFT]):
                self.player.moveLeft()
            if(keys[K_UP]):
                self.player.moveUp()
            if(keys[K_DOWN]):
                self.player.moveDown()
            

            # quit
            if(keys[K_ESCAPE]):
                self.running = False

            # update and draw
            self.on_loop()
            self.on_render()

            # delay frames
            time.sleep (x / 1000.0)

        # exit game
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
