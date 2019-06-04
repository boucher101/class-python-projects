# program template for Spaceship
from tkinter import *
from PIL import Image, ImageTk
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
max_rocks = 12

rock_group = set([])
missile_group = set([])
explosion_group = set([])

# useful constants
c = .01	#friction constant, higher means more friction
f = .1	#forward thrust constant, higher means more thrust
m = 5	#multiple of ships forward vector, higher means faster missile
s = .1	#ships angle velocity, higher means higher velocity

class ImageInfo:
    def __init__(self, center, coord, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.coord = coord
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_coord(self):
        return self.coord

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# ship image
ship_info = ImageInfo([45, 45], [0, 0, 90, 90], 45) # point right
double_ship = Image.open('double_ship.png')
double_ship = Image.composite(double_ship, Image.new('RGBA', double_ship.size), double_ship)

# missile image
missile_info = ImageInfo([5,5], [0, 0, 10, 10], 3, 50)
missile_image = Image.open('shot2.png')
missile_image = Image.composite(missile_image, Image.new('RGBA', missile_image.size), missile_image)

# asteroid images
asteroid_info = ImageInfo([45, 45], [0, 0, 90, 90], 40)
asteroid_image = Image.open('asteroid_blue.png')
asteroid_image = Image.composite(asteroid_image, Image.new('RGBA', asteroid_image.size), asteroid_image)

# animated explosion
explosion_info = ImageInfo([64, 64], [0, 0, 128, 128], 64, 24, True)
explosion_image = Image.open('explosion_alpha.png')
explosion_image = Image.composite(explosion_image, Image.new('RGBA', explosion_image.size), explosion_image)

# helper functions to handle transformations
def start_game():
    global lives, score
    score = 0
    lives = 3
    rock_spawner()

def angle_to_vector(ang):
    return [math.cos(math.radians(ang)), -math.sin(math.radians(ang))]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def process_sprite_group(sprite_set):
    for sprite in set(sprite_set):
            if sprite.update():
                sprite_set.remove(sprite)
            else:
                sprite.draw()
    
def group_collide(group, other_object):
    collision = False
    for element in set(group):
        if element.collide(other_object):
            explosion_group.add(Sprite(element.get_position(), [0,0], 0, 0, explosion_image, explosion_info))
            group.remove(element)
            collision = True
    return collision

def group_group_collide(first_group, second_group):
    collision_count = 0
    for element in set(first_group):
        if group_collide(second_group, element):
            collision_count += 1
            first_group.discard(element)
    return collision_count

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_ref = None
        self.image_center = info.get_center()
        self.image_coord = info.get_coord()
        self.radius = info.get_radius()
        
    def draw(self):
        if self.thrust:
            c_im = self.image.crop((self.image_coord[0]+self.image_coord[2], self.image_coord[1],
                                    self.image_coord[2]+self.image_coord[2], self.image_coord[3]))
        else:
            c_im = self.image.crop(self.image_coord)            
        
        c_im.load()
        self.image_ref = ImageTk.PhotoImage(c_im.rotate(self.angle))
        canvas.create_image(self.pos, image = self.image_ref)
        
        
    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] * f
            self.vel[1] += forward[1] * f

        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)
        
    def update_angle_vel(self, angle_vel):
        self.angle_vel = angle_vel
        
    def thrusters(self, thrust):
        self.thrust = thrust
        
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + forward[0] * self.radius, self.pos[1] + forward[1] * self.radius]
        missile_vel = [self.vel[0] + forward[0] * m, self.vel[1] + forward[1] * m]
        missile_group.add(Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info))

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_ref = None
        self.image_center = info.get_center()
        self.image_coord = info.get_coord()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = -1
        #if sound:
#            sound.rewind()
#            sound.play()
   
    def draw(self):
        if self.animated:
##            c_im = self.image.crop((self.image_coord[0] + self.image_coord[2] * self.age, self.image_coord[1],
##                                    self.image_coord[2] + self.image_coord[2] * self.age, self.image_coord[3]))
            c_im = self.image.crop((self.image_coord[2] * self.age, 0,
                                    self.image_coord[2] + self.image_coord[2] * self.age, self.image_coord[3]))
        else:
            c_im = self.image 

        c_im.load()
        r_im = c_im.rotate(self.angle)
        self.image_ref = ImageTk.PhotoImage(r_im)
        canvas.create_image(self.pos, image = self.image_ref)
        
    def update(self):
        # update angle
        self.angle += self.angle_vel 

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # increment age
        self.age += 1

        return self.age >= self.lifespan


    def collide(self, other_object):
        if dist(self.get_position(), other_object.get_position()) <= (self.get_radius() + other_object.get_radius()):
            return True
        else:
            return False
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
                  
def draw():
    global time, started, lives, score
    
    canvas.delete('all')

    # draw score and lives
    canvas.create_text(100, 50, text = "Lives", font = ('sans-serif', 32), fill = "White")
    canvas.create_text(680, 50, text = "Score", font = ('sans-serif', 32), fill = "White")
    canvas.create_text(100, 100, text = str(lives), font = ('sans-serif', 32), fill = "White")
    canvas.create_text(680, 100, text = str(score), font = ('sans-serif', 32), fill = "White")

    # draw ship
    my_ship.draw()
    
    # update ship and sprites
    process_sprite_group(rock_group)
    process_sprite_group(missile_group)
    process_sprite_group(explosion_group)

    # update ship
    my_ship.update()

    # draw splash screen if not started
    if not started:
        canvas.create_text(WIDTH/2, HEIGHT/2, text = "Click Screen to Start", font = ('sans-serif', 16), fill='White')
        
    if group_collide(rock_group, my_ship):
        lives -= 1
    
    if not lives:
        started = False
        for rock in set(rock_group):
            rock_group.remove(rock)
        
    score += group_group_collide(missile_group, rock_group)
    
    root.after(10, draw)
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    if started: 
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.randrange(-1, 2), random.randrange(-1, 2)]
        rock_ang_vel = random.choice([-3, 3])
        if dist(rock_pos, my_ship.get_position()) > (missile_info.get_radius() + my_ship.get_radius()) and len(rock_group) < max_rocks:
           rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_ang_vel, asteroid_image, asteroid_info))
        root.after(3000, rock_spawner)

def keydown(event):
    increment = 5
    if event.keysym == 'Left':
        my_ship.update_angle_vel(increment)
    elif event.keysym == 'Right':
        my_ship.update_angle_vel(-increment)
    elif event.keysym == 'Up':
        my_ship.thrusters(True)
    elif event.keysym == 'space':
        my_ship.shoot()

def keyup(event):
    if event.keysym == 'Left' or event.keysym == 'Right':
        my_ship.update_angle_vel(0)   
    if event.keysym == 'Up':
        my_ship.thrusters(False)

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(event):
    global started
    if not started:
        started = True
        start_game()
        
# initialize frame
root = Tk()
root.title('Spaceship')
canvas = Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0, background = 'Black')
canvas.pack()

# initialize ship and two sprites
my_ship = Ship([WIDTH/2, HEIGHT/2], [0, 0], 0, double_ship, ship_info)

# register handlers
draw()
canvas.bind_all("<Key>", keydown)
canvas.bind_all("<KeyRelease>", keyup)
canvas.bind_all("<Button-1>", click)


# get things rolling
root.mainloop()
