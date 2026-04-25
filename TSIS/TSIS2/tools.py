from collections import deque
import pygame


def flood_fill(surface, start_pos, new_color):
    x, y = start_pos
    width, height = surface.get_size()

    target_color = surface.get_at((x, y))
    new_color = pygame.Color(new_color)

    if target_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), new_color)

        queue.append((x + 1, y))
        queue.append((x - 1, y))
        queue.append((x, y + 1))
        queue.append((x, y - 1))


def draw_shape(surface, tool, color, start_pos, end_pos, brush_size):
    x1, y1 = start_pos
    x2, y2 = end_pos

    if tool == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, color, rect, brush_size)

    elif tool == "circle":
        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        pygame.draw.circle(surface, color, start_pos, radius, brush_size)

    elif tool == "square":
        size = min(abs(x2 - x1), abs(y2 - y1))
        sign_x = 1 if x2 >= x1 else -1
        sign_y = 1 if y2 >= y1 else -1
        rect = pygame.Rect(x1, y1, size * sign_x, size * sign_y)
        rect.normalize()
        pygame.draw.rect(surface, color, rect, brush_size)

    elif tool == "right_triangle":
        points = [start_pos, (x1, y2), end_pos]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == "equilateral_triangle":
        size = abs(x2 - x1)
        points = [
            (x1, y1),
            (x1 + size, y1),
            (x1 + size // 2, y1 - size)
        ]
        pygame.draw.polygon(surface, color, points, brush_size)

    elif tool == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [
            (cx, y1),
            (x2, cy),
            (cx, y2),
            (x1, cy)
        ]
        pygame.draw.polygon(surface, color, points, brush_size)