import time

import pygame as pg
import random
import sys

class Recursionlimit:
    def __init__(self, limit):
        self.limit = limit
        self.old_limit = 1_000

    def __enter__(self):
        self.old_limit = sys.getrecursionlimit()
        sys.setrecursionlimit(self.limit)

    def __exit__(self, type, value, tb):
        sys.setrecursionlimit(self.old_limit)


class CellsInABlob:
    NORMAL_CELL = (127, 255, 127)
    ANORMAL_CELL = (255, 127, 127)
    COUNTED_CELL = (127, 127, 255)

    ANORMAL_PERCENT = 0.5

    def count(self):
        r, c = random.randint(0, self.CELLS -1), random.randint(0, self.CELLS -1)
        while self.grid[r][c] != self.ANORMAL_CELL:
            r, c = random.randint(0, self.CELLS -1), random.randint(0, self.CELLS -1)

        self.update_cell(r, c)
        with Recursionlimit(100_000):
            return self.count_cells(r, c)

    def count_cells(self, r, c):
        if (not 0 <= r < self.CELLS) or (not 0 <= c < self.CELLS):
            return 0
        elif self.grid[r][c] != self.ANORMAL_CELL:
            return 0
        else:
            self.grid[r][c] = self.COUNTED_CELL
            self.update_cell(r, c)
            self.clock.tick(240)

            counted = 1
            to_check = [
                (r-1, c-1),
                (r-1, c),
                (r, c-1),
                (r+1, c+1),
                (r+1, c),
                (r, c+1),
                (r-1, c+1),
                (r+1, c-1),
            ]
            for _ in range(8):
                check = random.randint(0, len(to_check) - 1)
                counted += self.count_cells(*to_check.pop(check))

            return counted

    def __init__(self, number_of_cells, screen_size):
        self.CELLS = number_of_cells
        self.SCREEN_SIZE = screen_size

        self.CELL_SIZE = self.SCREEN_SIZE // self.CELLS

        self.run()

    def _generate_grid(self):
        self.grid = [[self.NORMAL_CELL for _ in range(self.CELLS)] for _ in range(self.CELLS)]

        for _ in range(int(self.CELLS ** 2 * self.ANORMAL_PERCENT)):
            r = random.randint(0, self.CELLS - 1)
            c = random.randint(0, self.CELLS - 1)

            self.grid[r][c] = self.ANORMAL_CELL

        self.grid[0][0] = self.ANORMAL_CELL

    def draw_grid(self):
        for r in range(self.CELLS):
            for c in range(self.CELLS):
                color = pg.Color(self.grid[r][c])
                pg.draw.rect(self.screen, color, pg.Rect(c * self.CELL_SIZE, r * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
        pg.display.flip()

    def run(self):
        pg.init()
        pg.font.init()
        myfont = pg.font.SysFont('Comic Sans MS', 100)
        self.screen = pg.display.set_mode((self.SCREEN_SIZE, self.SCREEN_SIZE))
        pg.display.set_caption("Cells In A Blob")
        self.clock = pg.time.Clock()
        run = True
        while run:
            self._generate_grid()
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    run = False

            self.draw_grid()
            count = self.count()
            textsurface = myfont.render(str(count), False, (0, 0, 0))
            self.screen.blit(textsurface,(0, 0))
            pg.display.flip()
            time.sleep(5)

    def update_cell(self, r, c):
        color = pg.Color(self.grid[r][c])
        pg.draw.rect(self.screen, color, pg.Rect(c * self.CELL_SIZE, r * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))
        pg.display.flip()


def main():
    CellsInABlob(100, 800)


if __name__ == '__main__':
    try:
        main()
    except BaseException as e:
        print(e)
