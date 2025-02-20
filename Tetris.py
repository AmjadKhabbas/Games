import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

# Shape colors
SHAPE_COLORS = [CYAN, YELLOW, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_shape = self.get_new_shape()
        self.next_shape = self.get_new_shape()
        self.game_over = False
        self.score = 0

    def get_new_shape(self):
        shape = random.choice(SHAPES)
        color = SHAPE_COLORS[SHAPES.index(shape) % len(SHAPE_COLORS)]
        return {'shape': shape, 'color': color, 'x': SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2, 'y': 0}

    def draw_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                pygame.draw.rect(self.screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_shape(self, shape):
        for y, row in enumerate(shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, shape['color'], ((shape['x'] + x) * BLOCK_SIZE, (shape['y'] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    def move_shape(self, dx, dy):
        self.current_shape['x'] += dx
        self.current_shape['y'] += dy
        if self.check_collision():
            self.current_shape['x'] -= dx
            self.current_shape['y'] -= dy
            return False
        return True

    def rotate_shape(self):
        shape = self.current_shape['shape']
        rotated_shape = [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]
        original_x = self.current_shape['x']
        self.current_shape['x'] = max(0, min(self.current_shape['x'], SCREEN_WIDTH // BLOCK_SIZE - len(rotated_shape[0])))
        self.current_shape['shape'] = rotated_shape
        if self.check_collision():
            self.current_shape['shape'] = shape
            self.current_shape['x'] = original_x

    def check_collision(self):
        for y, row in enumerate(self.current_shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    if (self.current_shape['y'] + y >= len(self.grid) or
                        self.current_shape['x'] + x < 0 or
                        self.current_shape['x'] + x >= len(self.grid[0]) or
                        self.grid[self.current_shape['y'] + y][self.current_shape['x'] + x] != BLACK):
                        return True
        return False

    def lock_shape(self):
        for y, row in enumerate(self.current_shape['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_shape['y'] + y][self.current_shape['x'] + x] = self.current_shape['color']
        self.clear_lines()
        self.current_shape = self.next_shape
        self.next_shape = self.get_new_shape()
        if self.check_collision():
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        for y in range(len(self.grid) - 1, -1, -1):
            if all(cell != BLACK for cell in self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [BLACK for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])
                lines_cleared += 1
        self.score += lines_cleared ** 2

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_shape(self.current_shape)
            self.draw_shape(self.next_shape)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_shape(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move_shape(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move_shape(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_shape()

            if not self.move_shape(0, 1):
                self.lock_shape()

            self.clock.tick(10)

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
