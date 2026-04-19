import pygame
import random
import sys

pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 400
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)

# Font for score and level
font = pygame.font.SysFont("Arial", 24)

clock = pygame.time.Clock()

# Initial snake position
snake = [(100, 100), (80, 100), (60, 100)]
dx, dy = CELL, 0

# Initial food position
food = (200, 200)

score = 0
level = 1
speed = 8


def random_food():
    """Generate food in a random place not occupied by the snake."""
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x, y) not in snake:
            return (x, y)


food = random_food()

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Change snake direction with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dx == 0:
                dx, dy = -CELL, 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx, dy = CELL, 0
            elif event.key == pygame.K_UP and dy == 0:
                dx, dy = 0, -CELL
            elif event.key == pygame.K_DOWN and dy == 0:
                dx, dy = 0, CELL

    # New head position
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # Check wall collision
    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        pygame.quit()
        sys.exit()

    # Check collision with itself
    if new_head in snake:
        pygame.quit()
        sys.exit()

    # Move snake
    snake.insert(0, new_head)

    # Check if food is eaten
    if new_head == food:
        score += 1

        # Increase level every 4 foods
        if score % 4 == 0:
            level += 1
            speed += 2

        food = random_food()
    else:
        snake.pop()

    # Drawing
    screen.fill(BLACK)

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL, CELL))

    # Draw food
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

    # Draw score and level
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(speed)