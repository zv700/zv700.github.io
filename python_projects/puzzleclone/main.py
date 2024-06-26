from settings import *          # from settings import allSettings, "*" asterisk/star means "all" or "everything"
from tetris import Tetris, Text       # from fileName.py import className, class names begin with Uppercase letter
import sys                      # import Python default module: sys
import pathlib                  # import allows you to use files in folders using specified path [use for sprites in assets/sprites, path defined in settings.py] => method below: load_images 


class App:
    def __init__(self):
        pg.init()       # all instances of pg are from settings.py where pygame is imported
        pg.display.set_caption('Blocktris')
        self.screen = pg.display.set_mode(WIN_RES)  # inputs: FIELD_RES = App window will only be the size of the playing field. WIN_RES = App window will include playing field and additional background for user interface
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()        # .png images for sprites available here
        self.tetris = Tetris(self)      # from tetris.py
        self.text = Text(self)

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]            # grab all *.png files from specified path and sets them to files variable
        images = [pg.image.load(file).convert_alpha() for file in files]                                     # loads image .png files using pygame library tools   
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]        # conforms image size to size of tile
        return images

    def set_timer(self):                # removes animation/Tetromino dependancy on framerate    # define a reserved user event value that will appear after a set period of time. Each time the user event occurs, will use animation trigger value (below: in check_events) all movement in game determined by value of animation trigger
        self.user_event = pg.USEREVENT + 0      # tetris.py Tetris class update() method will only run/be called if user event/ animation trigger are true
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_user_trigger = False      # trigger for speed up fall speed button press
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):         # draw function "draws"/displays the visual elements in the app window
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))        
        self.tetris.draw()      # tetris playing field is drawn AFTER the screen itself
        self.text.draw()
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:                  # allows key presses to control Tetromino movement, enables control() method in tetris.py
                self.tetris.control(pressed_key=event.key)  # call control method in instance of Tetris class in case of key press event, links classes: App to Tetris
            elif event.type == self.user_event:
                self.anim_trigger = True                    # all movement in game is determined by animation trigger/user event(button press)
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True


    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()
