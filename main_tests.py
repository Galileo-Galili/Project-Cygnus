import unittest
import pygame
from main import TrashItem, RecycleBin, RecycleRush, SCROLL_SPEED

# Test suite for the RecycleRush game
class TestRecycleRush(unittest.TestCase):
    
    # Test if a TrashItem instance is created with the correct properties
    def test_create_trash_item(self):
        trash_type = "paper"
        image = pygame.image.load('Assets/paperTrash.png')
        item = TrashItem(trash_type, image)
        
        # Check if the created instance is a TrashItem and has the correct trash_type
        self.assertIsInstance(item, TrashItem)
        self.assertEqual(item.trash_type, trash_type)

    # Test if a RecycleBin instance is created with the correct properties
    def test_create_recycle_bin(self):
        bin_type = "glass"
        image = pygame.image.load('Assets/GlassBin1.png')
        recycle_bin = RecycleBin(bin_type, image, 315, 480)
        
        # Check if the created instance is a RecycleBin and has the correct bin_type
        self.assertIsInstance(recycle_bin, RecycleBin)
        self.assertEqual(recycle_bin.bin_type, bin_type)

    # Test if a collision is correctly detected between a trash item and the corresponding recycle bin
    def test_check_collision(self):
        game = RecycleRush()
        trash_type = "paper"
        image = pygame.image.load('Assets/paperTrash.png')
        item = TrashItem(trash_type, image)
        item.rect.x, item.rect.y = game.paper_bin.rect.x, game.paper_bin.rect.y

        recycle_bin = game.paper_bin
        is_collision = item.check_collision(recycle_bin)
        
        # Check if the collision is detected as expected
        self.assertTrue(is_collision)

    # Test if a trash item's position is correctly updated upon calling the update() method
    def test_update_trash_item(self):
        trash_type = "plastic"
        image = pygame.image.load('Assets/plasticTrash.png')
        item = TrashItem(trash_type, image)
        initial_x = item.rect.x
        item.update()
        
        # Check if the trash item's x-coordinate has been updated by the scroll speed
        self.assertEqual(item.rect.x, initial_x + SCROLL_SPEED)

# Run the test suite with the specified arguments
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)
