from types import CellType
from sdl2 import *
from graphics import Graphics
from world import World
import settings
import enum
import time
import sys
import random
import ctypes

ctypes.c_uint32.__sub__ = lambda self, other : ctypes.c_uint32(self.value - other.value)
ctypes.c_uint32.__lt__ = lambda self, other : self.value < other.value

def main():
    graphics = Graphics()
    random.seed(time.time())
    world = World()
    quit = False
    event = SDL_Event()
    target_frame_time = ctypes.c_uint32(1000 // settings.FRAMES_PER_SECOND)
    
    while not quit:
        frame_start = ctypes.c_uint32(SDL_GetTicks())
        
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                quit = True
        
        world.resolve()
        world.render(graphics)
        graphics.present()
        frame_end = ctypes.c_uint32(SDL_GetTicks())
        frame_time = frame_end - frame_start
        
        if frame_time < target_frame_time:
            SDL_Delay(target_frame_time - frame_time)
    
if __name__ == "__main__":
    sys.exit(main())