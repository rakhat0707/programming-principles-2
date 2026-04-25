import pygame
import sys
import json
from pathlib import Path

from game import SnakeGame, WIDTH, HEIGHT, CELL
from db import setup_database, save_game, get_top10, get_personal_best


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS4 Snake Game")

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("Arial", 24)
SMALL_FONT = pygame.font.SysFont("Arial", 18)
BIG_FONT = pygame.font.SysFont("Arial", 42)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (190, 190, 190)
BLUE = (80, 150, 255)
GREEN = (0, 200, 0)
RED = (220, 0, 0)

BASE_DIR = Path(__file__).parent
SETTINGS_FILE = BASE_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],
    "grid": True,
    "sound": False
}


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = BLUE if self.rect.collidepoint(mouse) else GRAY

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        text = FONT.render(self.text, True, BLACK)
        rect = text.get_rect(center=self.rect.center)
        screen.blit(text, rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


settings = load_settings()


def draw_center(text, y, font=FONT, color=BLACK):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, rect)


def username_input_screen():
    username = ""

    while True:
        screen.fill(WHITE)

        draw_center("Enter Username", 180, BIG_FONT)
        draw_center(username + "|", 260, FONT)
        draw_center("Press Enter to continue", 330, SMALL_FONT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return username.strip() if username.strip() else "Player"

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif len(username) < 14 and event.unicode.isprintable():
                    username += event.unicode

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    play = Button(200, 210, 200, 50, "Play")
    leaderboard = Button(200, 280, 200, 50, "Leaderboard")
    settings_btn = Button(200, 350, 200, 50, "Settings")
    quit_btn = Button(200, 420, 200, 50, "Quit")

    while True:
        screen.fill(WHITE)

        draw_center("TSIS4 Snake", 120, BIG_FONT)

        for btn in [play, leaderboard, settings_btn, quit_btn]:
            btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if play.clicked(event):
                username = username_input_screen()
                return "play", username

            if leaderboard.clicked(event):
                leaderboard_screen()

            if settings_btn.clicked(event):
                settings_screen()

            if quit_btn.clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)


def game_screen(username):
    game = SnakeGame(username, settings)
    saved = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.set_direction((0, -CELL))
                elif event.key == pygame.K_DOWN:
                    game.set_direction((0, CELL))
                elif event.key == pygame.K_LEFT:
                    game.set_direction((-CELL, 0))
                elif event.key == pygame.K_RIGHT:
                    game.set_direction((CELL, 0))

        game.update()
        game.draw(screen, SMALL_FONT)

        if game.game_over:
            if not saved:
                save_game(username, game.score, game.level)
                saved = True

            return game_over_screen(username, game.score, game.level)

        pygame.display.flip()
        clock.tick(game.speed)


def game_over_screen(username, score, level):
    retry = Button(200, 390, 200, 50, "Retry")
    menu = Button(200, 460, 200, 50, "Main Menu")

    best = max(score, get_personal_best(username))

    while True:
        screen.fill(WHITE)

        draw_center("GAME OVER", 120, BIG_FONT, RED)
        draw_center(f"Player: {username}", 200)
        draw_center(f"Final Score: {score}", 240)
        draw_center(f"Level Reached: {level}", 280)
        draw_center(f"Personal Best: {best}", 320)

        retry.draw()
        menu.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if retry.clicked(event):
                return "retry"

            if menu.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen():
    back = Button(200, 530, 200, 45, "Back")

    while True:
        screen.fill(WHITE)

        draw_center("Leaderboard Top 10", 60, BIG_FONT)

        data = get_top10()

        y = 120
        header = "Rank  Username        Score   Level   Date"
        screen.blit(SMALL_FONT.render(header, True, BLACK), (30, 95))

        for i, row in enumerate(data, start=1):
            username, score, level, date = row
            line = f"{i:<5} {username:<14} {score:<7} {level:<7} {date}"
            screen.blit(SMALL_FONT.render(line, True, BLACK), (30, y))
            y += 35

        back.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back.clicked(event):
                return

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.flip()
        clock.tick(60)


def settings_screen():
    global settings

    grid_btn = Button(170, 180, 260, 45, "")
    sound_btn = Button(170, 245, 260, 45, "")
    color_btn = Button(170, 310, 260, 45, "")
    save_btn = Button(170, 420, 260, 50, "Save & Back")

    colors = [
        [0, 255, 0],
        [0, 180, 255],
        [255, 255, 0],
        [255, 0, 255],
        [255, 120, 0]
    ]

    while True:
        screen.fill(WHITE)

        draw_center("Settings", 100, BIG_FONT)

        grid_btn.text = f"Grid: {'ON' if settings.get('grid') else 'OFF'}"
        sound_btn.text = f"Sound: {'ON' if settings.get('sound') else 'OFF'}"
        color_btn.text = f"Snake Color: {settings.get('snake_color')}"

        for btn in [grid_btn, sound_btn, color_btn, save_btn]:
            btn.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if grid_btn.clicked(event):
                settings["grid"] = not settings.get("grid", True)

            if sound_btn.clicked(event):
                settings["sound"] = not settings.get("sound", False)

            if color_btn.clicked(event):
                current = settings.get("snake_color", [0, 255, 0])
                index = colors.index(current) if current in colors else 0
                settings["snake_color"] = colors[(index + 1) % len(colors)]

            if save_btn.clicked(event):
                save_settings(settings)
                return

        pygame.display.flip()
        clock.tick(60)


def main():
    setup_database()

    while True:
        action, username = main_menu()

        if action == "play":
            while True:
                result = game_screen(username)

                if result == "retry":
                    continue

                if result == "menu":
                    break


if __name__ == "__main__":
    main()