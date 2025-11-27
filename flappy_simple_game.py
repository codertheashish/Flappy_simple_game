import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 850, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Clean Play & Rain After Game Over")

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)
RED = (220, 20, 60)
CYAN = (0, 255, 255)

FUCHSIA = (255, 0, 255)

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 38, bold=True)
small_font = pygame.font.SysFont("Arial", 28)

# Bird physics
bird_x = 160
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.30
jump_power = -7

# Pipes
pipe_width = 90
pipe_gap = 320
pipe_speed = 1.7

pipes = []
score = 0

mini_birds = []

def create_rain_birds():
    global mini_birds
    mini_birds = []
    for _ in range(45):
        mini_birds.append([
            random.randint(0, WIDTH),
            random.randint(-HEIGHT, 0),
            random.randint(8, 16),
            random.uniform(0.6, 1.4)
        ])

def update_rain_birds():
    for b in mini_birds:
        b[1] += b[3]
        if b[1] > HEIGHT:
            b[0] = random.randint(0, WIDTH)
            b[1] = -10

def draw_mini_birds():
    for b in mini_birds:
        pygame.draw.ellipse(screen, YELLOW, (b[0], b[1], b[2], b[2] // 1.3))
        pygame.draw.circle(screen, BLACK, (b[0] + b[2]//2, b[1] + 2), 2)

def add_pipe():
    gap_y = random.randint(140, HEIGHT - 320)
    pipes.append([WIDTH, gap_y])

for _ in range(4):
    add_pipe()

def reset_game():
    global bird_y, bird_velocity, pipes, score, pipe_speed, pipe_gap
    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipes = []
    for _ in range(4):
        add_pipe()
    score = 0
    pipe_speed = 1.7
    pipe_gap = 320

def draw_bird(x, y):
    pygame.draw.ellipse(screen, YELLOW, (x - 26, y - 20, 52, 40))
    pygame.draw.circle(screen, WHITE, (x + 10, y - 4), 7)
    pygame.draw.circle(screen, BLACK, (x + 12, y - 4), 3)
    pygame.draw.polygon(screen, ORANGE, [(x + 28, y), (x + 42, y - 6), (x + 42, y + 6)])

def game_over_screen():
    create_rain_birds()
    while True:
        update_rain_birds()
        screen.fill(BLUE)
        draw_mini_birds()

        over = font.render("GAME OVER!", True, RED)
        score_text = font.render(f"Score: {score}", True, YELLOW)

        restart = small_font.render("Press R to Restart", True, FUCHSIA)
        exit_game = small_font.render("Press ESC to Exit", True, BLACK)

        screen.blit(over, (WIDTH//2 - over.get_width()//2, 220))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 270))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 330))
        screen.blit(exit_game, (WIDTH//2 - exit_game.get_width()//2, 370))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# =========================
#        MAIN LOOP
# =========================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_power
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    bird_velocity += gravity
    bird_y += bird_velocity

    for pipe in pipes:
        pipe[0] -= pipe_speed

    if pipes[0][0] < -pipe_width:
        pipes.pop(0)
        add_pipe()
        score += 1

        if score == 5:
            pipe_speed = 2.1
            pipe_gap = 280

    for pipe in pipes:
        pipe_x = pipe[0]
        gap_y = pipe[1]

        top_rect = pygame.Rect(pipe_x, 0, pipe_width, gap_y)
        bottom_rect = pygame.Rect(pipe_x, gap_y + pipe_gap, pipe_width, HEIGHT)

        if top_rect.collidepoint(bird_x, bird_y) or bottom_rect.collidepoint(bird_x, bird_y):
            game_over_screen()

    if bird_y <= 0 or bird_y >= HEIGHT:
        game_over_screen()

    screen.fill(BLUE)

    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe[0], 0, pipe_width, pipe[1]))
        pygame.draw.rect(screen, GREEN, (pipe[0], pipe[1] + pipe_gap, pipe_width, HEIGHT))

    draw_bird(bird_x, int(bird_y))

    score_display = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_display, (20, 20))

    pygame.display.update()
    clock.tick(60)
