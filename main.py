#this file was created by: Kian McLaughlin
'''
content from kids can code: http://kidscancode.org/blog/
kidscancode https://www.youtube.com/watch?v=Z2K2Yttvr5g
Curran McLaughlin(brother)
Chris Cozort
https://www.pygame.org/docs/ref/transform.html#pygame.transform.scale
https://geometry-dash.fandom.com/wiki/Category:Images
ChatGPT

Goals
- Create a geometry dash mimic 
- Have different obstacles that spawn the farther you go 
- Animate the character flipping 


'''


import pygame
import sys
import random
import os
pygame.init()

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')

# Constants
WIDTH, HEIGHT = 800, 405
FPS = 60
GRAVITY = .8 # how fast the player falls/ how long it stays in the air
JUMP_HEIGHT = -20 # how high it jumps
BACKGROUND_SCROLL_SPEED = 2  # Adjust the background scroll speed

# setting different colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Creating the window and seting name of window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algebra Dash")

"""
Coulding make os work to access folder so I just had it search for the image
from the code file instead of a seperate images file

with changing it to seperate folder using os I run into new problems that I do not know how to fix.
"""

player_image = pygame.image.load(os.path.join(img_folder,'player.png')).convert
obstacle_image = pygame.image.load(os.path.join(img_folder,'obstacle.png')).convert
particle_image = pygame.image.load(os.path.join(img_folder,'particle.png')).convert
block_image = pygame.image.load(os.path.join(img_folder,'block.png')).convert
background_image = pygame.image.load(os.path.join(img_folder,'background.png')).convert
new_obstacle_image = pygame.image.load(os.path.join(img_folder,'newobstacle.png')).convert

# Scale images to a new size so that it fits the game
player_image = pygame.transform.scale(player_image, (50, 50))
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))
particle_image = pygame.transform.scale(particle_image, (10, 10))
block_image = pygame.transform.scale(block_image, (50, 50))
new_obstacle_image = pygame.transform.scale(new_obstacle_image, (50, 50))

#create a class for the player character
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = player_image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.velocity = 0
        self.angle = 0

    def jump(self): #when the character jumps the particles shoot from the character
        self.velocity = JUMP_HEIGHT
        for _ in range(10):
            particle = Particle(self.rect.centerx, self.rect.centery)
            all_sprites.add(particle)
            particles.add(particle)
            self.angle += 9.1  # rotation speed
            self.image = pygame.transform.rotate(self.original_image, self.angle)

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0



class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = particle_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity_x = random.uniform(-2, 2) # this set the veolicty of the particles to different speeds
        self.velocity_y = random.uniform(-5, -1)

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        if self.rect.bottom < 0:
            self.kill()


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = block_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        self.rect.x -= 4


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, HEIGHT - 50)

    def update(self):
        self.rect.x -= 4
        if self.rect.right < 0:
            self.rect.topleft = (WIDTH, HEIGHT - 50)

class NewObstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = new_obstacle_image
        self.rect = self.image.get_rect()
        self.speed = 2

    def update(self): 
        self.rect.y += self.speed 
        self.rect.x += (self.speed - 1)
        if self.rect.y > HEIGHT-self.rect.height or self.rect.y < 0:
                self.speed = -self.speed
        



# Create sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
blocks = pygame.sprite.Group()
particles = pygame.sprite.Group()
newobstacles = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Main game loop
clock = pygame.time.Clock()
running = True

# Initial block positions
block_positions = [(200, HEIGHT - 125), (400, HEIGHT - 175), (600, HEIGHT - 225)]

for pos in block_positions:
    block = Block(*pos)
    all_sprites.add(block)
    blocks.add(block)

background_x = 0
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.rect.bottom == HEIGHT:
                player.jump()
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000  # converting milliseconds to seconds not needed but why not

        # Check how many seconds have passed
        if elapsed_time >= 5:
            # Spawn a new object 
            newobstacle = NewObstacle(WIDTH)
            newobstacles.add(newobstacle)
            all_sprites.add(newobstacle)

            # Reset the start time for the next interval
            start_time = current_time

    # Update
    all_sprites.update()

    # Check for collisions 
    if pygame.sprite.spritecollide(player, obstacles, False) or pygame.sprite.spritecollide(player, newobstacles, False):
        running = False

    # Check if player collides with blocks
    block_collision = pygame.sprite.spritecollide(player, blocks, False)
    if block_collision:
        block = block_collision[0]
        if player.rect.bottom > block.rect.top:
            player.rect.y = (block.rect.top - 50)

    # Generate obstacles and blocks
    if pygame.time.get_ticks() % 200 == 0:
        obstacle = Obstacle(WIDTH)
        obstacles.add(obstacle)
        all_sprites.add(obstacle)

        # Adjust block positions based on obstacle position
        block_x = obstacle.rect.x + random.randint(150, 300)
        block_y = HEIGHT - random.randint(100, 200)
        block = Block(block_x, block_y)
        all_sprites.add(block)
        blocks.add(block)

    # Scroll the background
    background_x -= BACKGROUND_SCROLL_SPEED
    if background_x <= -background_image.get_width():
        background_x = 0

    # Draw the background at different positions for the rolling effect
    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (background_x + background_image.get_width(), 0))

    all_sprites.draw(screen)
    obstacles.draw(screen)
    particles.draw(screen)
    blocks.draw(screen)
    newobstacles.draw(screen)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()
sys.exit() 
