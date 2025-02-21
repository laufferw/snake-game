import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 252)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)

# Food types and their properties
FOOD_TYPES = {
    'regular': {'color': RED, 'points': 10, 'weight': 70},
    'special': {'color': GOLD, 'points': 25, 'weight': 20},
    'bonus': {'color': PURPLE, 'points': 50, 'weight': 10, 'duration': 5000}  # Duration in milliseconds
}

# Base speed and speed increment
BASE_FPS = 8
FPS_INCREMENT = 2
POINTS_PER_LEVEL = 50

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.score = 0
        self.level = 1
        self.game_over = False
        self.level_complete = False
        self.food = self.spawn_food()
        self.food_type = 'regular'
        self.food_spawn_time = pygame.time.get_ticks()

    def get_food_type(self):
        weights = [FOOD_TYPES[t]['weight'] for t in FOOD_TYPES.keys()]
        food_type = random.choices(list(FOOD_TYPES.keys()), weights=weights)[0]
        return food_type

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if food not in self.snake:
                self.food_type = self.get_food_type()
                self.food_spawn_time = pygame.time.get_ticks()
                return food

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                elif self.level_complete:
                    if event.key == pygame.K_SPACE:
                        self.level_complete = False
                else:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.direction = (1, 0)
        return True
    
    def show_level_complete(self):
        font = pygame.font.Font(None, 48)
        level_complete_text = font.render(f'Level {self.level} Complete!', True, WHITE)
        press_space_text = font.render('Press SPACE to continue', True, WHITE)
        
        level_rect = level_complete_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 30))
        space_rect = press_space_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 30))
        
        self.screen.blit(level_complete_text, level_rect)
        self.screen.blit(press_space_text, space_rect)

    def update(self):
        if self.game_over:
            return

        # Move snake
        new_head = (
            (self.snake[0][0] + self.direction[0]) % GRID_WIDTH,
            (self.snake[0][1] + self.direction[1]) % GRID_HEIGHT
        )

        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check if bonus food should disappear
        if self.food_type == 'bonus' and \
           pygame.time.get_ticks() - self.food_spawn_time > FOOD_TYPES['bonus']['duration']:
            self.food = self.spawn_food()

        # Check if food is eaten
        if new_head == self.food:
            points = FOOD_TYPES[self.food_type]['points']
            self.score += points
            
            # Update level
            old_level = self.level
            new_level = (self.score // POINTS_PER_LEVEL) + 1
            if new_level > self.level:
                self.level = new_level
                self.level_complete = True
            
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw border
        pygame.draw.rect(self.screen, BLUE, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 5)

        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN,
                        (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                        GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw food
        food_color = FOOD_TYPES[self.food_type]['color']
        pygame.draw.rect(self.screen, food_color,
                    (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE,
                    GRID_SIZE - 2, GRID_SIZE - 2))

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        level_text = font.render(f'Level: {self.level}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))

        if self.game_over:
            game_over_text = font.render('Game Over! Press SPACE to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
            self.screen.blit(game_over_text, text_rect)
        elif self.level_complete:
            self.show_level_complete()

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            current_fps = BASE_FPS + (self.level - 1) * FPS_INCREMENT
            self.clock.tick(current_fps)

if __name__ == '__main__':
    game = SnakeGame()
    game.run()
    pygame.quit()
    sys.exit()

