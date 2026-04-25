import pygame
import random
import time


WIDTH = 600
HEIGHT = 700

ROAD_LEFT = 100
ROAD_WIDTH = 400
LANE_COUNT = 4
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

FINISH_DISTANCE = 5000


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ROAD = (55, 55, 55)
LINE = (230, 230, 230)
RED = (220, 40, 40)
YELLOW = (255, 220, 0)
ORANGE = (255, 150, 0)
PURPLE = (160, 0, 200)
GREEN = (0, 180, 0)
BLUE = (50, 120, 255)
CYAN = (0, 220, 220)
GRAY = (120, 120, 120)
BROWN = (120, 70, 20)
OIL = (20, 20, 20)
DARK_RED = (130, 0, 0)


CAR_COLORS = {
    "blue": BLUE,
    "red": RED,
    "green": GREEN,
    "purple": PURPLE
}


DIFFICULTY_SETTINGS = {
    "easy": {
        "base_speed": 4,
        "traffic_chance": 0.018,
        "obstacle_chance": 0.012,
        "powerup_chance": 0.006
    },
    "normal": {
        "base_speed": 5,
        "traffic_chance": 0.025,
        "obstacle_chance": 0.018,
        "powerup_chance": 0.006
    },
    "hard": {
        "base_speed": 6,
        "traffic_chance": 0.035,
        "obstacle_chance": 0.025,
        "powerup_chance": 0.005
    }
}


class RacerGame:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings

        difficulty = settings.get("difficulty", "normal")
        self.difficulty = DIFFICULTY_SETTINGS.get(difficulty, DIFFICULTY_SETTINGS["normal"])

        self.base_speed = self.difficulty["base_speed"]
        self.road_speed = self.base_speed

        self.player_lane = 1
        self.player = pygame.Rect(0, HEIGHT - 120, 45, 75)
        self.set_player_lane(self.player_lane)

        self.player_move_speed = 7

        self.traffic = []
        self.obstacles = []
        self.coins = []
        self.powerups = []
        self.road_events = []

        self.coin_score = 0
        self.coins_collected = 0
        self.distance = 0
        self.bonus_score = 0

        self.score = 0
        self.game_over = False
        self.finished = False

        self.active_power = None
        self.active_power_start = 0
        self.active_power_duration = 0
        self.shield_active = False

        self.last_spawn_time = time.time()
        self.spawn_cooldown = 0.35

        self.font = pygame.font.SysFont("Arial", 22)
        self.big_font = pygame.font.SysFont("Arial", 32)

    def set_player_lane(self, lane):
        lane = max(0, min(LANE_COUNT - 1, lane))
        self.player_lane = lane
        self.player.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2 - self.player.width // 2

    def get_lane_x(self, lane, width):
        return ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2 - width // 2

    def safe_lane_for_spawn(self):
        lanes = list(range(LANE_COUNT))
        random.shuffle(lanes)

        for lane in lanes:
            too_busy = False

            for obj in self.traffic + self.obstacles + self.coins + self.powerups + self.road_events:
                if abs(obj["rect"].y) < 120 and obj["lane"] == lane:
                    too_busy = True
                    break

            if not too_busy:
                return lane

        return random.randint(0, LANE_COUNT - 1)

    def spawn_traffic(self):
        lane = self.safe_lane_for_spawn()

        # Safe spawn logic: do not spawn directly in player's lane too often
        if lane == self.player_lane and random.random() < 0.6:
            lane = (lane + random.choice([1, -1])) % LANE_COUNT

        rect = pygame.Rect(self.get_lane_x(lane, 45), -90, 45, 75)

        self.traffic.append({
            "rect": rect,
            "lane": lane,
            "speed": self.road_speed + random.randint(0, 2),
            "color": random.choice([RED, ORANGE, PURPLE])
        })

    def spawn_obstacle(self):
        lane = self.safe_lane_for_spawn()
        kind = random.choice(["barrier", "oil", "pothole", "speed_bump"])

        rect = pygame.Rect(self.get_lane_x(lane, 55), -70, 55, 35)

        self.obstacles.append({
            "rect": rect,
            "lane": lane,
            "kind": kind
        })

    def spawn_coin(self):
        lane = self.safe_lane_for_spawn()

        coin_type = random.choice([
            {"value": 1, "color": YELLOW},
            {"value": 2, "color": ORANGE},
            {"value": 5, "color": PURPLE}
        ])

        rect = pygame.Rect(self.get_lane_x(lane, 24), -40, 24, 24)

        self.coins.append({
            "rect": rect,
            "lane": lane,
            "value": coin_type["value"],
            "color": coin_type["color"]
        })

    def spawn_powerup(self):
        if self.active_power is not None or len(self.powerups) > 0:
            return

        lane = self.safe_lane_for_spawn()
        kind = random.choice(["nitro", "shield", "repair"])

        color = {
            "nitro": CYAN,
            "shield": GREEN,
            "repair": WHITE
        }[kind]

        rect = pygame.Rect(self.get_lane_x(lane, 28), -45, 28, 28)

        self.powerups.append({
            "rect": rect,
            "lane": lane,
            "kind": kind,
            "color": color,
            "spawn_time": time.time()
        })

    def spawn_road_event(self):
        lane = self.safe_lane_for_spawn()
        kind = random.choice(["moving_barrier", "nitro_strip"])

        rect = pygame.Rect(self.get_lane_x(lane, 65), -80, 65, 30)

        self.road_events.append({
            "rect": rect,
            "lane": lane,
            "kind": kind,
            "direction": random.choice([-1, 1])
        })

    def activate_powerup(self, kind):
        self.active_power = kind
        self.active_power_start = time.time()

        if kind == "nitro":
            self.active_power_duration = 4
            self.road_speed = self.base_speed + 5
            self.bonus_score += 50

        elif kind == "shield":
            self.active_power_duration = 9999
            self.shield_active = True
            self.bonus_score += 30

        elif kind == "repair":
            self.active_power = None
            self.active_power_duration = 0
            self.bonus_score += 25

            if self.obstacles:
                self.obstacles.pop(0)

    def update_active_power(self):
        if self.active_power == "nitro":
            elapsed = time.time() - self.active_power_start

            if elapsed >= self.active_power_duration:
                self.active_power = None
                self.road_speed = self.base_speed

        elif self.active_power == "shield":
            pass

    def consume_shield(self):
        self.shield_active = False
        self.active_power = None

    def get_power_remaining(self):
        if self.active_power == "nitro":
            remaining = self.active_power_duration - (time.time() - self.active_power_start)
            return max(0, int(remaining))
        if self.active_power == "shield":
            return "until hit"
        return ""

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.player.x -= self.player_move_speed

        if keys[pygame.K_RIGHT]:
            self.player.x += self.player_move_speed

        if self.player.left < ROAD_LEFT:
            self.player.left = ROAD_LEFT

        if self.player.right > ROAD_LEFT + ROAD_WIDTH:
            self.player.right = ROAD_LEFT + ROAD_WIDTH

        self.player_lane = max(0, min(LANE_COUNT - 1, (self.player.centerx - ROAD_LEFT) // LANE_WIDTH))

    def update_spawning(self):
        progress_factor = self.distance / 1500
        traffic_chance = self.difficulty["traffic_chance"] + progress_factor * 0.01
        obstacle_chance = self.difficulty["obstacle_chance"] + progress_factor * 0.008
        powerup_chance = self.difficulty["powerup_chance"]

        if random.random() < traffic_chance:
            self.spawn_traffic()

        if random.random() < obstacle_chance:
            self.spawn_obstacle()

        if random.random() < 0.025:
            self.spawn_coin()

        if random.random() < powerup_chance:
            self.spawn_powerup()

        if random.random() < 0.004:
            self.spawn_road_event()

    def update_objects(self):
        for car in self.traffic:
            car["rect"].y += car["speed"]

        for obstacle in self.obstacles:
            obstacle["rect"].y += self.road_speed

        for coin in self.coins:
            coin["rect"].y += self.road_speed

        for powerup in self.powerups:
            powerup["rect"].y += self.road_speed

        for event in self.road_events:
            event["rect"].y += self.road_speed

            if event["kind"] == "moving_barrier":
                event["rect"].x += event["direction"] * 2

                if event["rect"].left < ROAD_LEFT or event["rect"].right > ROAD_LEFT + ROAD_WIDTH:
                    event["direction"] *= -1

        self.traffic = [x for x in self.traffic if x["rect"].top < HEIGHT]
        self.obstacles = [x for x in self.obstacles if x["rect"].top < HEIGHT]
        self.coins = [x for x in self.coins if x["rect"].top < HEIGHT]
        self.road_events = [x for x in self.road_events if x["rect"].top < HEIGHT]

        now = time.time()
        self.powerups = [
            x for x in self.powerups
            if x["rect"].top < HEIGHT and now - x["spawn_time"] <= 6
        ]

    def check_collisions(self):
        for car in self.traffic[:]:
            if self.player.colliderect(car["rect"]):
                if self.shield_active:
                    self.consume_shield()
                    self.traffic.remove(car)
                else:
                    self.game_over = True

        for obstacle in self.obstacles[:]:
            if self.player.colliderect(obstacle["rect"]):
                kind = obstacle["kind"]

                if kind == "oil":
                    self.player_move_speed = 4
                    self.obstacles.remove(obstacle)

                elif kind == "speed_bump":
                    self.road_speed = max(2, self.road_speed - 2)
                    self.obstacles.remove(obstacle)

                else:
                    if self.shield_active:
                        self.consume_shield()
                        self.obstacles.remove(obstacle)
                    else:
                        self.game_over = True

        for event in self.road_events[:]:
            if self.player.colliderect(event["rect"]):
                if event["kind"] == "nitro_strip":
                    self.activate_powerup("nitro")
                    self.road_events.remove(event)

                elif event["kind"] == "moving_barrier":
                    if self.shield_active:
                        self.consume_shield()
                        self.road_events.remove(event)
                    else:
                        self.game_over = True

        for coin in self.coins[:]:
            if self.player.colliderect(coin["rect"]):
                self.coin_score += coin["value"] * 10
                self.coins_collected += coin["value"]
                self.coins.remove(coin)

                # Enemy and track speed increase after collecting coins
                if self.coins_collected % 10 == 0:
                    self.base_speed += 1
                    self.road_speed += 1

        for powerup in self.powerups[:]:
            if self.player.colliderect(powerup["rect"]):
                self.activate_powerup(powerup["kind"])
                self.powerups.remove(powerup)

    def update_score(self):
        self.score = self.coin_score + int(self.distance / 5) + self.bonus_score

    def update(self):
        self.handle_input()
        self.update_active_power()

        self.distance += self.road_speed

        if self.distance >= FINISH_DISTANCE:
            self.finished = True
            self.game_over = True

        self.player_move_speed = 7

        self.update_spawning()
        self.update_objects()
        self.check_collisions()
        self.update_score()

    def draw_road(self, screen):
        screen.fill((30, 140, 30))
        pygame.draw.rect(screen, ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

        for i in range(1, LANE_COUNT):
            x = ROAD_LEFT + i * LANE_WIDTH
            pygame.draw.line(screen, LINE, (x, 0), (x, HEIGHT), 2)

        pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
        pygame.draw.line(screen, WHITE, (ROAD_LEFT + ROAD_WIDTH, 0), (ROAD_LEFT + ROAD_WIDTH, HEIGHT), 4)

    def draw_hud(self, screen):
        remaining = max(0, FINISH_DISTANCE - int(self.distance))

        hud_lines = [
            f"Player: {self.username}",
            f"Score: {self.score}",
            f"Coins: {self.coins_collected}",
            f"Distance: {int(self.distance)}",
            f"Remaining: {remaining}",
            f"Power: {self.active_power or 'None'} {self.get_power_remaining()}"
        ]

        y = 10
        for line in hud_lines:
            text = self.font.render(line, True, BLACK)
            screen.blit(text, (10, y))
            y += 24

    def draw_objects(self, screen):
        car_color = CAR_COLORS.get(self.settings.get("car_color", "blue"), BLUE)
        pygame.draw.rect(screen, car_color, self.player, border_radius=5)
        pygame.draw.rect(screen, WHITE, (self.player.x + 10, self.player.y + 10, 25, 18))

        for car in self.traffic:
            pygame.draw.rect(screen, car["color"], car["rect"], border_radius=5)

        for obstacle in self.obstacles:
            rect = obstacle["rect"]
            kind = obstacle["kind"]

            if kind == "barrier":
                pygame.draw.rect(screen, DARK_RED, rect)
            elif kind == "oil":
                pygame.draw.ellipse(screen, OIL, rect)
            elif kind == "pothole":
                pygame.draw.ellipse(screen, BROWN, rect)
            elif kind == "speed_bump":
                pygame.draw.rect(screen, ORANGE, rect)

        for coin in self.coins:
            pygame.draw.circle(screen, coin["color"], coin["rect"].center, 12)

        for powerup in self.powerups:
            pygame.draw.rect(screen, powerup["color"], powerup["rect"], border_radius=6)

        for event in self.road_events:
            rect = event["rect"]
            if event["kind"] == "moving_barrier":
                pygame.draw.rect(screen, RED, rect)
            elif event["kind"] == "nitro_strip":
                pygame.draw.rect(screen, CYAN, rect)

    def draw(self, screen):
        self.draw_road(screen)
        self.draw_objects(screen)
        self.draw_hud(screen)