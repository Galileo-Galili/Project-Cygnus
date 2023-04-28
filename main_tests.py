import pygame
from main import TrashItem, RecycleBin

pygame.init()

def test_trash_item_creation():
    trash_type = "paper"
    image = pygame.Surface((70, 70))
    trash_item = TrashItem(trash_type, image)

    assert trash_item.trash_type == trash_type
    assert trash_item.image == image
    assert trash_item.rect.width == 70
    assert trash_item.rect.height == 70

def test_recycle_bin_creation():
    bin_type = "paper"
    image = pygame.Surface((150, 280))
    x, y = 6, 480
    recycle_bin = RecycleBin(bin_type, image, x, y)

    assert recycle_bin.bin_type == bin_type
    assert recycle_bin.image == image
    assert recycle_bin.rect.x == x
    assert recycle_bin.rect.y == y

def test_trash_item_collision():
    trash_type = "plastic"
    image = pygame.Surface((70, 70))
    trash_item = TrashItem(trash_type, image)
    trash_item.rect.x = 5
    trash_item.rect.y = 5

    recycle_bin = RecycleBin("plastic", pygame.Surface((150, 280)), 0, 0)

    assert trash_item.check_collision(recycle_bin)

def test_trash_item_no_collision():
    trash_type = "glass"
    image = pygame.Surface((70, 70))
    trash_item = TrashItem(trash_type, image)
    trash_item.rect.x = 200
    trash_item.rect.y = 200

    recycle_bin = RecycleBin("glass", pygame.Surface((150, 280)), 0, 0)

    assert not trash_item.check_collision(recycle_bin)

if __name__ == "__main__":
    test_trash_item_creation()
    test_recycle_bin_creation()
    test_trash_item_collision()
    test_trash_item_no_collision()
    print("All tests passed.")
