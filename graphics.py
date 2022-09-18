# Module containing all the code for class 'Graphics'.
from sdl2 import *
import settings

class Graphics:
    # Initializes the default 'Graphics' object.
    # A 'Graphics' object is just a plain window with a renderer.
    def __init__(self):
        # Enables SDL's rendering functionality.
        SDL_Init(SDL_INIT_VIDEO)
        self.window = SDL_CreateWindow(
                b"Neighbours", 
                SDL_WINDOWPOS_CENTERED,
                SDL_WINDOWPOS_CENTERED,
                *settings.WINDOW_SIZE,
                SDL_WINDOW_SHOWN
                )
        # If the window is a frame, the renderer is the canvas.
        self.renderer = SDL_CreateRenderer(
            self.window,
            -1, 
            SDL_RENDERER_ACCELERATED
            )

    # Clean up. It's not required AFAIK thanks to the garbage collector, but we can do it ourselves so we might as well.
    def __del__(self):
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
        SDL_Quit() # Tells the program we're done using SDL.

    # QoL wrapper function.
    def fill_rect(self, rect, color):
        SDL_SetRenderDrawColor(self.renderer, *color)
        SDL_RenderFillRect(self.renderer, SDL_Rect(*rect))

    # QoL wrapper function. 
    def present(self):
        SDL_RenderPresent(self.renderer)
