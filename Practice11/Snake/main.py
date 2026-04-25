import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = [(100, 100)]
dx, dy = CELL, 0

foods = [
    {"value": 1, "color": (255, 0, 0)},
    {"value": 2, "color": (255, 165, 0)},
    {"value": 5, "color": (255, 255, 0)}
]

def new_food():
    return (random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL))

food = new_food()
food_data = random.choice(foods)
timer = 0

score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx, dy = -CELL, 0
            if event.key == pygame.K_RIGHT:
                dx, dy = CELL, 0
            if event.key == pygame.K_UP:
                dx, dy = 0, -CELL
            if event.key == pygame.K_DOWN:
                dx, dy = 0, CELL

    head = (snake[0][0] + dx, snake[0][1] + dy)

    # wall collision
    if head[0] < 0 or head[1] < 0 or head[0] >= WIDTH or head[1] >= HEIGHT:
        pygame.quit()
        sys.exit()

    if head in snake:
        pygame.quit()
        sys.exit()

    snake.insert(0, head)

    if head == food:
        score += food_data["value"]
        food = new_food()
        food_data = random.choice(foods)
        timer = 0
    else:
        snake.pop()

    # food timer
    timer += 1
    if timer > 100:
        food = new_food()
        food_data = random.choice(foods)
        timer = 0

    screen.fill((0, 0, 0))

    for s in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*s, CELL, CELL))

    pygame.draw.rect(screen, food_data["color"], (*food, CELL, CELL))

    pygame.display.flip()
    clock.tick(10)