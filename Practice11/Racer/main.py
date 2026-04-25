import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Advanced")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# player
player = pygame.Rect(180, 500, 40, 80)

# enemy
enemy = pygame.Rect(random.randint(0, 360), -100, 40, 80)
enemy_speed = 5

# coins with weights
coin_types = [
    {"value": 1, "color": (255, 255, 0)},
    {"value": 2, "color": (255, 165, 0)},
    {"value": 5, "color": (255, 0, 255)}
]

coin = pygame.Rect(random.randint(0, 380), -50, 20, 20)
coin_data = random.choice(coin_types)

coins = 0

while True:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5

    player.x = max(0, min(player.x, WIDTH - player.width))

    # enemy move
    enemy.y += enemy_speed
    if enemy.y > HEIGHT:
        enemy.y = -100
        enemy.x = random.randint(0, 360)

    # coin move
    coin.y += 5
    if coin.y > HEIGHT:
        coin.y = -50
        coin.x = random.randint(0, 380)
        coin_data = random.choice(coin_types)

    # collision
    if player.colliderect(enemy):
        print("GAME OVER")
        pygame.quit()
        sys.exit()

    if player.colliderect(coin):
        coins += coin_data["value"]

        # speed up every 10 coins
        if coins % 10 == 0:
            enemy_speed += 1

        coin.y = -50
        coin.x = random.randint(0, 380)
        coin_data = random.choice(coin_types)

    pygame.draw.rect(screen, (0, 0, 0), player)
    pygame.draw.rect(screen, (255, 0, 0), enemy)
    pygame.draw.circle(screen, coin_data["color"], coin.center, 10)

    text = font.render(f"Coins: {coins}", True, (0, 0, 0))
    screen.blit(text, (250, 10))

    pygame.display.flip()
    clock.tick(60)