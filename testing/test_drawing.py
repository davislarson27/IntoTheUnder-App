import pygame
from play.inventory.items_management import Inventory
from components.blocks.blocks import *

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Test Drawing")
clock = pygame.time.Clock()

# Create inventory
inventory = Inventory(screen, None, INVENTORY_HEIGHT=100, HEALTH_BAR_HEIGHT=50)
for i in range(1): inventory.add_item(Dirt)
for i in range(3): inventory.add_item(Rock)

inventory.build_from_current()

for i in range(2): inventory.add_item(Grass)



# Main loop
running = True
while running:
    mouse = pygame.mouse
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check clicks
    inventory.check_click(mouse, mx, my)
    
    # Clear screen
    screen.fill((220, 220, 220))

    inventory.draw()
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()