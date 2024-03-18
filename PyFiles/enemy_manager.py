from pygame.sprite import _Group, Sprite


class EnemyManager:
    def __init__(self) -> None:
        pass

    def get_random_enemy(self):
        """ used to get a random enemy object to let it spawn on a tile (see MapTile class)"""
        pass

class Enemy(Sprite):
    def __init__(self) -> None:
        super().__init__()

    


class FastEnemy(Enemy):
    def __init__(self) -> None:
        super().__init__()


class SmartEnemy(Enemy):
    def __init__(self) -> None:
        super().__init__()


class TankyEnemy(Enemy):
    def __init__(self) -> None:
        super().__init__()

