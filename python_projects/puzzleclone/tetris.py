from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft        # import pygame's freetype to be able to write text in app window

class Text:                 # when you make a new class, needs to be imported to main file
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02),     # specify the surface to write on (the app window) and the position of the text
                            text="BLOCKTRIS", fgcolor='white',                     # specify font's text, size, background color
                            size=TILE_SIZE * 1.35, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.22),      # positioning of text elements are in proportion to the window size => if you change tile size, text positions should move proportionally
                            text="Next", fgcolor='white',                     
                            size=TILE_SIZE * 1.3, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.67),     
                            text="Score", fgcolor='white',                     
                            size=TILE_SIZE * 1.3, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8),     
                            text=f'{self.app.tetris.score}', fgcolor='white',                     
                            size=TILE_SIZE * 1.2, bgcolor='black')

class Tetris:                                       # establish class that handles playing field
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()       # enables sprite usage + contains all Blocks that make up Tetromino on playing field, also need to add line to update() and draw()
        self.field_array = self.get_field_array()   # array has two functions: 1. element stores pointer to Block object 2. array used to calculate collisions
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False) # second instance of Tetromino. normal instance is True (used in playing field), second is False(False means controls and movement are not applied, is static, needs to be offset to the right to use in user interface for next Tetromino => settings.py => NEXT_POS_OFFSET)
        self.speed_up = False

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}    # score points awarded's values increases based on number of simultaneous full lines cleared

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    def check_full_lines(self):
        row = FIELD_H - 1                          # define row to be able to determine what needs to be removed when you clear a row       # called through update() below
        for y in range(FIELD_H - 1, -1, -1):        # iterate through the array from bottom to top, left to right
            for x in range(FIELD_W):                               # use row variable to reassign elements of the array
                self.field_array[row][x] = self.field_array[y][x]       # value of variable: row = value of y

                if self.field_array[y][x]:                          
                    self.field_array[row][x].pos = vec(x, y)        # reassign blocks' position values based on new values of indexes in array

            if sum(map(bool, self.field_array[y])) < FIELD_W:        # check number of blocks in current line. 
                row -= 1                                                # if row is incomplete, reduce value of row variable by 1 to reassign the next line. If row is full, then the value of the row variable does not change. Skip full lines and overwrite complete lines
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False          # exclude blocks from sprite group so they are not displayed/remove blocks that are not alive 
                    self.field_array[row][x] = 0                    # rewrite value of removed/not alive blocks to zero so collision system works
                    
                self.full_lines += 1
                
    def put_tetromino_blocks_in_array(self):        # method called after tetromino has landed
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):                      # makes 2d array the size of playing field, stops Tetrominoes from overlapping when they land at the bottom of playing field
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def is_game_over(self):     # Game ends when the position of a block's y value is 0 (origin height, top of screen) for 300 miliseconds
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(1500)
            return True

    def check_tetromino_landing(self):              # this method is called below in update() method
        if self.tetromino.landing:                  # when a tetromino lands at the bottom, it stops moving and a new Tetromino spawns up top
            if self.is_game_over():             # if game over, app restarts/reinitializes
                self.__init__(self.app)
            else:
                self.speed_up = False                   # speed up attribute is False by default, will change to True when pressing the move down key
                self.put_tetromino_blocks_in_array()    # Blocks added to array after landing
                self.next_tetromino.current = True                              # enables next tetromino user interface
                self.tetromino = self.next_tetromino                    # sets next tetromino(second static instance) to be active when the first tetromino instance(the active moving tetromino) is also active (they both exist at the same time)
                self.next_tetromino = Tetromino(self, current=False)    # sets the next tetromino (the second instance) to be False(static, no movement applied) on the right side in the user interface

    def control(self, pressed_key):                 # method listens for keyboard key presses to control Tetromino movement, linked to main.py check_events() => elif event.type == pg.KEYDOWN
        if pressed_key == pg.K_a:                   # Tetromino movement left is mapped to the 'a' key press
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_d:                 # Tetromino movement left is mapped to the 'd' key press
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_w:                 # Tetromino rotation 90 degrees is mapped to 'w' key press
            self.tetromino.rotate()
        elif pressed_key == pg.K_s:
            #self.tetromino.move(direction='down')   # Tetromino movement down is mapped to the 's' key press, press 's' key multiple times to increase downward fall speed [To do: figure out how to increase acceleration with button press and hold, next line accomplishes]
            self.speed_up = True

    def draw_grid(self):    
        for x in range(FIELD_W):    
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'white', 
                            (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
                                                    # without draw_grid function, tetris playing field would just be solid color background
                                                    # iterate over the size of the field, draw rectangles of grid based on size of one tile
                                                    # draws grid within itself(within the app visible playing field boundaries) color of grid lines are black

    def update(self):                               # method, method = Python function within Class
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]        # time interval that game logic will be sped up by
        #if self.app.anim_trigger:                   # corresponds to set_timer in main.py      # line split between above line and below line
        if trigger:    
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()
        #pass                                       # pass value is placeholder for when a method does not have body code yet, left in code for self-reference

    def draw(self):                                 # method
        self.draw_grid()                            # corresponds to parameters set above in draw_grid(self). "self.draw_grid()" goes here as like an on/off switch or plugging a light into a power outlet. You have a working lamp, but it won't turn on if it's not connected to electricty/power.
        self.sprite_group.draw(self.app.screen)
