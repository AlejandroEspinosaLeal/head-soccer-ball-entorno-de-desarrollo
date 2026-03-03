import pygame
from settings import WIDTH, HEIGHT, NEGRO

class StateMachine:
    def __init__(self, screen):
        self.screen = screen
        self.states = {}
        self.current_state = None
        self.fading = False
        self.fade_alpha = 0
        self.next_state_name = None

    def change_state(self, state_name, with_fade=True):
        if with_fade:
            self.fading = True
            self.next_state_name = state_name
        else:
            self._switch(state_name)

    def _switch(self, state_name):
        if self.current_state: 
            self.current_state.exit()
        self.current_state = self.states[state_name]
        self.current_state.enter()

    def update(self, events):
        if self.current_state and not self.fading:
            self.current_state.update(events)

    def draw(self):
        if self.current_state:
            self.current_state.draw(self.screen)

        if self.fading:
            self.fade_alpha += 15
            if self.fade_alpha >= 255:
                self._switch(self.next_state_name)
                self.fading = False
        elif self.fade_alpha > 0:
            self.fade_alpha -= 15
            
        if self.fade_alpha > 0:
            fade_surf = pygame.Surface((WIDTH, HEIGHT))
            fade_surf.fill(NEGRO)
            fade_surf.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surf, (0, 0))