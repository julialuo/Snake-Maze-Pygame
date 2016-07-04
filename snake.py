#Julia Luo, 07-03-2016
import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
grey = (115, 115, 115)
red = (255, 0, 0)
faded_red = (240, 129, 129)
green = (0, 155, 0)
faded_green = (109, 171, 119)

SCALE = 20
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 500
FPS = 15
MAZE_NUM = 10
MAZE_SIZE = 40 #multiple of scale

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


def draw_maze(maze_parts, colour):
    for coord in maze_parts:
        pygame.draw.rect(game_display, colour, [coord[0], coord[1], MAZE_SIZE, MAZE_SIZE])


def create_maze():
    maze_parts = [[] for x in range(MAZE_NUM)]
    for i in range(0, MAZE_NUM):
        maze_parts[i].append(random.randrange(0, DISPLAY_WIDTH - SCALE, SCALE))
        maze_parts[i].append(random.randrange(0, DISPLAY_HEIGHT - SCALE, SCALE))

        while maze_parts[i][0] == 0 and maze_parts[i][1] <= 100:
            maze_parts[i][0] = random.randrange(0, DISPLAY_WIDTH - SCALE, SCALE)
            maze_parts[i][1] = random.randrange(0, DISPLAY_HEIGHT - SCALE, SCALE)

    return maze_parts


def set_cherry(snake_body, maze_parts):
    cherry = []
    cherry.append(random.randrange(0, DISPLAY_WIDTH - SCALE, SCALE))
    cherry.append(random.randrange(0, DISPLAY_HEIGHT - SCALE, SCALE))
    conflict = True

    while conflict:
        cherry[0] = random.randrange(0, DISPLAY_WIDTH - SCALE, SCALE)
        cherry[1] = random.randrange(0, DISPLAY_HEIGHT - SCALE, SCALE)

        conflict = False
        for body_coord in snake_body:
            if cherry[0] == body_coord[0] and cherry[1] == body_coord[1]:
                conflict = True
        for maze_coord in maze_parts:
            if cherry[0] >= maze_coord[0] and cherry[0] < maze_coord[0] + MAZE_SIZE:
                if cherry[1] >= maze_coord[1] and cherry[1] < maze_coord[1] + MAZE_SIZE:
                    conflict = True
    return cherry


def game_loop():
    game_exit = False
    game_over = False
    snake_head = [0, 0]
    x_change = 0
    y_change = SCALE
    snake_body = []
    snake_length = 1
    maze_parts = create_maze()
    cherry = set_cherry(snake_body, maze_parts)

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a and x_change == 0:
                    x_change = -SCALE
                    y_change = 0
                elif event.key == pygame.K_RIGHT  or event.key == pygame.K_d and x_change == 0:
                    x_change = SCALE
                    y_change = 0
                elif event.key == pygame.K_UP  or event.key == pygame.K_w and y_change == 0:
                    x_change = 0
                    y_change = -SCALE
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s and y_change == 0:
                    x_change = 0
                    y_change = SCALE

        if snake_head[0] + x_change > DISPLAY_WIDTH - SCALE or snake_head[0] + x_change < 0 or snake_head[1] + \
                y_change > DISPLAY_HEIGHT - SCALE or snake_head[1] + y_change < 0:
            game_over = True

        if snake_head[0] + x_change == cherry[0] and snake_head[1] + y_change == cherry[1]:
            cherry = set_cherry(snake_body, maze_parts)
            snake_length += 1

        for body_coord in snake_body[:-1]:
            if snake_head[0] + x_change == body_coord[0] and snake_head[1] + y_change == body_coord[1]:
                game_over = True

        for maze_coord in maze_parts:
            if snake_head[0] + x_change >= maze_coord[0] and snake_head[0] + x_change < maze_coord[0] + MAZE_SIZE:
                if snake_head[1] + y_change >= maze_coord[1] and snake_head[1] + y_change < maze_coord[1] + MAZE_SIZE:
                    game_over = True

        if not game_over:
            snake_head[0] += x_change
            snake_head[1] += y_change
            temp = []
            temp.append(snake_head[0])
            temp.append(snake_head[1])
            snake_body.append(temp)

            if len(snake_body) > snake_length:
                del snake_body[0]

        game_display.fill(white)
        pygame.draw.rect(game_display, red, [cherry[0], cherry[1], SCALE, SCALE])
        draw_snake(snake_body, green)
        draw_maze(maze_parts, black)
        pygame.display.update()
        clock.tick(FPS)

        while game_over == True:
            game_display.fill(white)
            pygame.draw.rect(game_display, faded_red, [cherry[0], cherry[1], SCALE, SCALE])
            draw_snake(snake_body, faded_green)
            draw_maze(maze_parts, grey)
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