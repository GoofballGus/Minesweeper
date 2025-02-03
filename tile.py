import pygame as py

py.font.init()

font = py.font.SysFont('arial', 25)


class Tile(py.sprite.Sprite):
    def __init__(self, x, y, size, screen, bee=False):
        super().__init__()
        self.x: int = x
        self.y: int = y
        self.bee: bool = bee
        self.size: int = size
        self.screen: py.Surface = screen
        self.space: py.Rect = py.Rect(self.x, self.y, self.size, self.size)
        self.revealed = False
        self.flagged = False
        self.flagPoints = [(self.x + 1, self.y + 1),
                           (self.x + 38, self.y + 38),
                           (self.x + 1, self.y + 38),
                           (self.x + 38, self.y + 1)]
        self.count = 0

        self.draw()

    def draw(self, fill='black'):
        py.draw.rect(self.screen, fill, self.space, width=1)

    def reveal(self):
        self.revealed = True
        if self.bee:
            py.draw.rect(self.screen, 'black', self.space)
            py.draw.rect(self.screen, 'light grey', self.space, width=3)
            py.draw.circle(self.screen, 'yellow', (self.x + self.size // 2, self.y + self.size // 2), self.size // 2 - 2.5)
        else:
            py.draw.rect(self.screen, 'black', self.space)
            py.draw.rect(self.screen, 'light grey', self.space, width=3)

        if self.count > 0:
            text = font.render(str(self.count), True, (255, 255, 255))
            self.screen.blit(text, (self.x + self.size // 3, self.y + self.size // 3))

        py.display.update(self.space)

    def flag(self):
        print("Flagged!")
        py.draw.polygon(self.screen, 'red', self.flagPoints)
        self.flagged = True
