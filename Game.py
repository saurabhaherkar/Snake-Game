import random
import pygame
import  os

pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

screen_width = 900
screen_height = 600
# bgimg = pygame.image.load('snake.jpeg')
# bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game')
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    fps = 40
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        for event in pygame.event.get():
            gameWindow.fill((233, 120, 105))
            text_screen('Welcome to Snakes Game', black, 200, 230)
            text_screen('Press Space-Bar to play', black, 220, 270)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

            if event.type == pygame.QUIT:
                exit_game = True

        pygame.display.update()
        clock.tick(60)

def game_loop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 30
    velocity_x = 0
    velocity_y = 0
    if not os.path.exists('highscore.txt'):
        with open('highscore.txt', 'w') as f:
            f.write('0')

    with open("highscore.txt", "r") as f:
        hs = f.read()

    food_x = random.randint(20, screen_width)
    food_y = random.randint(20, screen_height)
    score = 0
    int_velocity = 5
    fps = 20

    snk_list = []
    snk_length = 1

    while not exit_game:
        if game_over:
            with open('highscore.txt', 'w') as f:
                f.write(str(hs))
            gameWindow.fill(white)
            text_screen('Game Over! Press ENTER to continue', red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = int_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -int_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -int_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = int_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score += 5

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                food_x = random.randint(20, screen_width/3)
                food_y = random.randint(20, screen_height/3)
                snk_length += 5
                fps += 5
                if score > int(hs):
                    hs = score

            gameWindow.fill(white)
            # gameWindow.blit(bgimg, (0, 0))
            text_screen('Score : '+ str(score) + ' Highscore : '+ str(hs), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()