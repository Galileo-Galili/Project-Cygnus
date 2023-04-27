import pygame
import random
import button
import sys
from pygame import mixer

pygame.init()
mixer.init()
# Add this line after the imports
SWAP_BINS_EVENT = pygame.USEREVENT + 1

# Add this line after initializing pygame
pygame.time.set_timer(SWAP_BINS_EVENT, 1000 * 3)  # 20 Seconds

WIDTH, HEIGHT = 480, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recycle Rush")
background = pygame.transform.scale(pygame.image.load('Assets/background1.jpg'), (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT = (150, 280)
TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT = (70, 70)
SCROLL_SPEED = 1
TRASH_ITEMS_INTERVAL = 120




class TrashItem(pygame.sprite.Sprite):
    def __init__(self, trash_type, image):
        super().__init__()
        self.trash_type = trash_type
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = -TRASH_ITEMS_WIDTH
        self.rect.y = 278
        self.dragging = False

    def update(self):
        if not self.dragging:
            self.rect.x += SCROLL_SPEED
            if self.rect.x > WIDTH:
                self.kill()


class RecycleBin(pygame.sprite.Sprite):
    def __init__(self, bin_type, image, x, y):
        super().__init__()
        self.bin_type = bin_type
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class RecycleRush:
    def __init__(self):
        self.life_image = pygame.image.load("Assets/heart.png")
        self.life_images = [pygame.transform.scale(
            self.life_image, (30, 30)) for _ in range(3)]

        self.pause_image = pygame.image.load("Assets/pause.png")
        self.pause = pygame.transform.scale(self.pause_image, (30, 30))

        self.conveyor_belt_image = pygame.image.load('Assets/conveyor3.png')
        self.conveyor_belt = pygame.transform.scale(
            self.conveyor_belt_image, (600, 50))
        self.conveyor_scroll = 0

        self.paper_bin_image = pygame.image.load("Assets/PaperBin1.png")
        self.paper_bin = RecycleBin("paper", pygame.transform.scale(
            self.paper_bin_image, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT)), 6, 480)

        self.plastic_bin_image = pygame.image.load("Assets/PlasticBin2.png")
        self.plastic_bin = RecycleBin("plastic", pygame.transform.scale(
            self.plastic_bin_image, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT)), 160, 480)

        self.glass_bin_image = pygame.image.load("Assets/GlassBin1.png")
        self.glass_bin = RecycleBin("glass", pygame.transform.scale(
            self.glass_bin_image, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT)), 315, 480)

        self.recycle_bins = pygame.sprite.Group(
            self.paper_bin, self.plastic_bin, self.glass_bin)

        self.paper_trash_image = pygame.image.load('Assets/paperTrash.png')
        self.paper_trash = pygame.transform.scale(
            self.paper_trash_image, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))

        self.plastic_trash_image = pygame.image.load('Assets/plasticTrash.png')
        self.plastic_trash = pygame.transform.scale(
            self.plastic_trash_image, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))

        self.glass_trash_image = pygame.image.load('Assets/glassTrash.png')
        self.glass_trash = pygame.transform.scale(
            self.glass_trash_image, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))

        self.trash_items = pygame.sprite.Group()
        self.trash_item_counter = 0

        

        self.score = 0
        self.lives = 3
        self.paused = False

        self.paper_items = 0
        self.plastic_items = 0
        self.glass_items = 0


        
        
    

    def game_over_screen(self):
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", 1, BLACK)
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"Score: {self.score}", 1, BLACK)

        total_items = self.score + (3 - self.lives)
        paper_percentage = (self.paper_items / total_items) * 100
        plastic_percentage = (self.plastic_items / total_items) * 100
        glass_percentage = (self.glass_items / total_items) * 100

        breakdown_font = pygame.font.Font(None, 36)
        paper_text = breakdown_font.render(
            f"Paper: {paper_percentage:.1f}%", 1, BLACK)
        plastic_text = breakdown_font.render(
            f"Plastic: {plastic_percentage:.1f}%", 1, BLACK)
        glass_text = breakdown_font.render(
            f"Glass: {glass_percentage:.1f}%", 1, BLACK)

        retry_font = pygame.font.Font(None, 36)
        retry_text = retry_font.render("Click to retry", 1, BLACK)

        while True:
            SCREEN.fill(WHITE)
            SCREEN.blit(game_over_text, (WIDTH // 2 -
                        game_over_text.get_width() // 2, 150))
            SCREEN.blit(score_text, (WIDTH // 2 -
                        score_text.get_width() // 2, 250))
            SCREEN.blit(paper_text, (WIDTH // 2 -
                        paper_text.get_width() // 2, 350))
            SCREEN.blit(plastic_text, (WIDTH // 2 -
                        plastic_text.get_width() // 2, 400))
            SCREEN.blit(glass_text, (WIDTH // 2 -
                        glass_text.get_width() // 2, 450))
            SCREEN.blit(retry_text, (WIDTH // 2 -
                        retry_text.get_width() // 2, 550))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return True

    def draw_conveyor_belt(self):
        rel_x = self.conveyor_scroll % self.conveyor_belt.get_rect().width
        SCREEN.blit(self.conveyor_belt,
                    (rel_x - self.conveyor_belt.get_rect().width, 350))

        if rel_x < WIDTH:
            SCREEN.blit(self.conveyor_belt, (rel_x, 350))
        self.conveyor_scroll += SCROLL_SPEED

    def pause_screen(self):
        pause_font = pygame.font.Font(None, 72)
        PAUSE_TEXT = pause_font.render("PAUSED", True, BLACK)

        while self.paused:
            self.bg_music = pygame.mixer.music.pause()
            SCREEN.fill(WHITE)
            SCREEN.blit(PAUSE_TEXT, (WIDTH // 2 - PAUSE_TEXT.get_width() //
                        2, HEIGHT // 8 - PAUSE_TEXT.get_height() // 2))

            RESUME_BUTTON = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Resume.png"), (300, 75)), pos=(WIDTH//2, 275),
                                          text_input="RESUME", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")
            RESTART_BUTTON = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Restart.png"), (300, 75)), pos=(WIDTH//2, 400),
                                           text_input="RESTART", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")
            QUIT_BUTTON = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Quit.png"), (300, 75)), pos=(WIDTH//2, 525),
                                        text_input="QUIT", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")
            # Changes Color when hovering
            RESUME_BUTTON.changeColor(pygame.mouse.get_pos())
            RESUME_BUTTON.update(SCREEN)

            # Changes Color when hovering
            RESTART_BUTTON.changeColor(pygame.mouse.get_pos())
            RESTART_BUTTON.update(SCREEN)

            # Changes Color when hovering
            QUIT_BUTTON.changeColor(pygame.mouse.get_pos())
            QUIT_BUTTON.update(SCREEN)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if RESUME_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        self.paused = False
                        self.bg_music = pygame.mixer.music.unpause()
                    elif RESTART_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        self.__init__()
                        self.bg_music = pygame.mixer.music.play(-1)
                    elif QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        sys.exit()

        return True

    def run(self):
        self.bg_music = pygame.mixer.music.load('Music/background_music.mp3')
        self.bg_music = pygame.mixer.music.play(-1)
        self.bg_music = pygame.mixer.music.set_volume(0.3)
        clock = pygame.time.Clock()
        switching_bins = False
        run = True
        dragging = False
        dragged_item = None

        while run:
            clock.tick(FPS)
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                 #This block handles the SWAP_BINS_EVENT
                elif event.type == SWAP_BINS_EVENT:
                    if not dragging:
                        recycle_bin_positions = [bin.rect.x for bin in self.recycle_bins]
                        random.shuffle(recycle_bin_positions)
                        for i, recycle_bin in enumerate(self.recycle_bins):
                            recycle_bin.rect.x = recycle_bin_positions[i]

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause.get_rect(topleft=(440, 10)).collidepoint(
                        pygame.mouse.get_pos()
                    ):
                        self.paused = not self.paused
                        if self.paused:
                            if not self.pause_screen():
                                run = False
                                break

                    else:
                        for item in self.trash_items:
                            if item.rect.collidepoint(pygame.mouse.get_pos()):
                                dragging = True
                                dragged_item = item
                                item_offset_x = item.rect.x - event.pos[0]
                                item_offset_y = item.rect.y - event.pos[1]
                                break

                elif event.type == pygame.MOUSEMOTION:
                    if dragging and dragged_item is not None:
                        dragged_item.dragging = True
                        dragged_item.rect.x = event.pos[0] + item_offset_x
                        dragged_item.rect.y = event.pos[1] + item_offset_y

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragging and dragged_item is not None:
                        dragged_item.dragging = False
                        correct_drop = False
                        for recycle_bin in self.recycle_bins:
                            if (
                                dragged_item.rect.colliderect(recycle_bin.rect)
                                and dragged_item.trash_type == recycle_bin.bin_type
                            ):
                                correct_drop = True
                                self.score += 1

                                if dragged_item.trash_type == "paper":
                                    self.paper_items += 1
                                elif dragged_item.trash_type == "plastic":
                                    self.plastic_items += 1
                                elif dragged_item.trash_type == "glass":
                                    self.glass_items += 1

                                dragged_item.kill()
                                break

                        if (
                            not correct_drop
                            and dragged_item.rect.y >= HEIGHT - RECYCLE_BIN_HEIGHT - 20
                        ):
                            self.lives -= 1
                            dragged_item.kill()

                        dragging = False
                        dragged_item = None

            if not self.paused:
                SCREEN.blit(background, (0, 0))
                
                self.trash_item_counter += 1
                if self.trash_item_counter % TRASH_ITEMS_INTERVAL == 0:
                    trash_type = random.choice(["paper", "plastic", "glass"])
                    trash_image = {
                        "paper": self.paper_trash,
                        "plastic": self.plastic_trash,
                        "glass": self.glass_trash,
                    }[trash_type]
                    trash_item = TrashItem(trash_type, trash_image)
                    self.trash_items.add(trash_item)

                self.trash_items.update()
                for item in self.trash_items:
                    if item.rect.x >= WIDTH:
                        self.lives -= 1
                        item.kill()
                        

                self.draw_conveyor_belt()
                self.recycle_bins.draw(SCREEN)
                self.trash_items.draw(SCREEN)

                

                for i in range(self.lives):
                    SCREEN.blit(self.life_images[i], (10 + 40 * i, 10))

                score_text = pygame.font.Font(
                    None, 36).render(str(self.score), 1, BLACK)
                SCREEN.blit(score_text, (WIDTH // 2 -
                            score_text.get_width() // 2, 10))

                SCREEN.blit(self.pause, (440, 10))

                pygame.display.update()

                if self.lives <= 0:
                    self.bg_music = pygame.mixer.music.pause()
                    pygame.mixer.music.load('Music/gameover_music.mp3')
                    pygame.mixer.music.play()

                    # Call the game_over_screen() method when the game ends
                    if self.game_over_screen():
                        # Restart the game after the game over screen
                        self.__init__()
                        self.run()
                    else:
                        pygame.quit()


if __name__ == "__main__":
    game = RecycleRush()
    game.run()

