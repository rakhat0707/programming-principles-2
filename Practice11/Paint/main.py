import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

color = (0, 0, 0)
mode = "draw"
drawing = False
start = None

screen.fill((255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: mode = "rect"
            if event.key == pygame.K_c: mode = "circle"
            if event.key == pygame.K_q: mode = "square"
            if event.key == pygame.K_t: mode = "triangle"
            if event.key == pygame.K_y: mode = "eq"
            if event.key == pygame.K_u: mode = "rhombus"

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end = event.pos

            if mode == "rect":
                pygame.draw.rect(screen, color, (*start, end[0]-start[0], end[1]-start[1]), 2)

            elif mode == "square":
                size = abs(end[0]-start[0])
                pygame.draw.rect(screen, color, (start[0], start[1], size, size), 2)

            elif mode == "circle":
                r = int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5)
                pygame.draw.circle(screen, color, start, r, 2)

            elif mode == "triangle":
                pygame.draw.polygon(screen, color, [start, (end[0], start[1]), end], 2)

            elif mode == "eq":
                x,y = start
                size = abs(end[0]-start[0])
                pygame.draw.polygon(screen, color,
                    [(x,y),(x+size,y),(x+size//2,y-size)], 2)

            elif mode == "rhombus":
                x1,y1 = start
                x2,y2 = end
                cx = (x1+x2)//2
                cy = (y1+y2)//2
                pygame.draw.polygon(screen, color,
                    [(cx,y1),(x2,cy),(cx,y2),(x1,cy)], 2)

        if event.type == pygame.MOUSEMOTION and drawing and mode == "draw":
            pygame.draw.circle(screen, color, event.pos, 5)

    pygame.display.flip()
    clock.tick(60)