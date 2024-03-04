import pygame

from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

dispW = 600
dispH = 800

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill(("#FA8072"))
        self.rect = self.surf.get_rect()

    def update(self, pressedKeys):
        if pressedKeys[K_w]:
            self.rect.move_ip(0, -5)
        if pressedKeys[K_s]:
            self.rect.move_ip(0, 5)
        if pressedKeys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressedKeys[K_d]:
            self.rect.move_ip(5, 0)
    
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > dispW:
            self.rect.right = dispW
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= dispH:
            self.rect.bottom = dispH

pygame.mixer.init()

pygame.init()

clock = pygame.time.Clock()

disp = pygame.display.set_mode((dispW, dispH))

player = Player()

allSprite = pygame.sprite.Group()
allSprite.add(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False
    
    pressedKeys = pygame.key.get_pressed()
    player.update(pressedKeys)

    disp.fill((255, 255, 255))

    for entity in allSprite:
        disp.blit(entity.surf, entity.rect)

    """if pygame.sprite.spritecollideany(player):
        print("WIP")"""

    pygame.display.flip()

    clock.tick(60)

