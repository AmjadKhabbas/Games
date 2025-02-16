import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Reaction Game")

# Set up font
font = pygame.font.Font(None, 74)

# Game variables
words = ["LEFT", "RIGHT", "UP", "DOWN"]
directions = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
current_word = random.choice(words)
current_direction = directions[words.index(current_word)]
score = 0
speed = 1.0
game_over = False

# Main game loop
while not game_over:
    screen.fill(BLACK)
    text = font.render(current_word, True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    start_time = time.time()
    key_pressed = False

    while time.time() - start_time < speed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == current_direction:
                    score += 1
                    speed *= 0.9
                    key_pressed = True
                    break
                else:
                    game_over = True
                    break
        if key_pressed:
            break

    if not key_pressed:
        game_over = True

    current_word = random.choice(words)
    current_direction = directions[words.index(current_word)]

# Display final score
screen.fill(BLACK)
text = font.render(f"Game Over! Score: {score}", True, WHITE)
screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
