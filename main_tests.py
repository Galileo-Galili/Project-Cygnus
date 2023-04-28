import unittest
import pygame
from main import TrashItem, RecycleBin, RecycleRush, SCROLL_SPEED

class TestRecycleRush(unittest.TestCase):
    def test_create_trash_item(self):
        trash_type = "paper"
        image = pygame.image.load('Assets/paperTrash.png')
        item = TrashItem(trash_type, image)
        self.assertIsInstance(item, TrashItem)
        self.assertEqual(item.trash_type, trash_type)

    def test_create_recycle_bin(self):
        bin_type = "glass"
        image = pygame.image.load('Assets/GlassBin1.png')
        recycle_bin = RecycleBin(bin_type, image, 315, 480)
        self.assertIsInstance(recycle_bin, RecycleBin)
        self.assertEqual(recycle_bin.bin_type, bin_type)

    def test_check_collision(self):
        game = RecycleRush()
        trash_type = "paper"
        image = pygame.image.load('Assets/paperTrash.png')
        item = TrashItem(trash_type, image)
        item.rect.x, item.rect.y = 6, 480

        recycle_bin = game.paper_bin
        is_collision = item.check_collision(recycle_bin)
        self.assertTrue(is_collision)

    def test_update_trash_item(self):
        trash_type = "plastic"
        image = pygame.image.load('Assets/plasticTrash.png')
        item = TrashItem(trash_type, image)
        initial_x = item.rect.x
        item.update()
        self.assertEqual(item.rect.x, initial_x + SCROLL_SPEED)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
