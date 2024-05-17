
import pygame
import random
from variables import *


SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

class Shape:
    VERSION = {
        'I': [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z': [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S': [[6, 7, 9, 10], [1, 5, 6, 10]],
        'L': [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J': [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T': [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O': [[1, 2, 5, 6]]
    }
    SHAPES = ['I', 'Z', 'S', 'L', 'J', 'T', 'O']
 
    #init
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(self.SHAPES)
        self.shape = self.VERSION[self.type]
        self.color = random.randint(1,4)
        self.orientation = 0

    #image
    def image(self):
        return self.shape[self.orientation]
    
    #rotate
    def rotate(self):
        self.orientation = (self.orientation + 1) % len(self.shape)

#Game class
class Tetris:

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.score = 0
        self.level = 1
        self.grid = [[0 for i in range(cols)] for j in range(rows)]
        self.next = None
        self.end = False
        self.new_shape()

    def make_grid(self):
        for i in range(self.rows + 1):
            pygame.draw.line(SCREEN, GRID, (0, CELL*i), (WIDTH, CELL*i))
        for j in range(self.cols + 1):
            pygame.draw.line(SCREEN, GRID, (CELL*j, 0), (CELL * j, (HEIGHT - 120))) 

    def new_shape(self):
        if not self.next:
            self.next = Shape(5,0)
        self.figure = self.next
        self.next = Shape(5,0)

    def collision(self):
        for i in range(4):
            for j in range(4):
                if(i*4 + j) in self.figure.image():
                    block_row = i + self.figure.y 
                    block_col = j + self.figure.x
                    # print(f'BR = {block_row} and BC = {block_col}')
                    if(block_row >= self.rows or block_col >= self.cols or block_col<0 or self.grid[block_row][block_col]>0):
                        return True
        
        return False
    
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if (i * 4 + j) in self.figure.image():
                    self.grid[i+self.figure.y][j+self.figure.x] = self.figure.color
                    

        self.remove_row()
        self.new_shape()
        if self.collision():
            self.end = True
    
    def remove_row(self):
        rerun = False
        for y in range(self.rows-1, 0, -1):
            completed = True
            
            for x in range(0, self.cols):
                if self.grid[y][x] == 0:
                    completed = False
                
            if completed:
                del self.grid[y]
                print()
                self.grid.insert(0, [0 for i in range(self.cols)])
                self.score += 1
                if self.score % 5 == 0:
                    self.level += 1
                rerun = True

        if rerun:
            self.remove_row() 


    def move_down(self):
        self.figure.y += 1
        if self.collision():
            self.figure.y -=1
            self.freeze()

    def move_left(self):
        self.figure.x -= 1
        if self.collision():
            self.figure.x += 1
    
    def move_right(self):
        self.figure.x += 1
        if self.collision():
            self.figure.x -= 1

    def freefall(self):
        while not self.collision():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def rotate(self):
        orientation = self.figure.orientation
        self.figure.rotate()
        if self.collision():
            self.figure.orientation = orientation

    def end_game(self):
        popup = pygame.Rect(50, 140, WIDTH - 100, HEIGHT - 350)
        pygame.draw.rect(SCREEN, BLACK, popup)
        pygame.draw.rect(SCREEN, LOSE, popup, 2)

        game_over = font2.render("GAME OVER!", True, WHITE )
        option1 =  font2.render("Press r to restart", True, LOSE)
        option2 =  font2.render("Press q to quit", True, LOSE)

        SCREEN.blit(game_over, (popup.centerx-game_over.get_width()/2, popup.y+20))
        SCREEN.blit(option1, (popup.centerx-option1.get_width()/2, popup.y+80))
        SCREEN.blit(option2, (popup.centerx-option2.get_width()/2, popup.y+110))
