import pygame
from settings import WIDTH, HEIGHT, FPS
from asset_manager import AssetManager
from state_machine import StateMachine
from states import IntroState, MainMenuState, DifficultyMenuState, GameplayState, SettingsState

def main():
    pygame.init()
    # PREPARAMOS EL MOTOR GRÁFICO PARA ESCALAR SIN ROMPERSE
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Head Soccer Pro")
    clock = pygame.time.Clock()

    assets = AssetManager()
    assets.load_assets()

    sm = StateMachine(screen)
    sm.states = {
        "Intro": IntroState(sm, assets),
        "MainMenu": MainMenuState(sm, assets),
        "DifficultyMenu": DifficultyMenuState(sm, assets),
        "Gameplay": GameplayState(sm, assets),
        "Settings": SettingsState(sm, assets) 
    }
    
    sm.change_state("Intro", with_fade=False)

    running = True
    while running:
        clock.tick(FPS)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and sm.current_state == sm.states["Intro"]:
                sm.change_state("MainMenu")

        sm.update(events)
        sm.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()