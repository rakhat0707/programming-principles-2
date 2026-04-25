import pygame
import sys
from datetime import datetime
from tools import flood_fill, draw_shape

pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint Application")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 16)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)
DARK_GRAY = (120, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 200, 0)
PURPLE = (160, 0, 200)

colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, WHITE]
current_color = BLACK

tool = "pencil"
brush_size = 5

drawing = False
start_pos = None
last_pos = None

typing = False
text_value = ""
text_pos = None


def canvas_pos(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def inside_canvas(pos):
    x, y = pos
    return 0 <= x < WIDTH and TOOLBAR_HEIGHT <= y < HEIGHT


def save_canvas():
    filename = datetime.now().strftime("paint_%Y%m%d_%H%M%S.png")
    pygame.image.save(canvas, filename)
    print("Saved:", filename)


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    info = f"Tool: {tool} | Brush: {brush_size}px | Color: {current_color}"
    text = small_font.render(info, True, BLACK)
    screen.blit(text, (10, 8))

    help_text = "P Pencil | L Line | R Rect | C Circle | E Eraser | F Fill | T Text | Q Square | A RightTri | W EquiTri | D Rhombus | 1/2/3 Size | Ctrl+S Save"
    help_surface = small_font.render(help_text, True, BLACK)
    screen.blit(help_surface, (10, 32))

    x = 10
    y = 55
    for color in colors:
        pygame.draw.rect(screen, color, (x, y, 25, 20))
        pygame.draw.rect(screen, BLACK, (x, y, 25, 20), 1)
        x += 35


def get_color_from_toolbar(pos):
    x, y = pos
    if 55 <= y <= 75:
        start_x = 10
        for i, color in enumerate(colors):
            rect = pygame.Rect(start_x + i * 35, 55, 25, 20)
            if rect.collidepoint(pos):
                return color
    return None


running = True

while running:
    preview = canvas.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if typing:
                if event.key == pygame.K_RETURN:
                    if text_value:
                        rendered = font.render(text_value, True, current_color)
                        canvas.blit(rendered, text_pos)
                    typing = False
                    text_value = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_value = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    text_value = text_value[:-1]

                else:
                    text_value += event.unicode

            else:
                if event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rect"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_t:
                    tool = "text"
                elif event.key == pygame.K_q:
                    tool = "square"
                elif event.key == pygame.K_a:
                    tool = "right_triangle"
                elif event.key == pygame.K_w:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_d:
                    tool = "rhombus"

                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_canvas()

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_color = get_color_from_toolbar(event.pos)
            if clicked_color is not None:
                current_color = clicked_color
                continue

            if inside_canvas(event.pos):
                pos = canvas_pos(event.pos)

                if tool == "fill":
                    flood_fill(canvas, pos, current_color)

                elif tool == "text":
                    typing = True
                    text_value = ""
                    text_pos = pos

                else:
                    drawing = True
                    start_pos = pos
                    last_pos = pos

        if event.type == pygame.MOUSEMOTION:
            if drawing and inside_canvas(event.pos):
                pos = canvas_pos(event.pos)

                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size)
                    last_pos = pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and inside_canvas(event.pos):
                end_pos = canvas_pos(event.pos)

                if tool == "line":
                    pygame.draw.line(canvas, current_color, start_pos, end_pos, brush_size)

                elif tool in ["rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]:
                    draw_shape(canvas, tool, current_color, start_pos, end_pos, brush_size)

            drawing = False
            start_pos = None
            last_pos = None

    mouse_pos = pygame.mouse.get_pos()

    if drawing and start_pos and inside_canvas(mouse_pos):
        end_pos = canvas_pos(mouse_pos)

        if tool == "line":
            pygame.draw.line(preview, current_color, start_pos, end_pos, brush_size)

        elif tool in ["rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]:
            draw_shape(preview, tool, current_color, start_pos, end_pos, brush_size)

    screen.fill(WHITE)
    screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if typing and text_pos is not None:
        rendered = font.render(text_value + "|", True, current_color)
        screen.blit(rendered, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    draw_toolbar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()