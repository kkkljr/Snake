import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SNAKE_SPEED = 10

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Background
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Snake initialization
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = (0, -1)  # Initial direction: up
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
bonus_food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
food_type = 1  # 1 for regular food, 2 for bonus food

# Game variables
running = True
clock = pygame.time.Clock()
score = 0

# Sound effects
eat_sound = pygame.mixer.Sound("eat.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

def game_over():
    game_over_sound.play()
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    quit()

def wrap_around(position):
    x, y = position
    if x < 0:
        x = GRID_WIDTH - 1
    elif x >= GRID_WIDTH:
        x = 0
    if y < 0:
        y = GRID_HEIGHT - 1
    elif y >= GRID_HEIGHT:
        y = 0
    return x, y

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != (0, 1):
                snake_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                snake_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                snake_direction = (1, 0)

    # Move the snake
    x, y = snake[0]
    new_head = (x + snake_direction[0], y + snake_direction[1])

    # Wrap around the screen
    new_head = wrap_around(new_head)

    # Check for collisions
    if new_head in snake[1:] or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
        game_over()

    snake.insert(0, new_head)

    # Check if the snake ate the food
    if snake[0] == food:
        score += 1
        eat_sound.play()
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        food_type = 1
    elif snake[0] == bonus_food:
        score += 5
        eat_sound.play()
        bonus_food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        food_type = 1
    else:
        snake.pop()

    # Generate random bonus food
    if random.randint(1, 100) <= 5 and food_type == 1:
        food_type = 2
        bonus_food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    # Clear the screen
    screen.fill(WHITE)
    screen.blit(background, (0, 0))

    # Draw food
    if food_type == 1:
        pygame.draw.rect(screen, GREEN, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    else:
        pygame.draw.rect(screen, BLUE, (bonus_food[0] * GRID_SIZE, bonus_food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    draw_score()
    pygame.display.flip()

    # Control game speed
    clock.tick(SNAKE_SPEED)

# Quit the game
pygame.quit()

