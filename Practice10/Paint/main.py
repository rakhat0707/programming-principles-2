import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# Colors
colors = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255)
}

current_color = colors["black"]

# Modes: draw, rect, circle, eraser
mode = "draw"

drawing = False
start_pos = None

screen.fill(WHITE := (255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                mode = "rect"
            elif event.key == pygame.K_c:
                mode = "circle"
            elif event.key == pygame.K_e:
                mode = "eraser"
            elif event.key == pygame.K_p:
                mode = "draw"

            # Color selection
            elif event.key == pygame.K_1:
                current_color = colors["black"]
            elif event.key == pygame.K_2:
                current_color = colors["red"]
            elif event.key == pygame.K_3:
                current_color = colors["green"]
            elif event.key == pygame.K_4:
                current_color = colors["blue"]

        # Mouse pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # Mouse released
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if mode == "rect":
                pygame.draw.rect(screen, current_color,
                                 (*start_pos,
                                  end_pos[0] - start_pos[0],
                                  end_pos[1] - start_pos[1]), 2)

            elif mode == "circle":
                radius = int(((end_pos[0] - start_pos[0]) ** 2 +
                              (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, 2)

        # Drawing with mouse movement
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "draw":
                pygame.draw.circle(screen, current_color, event.pos, 5)

            elif mode == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, 10)

    pygame.display.flip()
    clock.tick(60)