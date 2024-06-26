import pygame as pg

vec = pg.math.Vector2 # allows you to use vector based movement on a coordinate plane as opposed to writing math to represent size, shape, movement. Look up Vector2 for list of available movements, Unity also uses vector2 and its documentation has explanations of usage in plain English
# vector is a movement on a 2d plane using x and y at the same time, can move diagonally, mathematically: using pythagorian theorem to find the hypoteneuse(side 3) between the right triangle made by a movement on the x-axis(side 1) and a movement on the y-axis(side 2)

FPS = 60
FIELD_COLOR = (2, 2, 2)
BG_COLOR = (6, 13, 20)

SPRITE_DIR_PATH = 'assets/sprites'
FONT_PATH = 'assets/fonts/segoepr.ttf'

ANIM_TIME_INTERVAL = 350 # time in miliseconds, length/duration of animation, set method timer in main.py, # removes animation/Tetromino dependancy on framerate
FAST_ANIM_TIME_INTERVAL = 2 # time in miliseconds, for pressing down direction to speed up Tetromino fall rate


TILE_SIZE = 25      # reduce TILE_SIZE if game window is too big for display, scales down individual tiles
FIELD_SIZE = FIELD_W, FIELD_H = 8, 25
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE

FIELD_SCALE_W, FIELD_SCALE_H = 1.7, 1.0     # defines scaling factor of playing field
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H     # use scale of playing field from above line to calculate resolution of app window, increases width beyond playing field, adds background. apply window resolution to App class __init__ => self.screen

INIT_POS_OFFSET = vec(FIELD_W // 2 - 1, 0)  # sets starting position of Tetromino to the center of the top of the playing field[field size divided by 2], set variable within tetromino.py's Block class => __init__
NEXT_POS_OFFSET = vec(FIELD_W * 1.3, FIELD_H * 0.45)    # offset applied to Block class => tetromino.py => self.next_pos
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)} # Tetrominoes can only move in left, right, down directions. defined as a dictionary of vector increments KEY:VALUE where KEY = name of direction, VALUE = the vector movement/calculation associated with moving in that direction
    # link MOVE_DIRECTIONS variable to method: move in tetromino.py

TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0,-1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1 ,0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}

# Window resolution[FIELD_RES] is calculated using width[FIELD_W] and height[FIELD_H] = width * height
    # length of width and height in TILE_SIZE units
    # if FIELD_W = 10 and FIELD_H = 20, then 10 * 20 = 200 = window resolution/size[FIELD_RES] 

# Hierarchy of classes [smallest to largest]: Block => Tetromino => Tetris => App
    # Hierarcy allows App to be flexible/scalable
    # organization allows you to add special effects conveniently, object oriented organization
        # higher level classes: App and Tetris will have their own corresponding idividual class .py files
        # lower level classes: Tetromino and Block will be handled by one .py file
        # connect each class by importing elements up top
    
# Logic behind hierarchy classes explanation:
    # moving shapes that are stacked in Tetris are called Tetrominos 
    # each tetromino is made of 4 blocks
        # make each block its own class, so you can assign a sprite to a class
        # 4 sprites/blocks side to side will have a "stacking block" look that a lot of puzzle games have
    # all 4 blocks are controlled by the "tetromino" class
    # all tetromino class objects will be controlled by "Tetris" class [the playing field]
    # Tetris class is controlled/created within the "App" class


# Tetromino shape => TETROMINOS dictionary above, {KEY:VALUE}
    # origin point of a Tetromino is its pivot point [usually a point somewhere towards the top left, but close as possible to the center of the Tetromino]
    # KEY names describe the shape of the Tetromino/name of Tetromino => Blocks in Tetrominos are arranged similar to English letters, so name Tetrominos the names of corresponding letters
    # VALUE = coordinates of each of the Blocks that make up the Tetromino
        # list the 4 coordinates (x, y) of the top left corners of each block
        # first element of VALUE [first coordinate] will be the Pivot point (0,0) the origin of a 2d plane
        # coordinates are within Tetromino's own local coordinate system [Think: 2d graph (x axis, y axis) starting from the origin (0,0), one block takes up the space between 4 adjacent points arranged in a square]

# rotate one coordinate around another: if rotating point A around point P 90 degrees, subtract coordinates of point P from point A. A' = A - P
    # 1: A' = A - P   2: A" = A' .rotate   3: A = A" + P



