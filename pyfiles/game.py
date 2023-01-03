from pyfiles.player import Player


class Game:
    def __init__(self):
        self.level = 0
        self.coins = 0
        self.player = Player()
        self.enemies = []
    
    def spawn_enemies(self): # набивает self.enemies объектами класса Enemy
        pass

    def update(self): # обновляет игровые объекты каждый кадр
        for el in self.enemies:
            el.update()
        self.player.update()