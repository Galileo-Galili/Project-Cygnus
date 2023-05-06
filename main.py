import pygame
import random
import button
import sys
from pygame import mixer

pygame.init()
mixer.init()

# Custom swap bins events.
SWAP_BINS_EVENT = pygame.USEREVENT + 1

# Timer triggers the swap bins event every 3 seconds.
pygame.time.set_timer(SWAP_BINS_EVENT, 1000 * 3)

# Sets up the display window and background image.
WIDTH, HEIGHT = 480, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recycle Rush")
background = pygame.transform.scale(pygame.image.load('Assets/background1.jpg'), (WIDTH, HEIGHT))


# Sets up the game's colour and other game constants such as FPS, Scroll Spped of the belt, interval which items appear and size of bins and items.
WHITE = (255, 255, 255)
BROWN = (72, 60, 50)
BLACK = (0, 0, 0)
FPS = 60
RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT = (150, 280)
TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT = (80, 80)
SCROLL_SPEED = 2
TRASH_ITEMS_INTERVAL = 70



# TrashItem class represents a trash item on the conveyor belt.
class TrashItem(pygame.sprite.Sprite):
    def __init__(self, trash_type, image):
        super().__init__()
        self.trash_type = trash_type
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = -TRASH_ITEMS_WIDTH
        self.rect.y = 248
        self.dragging = False
    
    # Method to mve the trash items along the belt
    def update(self):
        if not self.dragging:
            self.rect.x += SCROLL_SPEED
            if self.rect.x > WIDTH:
                self.kill()
    
    # Check for collision with recycle bins
    def check_collision(self, recycle_bin):
        return self.rect.colliderect(recycle_bin.rect)

# RecycleBin class represents a recycling bin.
class RecycleBin(pygame.sprite.Sprite):
    def __init__(self, bin_type, image, x, y):
        super().__init__()
        self.bin_type = bin_type
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# RecycleRush class represents the main game logic and state.
class RecycleRush:
    # Initialize the game state.
    def __init__(self):

        # Loading all the music
        self.button_sound = pygame.mixer.Sound('Music/button_sound.wav')
        self.bg_music = pygame.mixer.music.load('Music/background_music.mp3')
        self.correct_sort_music = pygame.mixer.Sound('Music/correct_sort_music.mp3')
        self.life_lost_music = pygame.mixer.Sound('Music/incorrect_sort_music.wav')
        self.game_over_sound = pygame.mixer.Sound('Music/game_over.mp3')

        # Setting volume for all the music
        self.button_sound.set_volume(0.3)
        self.bg_music = pygame.mixer.music.set_volume(0.5)
        self.correct_sort_music.set_volume(0.3)
        self.game_over_sound.set_volume(0.3)
        self.life_lost_music.set_volume(0.3)


        # Loading all the images
        self.life_image = pygame.image.load("Assets/heart.png")
        self.life_images = [pygame.transform.scale(
            self.life_image, (30, 30)) for _ in range(3)]

        self.pause_image = pygame.image.load("Assets/pause.png")
        self.pause = pygame.transform.scale(self.pause_image, (30, 30))

        self.conveyor_belt_image = pygame.image.load('Assets/conveyor3.png')
        self.conveyor_belt = pygame.transform.scale(
            self.conveyor_belt_image, (600, 50))
        

        self.paper_bin_image = pygame.image.load("Assets/PaperBin.png")
        self.paper_bin = RecycleBin("paper", pygame.transform.scale(
            self.paper_bin_image, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT)), 6, 480)

        self.plastic_bin_image = pygame.image.load("Assets/PlasticBin.png")
        self.plastic_bin = RecycleBin("plastic", pygame.transform.scale(
            self.plastic_bin_image, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT)), 160, 480)

        self.glass_bin_image = pygame.image.load("Assets/GlassBin.png")
        self.glass_bin = RecycleBin("glass", pygame.transform.scale(
            self.glass_bin_image, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT)), 315, 480)

        # Sprite group for recycle bins
        self.recycle_bins = pygame.sprite.Group(
            self.paper_bin, self.plastic_bin, self.glass_bin)

        # Sprite group for trash items   
        self.trash_items = pygame.sprite.Group()
        self.trash_item_counter = 0


        # Initializing some vaiables
        self.conveyor_scroll = SCROLL_SPEED
        self.score = 0
        self.lives = 3
        self.paused = False
        self.paper_items = 0
        self.plastic_items = 0
        self.glass_items = 0

    # Check if the dragged item collides with the correct recycle bin.
    def check_collision(self, dragged_item):
        for recycle_bin in self.recycle_bins:
            if (
                dragged_item.rect.colliderect(recycle_bin.rect)
                and dragged_item.trash_type == recycle_bin.bin_type
            ):
                return True
        return False
    
    
    # Show the game over screen and display the player's score and breakdown of sorted and unsorted items.
    def game_over_screen(self):
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", 1, WHITE)
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"Score: {self.score}", 1, WHITE)

        total_items = self.score + (3 - self.lives)
        paper_percentage = (self.paper_items / total_items) * 100
        plastic_percentage = (self.plastic_items / total_items) * 100
        glass_percentage = (self.glass_items / total_items) * 100

        breakdown_font = pygame.font.Font(None, 36)
        paper_text = breakdown_font.render(
            f"Paper: {paper_percentage:.1f}%", 1, WHITE)
        plastic_text = breakdown_font.render(
            f"Plastic: {plastic_percentage:.1f}%", 1, WHITE)
        glass_text = breakdown_font.render(
            f"Glass: {glass_percentage:.1f}%", 1, WHITE)

        retry_font = pygame.font.Font(None, 36)
        retry_text = retry_font.render("Click to retry", 1, WHITE)

        while True:
            SCREEN.blit(background, (0, 0))
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
                
    # Draw the conveyor belt on the screen.
    def draw_conveyor_belt(self):
        rel_x = self.conveyor_scroll % self.conveyor_belt.get_rect().width
        SCREEN.blit(self.conveyor_belt,
                    (rel_x - self.conveyor_belt.get_rect().width, 320))

        if rel_x < WIDTH:
            SCREEN.blit(self.conveyor_belt, (rel_x, 320))
        self.conveyor_scroll += SCROLL_SPEED
    
    
    # Show the pause screen, allowing the player to resume, restart, or quit.
    def pause_screen(self):
        pause_font = pygame.font.Font(None, 72)
        PAUSE_TEXT = pause_font.render("PAUSED", True, BLACK)

        while self.paused:
            self.bg_music = pygame.mixer.music.pause()
            SCREEN.blit(background, (0, 0))
            SCREEN.blit(PAUSE_TEXT, (WIDTH // 2 - PAUSE_TEXT.get_width() //
                        2, HEIGHT // 8 - PAUSE_TEXT.get_height() // 2))

            RESUME_BUTTON = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Resume.png"), (300, 75)), pos=(WIDTH//2, 275),
                                          text_input="RESUME", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")
            RESTART_BUTTON = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Restart.png"), (300, 75)), pos=(WIDTH//2, 400),
                                           text_input="RESTART", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")
            DIFFICULTY_SELECT = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Quit.png"), (300, 75)), pos=(WIDTH//2, 525),
                                        text_input="CHANGE DIFFICULTY", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")
            QUIT_BUTTON = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Quit.png"), (300, 75)), pos=(WIDTH//2, 655),
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

            DIFFICULTY_SELECT.changeColor(pygame.mouse.get_pos())
            DIFFICULTY_SELECT.update(SCREEN)
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.button_sound.play()
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if RESUME_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        self.button_sound.play()
                        self.paused = False
                        self.bg_music = pygame.mixer.music.unpause()
                    
                    elif RESTART_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        self.button_sound.play()
                        self.__init__()
                        self.bg_music = pygame.mixer.music.play(-1)

                    elif DIFFICULTY_SELECT.checkForInput(pygame.mouse.get_pos()):
                        self.button_sound.play()
                        self.difficulty_select_screen()

                    elif QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        sys.exit()

        return True
    
    
    # Define a function to display the main menu screen.
    def main_menu_screen(self):
        
        while True:
            
            self.bg_music = pygame.mixer.music.stop()
            # Fill the screen with the background color.
            SCREEN.blit(background, (0, 0))

            # Display the game title.
            title_font = pygame.font.Font(None, 72)
            title_text = title_font.render("Recycle Rush", 1, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
            pygame.draw.rect(SCREEN, BROWN, title_rect.inflate(50, 20), border_radius=10)
            SCREEN.blit(title_text, title_rect)

            # Display the play button.
            play_button = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Resume.png"), (300, 75)), pos=(WIDTH//2, 325),
                                          text_input="PLAY", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")
            
            Quit_button = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Quit.png"), (300, 75)), pos=(WIDTH//2, 425),
                                        text_input="QUIT", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")

            # Changes Color when hovering
            play_button.changeColor(pygame.mouse.get_pos())
            play_button.update(SCREEN)

            # Changes Color when hovering
            Quit_button.changeColor(pygame.mouse.get_pos())
            Quit_button.update(SCREEN)

            # Update the display.
            pygame.display.update()

            # Handle events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.button_sound.play()
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(pygame.mouse.get_pos()):
                        self.button_sound.play()
                        self.difficulty_select_screen()
                        return
                    elif Quit_button.checkForInput(pygame.mouse.get_pos()):
                        sys.exit()   
    
    def difficulty_select_screen(self):
        
        global SCROLL_SPEED
        global TRASH_ITEMS_INTERVAL

        while True:
            
            # Fill the screen with the background color.
            SCREEN.blit(background, (0, 0))

            # Display the game title.
            title_font = pygame.font.Font(None, 52)
            title_text = title_font.render("SELECT DIFFICULTY", 1, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
            pygame.draw.rect(SCREEN, BROWN, title_rect.inflate(50, 20), border_radius=10)
            SCREEN.blit(title_text, title_rect)

            # Display the play button.
            easy_level_button = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Resume.png"), (300, 75)), pos=(WIDTH//2, 275),
                                          text_input="EASY", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")
            medium_level_button = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Restart.png"), (300, 75)), pos=(WIDTH//2, 400),
                                           text_input="MEDIUM", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")
            hard_level_button = button.Button(image=pygame.transform.scale(pygame.image.load("Assets/Quit.png"), (300, 75)), pos=(WIDTH//2, 525),
                                        text_input="HARD", font=pygame.font.Font(None, 40), base_color="#ffffff", hovering_color="#000000")

            # Changes Color when hovering
            easy_level_button.changeColor(pygame.mouse.get_pos())
            easy_level_button.update(SCREEN)

            # Changes Color when hovering
            medium_level_button.changeColor(pygame.mouse.get_pos())
            medium_level_button.update(SCREEN)

            # Changes Color when hovering
            hard_level_button.changeColor(pygame.mouse.get_pos())
            hard_level_button.update(SCREEN)

            # Update the display.
            pygame.display.update()

            # Handle events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.button_sound.play()
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_level_button.checkForInput(pygame.mouse.get_pos()):
                        self.button_sound.play()
                        SCROLL_SPEED = 1
                        TRASH_ITEMS_INTERVAL = 100
                        self.__init__()
                        self.bg_music = pygame.mixer.music.play(-1)
                        return
                        
                    
                    elif medium_level_button.checkForInput(pygame.mouse.get_pos()):
                        self.button_sound.play()
                        SCROLL_SPEED = 2
                        TRASH_ITEMS_INTERVAL = 65
                        self.__init__()
                        self.bg_music = pygame.mixer.music.play(-1)
                        return
                        
                    
                    elif hard_level_button.checkForInput(pygame.mouse.get_pos()):
                        self.button_sound.play()
                        SCROLL_SPEED = 2
                        TRASH_ITEMS_INTERVAL = 50
                        self.__init__()
                        self.bg_music = pygame.mixer.music.play(-1)
                        return                          

    # Main game loop.
    def run(self):   
        self.main_menu_screen()
        
        self.bg_music = pygame.mixer.music.play(-1)
        
        
        # Initialize the game clock and other variables.
        clock = pygame.time.Clock()
        run = True
        dragging = False    
        dragged_item = None

               
        # Main event loop.
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
                
                
                # this part handles what happens when u click mouse button on various game elements
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handling the pause button
                    if self.pause.get_rect(topleft=(440, 10)).collidepoint(
                        pygame.mouse.get_pos()
                        
                        
                    ):
                        self.button_sound.play()
                        self.paused = not self.paused
                        if self.paused:
                            if not self.pause_screen():
                                run = False
                                break

                    else:
                        # Implementing drag and drop
                        for item in self.trash_items:
                            if item.rect.collidepoint(pygame.mouse.get_pos()):
                                dragging = True
                                dragged_item = item
                                item_offset_x = item.rect.x - event.pos[0]
                                item_offset_y = item.rect.y - event.pos[1]
                                break
                
                # This part handles the drag
                elif event.type == pygame.MOUSEMOTION:
                    if dragging and dragged_item is not None:
                        dragged_item.dragging = True
                        dragged_item.rect.x = event.pos[0] + item_offset_x
                        dragged_item.rect.y = event.pos[1] + item_offset_y
                

                # This part handles collision handling
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragging and dragged_item is not None:
                        dragged_item.dragging = False
                        correct_drop = False
                        for recycle_bin in self.recycle_bins:
                            if self.check_collision(dragged_item):
                                correct_drop = True
                                self.score += 1

                                if dragged_item.trash_type == "paper":
                                    self.paper_items += 1
                                elif dragged_item.trash_type == "plastic":
                                    self.plastic_items += 1
                                elif dragged_item.trash_type == "glass":
                                    self.glass_items += 1

                                dragged_item.kill()

                                self.correct_sort_music.play()
                                break

                        if not correct_drop: 
                            
                            self.lives -= 1
                            dragged_item.kill()
                            if self.lives >=1:
                                self.life_lost_music.play()

                        dragging = False
                        dragged_item = None

            if not self.paused:
                
                SCREEN.blit(background, (0, 0))
                self.trash_item_counter += 1

                # This part blits trash items onto the screen randomly
                if self.trash_item_counter % TRASH_ITEMS_INTERVAL == 0:
                    trash_type = random.choice(["paper", "plastic", "glass"])
                    random_num = random.randint(1, 4)
                    trash_image = pygame.image.load(f'Assets/{trash_type.capitalize()}{random_num}.png')
                    trash_image = pygame.transform.scale(trash_image, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))
                    trash_item = TrashItem(trash_type, trash_image)
                    self.trash_items.add(trash_item)

                self.trash_items.update()
                for item in self.trash_items:
                    if item.rect.x >= WIDTH:
                        self.lives -= 1
                        item.kill()
                        if self.lives >=1:
                            self.life_lost_music.play()
                        

                self.draw_conveyor_belt()
                self.recycle_bins.draw(SCREEN)
                self.trash_items.draw(SCREEN)

                
                # This part manages the lives
                for i in range(self.lives):
                    SCREEN.blit(self.life_images[i], (10 + 40 * i, 10))

                score_text = pygame.font.Font(
                    None, 36).render(str(self.score), 1, WHITE)
                SCREEN.blit(score_text, (WIDTH // 2 -
                            score_text.get_width() // 2, 10))

                SCREEN.blit(self.pause, (440, 10))

                pygame.display.update()

                # This part calls the game over screem
                if self.lives <= 0:
                    self.bg_music = pygame.mixer.music.pause()
                    self.game_over_sound.play()

                    # Call the game_over_screen() method when the game ends
                    if self.game_over_screen():
                        # Restart the game after the game over screen
                        self.game_over_sound.stop()
                        self.__init__()
                        self.run()
                    else:
                        pygame.quit()

# Run the game.
if __name__ == "__main__":
    game = RecycleRush()
    game.run()
