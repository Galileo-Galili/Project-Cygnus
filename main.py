import pygame
import random
import sys
from button import Button


pygame.init()

# Make game window
WIDTH, HEIGHT = 480, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
# Giving our game window a name
pygame.display.set_caption("Recycle Rush")

# Variables
WHITE = (255, 255, 255)
FPS = 60

# Start time for timer
start_time = pygame.time.get_ticks()

RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT = (150, 250)
TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT = (70, 70)
TRASH_ITEMS_SPEED = 1  # pixels per frame
TRASH_ITEMS_INTERVAL = 120  # frames between generating trash items
trash_items_list = []  # list of trash items currently on the screen
trash_items_counter = 0  # counter for generating new trash items


# Top Screen Interface
font = pygame.font.Font(None, 36)  # Font for text
# Lifes
LIFE_IMAGE_1 = pygame.image.load("Assets/heart.png")
LIFE_1 = pygame.transform.scale(LIFE_IMAGE_1, (30, 30))
LIFE_IMAGE_2 = pygame.image.load("Assets/heart.png")
LIFE_2 = pygame.transform.scale(LIFE_IMAGE_2, (30, 30))
LIFE_IMAGE_3 = pygame.image.load("Assets/heart.png")
LIFE_3 = pygame.transform.scale(LIFE_IMAGE_3, (30, 30))

# Pause Button
PAUSE_IMAGE = pygame.image.load("Assets/pause.png")
PAUSE = pygame.transform.scale(PAUSE_IMAGE, (30, 30))
pause_rect = PAUSE.get_rect()
pause_rect.top = 0
pause_rect.right = 480

# 3 Recycle Bins
PAPER_BIN_IMAGE = pygame.image.load("Assets/paper.png")
PAPER_BIN = pygame.transform.scale(
    PAPER_BIN_IMAGE, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT))
PLASTIC_BIN_IMAGE = pygame.image.load("Assets/plastic.png")
PLASTIC_BIN = pygame.transform.scale(
    PLASTIC_BIN_IMAGE, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT))
GLASS_BIN_IMAGE = pygame.image.load("Assets/glass.png")
GLASS_BIN = pygame.transform.scale(
    GLASS_BIN_IMAGE, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT))

# Trash Items
PAPER_TRASH_IMAGE = pygame.image.load('Assets/paperTrash.png')
PAPER_TRASH = pygame.transform.scale(
    PAPER_TRASH_IMAGE, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))

PLASTIC_TRASH_IMAGE = pygame.image.load('Assets/plasticTrash.png')
PLASTIC_TRASH = pygame.transform.scale(
    PLASTIC_TRASH_IMAGE, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))

GLASS_TRASH_IMAGE = pygame.image.load('Assets/glassTrash.png')
GLASS_TRASH = pygame.transform.scale(
    GLASS_TRASH_IMAGE, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))


# Conveyor Belt
CONVEYOR_BELT_IMAGE = pygame.image.load('Assets/conveyor3.png')
CONVEYOR_BELT = pygame.transform.scale(CONVEYOR_BELT_IMAGE, (600, 50))
conveyor_belt_width = CONVEYOR_BELT.get_width()
SCROLL = 0

# MOVING TRASH ITEMS


def trash_items():
    global trash_items_list, trash_items_counter
    trash_items_counter += 1
    if trash_items_counter >= TRASH_ITEMS_INTERVAL:
        # generate a new trash item
        x = -TRASH_ITEMS_WIDTH  # start offscreen to the left
        y = 278  # y position on the conveyor belt

        trash_type = random.choice(['paper', 'plastic', 'glass'])

        if trash_type == 'paper':
            trash_image = PAPER_TRASH
        elif trash_type == 'plastic':
            trash_image = PLASTIC_TRASH
        else:
            trash_image = GLASS_TRASH
        trash_items_list.append({
            'image': trash_image,
            'rect': pygame.Rect(x, y, TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT),
            'type': trash_type
        })
        trash_items_counter = 0

    # update position of each trash item
    for trash_item in trash_items_list:
        trash_item['rect'].x += TRASH_ITEMS_SPEED

    # remove trash items that have gone offscreen
    trash_items_list = [
        trash_item for trash_item in trash_items_list if trash_item['rect'].right > 0]

    # blit each trash item onto the screen
    for trash_item in trash_items_list:
        SCREEN.blit(trash_item['image'], trash_item['rect'])

# Moving Conveyor belt


def conveyor_belt():
    global SCROLL
    rel_x = SCROLL % CONVEYOR_BELT.get_rect().width
    SCREEN.blit(CONVEYOR_BELT, (rel_x - CONVEYOR_BELT.get_rect().width, 350))

    if rel_x < WIDTH:
        SCREEN.blit(CONVEYOR_BELT, (rel_x, 350))
    SCROLL += 1


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Assets/font.ttf", size)


def paused():
    clicked = True

    PAUSE_MOUSE_POS = pygame.mouse.get_pos()
    while clicked:
        SCREEN.fill((255, 255, 255))
        PAUSE_TEXT = get_font(45).render("PAUSED", True, "Black")
        PAUSE_RECT = PAUSE_TEXT.get_rect(center=(WIDTH/2, 150))
        SCREEN.blit(PAUSE_TEXT, PAUSE_RECT)

        RESUME_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("Assets/Play Rect.png"), (300, 75)), pos=(WIDTH//2, 275),
                               text_input="RESUME", font=get_font(30), base_color="#ffffff", hovering_color="#000000")
        RESTART_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("Assets/Options Rect.png"), (300, 75)), pos=(WIDTH//2, 400),
                                text_input="RESTART", font=get_font(30), base_color="#ffffff", hovering_color="#000000")
        QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("Assets/Quit Rect.png"), (300, 75)), pos=(WIDTH//2, 525),
                             text_input="QUIT", font=get_font(30), base_color="#ffffff", hovering_color="#000000")

        for button in [RESUME_BUTTON, RESTART_BUTTON, QUIT_BUTTON]:
            button.changeColor(PAUSE_MOUSE_POS)
            button.update(SCREEN)

        PAUSE_BACK = Button(image=None, pos=(850, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        PAUSE_BACK.changeColor(PAUSE_MOUSE_POS)
        PAUSE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PAUSE_BACK.checkForInput(PAUSE_MOUSE_POS):
                    play()
                # if PLAY_BUTTON.checkForInput(PAUSE_MOUSE_POS):
                #     play()
                # if OPTIONS_BUTTON.checkForInput(PAUSE_MOUSE_POS):
                #     play()
                # if QUIT_BUTTON.checkForInput(PAUSE_MOUSE_POS):
                #     pygame.quit()
                #     sys.exit()

        pygame.display.update()


def timer():
    global timer_text

    # Blit the timer text onto the screen at position (10, 10)
    elapsed_time_seconds = (pygame.time.get_ticks() - start_time) // 1000
    elapsed_time_minutes = elapsed_time_seconds // 60
    elapsed_time_seconds %= 60

    timer_text = font.render(
        f"{elapsed_time_minutes:02}:{elapsed_time_seconds:02}", True, (0, 0, 0))


def draw_window():
    SCREEN.fill((255, 255, 0))
    SCREEN.blit(PAUSE, (440, 10))
    SCREEN.blit(LIFE_1, (WIDTH/2 - 40, 10))
    SCREEN.blit(LIFE_2, (WIDTH/2 - 10, 10))
    SCREEN.blit(LIFE_3, (WIDTH/2 + 20, 10))
    SCREEN.blit(PAPER_BIN, (10, 540))
    SCREEN.blit(PLASTIC_BIN, (170, 540))
    SCREEN.blit(GLASS_BIN, (320, 540))
    SCREEN.blit(timer_text, (10, 15))
    trash_items()
    conveyor_belt()
    pygame.draw.rect(SCREEN, (0, 0, 0), (6, 10, 70, 30), width=2)
    pygame.display.update()


def play():
    clock = pygame.time.Clock()

    # PAUSE_BUTTON = Button(image=pygame.image.load("Assets/pause.png"), pos=(440, 10),
    #                       text_input="PAUSE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    # Writing the run state
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_rect.collidepoint(event.pos):
                    print("Image Clicked")
                    paused()

            # SCREEN.blit()
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if PAUSE_BUTTON.checkForInput(pygame.mouse.get_pos):
            #         paused()
        timer()
        draw_window()

    pygame.quit()


if __name__ == "__main__":
    play()
