import pygame
import math


pygame.init()
# Make game window
WIDTH, HEIGHT = 480, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Giving our game window a name
pygame.display.set_caption("Recycle Rush")

# Variables
WHITE = (255, 255, 255)
FPS = 60
RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT = (150, 250)


# Top Screen Interface
# Lives
LIVE_IMAGE_1 = pygame.image.load("heart.png")
LIVE_1 = pygame.transform.scale(LIVE_IMAGE_1, (30, 30))  
LIVE_IMAGE_2 = pygame.image.load("heart.png")
LIVE_2 = pygame.transform.scale(LIVE_IMAGE_2, (30, 30))  
LIVE_IMAGE_3 = pygame.image.load("heart.png")
LIVE_3 = pygame.transform.scale(LIVE_IMAGE_3, (30, 30))  

# Pause Button
PAUSE_IMAGE = pygame.image.load("pause.png")
PAUSE = pygame.transform.scale(PAUSE_IMAGE, (30, 30)) 

# Timer
TIMER_IMAGE_1 = pygame.image.load("timer.png")
TIMER = pygame.transform.scale(TIMER_IMAGE_1, (70, 70)) 

# 3 Recycle Bins
PAPER_BIN_IMAGE = pygame.image.load("paper.png")
PAPER_BIN = pygame.transform.scale(PAPER_BIN_IMAGE, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT))
PLASTIC_BIN_IMAGE = pygame.image.load("plastic.png")
PLASTIC_BIN = pygame.transform.scale(PLASTIC_BIN_IMAGE, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT))
GLASS_BIN_IMAGE = pygame.image.load("glass.png")
GLASS_BIN = pygame.transform.scale(GLASS_BIN_IMAGE, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT))

# Conveyor Belt
CONVEYOR_BELT_IMAGE = pygame.image.load('conveyor3.png')
CONVEYOR_BELT = pygame.transform.scale(CONVEYOR_BELT_IMAGE, (600, 50))
conveyor_belt_width = CONVEYOR_BELT.get_width()
SCROLL = 0
TILES = math.ceil(WIDTH / conveyor_belt_width) + 1

# Moving Conveyor belt
# Define the starting position of the conveypr belt
conveyor_belt_pos = (10, 300)



def draw_window():
    global SCROLL
    WIN.fill(WHITE)
    WIN.blit(TIMER, (10, 10))
    WIN.blit(PAUSE, (440, 10))
    WIN.blit(LIVE_1, (190, 10))
    WIN.blit(LIVE_2, (225, 10))
    WIN.blit(LIVE_3, (260, 10))
    WIN.blit(PAPER_BIN, (10, 540))
    WIN.blit(PLASTIC_BIN, (170, 540))
    WIN.blit(GLASS_BIN, (320, 540))
    
  
# Draw multiple copies of the conveyor belt image side by side
    for i in range(TILES):
        x = i * conveyor_belt_width - SCROLL
        y = conveyor_belt_pos[1]
        WIN.blit(CONVEYOR_BELT, (x, y))

    # Increment the scrolling position
    SCROLL += 1

    # Check if the scrolling position has exceeded the width of a single conveyor belt image
    if SCROLL > conveyor_belt_width:
        SCROLL = 0

    pygame.display.update()
    



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