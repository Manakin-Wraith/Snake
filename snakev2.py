import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 640
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")

# Set up colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
colors = [RED, ORANGE, PURPLE, WHITE]

# Set up game variables
cell_size = 20
snake_speed = 5
info_area_height = 40

# Define Snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.positions = [(window_width // 2, window_height // 2)]
        self.direction = "RIGHT"
        self.color = GREEN

    def move(self):
        x, y = self.positions[0]
        if self.direction == "UP":
            y -= cell_size
        elif self.direction == "DOWN":
            y += cell_size
        elif self.direction == "LEFT":
            x -= cell_size
        elif self.direction == "RIGHT":
            x += cell_size
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.size:
            self.positions.pop()

    def change_direction(self, new_direction):
        if (new_direction == "UP" and self.direction != "DOWN" or
                new_direction == "DOWN" and self.direction != "UP" or
                new_direction == "LEFT" and self.direction != "RIGHT" or
                new_direction == "RIGHT" and self.direction != "LEFT"):
            self.direction = new_direction

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(window, self.color, (position[0], position[1], cell_size, cell_size))

    def check_collision(self):
        head = self.positions[0]
        if (head[0] < 0 or head[0] >= window_width or
                head[1] < 0 or head[1] >= window_height or
                head in self.positions[1:]):
            return True
        return False

    def check_food_collision(self, food):
     if self.positions[0] == food.position:
        self.size += food.blocks
        eaten_food_position = food.position  # Store the food position before generating a new one
        eaten_food_color = food.color  # Store the food color
        food.generate_position()
        # Return the food position, color along with the collision status
        return True, eaten_food_position, eaten_food_color  
     return False, None, None

# Define Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.blocks = 1
        self.generate_position()

    def generate_position(self):
        x = random.randint(0, (window_width - cell_size) // cell_size) * cell_size
        y = random.randint(0, (window_height - cell_size) // cell_size) * cell_size
        self.position = (x, y)
        self.color = random.choice([RED, ORANGE, PURPLE, WHITE])
        if self.color == ORANGE:
            self.blocks = 2
        elif self.color == PURPLE:
            self.blocks = 3
        elif self.color == WHITE:
            self.blocks = 5

    def draw(self):
        pygame.draw.rect(window, self.color, (self.position[0], self.position[1], cell_size, cell_size))


snake = Snake()
food = Food()
game_bg_color = random.choice(colors)

clock = pygame.time.Clock()

running = False
game_over = False
restart_game = False
paused = False

food_count = 0
font = pygame.font.Font(None, 24)
eaten_food_position = None

while not restart_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            restart_game = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not running and not game_over:
                    snake = Snake()
                    food = Food()
                    running = True
                elif game_over:
                    game_over = False
                    food_count = 0
            elif event.key == pygame.K_p:
                paused = not paused

        if running and not paused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
        
    if running and not paused:
        snake.move()
        window.fill(BLACK)

        if snake.check_collision():
            running = False
            game_over = True
            game_bg_color = random.choice(colors)

              # Check for food collision
        food_collision, new_eaten_food_position, eaten_food_color = snake.check_food_collision(food)
        if food_collision:
            food_count += 1
            eaten_food_position = new_eaten_food_position  # Update the eaten food position
            eaten_food_color = eaten_food_color

        snake.draw()

        if eaten_food_position is not None and eaten_food_color is not None:
            yummy_font = pygame.font.Font(None, 36)
            yummy_text = yummy_font.render("Yummy!", True, eaten_food_color)
            window.blit(yummy_text, eaten_food_position)

        food.draw()

        
        food_count_text = font.render("Food Count: " + str(food_count), True, WHITE)
        window.blit(food_count_text, (10, window_height - info_area_height + 10))

        pygame.display.update()
        clock.tick(snake_speed)
        
    if not running and not game_over:
        window.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACEBAR to start the game", True, WHITE)
        text_rect = text.get_rect(center=(window_width // 2, window_height // 2 - 50))
        window.blit(text, text_rect)
        pygame.display.flip()

    if game_over:
        window.fill(BLACK)
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2 - 50))
        window.blit(game_over_text, game_over_rect)

        food_count_text = font.render("Food Count: " + str(food_count), True, WHITE)
        food_count_rect = food_count_text.get_rect(center=(window_width // 2, window_height // 2 + 50))
        window.blit(food_count_text, food_count_rect)

        restart_text = font.render("Press SPACEBAR to start again", True, WHITE)
        restart_rect = restart_text.get_rect(center=(window_width // 2, window_height // 2 + 100))
        window.blit(restart_text, restart_rect)

        pygame.display.flip()

    if paused:
        font = pygame.font.Font(None, 36)
        pause_text = font.render("Game Paused", True, WHITE)
        pause_rect = pause_text.get_rect(center=(window_width // 2, window_height // 2))
        window.blit(pause_text, pause_rect)

        pygame.display.flip()

# Quit the game
pygame.quit()
