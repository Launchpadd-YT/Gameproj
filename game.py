import pygame
import sys
import os

from pygame.locals import (
    K_w,
    K_a,
    K_d,
    K_ESCAPE,
    KEYDOWN
)

# Constants
dispW = 1000
dispH = 800
fps = 60
tSize = 50

# Player properties
playerW = 50
playerH = 50
playerCol = ("#00FF00")
playerV = 5
g = 0.5
jumpH = 11


lvl = 0

# Load tilemaps for multiple levels
tilemaps = [
    [
        "XXXXXXXXXXXXXXXXXXXX",
        "X                  X",
        "XF                 X",
        "XXXXXXXXXXXX       X",
        "X                  X",
        "X             X    X",
        "X                  X",
        "X   X   XXXX       X",
        "X                  X",
        "XX                 X",
        "X                  X",
        "XXXXX   XXXXXXXX   X",
        "X                  X",
        "X                 XX",
        "X                  X",
        "XXXXXXXXXXXXXXXXXXXX",
    ],
    [
        "XXXXXXXXXXXXXXXXXXXX",
        "X                  X",
        "X                  X",
        "X                  X",
        "X                X X",
        "X                X X",
        "X              XXX X",
        "X          XLLLLLX X",
        "X      X   XXXXXXX X",
        "X      L   X       X",
        "XLLX       X       X",
        "X          X       X",
        "X      XXX X  LLXLLX",
        "X          X      FX",
        "X   X      XXXXXXXXX",
        "XXLLLLLLLLLLLLLLLLLX",
    ],
    [
        "XXXXXXXXXXXXXXXXXXXX",
        "X                  X",
        "X     LL           X",
        "X         XX       X",
        "X   LXXXXLXXLLX    X",
        "XL   XF       X    X",
        "XL   XXX      L   XX",
        "XXL  XLLLX    L    X",
        "X    X       XXX   X",
        "X   X        LX   XX",
        "X   L       X X   LX",
        "X       X     XX   X",
        "XLXXXXLLLLLLLLX    X",
        "XXXXXXXXXXXXXXX   XX",
        "X                  X",
        "XXXXXXXXXXXXXXXXXXXX",
    ],
    [
        "XXXXXXXXXXXXXXXXXXXX",
        "X                  X",
        "X                  X",
        "X    XX    L       X",
        "X  LLLLLLXLLLXXX   X",
        "X  L       L       X",
        "L   L            X X",
        "X    L   F         X",
        "XL      L     X    X",
        "X  XXXXXL          X",
        "X                 XX",
        "X                  X",
        "X          L    X  X",
        "X    X   X L X     X",
        "XX         L       X",
        "XLLLLLLLLLLLLLLLLLLX",
    ],
    [
        "XXXXXXXXXXXXXXXXXXXX",
        "X           XL     X",
        "X           XL     X",
        "X   XXXXXX  X    L X",
        "X  X LXLLL  X  XLX X",
        "X    LXLL   X X  X X",
        "XX   LXL   LX    X X",
        "X    LXL   LXX   X X",
        "X   XXXL   LXL   X X",
        "X     XLL   X   XX X",
        "XX    XLLL  X    X X",
        "XL    X     XXL  X X",
        "XLX   X   XXXLL  X X",
        "X    XX     XLL XX X",
        "X    LXX        XXFX",
        "XXXXXXXXLLXXXXXXXXXX",
    ],
    [
        "L     L  LL   L   L ",
        " L   L  L  L  L   L ",
        "  L L  L    L L   L ",
        "   L   L    L L   L ",
        "   L    L  L  L   L ",
        "   L     LL    LLL  ",
        "                    ",
        "  L     L L L   L   ",
        "  L     L L LL  L   ",
        "   L L L  L L L L   ",
        "   L L L  L L  LL   ",
        "    L L   L L   L   ",
        "X                  X",
        "X                  X",
        "X                  X",
        "XXXXXXXXXXXXXXXXXXXX",
    ],
]

instructions = [
    "Use A and D to go left and right, and W to jump.",
    "Watch out for Lava!",
    "ooooh... spiraly...",
    "The floor is lava!",
    "The tower of pain",
    "Good job! You won!"
]

instruction = None

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((playerW, playerH))
        self.image.fill(playerCol)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0

    def update(self):
        self.vx = 0
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            self.vx = -playerV
        if keys[K_d]:
            self.vx = playerV
        if keys[K_w] and self.on_ground():
            self.vy = -jumpH
            jumpSound.play()

        # Apply gravity
        self.vy += g
        if self.vy > 10:  # Terminal velocity
            self.vy = 10


        self.rect.y += self.vy
        self.check_collision_y()

        self.rect.x += self.vx
        self.check_collision_x()

    def check_collision_x(self):
        for tile in tiles:
            if tile.type == "reg" and self.rect.colliderect(tile.rect):
                if self.vx > 0:
                    self.rect.right = tile.rect.left
                elif self.vx < 0:
                    self.rect.left = tile.rect.right

    def check_collision_y(self):
        for tile in tiles:
            if tile.type == "reg" and self.rect.colliderect(tile.rect):
                if self.vy > 0:
                    self.rect.bottom = tile.rect.top
                    self.vy = 0
                elif self.vy < 0:
                    self.rect.top = tile.rect.bottom
                    self.vy = 0

    def on_ground(self):
        self.rect.y += 1
        is_on_ground = pygame.sprite.spritecollideany(self, tiles)
        self.rect.y -= 1
        return is_on_ground

    
# Tile class
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, color, tileType):
        super().__init__()
        self.image = pygame.Surface((tSize, tSize))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x * tSize
        self.rect.y = y * tSize
        self.type = tileType

class Instruction(pygame.sprite.Sprite):
    def __init__(self, txt):
        super().__init__()
        self.font = pygame.font.Font(None, 30)
        self.image = self.font.render(txt, True, "#FFFFFF")
        self.rect = self.image.get_rect(center = (dispW // 2, dispH - 25))

class Timer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.font = pygame.font.Font(None, 30)
        self.image = self.font.render("Time: 0", True, "#FFFFFF")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.startT = pygame.time.get_ticks()

    def update(self):
        if not timerStop:
            currT = pygame.time.get_ticks() - self.startT
            s = currT // 1000
            ms = (currT % 1000) // 10
            self.image = self.font.render(f"Time: {s:02d}.{ms:02d}", True, "#FFFFFF")

# Function to load tilemap
def load_tilemap(tilemap):
    tiles = pygame.sprite.Group()
    for row_index, row in enumerate(tilemap):
        for col_index, tile in enumerate(row):
            if tile == "X":
                tiles.add(Tile(col_index, row_index, "#000000", "reg"))
            elif tile == "L":
                tiles.add(Tile(col_index, row_index, "#FF0000", "lava"))
            elif tile == "F":
                tiles.add(Tile(col_index, row_index, "#0000FF", "fin"))
    return tiles

def updateInstruction(lvl):
    global instruction
    if instruction:
        all_sprites.remove(instruction)
    instruction = Instruction(instructions[lvl])
    all_sprites.add(instruction)


# Initialize Pygame
pygame.init()
pygame.mixer.init()
disp = pygame.display.set_mode((dispW, dispH))
pygame.display.set_caption("Dungeon Racers")
clock = pygame.time.Clock()

jumpSound = pygame.mixer.Sound("Gameproj/Jump.wav")
deathSound = pygame.mixer.Sound("Gameproj/Death.wav")
lvlSound = pygame.mixer.Sound("Gameproj/level.wav")
jumpSound.set_volume(0.5)
deathSound.set_volume(0.5)
lvlSound.set_volume(0.5)

# Create tiles for level 1
tiles = load_tilemap(tilemaps[0])

# Create player
player = Player(50, 625)
timer = Timer(10, 760)
all_sprites = pygame.sprite.Group()
all_sprites.add(player, timer)

updateInstruction(0)

# Game loop
running = True
lvl = 0
timerStop = False
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False
 
    # Update
    all_sprites.update()

    # Check if player reached the end of the level
    for tile in tiles:
        if tile.type == "fin" and player.rect.colliderect(tile.rect):
            lvlSound.play()
            lvl = (lvl + 1) % len(tilemaps)
            tiles = load_tilemap(tilemaps[lvl])
            player.rect.x = 50
            player.rect.y = 700
            updateInstruction(lvl)

    for tile in tiles:
        if tile.type == "lava" and player.rect.colliderect(tile.rect):
            deathSound.play()
            player.rect.x = 50
            player.rect.y = 700

    if lvl == 5 and not timerStop:
        timerStop = True

    # Render
    disp.fill("#ffffff")
    tiles.draw(disp)
    all_sprites.draw(disp)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(fps)

pygame.quit()
sys.exit()
