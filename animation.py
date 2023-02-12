import pygame

class SpriteSheet():
    def __init__(self, sheet, cell_width, cell_height, colour_key):
        self.sheet = sheet              # The sheet image
        self.width = cell_width         # Width of one image cell
        self.height = cell_height       # Height of one image cell
        self.colour_key = colour_key    # Background Colour Key for transparency

    # Returns a sub-image from the sheet from the supplied co-ordinates on the sheet. The grid scale is equal to the cell_width and cell_height
    def get_image(self, scale=1, cell=(0,0)):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((cell[0] * self.width), cell[1] * self.height, self.width, self.height))
        image = pygame.transform.scale(image, (self.width * scale, self.height * scale))
        image.set_colorkey(self.colour_key)

        return image

class AnimationSequence():
    def __init__(self, name, frames, sheet):
        self.name = name        # Reference ID for pulling the animation
        self.frames = frames    # A sequenced list of frame co-ordinates for each sub-image
        self.sheet = sheet      # The supplied sprite sheet
        self.current_index = 0  # The current animation frame's index in the sequence

    # Returns the sub-image from the sheet for the current frame index
    def draw(self, scale=1):
        frame_data = self.frames[int(self.current_index)]
        frame = self.sheet.get_image(scale, cell=(frame_data[0], frame_data[1]))
        #add error catching fopr out of range exceptions
        return frame
        
    # Iterates the sequences index state, or resets animation and returns -1 if the sequence is finish.
    def iterate(self, value=1): 
        self.current_index += value

        # if the next frame hop is larger than the number of frames in the animation, reset animation state and return -1
        if (self.current_index >= len(self.frames)):
            self.current_index = 0
            return -1
        
        return self.current_index
        
    def add_frame(self, frame):
        pass
        
    def add_frames(self, frames):
        pass

class AnimationHandler():
    def __init__(self, default_animation, default_scale = 1, animations=[]):
        self.queue = []                 # Animation queue, will animate each sequence in order
        self.is_held = False            # Flag for indicating a frame freeze
        self.hold_period = 0            # Duration of the frame freeze
        self.animations = animations    # List of animations supplied
        self.default_animation = {'animation': default_animation, 'scale': default_scale} # Default animation to be used
        self.current_animation = {'animation': default_animation, 'scale': default_scale} # Current animation being played

    # Adds the supplied animation to the animation library
    def add_animation(self, animation):
        if animation.name in self.animations:
            pass # add error catching
        else:
            self.animations.append(animation)

    # Removes the named animation sequence from the library
    def remove_animation_by_name(self, name):
        if name in self.animations:
            self.animations.remove(self.get_animation(name))

    # Gets an animation from the animation library by name
    def get_animation(self, name):

        for animation in self.animations:
            if name == animation.name:
                return self.animations[self.animations.index(name)]

        # if name in self.animations:
        #     return self.animations[self.animations.index(name)]
        # else:
        #     pass

    # Clears the animation queue and adds the supplied animation sequence
    def override_queue(self, animation, scale=1):
        self.queue.clear()
        self.queue.append(animation, scale)
    
    # Gets the named animation sequence, clears the animation queue, and then adds the named animation sequence
    def override_by_name(self, name, scale=1):
        self.override_queue(self.get_animation(name), scale)
    
    # Adds the named animation sequence to the end of the animation queue
    def queue_by_name(self, name, scale=1):
        self.append_queue(self.get_animation(name), scale)

    # Adds the supplied animation sequence to the end of the animation queue
    def append_queue(self, animation, scale=1):
        self.queue.append({'animation': animation, 'scale': scale})

    # Instructs handler to hold the frame for the supplied number of frames
    def hold_current(self, frames=1):
        self.is_held = True 
        self.hold_period = frames

    # State machine to supply the current animation frame, and then advance to the next frame or render the next freeze frame
    def animate(self, speed=1):
        frame = self.current_animation['animation'].draw(self.current_animation['scale'])

        if self.is_held:
            if self.hold_period > 0:
                self.hold_period -= 1
            else:
                self.is_held = False
        
        if (not self.is_held and self.current_animation['animation'].iterate(speed) < 0):
            if len(self.queue) > 0:
                self.current_animation = self.queue.pop()
            else:
                self.current_animation = self.default_animation

        return frame