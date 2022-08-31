from sdl2 import *
import settings

class Graphics:
    window = None
    renderer = None

    def __init__(self):
        SDL_Init(SDL_INIT_VIDEO)
        self.window = SDL_CreateWindow(
                b"Neighbours", 
                SDL_WINDOWPOS_CENTERED,
                SDL_WINDOWPOS_CENTERED,
                *settings.WINDOW_SIZE,
                SDL_WINDOW_SHOWN
                )
        self.renderer = SDL_CreateRenderer(
            self.window,
            -1, 
            SDL_RENDERER_ACCELERATED
            )

    def __del__(self):
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
        SDL_Quit()

    def fill_rect(self, rect, color):
        SDL_SetRenderDrawColor(self.renderer, *color)
        SDL_RenderFillRect(self.renderer, SDL_Rect(*rect))

    def present(self):
        SDL_RenderPresent(self.renderer)