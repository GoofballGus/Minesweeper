import math
from board import Board
import pygame as py

width = 400
height = 400
size = 40

LEFT = 1
RIGHT = 3

screen = py.display.set_mode((400, 400))
py.display.set_caption("Minesweeper")
img = py.image.load('minesweeper bomb.png')
py.display.set_icon(img)

clock = py.time.Clock()

board = Board(width, height, size, screen)

screen.fill((128, 128, 128))
board.draw()

if board.debug:
    board.rev_debug()
    py.display.flip()

mouseX, mouseY = 3, 3

while board.run:
    clock.tick(30)
    for event in py.event.get():
        if event.type == py.MOUSEBUTTONDOWN:
            mouseX = math.floor(py.mouse.get_pos()[0] / size)
            mouseY = math.floor(py.mouse.get_pos()[1] / size)
            print(mouseX, mouseY)

            tile = board.grid[mouseX][mouseY]

            if event.button == LEFT:
                print('LEFT')
                board.count_adjacent_mines(mouseX, mouseY, tile)
                board.reveal_adjacent_tiles(mouseX, mouseY, tile)
                board.reveal_tile(mouseX, mouseY)

            elif event.button == RIGHT:
                print('RIGHT')
                board.flag_tile(mouseX, mouseY)
                py.display.update()

            board.check_game()
            py.display.update()

        if event.type == py.QUIT:
            py.quit()
            quit()

    py.display.update()
