import pygame
import sys
import random
import os
from random import randint, choice

# Paths
game_dir = os.path.abspath(os.getcwd())
backgrounds_path = os.path.join(game_dir, '../graphics/backgrounds')
pipe_path = os.path.join(game_dir, '../graphics/flappyBird/pipes')
bird_path = os.path.join(game_dir, '../graphics/flappyBird/flying')
font_path = os.path.join(game_dir, '../font')

# Dimension, fps, name, background information
FPS = 60
WINWIDTH = 800
WINHEIGHT = 400
GROUND = 330
GAMENAME = 'Flappy Bird'
BACKGROUND_COLOR = (94, 129, 162)


class Obstacle:
    def __init__(self, pipe):
        pipe_up = pygame.image.load(os.path.join(pipe_path, 'pipe_up.png')).convert_alpha()
        pipe_down = pygame.image.load(os.path.join(pipe_path, 'pipe_down.png')).convert_alpha()
        self.rect = []
        self.image = []
        if pipe == 'up':
            pipe_up = pygame.transform.scale(pipe_up, (80, randint(150, 200)))
            self.image.append(pipe_up)
            self.rect.append(self.image[0].get_rect(midbottom=(randint(900, 1100), GROUND)))
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
            self.rect.append(pipe_up.get_rect(midbottom=(x_pos, GROUND)))
            self.rect.append(pipe_down.get_rect(midtop=(x_pos, 0)))

    def transform(self):
        pass

    def draw(self):
        for (s, r) in zip(self.image, self.rect):
            DISPLAYSURF.blit(s, r)

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
        DISPLAYSURF.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect

    def get_y_pos(self):
        return self.rect.y

    def set(self):
        self.rect.y = 150


def main():
    global TEXTFONT, DISPLAYSURF, STARTTIME, SCORE

    # Pygame initialization and basic set up of the global variables.
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    TEXTFONT = pygame.font.Font(os.path.join(font_path, 'Pixeltype.ttf'), 50)
    STARTTIME = 0
    SCORE = 0

    pygame.display.set_caption(GAMENAME)
    clock = pygame.time.Clock()
    game_active = False

    # Backgrounds
    sky_surface, ground_surface = create_background()

    # Intro screen
    game_name = TEXTFONT.render(GAMENAME, False, (111, 196, 169))
    game_name_rect = game_name.get_rect(center=(400, 80))

    game_message = TEXTFONT.render('Press Enter to play', False, (111, 196, 169))
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
                terminate()
            if game_active:
                if event.type == obstacle_timer:
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
                    STARTTIME = int(pygame.time.get_ticks() / 1000)
        if game_active:
            # Draw backgrounds
            DISPLAYSURF.blit(sky_surface, (0, 0))
            DISPLAYSURF.blit(ground_surface, (0, GROUND))

            # Display score
            SCORE = display_score()

            # Draw bird
            bird.draw()
            bird.update()
            if bird.get_y_pos() > GROUND:
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
            DISPLAYSURF.fill(BACKGROUND_COLOR)
            DISPLAYSURF.blit(bird_stand, bird_stand_rect)
            score_message = TEXTFONT.render(f'Your score: {SCORE}', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 330))
            DISPLAYSURF.blit(game_name, game_name_rect)

            if SCORE == 0:
                DISPLAYSURF.blit(game_message, game_message_rect)
            else:
                DISPLAYSURF.blit(score_message, score_message_rect)
        pygame.display.update()
        clock.tick(FPS)


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - STARTTIME
    score_surf = TEXTFONT.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    DISPLAYSURF.blit(score_surf, score_rect)
    return current_time


def terminate():
    pygame.quit()
    sys.exit()


def create_background():
    sky_surface = pygame.image.load(os.path.join(backgrounds_path, 'Sky.png')).convert_alpha()
    sky_surface = pygame.transform.scale(sky_surface, (WINWIDTH, GROUND))
    ground_surface = pygame.image.load(os.path.join(backgrounds_path, 'ground.png')).convert_alpha()
    return sky_surface, ground_surface


if __name__ == '__main__':
    main()