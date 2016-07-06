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
DISPLAY_WIDTH = 700
DISPLAY_HEIGHT = 500
MAZE_SIZE = 40 #multiple of scale

game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption('Snake Maze')
clock = pygame.time.Clock()

small_font = pygame.font.SysFont('Century Gothic', 24)
med_font = pygame.font.SysFont('Century Gothic', 50)
large_font = pygame.font.SysFont('Century Gothic', 80)

snake_head_img = pygame.image.load('snake head.png')
snake_head_faded_img = pygame.image.load('snake head faded.png')

def display_text(text, size, colour, position, y_displace = 0):
    if size == 'small':
        screen_text = small_font.render(text, True, colour)
    elif size == 'medium':
        screen_text = med_font.render(text, True, colour)
    elif size == 'large':
        screen_text = large_font.render(text, True, colour)
    if position == 'center':
        game_display.blit(screen_text, [DISPLAY_WIDTH/2 - screen_text.get_rect().width/2, DISPLAY_HEIGHT/2 -
                                        screen_text.get_rect().height/2 + y_displace])
    elif position == 'top center':
        game_display.blit(screen_text, [DISPLAY_WIDTH / 2 - screen_text.get_rect().width / 2, y_displace])

def draw_snake(snake_head_rotated, snake_body, colour):
    game_display.blit(snake_head_rotated, [snake_body[-1][0], snake_body[-1][1]])
    for coord in snake_body[:-1]:
        pygame.draw.rect(game_display, colour, [coord[0], coord[1], SCALE, SCALE])


def draw_maze(maze_parts, colour):
    for coord in maze_parts:
        pygame.draw.rect(game_display, colour, [coord[0], coord[1], MAZE_SIZE, MAZE_SIZE])


def create_maze(maze_num):
    maze_parts = [[] for x in range(maze_num)]
    for i in range(0, maze_num):
        maze_parts[i].append(random.randrange(0, DISPLAY_WIDTH - SCALE, SCALE))
        maze_parts[i].append(random.randrange(0, DISPLAY_HEIGHT - SCALE, SCALE))

        while maze_parts[i][0] == 0 and maze_parts[i][1] <= DISPLAY_HEIGHT/2:
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


def game_intro():
    intro = True
    continue_game = True

    while intro:
        game_display.fill(white)
        display_text('Snake Maze', 'large', green, 'center', -100)
        display_text('Rules are simple - eat the cherry and', 'small', black,
                     'center', -30)
        display_text('avoid the maze blocks and edges', 'small', black,
                     'center')
        display_text("Press 'e' for easy mode", 'small', red, 'center', 30)
        display_text("Press 'm' for medium mode", 'small', red, 'center', 60)
        display_text("Press 'h' for hard mode", 'small', red, 'center', 90)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                continue_game = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    fps = 10
                    maze_num = 5
                    intro = False
                elif event.key == pygame.K_m:
                    fps = 15
                    maze_num = 10
                    intro = False
                elif event.key == pygame.K_h:
                    fps = 20
                    maze_num = 15
                    intro = False


    return fps, maze_num, continue_game


def game_loop(fps, maze_num):
    game_exit = False
    game_over = False
    snake_head = [0, 0]
    x_change = 0
    y_change = SCALE
    snake_body = []
    snake_length = 2
    maze_parts = create_maze(maze_num)
    cherry = set_cherry(snake_body, maze_parts)
    rotation = 180
    score = 0

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and x_change == 0:
                    x_change = -SCALE
                    y_change = 0
                    rotation = 90
                elif (event.key == pygame.K_RIGHT  or event.key == pygame.K_d) and x_change == 0:
                    x_change = SCALE
                    y_change = 0
                    rotation = 270
                elif (event.key == pygame.K_UP  or event.key == pygame.K_w) and y_change == 0:
                    x_change = 0
                    y_change = -SCALE
                    rotation = 0
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and y_change == 0:
                    x_change = 0
                    y_change = SCALE
                    rotation = 180

        if snake_head[0] + x_change > DISPLAY_WIDTH - SCALE or snake_head[0] + x_change < 0 or snake_head[1] + \
                y_change > DISPLAY_HEIGHT - SCALE or snake_head[1] + y_change < 0:
            game_over = True

        if snake_head[0] + x_change == cherry[0] and snake_head[1] + y_change == cherry[1]:
            cherry = set_cherry(snake_body, maze_parts)
            snake_length += 1
            score += 10

        for body_coord in snake_body[:-1]:
            if snake_head[0] + x_change == body_coord[0] and snake_head[1] + y_change == body_coord[1]:
                game_over = True

        for maze_coord in maze_parts:
            if snake_head[0] + x_change >= maze_coord[0] and snake_head[0] + x_change < maze_coord[0] + MAZE_SIZE:
                if snake_head[1] + y_change >= maze_coord[1] and snake_head[1] + y_change < maze_coord[1] + MAZE_SIZE:
                    game_over = True

        if not game_over:
            snake_head_rotated = pygame.transform.rotate(snake_head_img, rotation)
            snake_head_faded_rotated = pygame.transform.rotate(snake_head_faded_img, rotation)
            snake_head[0] += x_change
            snake_head[1] += y_change
            temp = []
            temp.append(snake_head[0])
            temp.append(snake_head[1])
            snake_body.append(temp)

            if len(snake_body) > snake_length:
                del snake_body[0]

        game_display.fill(white)
        pygame.draw.ellipse(game_display, red, [cherry[0], cherry[1], SCALE, SCALE])
        draw_snake(snake_head_rotated, snake_body, green)
        draw_maze(maze_parts, black)
        score_text = 'Score = ' + str(score)
        display_text(score_text, 'small', grey, 'top center')
        pygame.display.update()
        clock.tick(fps)

        while game_over == True:
            game_display.fill(white)
            pygame.draw.ellipse(game_display, faded_red, [cherry[0], cherry[1], SCALE, SCALE])
            draw_snake(snake_head_faded_rotated, snake_body, faded_green)
            draw_maze(maze_parts, grey)
            display_text('GAME OVER', 'large', red, 'center', -25)
            display_text("Press 'space' to play again or 'r' to return to menu", 'small', black, 'center', 25)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        fps, maze_num, continue_game = game_intro()
                        if continue_game:
                            game_loop(fps, maze_num)
                    elif event.key == pygame.K_SPACE:
                        game_loop(fps, maze_num)

    pygame.quit()
    quit()

fps, maze_num, continue_game = game_intro()
if continue_game:
    game_loop(fps, maze_num)