#Julia Luo, 07-03-2016
import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
faded_red = (240, 129, 129)
green = (0, 155, 0)
faded_green = (109, 171, 119)

SCALE = 20
SPEED = 20
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FPS = 15

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Snake Maze')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

def display_text(text, colour, position):
    screen_text = font.render(text, True, colour)
    if position == 'center':
        game_display.blit(screen_text, [DISPLAY_WIDTH/2 - screen_text.get_rect().width/2, DISPLAY_HEIGHT/2 -
                                        screen_text.get_rect().height/2])

def draw_snake(snake_body, colour):
    for coord in snake_body:
        pygame.draw.rect(game_display, colour, [coord[0], coord[1], SCALE, SCALE])

def game_loop():
    game_exit = False
    game_over = False
    head_x = 0
    head_y = 0
    x_change = 0
    y_change = SPEED
    snake_body = []
    snake_length = 1
    cherry_x = random.randrange(0, DISPLAY_WIDTH - SCALE, SCALE)
    cherry_y = random.randrange(0, DISPLAY_HEIGHT - SCALE, SCALE)

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

        if head_x + x_change == cherry_x and head_y + y_change == cherry_y:
            cherry_x = random.randrange(0, DISPLAY_WIDTH - SCALE, SCALE)
            cherry_y = random.randrange(0, DISPLAY_HEIGHT - SCALE, SCALE)
            snake_length += 1

        for body_coord in snake_body[:-1]:
            if head_x + x_change == body_coord[0] and head_y + y_change == body_coord[1]:
                game_over = True

        if not game_over:
            head_x += x_change
            head_y += y_change

            snake_head = []
            snake_head.append(head_x)
            snake_head.append(head_y)
            snake_body.append(snake_head)

            if (len(snake_body) > snake_length):
                del snake_body[0]

        game_display.fill(white)
        pygame.draw.rect(game_display, red, [cherry_x, cherry_y, SCALE, SCALE])
        draw_snake(snake_body, green)
        pygame.display.update()
        clock.tick(FPS)

        while game_over == True:
            game_display.fill(white)
            draw_snake(snake_body, faded_green)
            pygame.draw.rect(game_display, faded_red, [cherry_x, cherry_y, SCALE, SCALE])
            display_text("Game Over, press 'space' to play again or 'esc' to quit", red, 'center')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_exit = True
                        game_over = False
                    elif event.key == pygame.K_SPACE:
                        game_loop()

    pygame.quit()
    quit()

game_loop()