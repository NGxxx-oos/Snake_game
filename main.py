import pygame
import random
import time


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and \
           (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new_x = cur[0] + (x * GRID_SIZE)
        new_y = cur[1] + (y * GRID_SIZE)

        
        if not (0 <= new_x < SCREEN_WIDTH and 0 <= new_y < SCREEN_HEIGHT):
            return False 

        new_position = (new_x, new_y)

        
        if len(self.positions) > 2 and new_position in self.positions[1:]:
            return False 

        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True 

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def eat(self):
        self.length += 1
        self.score += 10

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

    def handle_keys(self, key):
        if key == pygame.K_UP:
            self.turn(UP)
        elif key == pygame.K_DOWN:
            self.turn(DOWN)
        elif key == pygame.K_LEFT:
            self.turn(LEFT)
        elif key == pygame.K_RIGHT:
            self.turn(RIGHT)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Змейка")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.snake = Snake()
        self.food = Food()
        self.font = pygame.font.SysFont("monospace", 24)
        self.big_font = pygame.font.SysFont("monospace", 48, bold=True)
        self.clock = pygame.time.Clock()
        self.high_score = 0
        self.game_over = False
        self.paused = False

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    self.paused = not self.paused
                elif self.game_over and event.key == pygame.K_r: 
                    self.reset_game()
                elif not self.game_over and not self.paused:
                    self.snake.handle_keys(event.key)
        return True

    def _update_game_state(self):
        if self.game_over or self.paused:
            return

        if not self.snake.move(): 
            self.game_over = True
            return

        if self.snake.get_head_position() == self.food.position:
            self.snake.eat()
            self.food.randomize_position()
            if self.snake.score > self.high_score:
                self.high_score = self.snake.score

    def _draw_elements(self):
        self.surface.fill(BLACK)
        self.snake.draw(self.surface)
        self.food.draw(self.surface)

        score_text = self.font.render(f"Счет: {self.snake.score}  Рекорд: {self.high_score}", 1, WHITE)
        self.surface.blit(score_text, (5, 5))

        if self.paused:
            pause_text = self.big_font.render("Пауза", 1, WHITE)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.surface.blit(pause_text, text_rect)

        if self.game_over:
            game_over_text = self.big_font.render("Хана! Нажми 'R' Заново", 1, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.surface.blit(game_over_text, text_rect)

        self.screen.blit(self.surface, (0, 0))
        pygame.display.update()

    def reset_game(self):
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
        self.paused = False

    def run(self):
        running = True
        while running:
            self.clock.tick(10 + self.snake.length) 
            running = self._handle_input()
            self._update_game_state()
            self._draw_elements()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
