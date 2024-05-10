import pygame
from pygame import gfxdraw

framerate = 60
window_size = (700, 700)
time_left = 60
background_color = pygame.Color(255, 255, 255)

def draw_light(screen, position, color: pygame.Color) -> None:
    gfxdraw.aacircle(screen, *position, 120, color)
    gfxdraw.filled_circle(screen, *position, 120, color)

def main() -> None:
    pygame.init()
    if not pygame.font:
        raise Warning("Fonts are disabled.")

    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()
    running = True
    
    if pygame.font:
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill(background_color)
        font = pygame.font.Font(None, 64)
    

    window_center = ( int(window_size[0]/2), int(window_size[1]/2) )

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(background_color)
        
        text = font.render(f'Timer: {time_left} s', True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)
        screen.blit(background, (0, 0))

        # Rendering
        draw_light(screen=screen, position=window_center, color=pygame.Color(255, 0, 0))

        pygame.display.flip()
        clock.tick(framerate)

if __name__ == '__main__':
    main()
