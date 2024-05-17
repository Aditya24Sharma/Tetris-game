import pygame
import sys
from variables import *
from classes import Shape, Tetris

pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    tetris = Tetris(ROWS, COLS)
    clock = pygame.time.Clock()
    counter = 0
    move = True
    run = True
    space_pressed = False
    while run:
        SCREEN.fill(BG_COLOR)

        #running each events in pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
        
        #check key values
        keys = pygame.key.get_pressed()
        if not tetris.end:
            if keys[pygame.K_LEFT]:
                tetris.move_left()
            elif keys[pygame.K_RIGHT]:
                tetris.move_right()
            elif keys[pygame.K_DOWN]:
                tetris.move_down()
            elif keys[pygame.K_UP]:
                tetris.rotate()
            elif keys[pygame.K_SPACE]:
                space_pressed = True
        if keys[pygame.K_r]:
            tetris.__init__(ROWS, COLS)
        if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                run = False 

        tetris.make_grid()

        #show shape on the screen
        if tetris.figure:
            for i in range(4):
                for j in range(4):
                    if(i*4 + j) in tetris.figure.image():
                        shape = ASSETS[tetris.figure.color]
                        x = CELL * (tetris.figure.x + j)
                        y = CELL * (tetris.figure.y + i)
                        SCREEN.blit(shape, (x,y))
                        pygame.draw.rect(SCREEN, WHITE, (x,y,CELL, CELL), 1)
        
        #for constant speed of the screen
        counter += 1
        if counter >= 15000:
            counter = 0

        #move the shape
        if move:
            if counter % (FPS//(tetris.level*2)) == 0:
                if not tetris.end:
                    if space_pressed:
                        tetris.freefall()
                        space_pressed = False
                    else: 
                        tetris.move_down()

        #keep fallen shapes on screen
        for x in range(ROWS):
            for y in range(COLS):
                if tetris.grid[x][y] > 0:
                    value = tetris.grid[x][y]
                    image = ASSETS[value]
                    SCREEN.blit(image, (y*CELL, x*CELL))
                    pygame.draw.rect(SCREEN, WHITE, (y*CELL,x*CELL, CELL, CELL), 1)

        #Control Panel
        if tetris.next:
            for i in range(4):
                for j in range(4):
                    if(i*4 + j) in tetris.next.image():
                        image = ASSETS[tetris.next.color]
                        x = CELL * (tetris.next.x + j - 4)
                        y = HEIGHT- 100 + CELL * (tetris.next.y + i)
                        SCREEN.blit(image, (x,y))

        #checking for end game
        if tetris.end:
            tetris.end_game()


        #Stats
        score_text = font.render(f'{tetris.score}', True, WHITE)
        level_text = font2.render(f'Level: {tetris.level}', True, WHITE)
        SCREEN.blit(score_text, (250- score_text.get_width()//2, HEIGHT-110))
        SCREEN.blit(level_text, (250- level_text.get_width()//2, HEIGHT-30))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

    
