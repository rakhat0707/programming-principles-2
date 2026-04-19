import pygame
import random

pygame.init()

# окно
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# игрок
player_w, player_h = 50, 80
player_x = WIDTH // 2 - player_w // 2
player_y = HEIGHT - 100
player_speed = 5

# враг
enemy_w, enemy_h = 50, 80
enemy_x = random.randint(0, WIDTH - enemy_w)
enemy_y = -100
enemy_speed = 5

# монета
coin_size = 20
coin_x = random.randint(0, WIDTH - coin_size)
coin_y = -50
coin_speed = 5

coins_collected = 0

running = True

while running:
    screen.fill(WHITE)

    # события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # ограничение по экрану
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_w:
        player_x = WIDTH - player_w

    # движение врага
    enemy_y += enemy_speed
    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(0, WIDTH - enemy_w)

    # движение монеты
    coin_y += coin_speed
    if coin_y > HEIGHT:
        coin_y = -50
        coin_x = random.randint(0, WIDTH - coin_size)

    # прямоугольники
    player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_w, enemy_h)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)

    # столкновение с врагом
    if player_rect.colliderect(enemy_rect):
        print("GAME OVER")
        running = False

    # столкновение с монетой
    if player_rect.colliderect(coin_rect):
        coins_collected += 1
        coin_y = -50
        coin_x = random.randint(0, WIDTH - coin_size)

    # рисуем
    pygame.draw.rect(screen, BLACK, player_rect)
    pygame.draw.rect(screen, (255, 0, 0), enemy_rect)
    pygame.draw.circle(screen, YELLOW, (coin_x + 10, coin_y + 10), 10)

    # счётчик (правый верхний угол)
    text = font.render(f"Coins: {coins_collected}", True, BLACK)
    screen.blit(text, (WIDTH - 150, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()