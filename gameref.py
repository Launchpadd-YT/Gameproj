# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_w,
    K_s,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the disp width and height
dispW = 800
dispH = 600


# Define the Player object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("/home/mikkomorgan/Documents/Coding/Programming_Essentials/gameProject/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on keypresses
    def update(self, pressedKeys):
        if pressedKeys[K_w]:
            self.rect.move_ip(0, -5)
            upSound.play()
        if pressedKeys[K_s]:
            self.rect.move_ip(0, 5)
            downSound.play()
        if pressedKeys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressedKeys[K_d]:
            self.rect.move_ip(5, 0)

        # Keep player on the disp
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > dispW:
            self.rect.right = dispW
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= dispH:
            self.rect.bottom = dispH


# Define the enemy object extending pygame.sprite.Sprite
# Instead of a surface, we use an image for a better looking sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("/home/mikkomorgan/Documents/Coding/Programming_Essentials/gameProject/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(dispW + 20, dispW + 100),
                random.randint(0, dispH),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the enemy based on speed
    # Remove it when it passes the left edge of the disp
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Define the cloud object extending pygame.sprite.Sprite
# Use an image for a better looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("/home/mikkomorgan/Documents/Coding/Programming_Essentials/gameProject/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(dispW + 20, dispW + 100),
                random.randint(0, dispH),
            )
        )

    # Move the cloud based on a constant speed
    # Remove it when it passes the left edge of the disp
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# Setup for sounds, defaults are good
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the disp object
# The size is determined by the constant dispW and dispH
disp = pygame.display.set_mode((dispW, dispH))

# Create custom events for adding a new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, cloud sprites, and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for position updates
# - all_sprites isused for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
allSprite = pygame.sprite.Group()
allSprite.add(player)

# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("/home/mikkomorgan/Documents/Coding/Programming_Essentials/gameProject/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# Load all our sound files
# Sound sources: Jon Fincher
upSound = pygame.mixer.Sound("/home/mikkomorgan/Documents/Coding/Programming_Essentials/gameProject/Rising_putter.ogg")
downSound = pygame.mixer.Sound("/home/mikkomorgan/Documents/Coding/Programming_Essentials/gameProject/Falling_putter.ogg")
collSound = pygame.mixer.Sound("/home/mikkomorgan/Documents/Coding/Programming_Essentials/gameProject/Collision.ogg")

# Set the base volume for all sounds
upSound.set_volume(0.5)
downSound.set_volume(0.5)
collSound.set_volume(0.5)

# Variable to keep our main loop running
running = True

# Our main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False

        # Should we add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy, and add it to our sprite groups
            newEnemy = Enemy()
            enemies.add(newEnemy)
            allSprite.add(newEnemy)

        # Should we add a new cloud?
        elif event.type == ADDCLOUD:
            # Create the new cloud, and add it to our sprite groups
            newCloud = Cloud()
            clouds.add(newCloud)
            allSprite.add(newCloud)

    # Get the set of keys pressed and check for user input
    pressedKeys = pygame.key.get_pressed()
    player.update(pressedKeys)

    # Update the position of our enemies and clouds
    enemies.update()
    clouds.update()

    # Fill the disp with sky blue
    disp.fill((165, 93, 53))

    # Draw all our sprites
    for entity in allSprite:
        disp.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, remove the player
        player.kill()

        # Stop any moving sounds and play the collision sound
        upSound.stop()
        downSound.stop()
        collSound.play()

        # Stop the loop
        running = False

    # Flip everything to the display
    pygame.display.flip()

    # Ensure we maintain a 30 frames per second rate
    clock.tick(60)

# At this point, we're done, so we can stop and quit the mixer
pygame.mixer.music.stop()
pygame.mixer.quit()


