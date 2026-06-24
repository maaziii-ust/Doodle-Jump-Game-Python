import pygame
import random
import sys

pygame.init()

# ---------------- WINDOW ----------------
WIDTH = 400
HEIGHT = 600
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

clock = pygame.time.Clock()
FPS = 60

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
GREEN = (0, 200, 100)
BLUE = (0, 120, 255)
RED = (255, 0, 0)

# ---------------- PLAYER ----------------
player_width = 40
player_height = 40
player_vel_y = 0
gravity = 0.5
jump_power = -12
player_speed = 5

# ---------------- PLATFORMS ----------------
platform_width = 70
platform_height = 10
platforms = []

for i in range(7):
    x = random.randint(0, WIDTH - platform_width)
    y = HEIGHT - i * 80
    platforms.append(pygame.Rect(x, y, platform_width, platform_height))

player_x = platforms[0].x + (platform_width - player_width) // 2
player_y = platforms[0].y - player_height

player_vel_y = jump_power

# ---------------- SCORE ----------------
score = 0
font = pygame.font.SysFont(None, 36)

# ---------------- DRAW ----------------
def draw_window():
    gameWindow.fill(WHITE)

    # Player
    pygame.draw.rect(gameWindow, BLUE, (player_x, player_y, player_width, player_height))

    # Platforms
    for platform in platforms:
        pygame.draw.rect(gameWindow, GREEN, platform)

    # Score
    score_text = font.render("Score: " + str(score), True, RED)
    gameWindow.blit(score_text, (10, 10))

    pygame.display.update()

# ---------------- MAIN LOOP ----------------
game_over = True
while game_over:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                pygame.quit()

                # Restart game
                game_over = True
                continue

                sys.exit()
        
    keys = pygame.key.get_pressed()

    # Player movement
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Screen wrap
    if player_x > WIDTH:
        player_x = -player_width
    if player_x < -player_width:
        player_x = WIDTH

    # Gravity
    player_vel_y += gravity
    player_y += player_vel_y

    # Platform collision
    for platform in platforms:
        if (
            player_vel_y > 0
            and pygame.Rect(player_x, player_y, player_width, player_height).colliderect(platform)
        ):
            player_vel_y = jump_power

    # Scroll screen
    if player_y < HEIGHT // 3:
        diff = HEIGHT // 3 - player_y
        player_y = HEIGHT // 3
        score += diff

        for platform in platforms:
            platform.y += diff
            if platform.y > HEIGHT:
                platform.y = 0
                platform.x = random.randint(0, WIDTH - platform_width)

    # Game over
    if player_y > HEIGHT:
        game_over = False

    draw_window()

# ---------------- GAME OVER ----------------
while True:

    gameWindow.fill(WHITE)

    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, BLUE)
    restart_text = font.render("Press ENTER to Restart", True, (0, 0, 0))

    gameWindow.blit(
        game_over_text,
        (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80)
    )

    gameWindow.blit(
        score_text,
        (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20)
    )

    gameWindow.blit(
        restart_text,
        (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 30)
    )

    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                pygame.quit()

                # Restart game
                import subprocess
                subprocess.Popen([sys.executable, __file__])

                sys.exit()

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
