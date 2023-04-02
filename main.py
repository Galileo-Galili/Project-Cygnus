import pygame
import random


pygame.init()

# Make game window
WIDTH, HEIGHT = 480, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# Giving our game window a name
pygame.display.set_caption("Recycle Rush")

# Variables
WHITE = (255, 255, 255)
FPS = 60
RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT = (150, 250)
TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT = (70, 70)
SCROLL_SPEED = 2 # pixels per frame
TRASH_ITEMS_INTERVAL = 60 # frames between generating trash items
TRASH_ITEMS_LIST = [] # list of trash items currently on the screen
TRASH_ITEM_COUNTER = 0 # counter for generating new trash items
SCROLL = 0


# Top Screen Interface
# Lifes
def lives():
    LIFE_IMAGE_1 = pygame.image.load("heart.png")
    LIFE_1 = pygame.transform.scale(LIFE_IMAGE_1, (30, 30))  
    LIFE_IMAGE_2 = pygame.image.load("heart.png")
    LIFE_2 = pygame.transform.scale(LIFE_IMAGE_2, (30, 30))  
    LIFE_IMAGE_3 = pygame.image.load("heart.png")
    LIFE_3 = pygame.transform.scale(LIFE_IMAGE_3, (30, 30))  

    SCREEN.blit(LIFE_1, (10, 10))
    SCREEN.blit(LIFE_2, (45, 10))
    SCREEN.blit(LIFE_3, (80, 10))

# Pause Screen
def pause_screen():
    PAUSE_IMAGE = pygame.image.load("pause.png")
    PAUSE = pygame.transform.scale(PAUSE_IMAGE, (30, 30)) 

    SCREEN.blit(PAUSE, (440, 10))

# Three Recycle Bins
def recycle_bins():
    PAPER_BIN_IMAGE = pygame.image.load("paper.png")
    PAPER_BIN = pygame.transform.scale(PAPER_BIN_IMAGE, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT))
    PLASTIC_BIN_IMAGE = pygame.image.load("plastic.png")
    PLASTIC_BIN = pygame.transform.scale(PLASTIC_BIN_IMAGE, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT))
    GLASS_BIN_IMAGE = pygame.image.load("glass.png")
    GLASS_BIN = pygame.transform.scale(GLASS_BIN_IMAGE, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT))

    SCREEN.blit(PAPER_BIN, (10, 540))
    SCREEN.blit(PLASTIC_BIN, (170, 540))
    SCREEN.blit(GLASS_BIN, (320, 540))


# Trash items and moving trash items along the belt
def trash_items():

    PAPER_TRASH_IMAGE = pygame.image.load('paperTrash.png')
    PAPER_TRASH = pygame.transform.scale(PAPER_TRASH_IMAGE, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))

    PLASTIC_TRASH_IMAGE = pygame.image.load('plasticTrash.png')
    PLASTIC_TRASH = pygame.transform.scale(PLASTIC_TRASH_IMAGE, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))

    GLASS_TRASH_IMAGE = pygame.image.load('glassTrash.png')
    GLASS_TRASH = pygame.transform.scale(GLASS_TRASH_IMAGE, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))
    
    global TRASH_ITEMS_LIST, TRASH_ITEM_COUNTER
    TRASH_ITEM_COUNTER += 1
    if TRASH_ITEM_COUNTER >= TRASH_ITEMS_INTERVAL:
        # generate a new trash item
        x = -TRASH_ITEMS_WIDTH # start offscreen to the left
        y = 278 # y position on the conveyor belt
        
        trash_type = random.choice(['paper', 'plastic', 'glass'])
        
        if trash_type == 'paper':
            trash_image = PAPER_TRASH
        elif trash_type == 'plastic':
            trash_image = PLASTIC_TRASH
        else:
            trash_image = GLASS_TRASH
        TRASH_ITEMS_LIST.append({
            'image': trash_image,
            'rect': pygame.Rect(x, y, TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT),
            'type': trash_type
        })
        TRASH_ITEM_COUNTER = 0

    # update position of each trash item
    for trash_item in TRASH_ITEMS_LIST:
        trash_item['rect'].x += SCROLL_SPEED

    # remove trash items that have gone offscreen
    TRASH_ITEMS_LIST = [trash_item for trash_item in TRASH_ITEMS_LIST if trash_item['rect'].right > 0]

    # blit each trash item onto the screen
    for trash_item in TRASH_ITEMS_LIST:
        SCREEN.blit(trash_item['image'], trash_item['rect'])


# Conveyor Belt
CONVEYOR_BELT_IMAGE = pygame.image.load('conveyor3.png')
CONVEYOR_BELT = pygame.transform.scale(CONVEYOR_BELT_IMAGE, (600, 50))
conveyor_belt_width = CONVEYOR_BELT.get_width()

# Moving Conveyor belt
def conveyor_belt():
    global SCROLL
    rel_x = SCROLL % CONVEYOR_BELT.get_rect().width
    SCREEN.blit(CONVEYOR_BELT, (rel_x - CONVEYOR_BELT.get_rect().width, 350))

    if rel_x < WIDTH:
        SCREEN.blit(CONVEYOR_BELT, (rel_x, 350))
    SCROLL += SCROLL_SPEED


def draw_window():
    
    SCREEN.fill(WHITE)
    pause_screen()
    lives()
    recycle_bins() 
    trash_items()
    conveyor_belt()

    pygame.display.update()
    


# Main Loop
def main():
    clock = pygame.time.Clock()
    # Writing the run state
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()