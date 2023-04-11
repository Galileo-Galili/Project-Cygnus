import pygame
import random

pygame.init()

WIDTH, HEIGHT = 480, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recycle Rush")

WHITE = (255, 255, 255)
FPS = 60
RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT = (150, 250)
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

    def update(self):
        self.rect.x += SCROLL_SPEED

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
        self.life_image = pygame.image.load("heart.png")
        self.life_images = [pygame.transform.scale(self.life_image, (30, 30)) for _ in range(3)]

        self.pause_image = pygame.image.load("pause.png")
        self.pause = pygame.transform.scale(self.pause_image, (30, 30))

        self.conveyor_belt_image = pygame.image.load('conveyor3.png')
        self.conveyor_belt = pygame.transform.scale(self.conveyor_belt_image, (600, 50))
        self.conveyor_scroll = 0

        self.paper_bin_image = pygame.image.load("paper.png")
        self.paper_bin = RecycleBin("paper", pygame.transform.scale(self.paper_bin_image, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT)), 10, 540)

        self.plastic_bin_image = pygame.image.load("plastic.png")
        self.plastic_bin = RecycleBin("plastic", pygame.transform.scale(self.plastic_bin_image, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT)), 170, 540)

        self.glass_bin_image = pygame.image.load("glass.png")
        self.glass_bin = RecycleBin("glass", pygame.transform.scale(self.glass_bin_image, (RECYCLE_BIN_WIDTH, RECYCLE_BIN_HEIGHT)), 320, 540)

        self.recycle_bins = pygame.sprite.Group(self.paper_bin, self.plastic_bin, self.glass_bin)

        self.paper_trash_image = pygame.image.load('paperTrash.png')
        self.paper_trash = pygame.transform.scale(self.paper_trash_image, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))

        self.plastic_trash_image = pygame.image.load('plasticTrash.png')
        self.plastic_trash = pygame.transform.scale(self.plastic_trash_image, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))

        self.glass_trash_image = pygame.image.load('glassTrash.png')
        self.glass_trash = pygame.transform.scale(self.glass_trash_image, (TRASH_ITEMS_WIDTH, TRASH_ITEMS_HEIGHT))

        self.trash_items = pygame.sprite.Group()
        self.trash_item_counter = 0

    def generate_trash_item(self):
        trash_type = random.choice(['paper', 'plastic', 'glass'])

        if trash_type == 'paper':
            trash_image = self.paper_trash
        elif trash_type == 'plastic':
            trash_image = self.plastic_trash
        else:
            trash_image = self.glass_trash

        trash_item = TrashItem(trash_type, trash_image)
        self.trash_items.add(trash_item)

    def draw_window(self):
        SCREEN.fill(WHITE)
        SCREEN.blit(self.pause, (440, 10))

        for i, life_image in enumerate(self.life_images):
            SCREEN.blit(life_image, (10 + i * 35, 10))

        self.recycle_bins.draw(SCREEN)
        self.trash_items.draw(SCREEN)
        self.draw_conveyor_belt()

        pygame.display.update()

    def draw_conveyor_belt(self):
        rel_x = self.conveyor_scroll % self.conveyor_belt.get_rect().width
        SCREEN.blit(self.conveyor_belt, (rel_x - self.conveyor_belt.get_rect().width, 350))

        if rel_x < WIDTH:
            SCREEN.blit(self.conveyor_belt, (rel_x, 350))
        self.conveyor_scroll += SCROLL_SPEED

    def run(self):
        clock = pygame.time.Clock()
        run = True
        dragging = False
        dragged_item = None

        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for trash_item in self.trash_items.sprites():
                        if trash_item.rect.collidepoint(pygame.mouse.get_pos()):
                            dragging = True
                            dragged_item = trash_item
                            trash_item.drag_offset = (
                                pygame.mouse.get_pos()[0] - trash_item.rect.x,
                                pygame.mouse.get_pos()[1] - trash_item.rect.y
                            )
                            trash_item.initial_x = trash_item.rect.x
                            trash_item.initial_y = trash_item.rect.y

                elif event.type == pygame.MOUSEMOTION:
                    if dragging and dragged_item is not None:
                        dragged_item.rect.x = pygame.mouse.get_pos()[0] - dragged_item.drag_offset[0]
                        dragged_item.rect.y = pygame.mouse.get_pos()[1] - dragged_item.drag_offset[1]

                        colliding_bin = None
                        for recycle_bin in self.recycle_bins.sprites():
                            if recycle_bin.rect.colliderect(dragged_item.rect):
                                colliding_bin = recycle_bin
                                break

                        if colliding_bin and colliding_bin.bin_type == dragged_item.trash_type:
                            self.trash_items.remove(dragged_item)
                            dragged_item = None

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragging:
                        dragging = False

                        if dragged_item is not None:
                            dragged_item.rect.x = dragged_item.initial_x
                            dragged_item.rect.y = dragged_item.initial_y
                        dragged_item = None

            self.trash_item_counter += 1
            if self.trash_item_counter >= TRASH_ITEMS_INTERVAL:
                self.generate_trash_item()
                self.trash_item_counter = 0

            self.trash_items.update()
            self.draw_window()

        pygame.quit()

if __name__ == "__main__":
    game = RecycleRush()
    game.run()

