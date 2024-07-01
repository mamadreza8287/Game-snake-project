import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Snake
snake_size = 20
snake_speed = 20
snake_color = random.choice(colors)
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'

# Food
food_color = (0, 255, 0)
food_pos = [random.randrange(1, (screen_width//snake_size)) * snake_size, random.randrange(1, (screen_height//snake_size)) * snake_size]

# Game variables
score = 0
font = pygame.font.SysFont(None, 40)

# Main game loop
game_over = False
clock = pygame.time.Clock()
start_game = False

# Border color
border_color = (100, 100, 100)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_game = True
            if event.key == pygame.K_ESCAPE:
                game_over = True

    if not start_game:
        screen.fill(white)
        start_font = font.render("Press SPACE to start the game", True, black)
        screen.blit(start_font, (screen_width//2 - 150, screen_height//2))
        pygame.display.update()
        continue

    # Game logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and direction != 'RIGHT':
        direction = 'LEFT'
    if keys[pygame.K_RIGHT] and direction != 'LEFT':
        direction = 'RIGHT'
    if keys[pygame.K_UP] and direction != 'DOWN':
        direction = 'UP'
    if keys[pygame.K_DOWN] and direction != 'UP':
        direction = 'DOWN'

    if direction == 'RIGHT':
        snake_pos[0] += snake_size
    if direction == 'LEFT':
        snake_pos[0] -= snake_size
    if direction == 'UP':
        snake_pos[1] -= snake_size
    if direction == 'DOWN':
        snake_pos[1] += snake_size

    # Snake grows by eating food
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        snake_color = random.choice(colors)
        food_pos = [random.randrange(1, (screen_width//snake_size)) * snake_size, random.randrange(1, (screen_height//snake_size)) * snake_size]
    else:
        snake_body.pop()

    # Wrap snake around the screen
    if snake_pos[0] >= screen_width:
        snake_pos[0] = 0
    if snake_pos[0] < 0:
        snake_pos[0] = screen_width - snake_size
    if snake_pos[1] >= screen_height:
        snake_pos[1] = 0
    if snake_pos[1] < 0:
        snake_pos[1] = screen_height - snake_size

    # Draw everything on the screen
    screen.fill(white)
    
    # Draw border with random color
    border_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    pygame.draw.rect(screen, border_color, (0, 0, screen_width, snake_size))
    pygame.draw.rect(screen, border_color, (0, 0, snake_size, screen_height))
    pygame.draw.rect(screen, border_color, (0, screen_height - snake_size, screen_width, snake_size))
    pygame.draw.rect(screen, border_color, (screen_width - snake_size, 0, snake_size, screen_height))
    
    for pos in snake_body:
        pygame.draw.rect(screen, snake_color, pygame.Rect(pos[0], pos[1], snake_size, snake_size))
    pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))

    # Display user's score
    score_font = font.render("Score: " + str(score), True, black)
    screen.blit(score_font, (10, 10))

    # Game over if snake hits itself
    if any(block == snake_pos for block in snake_body[1:]):
        game_over = True

    # Update the display
    pygame.display.update()

    # Frame rate
    clock.tick(10)

# Game over message
game_over_font = pygame.font.SysFont(None, 70)
game_over_text = game_over_font.render("GAME OVER!", True, black)
game_over_rect = game_over_text.get_rect(center=(screen_width//2, screen_height//2))
screen.blit(game_over_text, game_over_rect)
pygame.display.flip()

pygame.quit()