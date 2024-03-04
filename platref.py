import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Platformer")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load the tile map
tile_map = [
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
    "P                                                          P",
    "P                                                          P",
    "P                                                          P",
    "P                                                          P",
    "P                                                          P",
    "P                                                          P",
    "P                                                          P",
    "P                                                          P",
    "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
]

# Define tile size and map dimensions
TILE_SIZE = 32
MAP_WIDTH = len(tile_map[0]) * TILE_SIZE
MAP_HEIGHT = len(tile_map) * TILE_SIZE

# Define player properties
player_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
player_image.fill((255, 0, 0))
player_rect = player_image.get_rect()
player_rect.x = 100
player_rect.y = 100
player_speed = 5

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # Draw background
    screen.fill(WHITE)

    # Draw tile map
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == "P":
                pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw player
    screen.blit(player_image, player_rect)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()