import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Baby blue colors
BABY_BLUE = (173, 216, 230)
DARK_BLUE = (0, 102, 204)
RED = (255, 0, 0)
GREEN = (0, 170, 0)
SKIN_TONE = (255, 219, 172)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SPACE ADVENTURE - Mario & Luigi Below!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Player (you!)
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_w = 40
player_h = 40
player_speed = 5

# Mario at bottom
mario_x = SCREEN_WIDTH // 3
mario_y = SCREEN_HEIGHT - 80
mario_w = 30
mario_h = 40

# Luigi at bottom
luigi_x = (SCREEN_WIDTH * 2) // 3
luigi_y = SCREEN_HEIGHT - 80
luigi_w = 30
luigi_h = 40

# Lasers from Mario and Luigi
lasers = []
laser_timer = 0

# Score/Lives
lives = 3
score = 0
game_running = True

def draw_mario(x, y, width, height):
    # Body
    pygame.draw.rect(screen, RED, (x, y + 15, width, 15))
    # Head
    pygame.draw.circle(screen, SKIN_TONE, (int(x + width // 2), int(y + 8)), 7)
    # Eyes
    pygame.draw.circle(screen, WHITE, (int(x + 5), int(y + 6)), 2)
    pygame.draw.circle(screen, WHITE, (int(x + width - 5), int(y + 6)), 2)
    pygame.draw.circle(screen, BLACK, (int(x + 5), int(y + 6)), 1)
    pygame.draw.circle(screen, BLACK, (int(x + width - 5), int(y + 6)), 1)
    # Hat
    pygame.draw.rect(screen, (200, 0, 0), (x - 2, y - 3, width + 4, 6))

def draw_luigi(x, y, width, height):
    # Body
    pygame.draw.rect(screen, GREEN, (x, y + 15, width, 15))
    # Head
    pygame.draw.circle(screen, SKIN_TONE, (int(x + width // 2), int(y + 8)), 7)
    # Eyes
    pygame.draw.circle(screen, WHITE, (int(x + 5), int(y + 6)), 2)
    pygame.draw.circle(screen, WHITE, (int(x + width - 5), int(y + 6)), 2)
    pygame.draw.circle(screen, BLACK, (int(x + 5), int(y + 6)), 1)
    pygame.draw.circle(screen, BLACK, (int(x + width - 5), int(y + 6)), 1)
    # Hat
    pygame.draw.rect(screen, (0, 100, 0), (x - 2, y - 3, width + 4, 6))

# Game loop
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
    
    keys = pygame.key.get_pressed()
    
    # Player movement
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x = max(0, player_x - player_speed)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x = min(SCREEN_WIDTH - player_w, player_x + player_speed)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y = max(0, player_y - player_speed)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y = min(SCREEN_HEIGHT - player_h, player_y + player_speed)
    
    # Mario and Luigi shoot lasers
    laser_timer += 1
    if laser_timer > 30:
        # Mario shoots
        lasers.append({
            'x': mario_x + mario_w // 2,
            'y': mario_y,
            'vx': random.uniform(-2, 2),
            'vy': -5
        })
        # Luigi shoots
        lasers.append({
            'x': luigi_x + luigi_w // 2,
            'y': luigi_y,
            'vx': random.uniform(-2, 2),
            'vy': -5
        })
        laser_timer = 0
    
    # Update lasers
    lasers = [l for l in lasers if l['y'] > 0]
    for laser in lasers:
        laser['x'] += laser['vx']
        laser['y'] += laser['vy']
    
    # Check laser-player collisions
    player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
    for laser in lasers[:]:
        laser_rect = pygame.Rect(laser['x'] - 3, laser['y'] - 3, 6, 6)
        if player_rect.colliderect(laser_rect):
            lives -= 1
            lasers.remove(laser)
            if lives <= 0:
                game_running = False
            else:
                # Reset player position
                player_x = SCREEN_WIDTH // 2
                player_y = SCREEN_HEIGHT // 2
            break
    
    # Score increases over time
    score += 1
    
    # Draw everything
    screen.fill(BABY_BLUE)
    
    # Draw stars
    random.seed(1)  # Same seed for consistent stars
    for _ in range(30):
        sx = random.randint(0, SCREEN_WIDTH)
        sy = random.randint(0, SCREEN_HEIGHT - 100)
        pygame.draw.circle(screen, WHITE, (sx, sy), 1)
    
    # Draw player (spaceship)
    pygame.draw.polygon(screen, YELLOW, [
        (player_x + player_w // 2, player_y),
        (player_x, player_y + player_h),
        (player_x + player_w // 2, player_y + player_h - 10),
        (player_x + player_w, player_y + player_h)
    ])
    
    # Draw lasers
    for laser in lasers:
        pygame.draw.circle(screen, YELLOW, (int(laser['x']), int(laser['y'])), 4)
    
    # Draw ground area
    pygame.draw.rect(screen, DARK_BLUE, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
    
    # Draw Mario
    draw_mario(mario_x, mario_y, mario_w, mario_h)
    
    # Draw Luigi
    draw_luigi(luigi_x, luigi_y, luigi_w, luigi_h)
    
    # Draw text
    lives_text = font.render(f"Lives: {lives}", True, RED)
    score_text = font.render(f"Score: {score // 60}", True, BLACK)
    screen.blit(lives_text, (10, 10))
    screen.blit(score_text, (SCREEN_WIDTH - 200, 10))
    
    # Draw instructions
    instructions = small_font.render("WASD/ARROWS = Move | Avoid Mario & Luigi lasers!", True, BLACK)
    screen.blit(instructions, (10, SCREEN_HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(FPS)

# Game over screen
screen.fill(BABY_BLUE)
if lives <= 0:
    game_over_text = font.render("GAME OVER!", True, RED)
    msg = small_font.render(f"Final Score: {score // 60}", True, BLACK)
else:
    game_over_text = font.render("YOU SURVIVED!", True, GREEN)
    msg = small_font.render(f"Final Score: {score // 60}", True, BLACK)

screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 40))
screen.blit(msg, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20))
pygame.display.flip()

pygame.time.wait(2000)
pygame.quit()
