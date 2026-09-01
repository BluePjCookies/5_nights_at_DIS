import pygame
# Load spritesheet
spritesheet = pygame.image.load(
    "/Users/Joshua/Project3/assets/Sprite/chibi-layered copy.png"
).convert_alpha()


# --------------------------------
# Get one sprite from spritesheet
# --------------------------------

def get_sprite(x, y):
    return spritesheet.subsurface(
        pygame.Rect(x, y, 16, 16)
    )


# Directions
player_images = {
    "down": get_sprite(0, 0),
    "left": get_sprite(16, 0),
    "up": get_sprite(32, 0),
    "right": pygame.transform.flip(get_sprite(16, 0),  1, 0)
}