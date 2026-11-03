import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

BLUE = (135, 206, 250)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 36)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.radius = 15
        self.gravity = 0.5
        self.movement = 0
        
        try:
            self.image = pygame.image.load(r'C:\Users\ASUS\OneDrive\Pictures\flappy.png').convert_alpha()
            self.image.set_colorkey((255, 255, 255)) 
            self.image = pygame.transform.scale(self.image, (40, 30))
        except:
            self.image = None

    def update(self):
        self.movement += self.gravity
        self.y += self.movement

    def jump(self):
        self.movement = 0
        self.movement -= 8

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x - 20, int(self.y) - 15))
        else:
            pygame.draw.circle(surface, (255, 215, 0), (self.x, int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
class PipeManager:
    def __init__(self):
        self.pipe_width = 60
        self.pipe_gap = 150
        self.pipe_speed = 3
        self.pipes = []
        self.spawn_timer = 0

    def update_and_spawn(self):     
        self.spawn_timer += 1
        if self.spawn_timer > 90:  
            gap_y = random.randint(150, 450)
            top_pipe = pygame.Rect(SCREEN_WIDTH, 0, self.pipe_width, gap_y - (self.pipe_gap // 2))
            bottom_pipe = pygame.Rect(SCREEN_WIDTH, gap_y + (self.pipe_gap // 2), self.pipe_width, SCREEN_HEIGHT - (gap_y + (self.pipe_gap // 2)))
            self.pipes.extend([top_pipe, bottom_pipe])
            self.spawn_timer = 0

        for pipe in self.pipes:
            pipe.x -= self.pipe_speed

        self.pipes = [pipe for pipe in self.pipes if pipe.right > -150]

    def draw(self, surface):
        for pipe in self.pipes:
            pygame.draw.rect(surface, GREEN, pipe)

    def check_collision(self, bird_rect):
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe):
                return True
        return False

    def reset(self):
        self.pipes.clear()
        self.spawn_timer = 0

bird = Bird()
pipe_manager = PipeManager()
score = 0
game_active = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird.jump()
                else:
                    bird = Bird()
                    pipe_manager.reset()
                    score = 0
                    game_active = True

    if game_active:
        bird.update()
        pipe_manager.update_and_spawn()

        if pipe_manager.check_collision(bird.get_rect()) or bird.y <= 0 or bird.y >= SCREEN_HEIGHT:
            game_active = False

        score += 1

    screen.fill(BLUE) 

    pipe_manager.draw(screen)
    bird.draw(screen)

    score_surface = font.render(f"Skor: {score // 10}", True, BLACK)
    screen.blit(score_surface, (10, 10))

    if not game_active:
        game_over_surface = font.render("GAME OVER - Tekan Spasi untuk Main Lagi", True, BLACK)
        screen.blit(game_over_surface, (40, 280))

    pygame.display.update()
    clock.tick(60)