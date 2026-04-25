import pygame
import random
from db import get_personal_best

WIDTH, HEIGHT = 600, 600
CELL = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
FOOD_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0)]
POISON_COLOR = (120, 0, 0)
OBSTACLE_COLOR = (100, 100, 100)
POWER_SPEED = (0, 200, 255)
POWER_SLOW = (180, 0, 255)
POWER_SHIELD = (0, 255, 255)


class SnakeGame:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings

        self.snake = [(300, 300), (280, 300), (260, 300)]
        self.direction = (CELL, 0)
        self.next_direction = (CELL, 0)

        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.base_speed = 8
        self.speed = self.base_speed

        self.food = None
        self.food_value = 1
        self.food_color = FOOD_COLORS[0]
        self.food_spawn_time = 0
        self.food_lifetime = 6000

        self.poison = None
        self.poison_spawn_time = 0

        self.powerup = None
        self.powerup_type = None
        self.powerup_spawn_time = 0

        self.active_power = None
        self.active_power_start = 0
        self.active_power_duration = 5000
        self.shield = False

        self.obstacles = []

        self.game_over = False
        self.personal_best = get_personal_best(username)

        self.spawn_food()
        self.spawn_poison()

    def random_cell(self):
        return (
            random.randrange(0, WIDTH, CELL),
            random.randrange(0, HEIGHT, CELL)
        )

    def is_free_cell(self, pos):
        return (
            pos not in self.snake and
            pos not in self.obstacles and
            pos != self.food and
            pos != self.poison and
            pos != self.powerup
        )

    def get_free_cell(self):
        while True:
            pos = self.random_cell()
            if self.is_free_cell(pos):
                return pos

    def spawn_food(self):
        self.food = self.get_free_cell()
        self.food_value = random.choice([1, 2, 5])

        if self.food_value == 1:
            self.food_color = FOOD_COLORS[0]
        elif self.food_value == 2:
            self.food_color = FOOD_COLORS[1]
        else:
            self.food_color = FOOD_COLORS[2]

        self.food_spawn_time = pygame.time.get_ticks()

    def spawn_poison(self):
        self.poison = self.get_free_cell()
        self.poison_spawn_time = pygame.time.get_ticks()

    def spawn_powerup(self):
        if self.powerup is not None:
            return

        self.powerup = self.get_free_cell()
        self.powerup_type = random.choice(["speed", "slow", "shield"])
        self.powerup_spawn_time = pygame.time.get_ticks()

    def generate_obstacles(self):
        if self.level < 3:
            return

        self.obstacles = []
        head = self.snake[0]

        count = min(5 + self.level, 15)

        while len(self.obstacles) < count:
            pos = self.random_cell()

            # Do not trap snake near current head
            distance = abs(pos[0] - head[0]) + abs(pos[1] - head[1])

            if distance < CELL * 4:
                continue

            if self.is_free_cell(pos):
                self.obstacles.append(pos)

    def set_direction(self, new_direction):
        dx, dy = new_direction
        cur_dx, cur_dy = self.direction

        if (dx, dy) != (-cur_dx, -cur_dy):
            self.next_direction = new_direction

    def apply_powerup(self):
        now = pygame.time.get_ticks()

        if self.powerup_type == "speed":
            self.active_power = "speed"
            self.active_power_start = now
            self.speed = self.base_speed + 5

        elif self.powerup_type == "slow":
            self.active_power = "slow"
            self.active_power_start = now
            self.speed = max(4, self.base_speed - 4)

        elif self.powerup_type == "shield":
            self.active_power = "shield"
            self.shield = True

        self.powerup = None
        self.powerup_type = None

    def update_powerup_timer(self):
        now = pygame.time.get_ticks()

        # Field power-up disappears after 8 seconds
        if self.powerup and now - self.powerup_spawn_time > 8000:
            self.powerup = None
            self.powerup_type = None

        # Active timed powers last 5 seconds
        if self.active_power in ["speed", "slow"]:
            if now - self.active_power_start > self.active_power_duration:
                self.active_power = None
                self.speed = self.base_speed

    def collision_with_death(self, head):
        wall_collision = (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT
        )

        self_collision = head in self.snake
        obstacle_collision = head in self.obstacles

        if wall_collision or self_collision or obstacle_collision:
            if self.shield:
                self.shield = False
                self.active_power = None

                # If shield hits wall, keep snake inside
                fixed_x = min(max(head[0], 0), WIDTH - CELL)
                fixed_y = min(max(head[1], 0), HEIGHT - CELL)
                self.snake[0] = (fixed_x, fixed_y)
                return False

            return True

        return False

    def update(self):
        now = pygame.time.get_ticks()

        self.update_powerup_timer()

        # Food disappears after timer
        if now - self.food_spawn_time > self.food_lifetime:
            self.spawn_food()

        # Poison respawns sometimes
        if self.poison is None or now - self.poison_spawn_time > 10000:
            self.spawn_poison()

        # Spawn power-up sometimes
        if self.powerup is None and random.random() < 0.01:
            self.spawn_powerup()

        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if self.collision_with_death(new_head):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += self.food_value * 10
            self.food_eaten += 1
            self.spawn_food()

            if self.food_eaten % 4 == 0:
                self.level += 1
                self.base_speed += 1
                self.speed = self.base_speed
                self.generate_obstacles()

        elif new_head == self.poison:
            # Poison shortens snake by 2
            if len(self.snake) <= 3:
                self.game_over = True
                return

            self.snake.pop()
            self.snake.pop()
            self.poison = None

        elif new_head == self.powerup:
            self.apply_powerup()
            self.snake.pop()

        else:
            self.snake.pop()

    def draw_grid(self, screen):
        if not self.settings.get("grid", True):
            return

        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, (35, 35, 35), (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, (35, 35, 35), (0, y), (WIDTH, y))

    def draw(self, screen, font):
        screen.fill(BLACK)
        self.draw_grid(screen)

        snake_color = tuple(self.settings.get("snake_color", [0, 255, 0]))

        for part in self.snake:
            pygame.draw.rect(screen, snake_color, (*part, CELL, CELL))

        pygame.draw.rect(screen, self.food_color, (*self.food, CELL, CELL))

        if self.poison:
            pygame.draw.rect(screen, POISON_COLOR, (*self.poison, CELL, CELL))

        if self.powerup:
            if self.powerup_type == "speed":
                color = POWER_SPEED
            elif self.powerup_type == "slow":
                color = POWER_SLOW
            else:
                color = POWER_SHIELD

            pygame.draw.rect(screen, color, (*self.powerup, CELL, CELL))

        for block in self.obstacles:
            pygame.draw.rect(screen, OBSTACLE_COLOR, (*block, CELL, CELL))

        hud = [
            f"Player: {self.username}",
            f"Score: {self.score}",
            f"Level: {self.level}",
            f"Best: {self.personal_best}",
            f"Power: {self.active_power or 'None'}"
        ]

        y = 10
        for line in hud:
            text = font.render(line, True, WHITE)
            screen.blit(text, (10, y))
            y += 25