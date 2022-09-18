from types import CellType
from sdl2 import *
from graphics import Graphics
from world import World
import settings
import time
import sys
import random
import ctypes

# Just QoL so that we can use C's 'uint32' with regular operators.
ctypes.c_uint32.__sub__ = lambda self, other : ctypes.c_uint32(self.value - other.value)
ctypes.c_uint32.__lt__ = lambda self, other : self.value < other.value

def main():
    graphics = Graphics() # Our graphics.
    random.seed(time.time()) # Seeding random with time.
    world = World() # Our world.
    running = True 
    event = SDL_Event()
    target_frame_time = ctypes.c_uint32(1000 // settings.FRAMES_PER_SECOND) # The amount of time in milliseconds that each frame should last for (at least).
    rounds = 0 # To keep track of the number of rounds.
    resolved = False
    
    while running:
        frame_start = ctypes.c_uint32(SDL_GetTicks()) # Get the current CPU tick in milliseconds.
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT: # If we press the X-button, stop the program.
                running = False
        
        # If the world is not resolved, resolve it.
        if not resolved:
            rounds = rounds + 1
            satisfied = world.resolve()
            if satisfied > 0.8: # To avoid unnecessary console-clutter.
                print(str(round(100.0 * satisfied, 2)) + "%") 

            if satisfied == 1.0:
                resolved = True
                print("Finished in " + str(rounds) + " rounds.")

        world.render(graphics) # Render the world.
        graphics.present() # Present the world.
        frame_end = ctypes.c_uint32(SDL_GetTicks())
        frame_time = frame_end - frame_start # 'frame_time': the total amount of time in milliseconds that has passed since we began the frame.
        
        # If we are rendering too fast: slow down.
        if frame_time < target_frame_time:
            SDL_Delay(target_frame_time - frame_time)
    
if __name__ == "__main__":
    sys.exit(main())
