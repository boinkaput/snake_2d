import sys
sys.path.insert(0, 'package/')

import os, pygame, sys, time, random
from recordtype import recordtype

os.environ['SDL_AUDIODRIVER'] = 'dsp'

Position = recordtype('Position', ['x', 'y'])

BLACK = (0, 0, 0)
FPS = 120
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

SCORE_COLOR = (255, 255, 255)
SCORE_HEIGHT = 50

BORDER_START_X = 0
BORDER_START_Y = 100
BORDER_WIDTH = 500
BORDER_HEIGHT = 400
BORDER_THICKNESS = 10

SNAKE_HEAD_COLOR = (255, 128, 0)
SNAKE_COLOR = (0, 255, 0)
SNAKE_WIDTH = 10
SNAKE_HEIGHT = 10

APPLE_COLOR = (255, 0, 0)
APPLE_RADIUS = 5

DELAY = 0.1
VELOCITY = 10

UP = Position(0, -VELOCITY)
DOWN = Position(0, VELOCITY)
LEFT = Position(-VELOCITY, 0)
RIGHT = Position(VELOCITY, 0)

CLICK_MESSAGE_COLOR = (255, 128, 0)

pygame.init()
font = pygame.font.SysFont("monospace", 20)

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

def generateSnake():
    return [Position(50, 300)]

def generateApple(snake):
    global apple

    new_apple_x = random.randrange(BORDER_START_X + BORDER_THICKNESS, BORDER_START_X + BORDER_WIDTH - BORDER_THICKNESS, SNAKE_WIDTH // 2)
    new_apple_y = random.randrange(BORDER_START_Y + BORDER_THICKNESS, BORDER_START_Y + BORDER_HEIGHT - BORDER_THICKNESS, SNAKE_HEIGHT // 2)

    while not (new_apple_x % SNAKE_WIDTH == SNAKE_WIDTH / 2) or new_apple_x in [s.x for s in snake]:
        new_apple_x = random.randrange(BORDER_START_X + BORDER_THICKNESS, BORDER_START_X + BORDER_WIDTH - BORDER_THICKNESS, SNAKE_WIDTH // 2)

    while not (new_apple_y % SNAKE_HEIGHT == SNAKE_HEIGHT / 2) or new_apple_y in [s.y for s in snake]:
        new_apple_y = random.randrange(BORDER_START_Y + BORDER_THICKNESS, BORDER_START_Y + BORDER_HEIGHT - BORDER_THICKNESS, SNAKE_HEIGHT // 2)

    apple = Position(new_apple_x, new_apple_y)

def updateScore(snake, high_score):
    text = f"Score: {len(snake) - 1}        High Score: {high_score}"
    label = font.render(text, True, SCORE_COLOR)
    window.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, SCORE_HEIGHT))

    pygame.draw.rect(window, SCORE_COLOR, (BORDER_START_X, BORDER_START_Y, BORDER_WIDTH, BORDER_HEIGHT), BORDER_THICKNESS)

def updateSnake(snake, direction, apple):
    snake.insert(0, Position(snake[0].x + direction.x, snake[0].y + direction.y))

    snake_head = pygame.Rect(snake[0].x, snake[0].y, SNAKE_WIDTH, SNAKE_HEIGHT)
    if not snake_head.collidepoint((apple.x, apple.y)):
        snake.pop()
    else:
        generateApple(snake)

    pygame.draw.rect(window, SNAKE_HEAD_COLOR, (snake[0].x, snake[0].y, SNAKE_WIDTH, SNAKE_HEIGHT))

    for i in range(1, len(snake)):
        pygame.draw.rect(window, SNAKE_COLOR, (snake[i].x, snake[i].y, SNAKE_WIDTH, SNAKE_HEIGHT))

    time.sleep(DELAY)

def drawApple(apple):
    pygame.draw.circle(window, APPLE_COLOR, (apple.x, apple.y), APPLE_RADIUS)

def getHighScore():
    if os.path.isfile("save.txt"):
        with open('save.txt', 'r') as f:
            return int(f.read())

    return 0

def saveScore(high_score):
    with open('save.txt', 'w') as f:
        f.write(f"{high_score}")

def drawGameOver(snake):
    font = pygame.font.SysFont("monospace", 50)
    text = f"Score: {len(snake) - 1}"
    label = font.render(text, False, SCORE_COLOR)
    window.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, (SCREEN_HEIGHT - label.get_height()) / 2))

    font = pygame.font.SysFont("monospace", 20, True)
    message = "Click to continue..."
    label = font.render(message, False, CLICK_MESSAGE_COLOR)
    window.blit(label, ((SCREEN_WIDTH - label.get_width()) / 2, SCREEN_HEIGHT - 100))

def main():
    global high_score, snake, direction
    while True:
        window.fill(BLACK)
        updateScore(snake, high_score)
        updateSnake(snake, direction, apple)
        drawApple(apple)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = UP
                    return
                elif event.key == pygame.K_DOWN:
                    direction = DOWN
                    return
                elif event.key == pygame.K_LEFT:
                    direction = LEFT
                    return
                elif event.key == pygame.K_RIGHT:
                    direction = RIGHT
                    return

        pygame.display.update()
        clock.tick(FPS)

def game():
    global high_score, snake, apple, direction
    while True:
        window.fill(BLACK)
        updateScore(snake, high_score)
        updateSnake(snake, direction, apple)
        drawApple(apple)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT

        high_score = max(high_score, len(snake) - 1)

        if snake[0].x < BORDER_START_X or snake[0].x >= BORDER_START_X + BORDER_WIDTH or\
        snake[0].y < BORDER_START_Y or snake[0].y >= BORDER_START_Y + BORDER_HEIGHT or\
        (snake[0].x, snake[0].y) in [(snake[i].x, snake[i].y) for i in range(1, len(snake))]:
            saveScore(high_score)
            time.sleep(1)
            return

        pygame.display.update()
        clock.tick(FPS)

def gameOver():
    global snake
    while True:
        window.fill(BLACK)
        drawGameOver(snake)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    while True:
        high_score = getHighScore()
        snake = generateSnake()
        generateApple(snake)
        direction = Position(0, 0)

        main()
        game()
        gameOver()
