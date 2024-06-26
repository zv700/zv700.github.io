from settings import *
import random

class Block(pg.sprite.Sprite):                              # Block class will use sprites, so it must inherit from sprite group in tetris.py/pygame library
    def __init__(self, tetromino, pos):                     # pos = position on the playing field, is the coordinate of the top left corner of the tile, value of block does not take into account size of tile
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True                                   # for removing full lines of blocks. "Not alive" or alive = False means block gets cleared from playing field. Corresponds to is_alive below
        
        super().__init__(tetromino.tetris.sprite_group)     # draw the block by passing the sprite group through the constructor of the parent sprite class
        self.image = tetromino.image                         # enables sprite/.png use for Blocks from asset directory, corresponds to random image accessed in Tetromino class
        #self.image = pg.Surface([TILE_SIZE, TILE_SIZE])     # generic pygame library image asset use, the sprite image will take up the width and height values of one tile
        #self.image.fill('orange')                           # generic pygame library image asset use, Block color, fills whole block with color 
        #pg.draw.rect(self.image, 'coral', (1, 1, TILE_SIZE - 2, TILE_SIZE - 2), border_radius=8)       # generic pygame library image asset use, gives Blocks rounded corners, easier to differentiate Block boundaries when they land at bottom/stack on each other
        
        self.rect = self.image.get_rect()                                   # defines the Block shape as a rectangle, gets rectangle sprite image from library
        #self.rect.topleft = pos[0] * TILE_SIZE, pos[1] * TILE_SIZE         # defines the coordinate of the Block to be the top left point on playing field's coordinate plane. Line accomplishes same as line below. This line made obsolete/simplified on line below by adding vector (vect = pg.math.Vector2) to settings.py, vector = width * height
        #self.rect.topleft = self.pos * TILE_SIZE                           #This line replaced by seperate method below: set_rect_pos

        self.sfx_image = self.image.copy() # makes a copy of block
        self.sfx_image.set_alpha(110)    # sets copy block's transparency
        self.sfx_speed = random.uniform(0.2, 0.6)            # random speed value of copy block
        self.sfx_cycles = random.randrange(6, 8)
        self.cycle_counter = 0

    def sfx_end_time(self):     # method determines duration of sfx effect by setting the animation's ending condition
        if self.tetromino.tetris.app.anim_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True

    def sfx_run(self):   # replaces current block image with a transparent copy that moves up
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)

    def is_alive(self):             # called below in update()
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()             # step removes block from landed array
            else:
                self.kill()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self):                                 # allows Blocks/Tetrominoes to move, changes position on coordinate plane. rectangle position (position of Blocks on coordinate plane) need to be updated every time a block's position changes in order for the Tetromino class to be able to move (because Tetrominoes are made of Blocks)
        pos = [self.next_pos, self.pos][self.tetromino.current]     # position of Block is determined by the current Tetromino's position
        self.rect.topleft = pos * TILE_SIZE

    def update(self):                                       # Block class and Tetromino class each have their own update() method. for Blocks: set_rect_pos() + update() = Block movement. set the positon, then update the position after it moves. By default will move 60 blocks per second (really fast) because of FPS framerate
        self.is_alive()
        self.set_rect_pos()

    def is_collide(self, pos):                              # takes certain position as input, checks to see if Block is inside of playing field
        x, y = int(pos.x), int(pos.y)                       # if Block is inside playing field, then there is no collision
        if 0 <= x < FIELD_W and y < FIELD_H and (                # sets the playing field borders as boundaries. Top left corner is origin (0, 0). "if 0 <= x < FIELD_W" sets 0 on the x axis (the left side of the playing field) as a boundary to collide with, if x value is less than the total width of the playing field then the Block can collide/collision enabled, so if a Block is in the middle of the playing field and not touching either left or right boundaries it does not have collision. "y < FIELD_H" means if the value for y is less than the total field height, then the block will have collision applied. Since blocks start from the top and are always falling, they always have collision on the y-axis with the one exception of when they first spawn up top.
                y < 0 or not self.tetromino.tetris.field_array[y][x]):    # additional check to see if there are other blocks in the array (blocks that have landed), ignores array if Block is above playing field. This step allows Tetrominoes stack on each other 
            return False                                    # False means there is collision: "is_collide" = Block is colliding with something/touching a boundary or Tetromino touching another Tetromino
        return True                                         # True means there is no collision: Block is in the middle of the playing field not touching anything

class Tetromino:
    def __init__(self, tetris, current=True):                             # links tetromino to tetris.py   "current=True" corresponds to next tetromino user interface => tetris.py => class Tetris => self.next_tetromino
        self.tetris = tetris                                # import Tetromino class in tetris.py and create an instance of Tetromino class within tetris.py's "class Tetris:" and update()
        #Block(self, (4,7))                                 # places a Block at coordinates (4, 7) on the (10 x 20) playing field, made obsolete by below: self.shape and self.block 
        self.shape = random.choice(list(TETROMINOES.keys()))                    # corresponds to shape KEY within TETROMINO dictionary in settings.py, can set a specific shape or set to random(using random ported from dictionary above), specify that list of possible random choices come from TETROMINIOES dictionary's KEY values from settings.py, every time you start program a random Tetromino will appear
        self.image = random.choice(tetris.app.images)       # loads a random .png for each Tetromino, accessed above in Block class __init__
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]     # Block's attribute will be instances of Block class, positions come from shape attribute
        self.landing = False                                # method to check for landing in tetris.py: "check_tetromino_landing()". Condition for changing False to True below in move() method: "elif direction == 'down':"
        self.current = current

    def rotate(self):
        pivot_pos = self.blocks[0].pos # pivot point of Tetromino is origin [0]
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]       #if no collision, then assign new position to each Block

    def is_collide(self, block_positions):                  # Tetromino collision takes into account position/collision for all 4 blocks making up a Tetromino
        return any(map(Block.is_collide, self.blocks, block_positions))                   # "any()" function lets you know if any Blocks (at least one block) have collision based on position of block on coordinate plane and "is_collide()" method within Block class. "map()" function calls "is_collide" within Blocks class to check True or False

    def move(self, direction):                              # depending on value of direction parameter, gets increment vector VALUE from MOVEMENT_DIRECTION library assiciated with each direction KEY
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]         # forms new position for each Block in a Tetromino taking into account values of direction of movement
        is_collide = self.is_collide(new_block_positions)                                   # checks to see if at leas one block has a collision at new position

        if not is_collide:                                  # if no collision, then move all Blocks within a Tetromino to new positions
            for block in self.blocks:
                block.pos += move_direction                 # adds increment vector VALUE and adds it to position coordinates of each block

        elif direction == 'down':   # corresponds to self.landing above in class Tetromino => __init__      sets landing to True if the movement direction is down and there is a collision happening from downward movement (if the Tetromino touches the bottom of the playing field, then it has landed/will stop moving left and right)
            self.landing = True

    def update(self):
        self.move(direction='down')                         # causes tetromino to automatically move down, actual user control of movement of blocks comes from above: self_rect_pos
        #pg.time.wait(200)                                  # temporary solution to Blocks/Tetrominoes moving too fast, offset tetromino movement by 200 miliseconds, will also offset left and right movement speed (not desirable, jerky movements). Made obsolete by ANIM_TIME_INTERVAL in settings.py
