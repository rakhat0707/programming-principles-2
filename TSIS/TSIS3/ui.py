import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
DARK_GRAY = (120, 120, 120)
BLUE = (70, 130, 255)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        color = BLUE if self.rect.collidepoint(mouse_pos) else GRAY

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def draw_text(screen, text, x, y, font, color=BLACK):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_center_text(screen, text, y, font, color=BLACK):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(surface, rect)