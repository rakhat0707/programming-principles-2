import pygame
import sys

from racer import RacerGame, WIDTH, HEIGHT
from persistence import load_settings, save_settings, load_leaderboard, add_score
from ui import Button, draw_text, draw_center_text


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 42)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 160, 0)
RED = (220, 0, 0)
BLUE = (50, 120, 255)


settings = load_settings()


def username_screen():
    name = ""

    while True:
        screen.fill(WHITE)

        draw_center_text(screen, "Enter Username", 180, big_font)
        draw_center_text(screen, name + "|", 260, font)
        draw_center_text(screen, "Press Enter to continue", 330, small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip() if name.strip() else "Player"

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif len(name) < 12:
                    if event.unicode.isprintable():
                        name += event.unicode

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    play_btn = Button(200, 230, 200, 50, "Play")
    leaderboard_btn = Button(200, 300, 200, 50, "Leaderboard")
    settings_btn = Button(200, 370, 200, 50, "Settings")
    quit_btn = Button(200, 440, 200, 50, "Quit")

    while True:
        screen.fill(WHITE)

        draw_center_text(screen, "TSIS3 Racer", 120, big_font)

        for btn in [play_btn, leaderboard_btn, settings_btn, quit_btn]:
            btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if play_btn.clicked(event):
                username = username_screen()
                return "play", username

            if leaderboard_btn.clicked(event):
                leaderboard_screen()

            if settings_btn.clicked(event):
                settings_screen()

            if quit_btn.clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)


def game_screen(username):
    global settings

    game = RacerGame(username, settings)
    saved = False

    while True:
        game.update()
        game.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if game.game_over and not saved:
            add_score(username, game.score, int(game.distance), game.coins_collected)
            saved = True
            return game_over_screen(game, username)

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(game, username):
    retry_btn = Button(190, 430, 220, 50, "Retry")
    menu_btn = Button(190, 500, 220, 50, "Main Menu")

    while True:
        screen.fill(WHITE)

        title = "FINISHED!" if game.finished else "GAME OVER"
        draw_center_text(screen, title, 120, big_font, RED)

        draw_text(screen, f"Player: {username}", 180, 200, font)
        draw_text(screen, f"Score: {game.score}", 180, 240, font)
        draw_text(screen, f"Distance: {int(game.distance)}", 180, 280, font)
        draw_text(screen, f"Coins: {game.coins_collected}", 180, 320, font)

        retry_btn.draw(screen, font)
        menu_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if retry_btn.clicked(event):
                return "retry"

            if menu_btn.clicked(event):
                return "menu"

        pygame.display.flip()
        clock.tick(60)


def leaderboard_screen():
    back_btn = Button(200, 620, 200, 45, "Back")

    while True:
        screen.fill(WHITE)
        data = load_leaderboard()

        draw_center_text(screen, "Top 10 Leaderboard", 70, big_font)

        y = 140
        draw_text(screen, "Rank   Name          Score     Distance", 80, 110, small_font)

        for i, item in enumerate(data[:10], start=1):
            line = f"{i:<5}  {item['name']:<12}  {item['score']:<8}  {item['distance']}"
            draw_text(screen, line, 80, y, small_font)
            y += 35

        back_btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_btn.clicked(event):
                return

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        pygame.display.flip()
        clock.tick(60)


def settings_screen():
    global settings

    sound_btn = Button(170, 180, 260, 45, "")
    color_btn = Button(170, 250, 260, 45, "")
    diff_btn = Button(170, 320, 260, 45, "")
    save_btn = Button(170, 430, 260, 50, "Save & Back")

    colors = ["blue", "red", "green", "purple"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill(WHITE)

        draw_center_text(screen, "Settings", 90, big_font)

        sound_btn.text = f"Sound: {'ON' if settings.get('sound') else 'OFF'}"
        color_btn.text = f"Car Color: {settings.get('car_color')}"
        diff_btn.text = f"Difficulty: {settings.get('difficulty')}"

        for btn in [sound_btn, color_btn, diff_btn, save_btn]:
            btn.draw(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if sound_btn.clicked(event):
                settings["sound"] = not settings.get("sound", True)

            if color_btn.clicked(event):
                current = settings.get("car_color", "blue")
                index = colors.index(current)
                settings["car_color"] = colors[(index + 1) % len(colors)]

            if diff_btn.clicked(event):
                current = settings.get("difficulty", "normal")
                index = difficulties.index(current)
                settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]

            if save_btn.clicked(event):
                save_settings(settings)
                return

        pygame.display.flip()
        clock.tick(60)


def main():
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