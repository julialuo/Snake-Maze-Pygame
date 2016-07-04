#Julia Luo, 07-03-2016
import pygame

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

SCALE = 10
SPEED = SCALE/2
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FPS = 60

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Snake Maze')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

def display_text(text, colour, position):
    screen_text = font.render(text, True, colour)
    if position == 'center':
        game_display.blit(screen_text, [DISPLAY_WIDTH/2 - screen_text.get_rect().width/2, DISPLAY_HEIGHT/2 -
                                        screen_text.get_rect().height/2])

def game_loop():
    game_exit = False
    game_over = False
    head_x = 0
    head_y = 0
    x_change = 0
    y_change = SPEED

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -SPEED
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = SPEED
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    x_change = 0
                    y_change = -SPEED
                elif event.key == pygame.K_DOWN and y_change == 0:
                    x_change = 0
                    y_change = SPEED

        if head_x + x_change > DISPLAY_WIDTH - SCALE or head_x + x_change < 0 or head_y + y_change > DISPLAY_HEIGHT - SCALE \
                or head_y + y_change < 0:
            game_over = True

        if not game_over:
            head_x += x_change
            head_y += y_change

        game_display.fill(white)
        pygame.draw.rect(game_display, black, [head_x, head_y, SCALE, SCALE])
        pygame.display.update()
        clock.tick(FPS)

        while game_over == True:
            game_display.fill(white)
            pygame.draw.rect(game_display, black, [head_x, head_y, SCALE, SCALE])
            display_text("Game Over, press 'space' to play again or 'esc' to quit", red, 'center')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_exit = True
                        game_over = False
                    elif event.key == pygame.K_SPACE:
                        game_loop()

    pygame.quit()
    quit()

game_loop()