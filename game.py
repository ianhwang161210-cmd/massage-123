import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_SKY = (135, 206, 235)
GREEN_GRASS = (34, 139, 34)
RED = (255, 0, 0)
SKIN_TONE = (255, 219, 172)
GOLD = (255, 215, 0)
DARK_GRAY = (68, 68, 68)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
LESOTHO_BLUE = (0, 82, 204)
DARK_GREEN = (0, 122, 94)
LIME_GREEN = (50, 205, 50)

class LesothoFlagBullet:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.width = 8
        self.height = 6
        self.lifetime = 300  # frames
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # gravity
        self.lifetime -= 1
        
    def is_alive(self):
        return self.lifetime > 0 and 0 <= self.x < SCREEN_WIDTH and 0 <= self.y < SCREEN_HEIGHT
        
    def draw(self, screen):
        if not self.is_alive():
            return
            
        stripe_height = self.height / 3
        
        # White stripe
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, stripe_height))
        
        # Blue stripe
        pygame.draw.rect(screen, LESOTHO_BLUE, (self.x, self.y + stripe_height, self.width, stripe_height))
        
        # Green stripe
        pygame.draw.rect(screen, DARK_GREEN, (self.x, self.y + stripe_height * 2, self.width, stripe_height))
        
        # Border
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 1)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class PlayerBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 10
        self.width = 5
        self.height = 10
        
    def update(self):
        self.x += self.vx
        
    def is_alive(self):
        return self.x < SCREEN_WIDTH
        
    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Orb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.health = 1
        self.shoot_timer = random.randint(30, 80)
        self.bullets = []
        
    def update(self):
        self.shoot_timer -= 1
        
        # Shoot Lesotho flags
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = random.randint(30, 80)
            
        # Update bullets
        self.bullets = [b for b in self.bullets if b.is_alive()]
        for bullet in self.bullets:
            bullet.update()
            
    def shoot(self):
        # Shoot in random directions
        angle = random.uniform(0, 2 * math.pi)
        speed = 3
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        bullet = LesothoFlagBullet(self.x, self.y, vx, vy)
        self.bullets.append(bullet)
        
    def draw(self, screen):
        # Draw orb
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y)), self.radius, 3)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)
            
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        
    def get_flag_bullets(self):
        return self.bullets

class MarioFinal:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2 - 50
        self.width = 40
        self.height = 60
        self.health = 5
        self.max_health = 5
        self.attack_timer = 0
        self.attack_cooldown = 120  # frames between attacks
        self.lightning_bolts = []
        self.visible = False
        self.entrance_timer = 0
        
    def enter_screen(self):
        self.visible = True
        self.entrance_timer = 60
        self.x = SCREEN_WIDTH / 2
        self.y = -100
        
    def update(self):
        if not self.visible:
            return
            
        # Entrance animation
        if self.entrance_timer > 0:
            self.entrance_timer -= 1
            self.y += 2
        
        # Attack
        self.attack_timer -= 1
        if self.attack_timer <= 0 and self.visible and self.entrance_timer <= 0:
            self.attack()
            self.attack_timer = self.attack_cooldown
            
        # Update lightning
        self.lightning_bolts = [b for b in self.lightning_bolts if b['lifetime'] > 0]
        for bolt in self.lightning_bolts:
            bolt['lifetime'] -= 1
            
    def attack(self):
        # Create lightning bolts from Mario
        num_bolts = random.randint(2, 4)
        for _ in range(num_bolts):
            angle = random.uniform(0, 2 * math.pi)
            bolt = {
                'angle': angle,
                'distance': 0,
                'lifetime': 30
            }
            self.lightning_bolts.append(bolt)
            
    def draw(self, screen):
        if not self.visible:
            return
            
        # Mario body (red)
        pygame.draw.rect(screen, RED, (self.x - 10, self.y + 15, 20, 25))
        
        # Mario head (skin tone)
        pygame.draw.circle(screen, SKIN_TONE, (int(self.x), int(self.y + 10)), 12)
        
        # Eyes (very wide and creepy)
        pygame.draw.circle(screen, WHITE, (int(self.x - 5), int(self.y + 8)), 4)
        pygame.draw.circle(screen, WHITE, (int(self.x + 5), int(self.y + 8)), 4)
        pygame.draw.circle(screen, BLACK, (int(self.x - 5), int(self.y + 8)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x + 5), int(self.y + 8)), 2)
        
        # Hat (red)
        pygame.draw.polygon(screen, (204, 0, 0), [
            (self.x - 15, self.y + 2),
            (self.x + 15, self.y + 2),
            (self.x + 12, self.y - 5),
            (self.x - 12, self.y - 5)
        ])
        
        # Pants (blue)
        pygame.draw.rect(screen, (0, 0, 255), (self.x - 8, self.y + 40, 16, 8))
        
        # Health bar
        bar_width = 80
        bar_height = 10
        bar_x = self.x - bar_width / 2
        bar_y = self.y - 40
        
        # Background
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, LIME_GREEN, (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw lightning
        for bolt in self.lightning_bolts:
            self._draw_lightning(screen, bolt)
            
    def _draw_lightning(self, screen, bolt):
        # Draw lightning bolt
        angle = bolt['angle']
        num_segments = 20
        max_distance = 400
        
        prev_x = self.x
        prev_y = self.y + 30
        
        for i in range(num_segments):
            t = i / num_segments
            distance = t * max_distance * (bolt['lifetime'] / 30)
            
            x = self.x + math.cos(angle) * distance
            y = self.y + 30 + math.sin(angle) * distance
            
            # Add zigzag
            zigzag = math.sin(i * 0.5) * 10
            x += zigzag
            
            pygame.draw.line(screen, CYAN, (int(prev_x), int(prev_y)), (int(x), int(y)), 3)
            prev_x = x
            prev_y = y
            
    def get_rect(self):
        return pygame.Rect(self.x - 20, self.y - 20, 40, 80)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("🎮 ORB SHOOTER - MARIO BOSS BATTLE 🎮")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.reset_game()
        
    def reset_game(self):
        self.player_x = SCREEN_WIDTH / 2
        self.player_y = SCREEN_HEIGHT - 50
        self.player_width = 30
        self.player_height = 40
        self.player_speed = 6
        
        self.orbs = []
        self.player_bullets = []
        self.score = 0
        self.game_time = 0
        self.game_running = True
        self.mario_arrived = False
        self.mario = MarioFinal()
        
        # Spawn initial orbs
        self.spawn_orbs()
        
    def spawn_orbs(self, count=3):
        for _ in range(count):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(80, 250)
            self.orbs.append(Orb(x, y))
                
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.shoot()
                if event.key == pygame.K_r and not self.game_running:
                    self.reset_game()
        return True
        
    def shoot(self):
        bullet = PlayerBullet(self.player_x + self.player_width / 2, self.player_y)
        self.player_bullets.append(bullet)
        
    def update(self):
        keys = pygame.key.get_pressed()
        
        # Player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x = max(0, self.player_x - self.player_speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x = min(SCREEN_WIDTH - self.player_width, self.player_x + self.player_speed)
            
        # Update game time
        self.game_time += 1
        
        # Mario boss appears at 60 seconds (3600 frames)
        if self.game_time == 3600 and not self.mario_arrived:
            self.mario_arrived = True
            self.mario.enter_screen()
            
        # Update orbs
        for orb in self.orbs:
            orb.update()
            
        # Update player bullets
        self.player_bullets = [b for b in self.player_bullets if b.is_alive()]
        for bullet in self.player_bullets:
            bullet.update()
            
        # Update Mario
        self.mario.update()
        
        # Check bullet-orb collisions
        for orb in self.orbs[:]:
            for bullet in self.player_bullets[:]:
                if bullet.get_rect().colliderect(orb.get_rect()):
                    orb.health -= 1
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    if orb.health <= 0:
                        self.orbs.remove(orb)
                        self.score += 100
                        # Spawn replacement orb
                        if self.mario_arrived or random.random() > 0.3:
                            self.spawn_orbs(1)
                    break
                    
        # Check bullet-Mario collisions
        if self.mario_arrived:
            for bullet in self.player_bullets[:]:
                if bullet.get_rect().colliderect(self.mario.get_rect()):
                    self.mario.health -= 1
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    if self.mario.health <= 0:
                        self.game_running = False
                    break
                    
        # Check flag bullet-player collisions
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        
        for orb in self.orbs:
            for flag_bullet in orb.get_flag_bullets():
                if flag_bullet.get_rect().colliderect(player_rect):
                    self.game_running = False
                    break
                    
        # Check Mario lightning-player collisions
        for bolt in self.mario.lightning_bolts:
            # Simple distance check for lightning
            bolt_x = self.mario.x + math.cos(bolt['angle']) * 300
            bolt_y = self.mario.y + 30 + math.sin(bolt['angle']) * 300
            
            distance = math.sqrt((self.player_x - bolt_x) ** 2 + (self.player_y - bolt_y) ** 2)
            if distance < 30:
                self.game_running = False
        
    def draw(self):
        # Sky
        self.screen.fill(BLUE_SKY)
        
        # Ground
        pygame.draw.rect(self.screen, GREEN_GRASS, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        
        # Draw orbs and their bullets
        for orb in self.orbs:
            orb.draw(self.screen)
            
        # Draw player
        pygame.draw.rect(self.screen, (50, 150, 255), (self.player_x, self.player_y, self.player_width, self.player_height))
        pygame.draw.polygon(self.screen, (100, 200, 255), [
            (self.player_x + self.player_width / 2 - 8, self.player_y),
            (self.player_x + self.player_width / 2 + 8, self.player_y),
            (self.player_x + self.player_width / 2, self.player_y - 10)
        ])
        
        # Draw player bullets
        for bullet in self.player_bullets:
            bullet.draw(self.screen)
            
        # Draw Mario
        if self.mario_arrived:
            self.mario.draw(self.screen)
            
        # Draw Mario's chanting text (creepy hashtags)
        if self.mario_arrived and self.mario.entrance_timer <= 0:
            chant_text = "##################################"
            font = pygame.font.Font(None, 16)
            chant_surface = font.render(chant_text, True, BLACK)
            self.screen.blit(chant_surface, (self.mario.x - 100, self.mario.y - 60))
            
        # HUD
        score_text = self.font_medium.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # Timer
        seconds = self.game_time / 60
        timer_text = self.font_medium.render(f"Time: {seconds:.1f}s", True, BLACK)
        self.screen.blit(timer_text, (SCREEN_WIDTH - 250, 10))
        
        # Boss timer
        if not self.mario_arrived:
            boss_time = max(0, 60 - seconds)
            boss_text = self.font_small.render(f"Boss arrives in: {boss_time:.1f}s", True, RED)
            self.screen.blit(boss_text, (SCREEN_WIDTH / 2 - 120, 10))
        else:
            boss_text = self.font_medium.render("MARIO BOSS!", True, RED)
            self.screen.blit(boss_text, (SCREEN_WIDTH / 2 - 100, 10))
        
        # Game over screen
        if not self.game_running:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            if self.mario.health <= 0:
                game_over_text = self.font_large.render("YOU WON!", True, GOLD)
                msg = "Mario has been defeated!"
            else:
                game_over_text = self.font_large.render("GAME OVER!", True, RED)
                msg = "You were hit!"
                
            msg_text = self.font_small.render(msg, True, WHITE)
            score_text = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font_small.render("Press R to restart", True, WHITE)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 100))
            self.screen.blit(msg_text, (SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 - 20))
            self.screen.blit(score_text, (SCREEN_WIDTH / 2 - 130, SCREEN_HEIGHT / 2 + 30))
            self.screen.blit(restart_text, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 90))
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
