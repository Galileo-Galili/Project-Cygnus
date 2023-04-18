import pygame

class TrashItems(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, image):
        super().__init__()
        self.width = width
        self.height = height
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))

    def add_trash_images():
        