
import pygame
import random
import os
import math

#from pygame.sprite import _Group
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED  = (255,   0,   0)
GREEN = (0, 255, 0)
PURPLE = (255, 0, 255)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

cwd = os.getcwd()

DIR = cwd + "\midia"
DIR_PLAYER = DIR + "\player16x16"

PLAYER_X0 = 20
PLAYER_Y0 = SCREEN_HEIGHT - 80

FPS = 60

# class SpriteSheet(object):
#     """ Class used to grab images out of a sprite sheet. """ 
 
#     def __init__(self, file_name):
#         """ Constructor. Pass in the file name of the sprite sheet. """
 
#         # Load the sprite sheet.
#         self.sprite_sheet = pygame.image.load(file_name).convert()
 
 
#     def get_image(self, x, y, width, height):
#         """ Grab a single image out of a larger spritesheet
#             Pass in the x, y location of the sprite
#             and the width and height of the sprite. """
 
#         # Create a new blank image
#         image = pygame.Surface([width, height]).convert()
 
#         # Copy the sprite from the large sheet onto the smaller image
#         image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
#         # Assuming black works as the transparent color
#         image.set_colorkey(BLACK)
 
#         # Return the image
#         return image
    
    

class Player(pygame.sprite.Sprite):
    
    
    def __init__(self, x , y, death_sound, pickup_sound):
            
        super().__init__()
        
        self.idle = pygame.image.load(DIR_PLAYER + "\player-idle\sprite_0.png").convert_alpha()
        self.idle = pygame.transform.scale(self.idle, (48, 48))
        
        self.walk0 = pygame.image.load(DIR_PLAYER + "\player-walk\sprite_0.png").convert_alpha()
        self.walk0 = pygame.transform.scale(self.walk0, (48, 48))
        self.walk1 = pygame.image.load(DIR_PLAYER + "\player-walk\sprite_1.png").convert_alpha()
        self.walk1 = pygame.transform.scale(self.walk1, (48, 48))
        
        self.walk = [self.walk0, self.walk1]
        
        self.image = self.idle
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
            
        self.change_x = 0
        self.change_y = 0
        
        self.index = 0
        
        self.death_count = 0
        
        self.score = 0
        
        self.death_sound = death_sound
        
    
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y
    
    def update(self , walls, enemies, goals):
        # updating position
        #up and down
        self.rect.x += self.change_x
        
        # enemy_hit_list = pygame.sprite.spritecollide(self, enemies, False)
        # if len(enemy_hit_list) > 0: # morte :(
        #     self.rect.x = PLAYER_X0
        #     self.rect.y = PLAYER_Y0
        #     self.death_sound.play()
        #     self.death_count += 1
        for enemy in enemies:
            
            if pygame.sprite.collide_rect_ratio(0.6)(self, enemy):
                self.rect.x = PLAYER_X0
                self.rect.y = PLAYER_Y0
                self.death_sound.play()
                self.death_count += 1
            
            
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in wall_hit_list:
            if self.change_x > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right
        
        goal_hit_list = pygame.sprite.spritecollide(self, goals, True)
        for goal in goal_hit_list:
            self.score += 1
            pickup_sound.play()
            
            
        # left and right
        self.rect.y += self.change_y
        
        
        # enemy_hit_list = pygame.sprite.spritecollide(self, enemies, False)
        # if len(enemy_hit_list) > 0: # morte :(
        #     self.rect.x = PLAYER_X0
        #     self.rect.y = PLAYER_Y0
        #     self.death_sound.play()
        #     self.death_count += 1
        for enemy in enemies:
            
            if pygame.sprite.collide_rect_ratio(0.6)(self, enemy):
                self.rect.x = PLAYER_X0
                self.rect.y = PLAYER_Y0
                self.death_sound.play()
                self.death_count += 1
            
        
        wall_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for wall in wall_hit_list:
            if self.change_y > 0:
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom
        
        goal_hit_list = pygame.sprite.spritecollide(self, goals, True)
        for goal in goal_hit_list:
            self.score += 1
            pickup_sound.play()
        
        
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top < 0:
            self.rect.top = 0
        
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
        # updating image
        if self.change_x != 0 or self.change_y != 0:
            self.image = self.walk[int(self.index)]
        else:
            self.image = self.idle
        
        # updating index
        if self.index < len(self.walk) - 1:
            self.index += 0.05
        else:
            self.index = 0
        
        
        
        # add collision detection here !!

class Wall(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, color):
        super().__init__()
        
        
        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        
class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, x, y, change_x, change_y, size, period = 1, type = 1):
        super().__init__()
        self.type = type
        
        if self.type == 1:
            self.image = pygame.image.load(DIR + "\shuriken3.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (size, size))
        elif self.type == 2:
            self.image = pygame.image.load(DIR + "\police.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (size, size))
        elif self.type == 3:
            self.image = pygame.image.load(DIR + "\enemy3.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (size, size))
            
        self.image.set_colorkey(WHITE)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.change_x = change_x
        self.change_y = change_y
        
        self.period = period
        
        
        
        if self.type == 2:
            self.change_x0 = change_x
            self.change_y0 = change_y
            self.parado = False
            self.i = 0
            
        if self.type == 3:
            self.change_x0 = change_x
            self.change_y0 = change_y
            
            self.change_y = 0
            self.index_x = 0
            self.index_y = 0
            
        

    
    def change_speed(self, frames):
        if self.type == 1:
            if frames % (int(self.period * FPS)) == 0:
                self.change_x = -self.change_x
                self.change_y = -self.change_y
                
        elif self.type == 2:
            if frames % (int(self.period * FPS)) == 0:
                if not self.parado:
                    self.change_x = 0
                    self.change_y = 0
                    self.parado = not self.parado
                    
                else:
                    self.parado = not self.parado
                    self.i += 1
                    if self.i % 2 == 0:
                        self.change_x = self.change_x0
                        self.change_y = self.change_y0
                    else:
                        self.change_x = -self.change_x0
                        self.change_y = -self.change_y0
                        
        elif self.type == 3:
            if frames % (int(self.period * FPS)) == 0:
                if self.change_x != 0:
                    self.change_x = 0
                    
                    self.index_y += 1
                    if self.index_y % 2 == 0: 
                        self.change_y = self.change_y0
                    else:
                        self.change_y = -self.change_y0
                        
                    
                elif self.change_y != 0:
                    self.change_x = self.change_x0
                    self.change_y = 0
                    
                    self.index_x += 1
                    if self.index_x % 2 == 0: 
                        self.change_x = self.change_x0
                    else:
                        self.change_x = -self.change_x0
                    
                    
            
            
    
    # def para_retoma(self, frames):
    #     if self.pode_parar:
    #         if frames % (int(self.period_parado * FPS)) == 0:
    #             if self.parado:
    #                 self.change_x = self.change_x0
    #                 self.change_y = self.change_y0
    #                 self.parado = not self.parado
    #             else:
    #                 self.change_x = 0
    #                 self.change_y = 0
    #                 self.parado = not self.parado
                    
            
    
    def update(self):
        if self.type == 1 or self.type == 2 or self.type == 3:
            self.rect.x += self.change_x
            self.rect.y += self.change_y
            
        
            
        
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top < 0:
            self.rect.top = 0
        
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(DIR + "\weed.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(WHITE)
        
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Image(pygame.sprite.Sprite):
    
    def __init__(self, x, y, image, size_x, size_y):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
        
        
        
        
# LEVELS ------------------------------------------
class Level(object):
    """ Base class for all rooms. """
 
    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None
    goal_list = None

    def __init__(self):
        """ Constructor, create our lists. """
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.goal_list = pygame.sprite.Group()
        self.text = None

class Level1(Level):
    def __init__(self, goals = 1):
        super().__init__()
        
        self.goals = goals
        # (self, x, y, width, height, color) paredes
        walls = [ [0, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 100, 50, BLUE],
                  [100, SCREEN_HEIGHT - 400, SCREEN_WIDTH-100 , 50, BLUE],
                  [100, 100, 50, SCREEN_HEIGHT - 500, BLUE],
                  [250, 0, 50, 200, BLUE],
                  [250, 270, 50, 160, BLUE],
                  
                  [400, 100, 50, SCREEN_HEIGHT - 500, BLUE],
            
        ]
        
        # (self, x, y, change_x, change_y, size, period = 1) inimigos. change_x e change_y são invertem !
        enemies = [ [100, SCREEN_HEIGHT- 75, -10, 0, 60, 1],
                    [SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150, 5, 0, 60, 2],
                    [SCREEN_WIDTH - 60, SCREEN_HEIGHT - 350, 0, 0, 60, 1], # Parado de cima
                    [0, SCREEN_HEIGHT - 265, 0, 0, 60, 1], # Parado debaixo
                    
                    [SCREEN_WIDTH - 150, SCREEN_HEIGHT - 250, 4, 0, 50, 3], #vai pra esquerda e direita de cima
                    [100, SCREEN_HEIGHT - 350, -4, 0, 50, 3], #vai pra esquerda e direita debaixo
                    
                    [SCREEN_WIDTH - 150, SCREEN_HEIGHT - 250, 2, 2, 50, 0.8], # diagonal
                    [SCREEN_WIDTH - 450, SCREEN_HEIGHT - 250, -2, 2, 50, 0.8], # diagonal 2
                    
                    [SCREEN_WIDTH - 700, SCREEN_HEIGHT - 250, 0, 2, 50, 0.8], # sobe e desce
                    
                    [0, 60, -2, 0, 30, 1.6], #esquerda e direita superior
                    
                    [310, 0, 0, -2, 30, 3],
                    [210, 0, 0, -2, 30, 3],
                    
                    [370, 0, 0, -6, 30, 1],
                    [150, 0, 0, -6, 30, 1],
                    
                    #ultima parte
                    [SCREEN_WIDTH - 50, 0, 3, -3, 50, 1.8],
                    [SCREEN_WIDTH - 50, 350, 3, 3, 50, 1.8],
                    [SCREEN_WIDTH - 100, 150, 2, 0, 100, 3.8],
                    
                    [SCREEN_WIDTH / 2 - 40, 0, -3, 0, 75, 2.5],
                    [SCREEN_WIDTH / 2 - 40, 320, -4, 0, 75, 1.875],
                    
                    
                    
                    
            
        ]
        
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
            
        for item in enemies:
            enemy = Enemy(item[0], item[1], item[2], item[3], item[4], item[5])
            self.enemy_sprites.add(enemy)
        
        goal = Goal(SCREEN_WIDTH - 50, 175)
        # goal = Goal(PLAYER_X0, PLAYER_Y0)
        self.goal_list.add(goal)    
        
        self.text = font.render("Use as setas para se mover. Pegue a cannabis", True, BLACK)
        
class Level2(Level):
    def __init__(self, goals = 1):
        super().__init__()
        self.goals = goals
        walls = [
            # (self, x, y, width, height, color) paredes
            #corredor vertical
            [330, 100, 20, SCREEN_HEIGHT-100, RED],
            [430, 0, 20, SCREEN_HEIGHT/2 - 50, RED],
            [430, SCREEN_HEIGHT/2 + 50, 20, SCREEN_HEIGHT/2 - 50, RED],
            #corredor horizontal
            [450, SCREEN_HEIGHT/2 + 50, 480, 20, RED],
            [450, SCREEN_HEIGHT/2 - 70, 480, 20, RED], #parede de cima
            #blocos
            [520, 540, 70, 70, RED],
            [670, 540, 70, 70, RED],
            [820, 540, 110, 70, RED],
            
            [520, 680, 70, 60, RED],
            [670, 680, 70, 60, RED],
            [820, 680, 110, 60, RED],
            
            #superior esquerdo
            [450, 120, 96, 120, RED],
            [642, 120, 96, 120, RED],
            [834, 120, 96, 120, RED],
            
            
        ]
        
        enemies = [
            # (self, x, y, change_x, change_y, size, period = 1, type = 1):
            # fantasmas iniciais
            [150, SCREEN_HEIGHT-50, 0, -5, 50, 1.5, 2],
            [150, 0, 0, 6, 50, 1.7, 2],
            
            [250, SCREEN_HEIGHT-50, 0, -6, 50, 1.3, 2],
            [250, 0, 0, 7, 50, 1.1, 2],
            
            [0, 0, 6, 0, 50, 1, 2],
            
            #serras inicial
            [0, 0, 0, 4 , 75, 2.5, 1],
            [0, 150, 3, 0 , 50, 1.6, 1],
            [0, 450, 2, 0 , 70, 1.9, 1],
            
            #corredores
            [370, 0, 0, 3, 50, 3, 2],
            [370, SCREEN_HEIGHT/2-40, 3, 0, 40, 3, 1],
            [SCREEN_WIDTH-40, SCREEN_HEIGHT/2, -3, 0, 40, 3, 1],
            
            #fantasmas na extrema direita
            [SCREEN_WIDTH-60, 0, 0, 3, 60, 1.7, 2],
            [SCREEN_WIDTH-60, SCREEN_HEIGHT-60, 0, -3, 60, 1.7, 2],
            
            #canto superior direito
            [SCREEN_WIDTH-80, 20, -3, 0, 80, 2, 2],
            [460, 250, 4, 0, 80, 1.5, 2],
            [SCREEN_WIDTH-240, 0, 0, 3, 60, 1.5, 2],
            
            #canto inf direito
            [SCREEN_WIDTH-250, 480, 0, 3, 60, 1.4, 2],
            [SCREEN_WIDTH-400, SCREEN_HEIGHT-60, 0, -3, 60, 1.4, 2],
            [SCREEN_WIDTH-480, SCREEN_HEIGHT-60, 3, 0, 50, 2, 1],
            [SCREEN_WIDTH-480, SCREEN_HEIGHT-180, 3, 0, 50, 2, 2],
            [SCREEN_WIDTH-550, SCREEN_HEIGHT-320, 3, 0, 50, 1.5, 1], #serra superior
            
            
        ]
        
        goals = [
            [SCREEN_WIDTH / 2 - 25, 25],
            [SCREEN_WIDTH / 2 - 35, SCREEN_HEIGHT - 55],
            # [PLAYER_X0, PLAYER_Y0],
            # [PLAYER_X0, PLAYER_Y0],
            
            
        ]
        for item in goals:
            goal = Goal(item[0], item[1])
            self.goal_list.add(goal)
            
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
            
        for item in enemies:
            enemy = Enemy(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
            self.enemy_sprites.add(enemy)
        
        self.text = font.render("Precisamos de mais cannabis!", True, BLACK)

class Level3(Level):
    def __init__(self, goals = 1):
        super().__init__()
        self.goals = goals
        
        walls = [ 
            # (self, x, y, width, height, color) paredes
            [SCREEN_WIDTH/2-25, 100, 50, SCREEN_HEIGHT-100, PURPLE],
            
        ]
        
        enemies = [
            # (self, x, y, change_x, change_y, size, period = 1, type = 1):
            # blocos iniciais
            [340, 100 ,-5, -5, 50, 0.8, 3], # bloco canto sup esq
            [200,200, 0, 0, 100, 1, 3],
            
            [200,SCREEN_HEIGHT-100, 0, 0, 100, 1, 3],
            
            [100, 400 ,10, -10, 50, 0.4, 3], 
            [200,500, 0, 0, 100, 1, 3],
            
            #serras
            [0, 600, 0, -8, 75, 1, 1],
            [400, 600, 0, -6, 75, 1.5, 1],
            
            #fantasmas
            [0, 350, 5, 0, 75, 1.3, 2],
            [0,0, 5, 0, 75, 1.5, 1],
            
            #segunda metade
            [SCREEN_WIDTH/2, 0, 5, 0, 75, 1.3, 2],
            
            # 6 blocos
            [600, 320, 5, 4, 60, 1, 3],
            [SCREEN_WIDTH-100, 320, -5, 4, 60, 1, 3],
            
            [600, 520, 6, 5, 60, 0.8, 3],
            [SCREEN_WIDTH-100, 520, -6, 5, 60, 0.8, 3],
            
            [650, 620, 5, 5, 60, 0.6, 3],
            [SCREEN_WIDTH-150, 620, -5, 5, 60, 0.6, 3],
            
            [650, 770, 7, 5, 60, 0.5, 3],
            [SCREEN_WIDTH-150, 770, -7, 5, 60, 0.5, 3],
            
            
            
            [SCREEN_WIDTH/2+40, 0, 0, 6, 75, 2, 1],
            [SCREEN_WIDTH-75, SCREEN_HEIGHT-75, 0, -6, 75, 2, 1],
            
            
            [SCREEN_WIDTH-75, SCREEN_HEIGHT-75, -4, 0, 75, 1.6, 2]
            
            
            
            
            

        ]
        
        goals = [
            
            [SCREEN_WIDTH-50, SCREEN_HEIGHT-50],
        #    [PLAYER_X0, PLAYER_Y0 -150],
            
        ]
        
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
        
        for item in goals:
            goal = Goal(item[0], item[1])
            self.goal_list.add(goal)
        
            
        for item in enemies:
            enemy = Enemy(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
            self.enemy_sprites.add(enemy)
        
        self.text = font.render("Apenas mais uma para Epifania!", True, BLACK)
    
    
class Level4(Level):
    def __init__(self, goals = 1):
        super().__init__()
        self.goals = goals
        
        self.text = font.render("Parabens!!! Obrigado por jogar.", True, BLACK)
    

# def vitoria(screen):
#     # images = pygame.sprite.Group()
#     # asuna = Image(0, 0, DIR + "\\asuna.png")
#     # images.add(asuna)
    
#     # mashiro = Image(SCREEN_WIDTH - 200, 0, DIR + "\mashiro.png")
#     # images.add(mashiro)
    
#     # cake = Image(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100, DIR + "\cake.png")
#     # images.add(cake)
    
#     # images.draw(screen)
    
#     asuna = pygame.image.load(DIR + "\\asuna.jpg").convert_alpha()
    
#     screen.blit(asuna, [0, 0])
    
    
    
    
    
    
    
    # print("vitoria")
    # screen.fill(WHITE)
    # text = font.render("VOCÊ GANHOU!", True, BLACK)
    # screen.blit(text, [SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100])
    # pygame.display.flip()
    # pygame.time.wait(6000)
    # pygame.quit()

# initializing the game
pygame.init()




# audio

death_sound = pygame.mixer.Sound(DIR + '\death_sound.wav')
pickup_sound = pygame.mixer.Sound(DIR + '\pickup.wav')


pygame.mixer.music.load(DIR + '\piano_loop.wav')
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play(-1) # -1 = loop forever

# text
#font = pygame.font.Font(None, 30)
font = pygame.font.SysFont('calibri', 30)









screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.RESIZABLE)
pygame.display.set_caption('JOGO 1')

pygame.display.set_caption("Epifania")
clock = pygame.time.Clock()

pygame_icon = pygame.image.load(DIR + "\weed.png").convert_alpha()
pygame_icon.set_colorkey(WHITE)
pygame.display.set_icon(pygame_icon)



#SETTING UP LEVELS -------------------------------------------------------------
levels = []
level = Level1(1)
levels.append(level)

level = Level2(2)
levels.append(level)

level = Level3()
levels.append(level)

level = Level4()
levels.append(level)

level_index = 0
current_level = levels[level_index]

# other sprites
moving_sprites = pygame.sprite.Group()

player = Player(PLAYER_X0 , PLAYER_Y0, death_sound, pickup_sound)

moving_sprites.add(player)

# MAIN LOOP -------------------------------------------------------------------
done = False
frames = 0
seconds = 0
start_time = 90
dt = 0


while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-6, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(6, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -6)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 6)
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(6, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-6, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 6)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -6)
                    
                
        for enemy in current_level.enemy_sprites:
            enemy.change_speed(frames)
            

        moving_sprites.update(current_level.wall_list, current_level.enemy_sprites, current_level.goal_list)
        current_level.enemy_sprites.update()
        
        # se o jogador passou de fase :)
        if player.score == current_level.goals:
            level_index += 1
            
            # if level_index == 3: #vitoria
            #     vitoria(screen)
            #     done = True
            #     break
            
            current_level = levels[level_index]
            player.score = 0
            player.rect.x = PLAYER_X0
            player.rect.y = PLAYER_Y0
            frames = 0
            
            
        
        # drawing
        
        #vitoria
        if level_index == 3:
            
            
            asuna = Image(0, 200, DIR + "\\asuna.jpg", 410, 456)
            moving_sprites.add(asuna)
            
            mashiro = Image(SCREEN_WIDTH - 200, 200, DIR + "\mashiro.png", 190, 398)
            moving_sprites.add(mashiro)
            
            cake = Image(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100, DIR + "\cake.jpg", 207, 243)
            moving_sprites.add(cake)
            
            hidas = Image(SCREEN_WIDTH-130, SCREEN_HEIGHT -158, DIR + "\hidas.png", 130, 158)
            moving_sprites.add(hidas)
            
            moving_sprites.remove(player)
            
            pygame.mixer.music.stop()
            pygame.mixer.music.load(DIR + '\win_song.mp3')
            pygame.mixer.music.play(0)
            
        
        screen.fill(WHITE)
        current_level.wall_list.draw(screen)
        current_level.enemy_sprites.draw(screen)
        current_level.goal_list.draw(screen)
        moving_sprites.draw(screen)
        
        

        
        # text
        text = font.render("Mortes: " + str(player.death_count), True, BLACK)
        screen.blit(text, [100, 10])
        
        text = font.render("Level " + str(level_index + 1), True, BLACK)
        screen.blit(text, [10, 10])
        
        if current_level.text != None:
            screen.blit(current_level.text, [10, SCREEN_HEIGHT - 30])
        
        
        
        
        
        
        
        
        
        
        total_seconds = dt // FPS
    
        # Divide by 60 to get total minutes
        minutes = total_seconds // 60
    
        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
    
        # Use python string formatting to format in leading zeros
        output_string = "Tempo: {0:02}:{1:02}".format(minutes, seconds)
    
        # Blit to the screen
        text = font.render(output_string, True, BLACK)
        screen.blit(text, [10, 40])
    

 
        
        
        
        
        
        
        
        
        
        
        
        
        pygame.display.flip()
        
        frames += 1
        dt +=1
        seconds = frames // 60
        clock.tick(60)

        if level_index == 3:
            pygame.time.wait(10000)
            pygame.quit()
            break