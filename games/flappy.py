import pygame
import random
import os
from random import randint, choice

# Paths
game_dir = os.path.abspath(os.getcwd())
backgrounds_path = os.path.join(game_dir, '../graphics/backgrounds')
pipe_path = os.path.join(game_dir, '../graphics/flappyBird/pipes')
bird_path = os.path.join(game_dir, '../graphics/flappyBird/flying')
font_path = os.path.join(game_dir, '../font')

# Dimensions
width = 800
height = 400
ground = 330
screen = pygame.display.set_mode((width, height))
score = 0


class Obstacle:
    def __init__(self, pipe):
        pipe_up = pygame.image.load(os.path.join(pipe_path, 'pipe_up.png')).convert_alpha()
        pipe_down = pygame.image.load(os.path.join(pipe_path, 'pipe_down.png')).convert_alpha()
        self.rect = []
        self.image = []
        if pipe == 'up':
            pipe_up = pygame.transform.scale(pipe_up, (80, randint(150, 200)))
            self.image.append(pipe_up)
            self.rect.append(self.image[0].get_rect(midbottom=(randint(900, 1100), ground)))
        elif pipe == 'down':
            pipe_down = pygame.transform.scale(pipe_down, (80, randint(150, 200)))
            self.image.append(pipe_down)
            self.rect.append(self.image[0].get_rect(midtop=(randint(900, 1100), 0)))
        else:
            p_height = randint(20, 200)
            pipe_up = pygame.transform.scale(pipe_up, (80, p_height))
            pipe_down = pygame.transform.scale(pipe_down, (80, 200-p_height))
            self.image = [pipe_up, pipe_down]
            x_pos = random.randint(900, 1100)
            self.rect.append(pipe_up.get_rect(midbottom=(x_pos, ground)))
            self.rect.append(pipe_down.get_rect(midtop=(x_pos, 0)))

    def transform(self):
        pass

    def draw(self):
        for (s, r) in zip(self.image, self.rect):
            screen.blit(s, r)

    def update(self):
        for r in self.rect:
            r.x -= 5

    def get_rect(self):
        return self.rect

    def get_x_pos(self):
        return self.rect[0].x


class Bird:
    def __init__(self):
        bird_1 = pygame.image.load(os.path.join(bird_path, 'frame-1.png')).convert_alpha()
        bird_2 = pygame.image.load(os.path.join(bird_path, 'frame-2.png')).convert_alpha()
        bird_3 = pygame.image.load(os.path.join(bird_path, 'frame-3.png')).convert_alpha()
        bird_4 = pygame.image.load(os.path.join(bird_path, 'frame-4.png')).convert_alpha()
        bird_5 = pygame.image.load(os.path.join(bird_path, 'frame-5.png')).convert_alpha()
        bird_6 = pygame.image.load(os.path.join(bird_path, 'frame-6.png')).convert_alpha()
        bird_7 = pygame.image.load(os.path.join(bird_path, 'frame-7.png')).convert_alpha()
        bird_8 = pygame.image.load(os.path.join(bird_path, 'frame-8.png')).convert_alpha()
        self.birdLst = [bird_1, bird_2, bird_3, bird_4, bird_5, bird_6, bird_7, bird_8]
        for i, b in enumerate(self.birdLst):
            self.birdLst[i] = pygame.transform.rotozoom(b, 0, 0.05)
        self.birdIdx = 0

        self.image = self.birdLst[self.birdIdx]
        self.rect = self.image.get_rect(midbottom=(300, 150))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -3
        else:
            self.gravity = 3

    def apply_gravity(self):
        self.rect.y += self.gravity
        if self.rect.y < 0:
            self.rect.y = 0

    def bird_animation(self):
        self.birdIdx += 0.2
        if self.birdIdx >= len(self.birdLst):
            self.birdIdx = 0
        self.image = self.birdLst[int(self.birdIdx)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.bird_animation()

    def draw(self):
        screen.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect

    def get_y_pos(self):
        return self.rect.y

    def set(self):
        self.rect.y = 150

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


pygame.init()
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
font = pygame.font.Font(os.path.join(font_path, 'Pixeltype.ttf'), 50)
# font = pygame.font.Font('../font/Pixeltype.ttf', 50)
game_active = False
start_time = 0

# Backgrounds
sky_surface = pygame.image.load(os.path.join(backgrounds_path, 'Sky.png')).convert_alpha()
sky_surface = pygame.transform.scale(sky_surface, (width, ground))
ground_surface = pygame.image.load(os.path.join(backgrounds_path, 'ground.png')).convert_alpha()

# Intro screen
game_name = font.render('Flappy Bird', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = font.render('Press Enter to play', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 340))

bird_stand = pygame.image.load(os.path.join(bird_path, 'frame-8.png')).convert_alpha()
bird_stand = pygame.transform.rotozoom(bird_stand, 0, 0.2)
bird_stand_rect = bird_stand.get_rect(center=(400, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

# Bird and Pipes
bird = Bird()
obstacle_list = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                print('Add 1 pipe')
                obstacle_list.append((Obstacle(choice(['up', 'down', 'both', 'both', 'both']))))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Press esc to quit game,
                # should clear obstacle_list
                game_active = False
                obstacle_list.clear()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                obstacle_list.clear()
                game_active = True
                bird.set()
                start_time = int(pygame.time.get_ticks() / 1000)
    if game_active:
        # Draw backgrounds
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, ground))

        # Display score
        score = display_score()

        # Draw bird
        bird.draw()
        bird.update()
        if bird.get_y_pos() > ground:
            game_active = False

        # Draw pipe
        for obstacle in obstacle_list:
            obstacle.draw()
            obstacle.update()
            for r in obstacle.get_rect():
                if bird.get_rect().colliderect(r):
                    game_active = False
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.get_x_pos() >= -100]
        # print(bird.get_y_pos())
    else:
        screen.fill((94, 129, 162))
        screen.blit(bird_stand, bird_stand_rect)
        score_message = font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            # obstacle_list.clear()
            screen.blit(score_message, score_message_rect)
    pygame.display.update()
    clock.tick(60)
