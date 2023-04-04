# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 10:47:01 2022

@author: twitc
"""


import pygame

pygame.init()


# world stuff
s_width = 800
s_height = int(s_width * .8)
screen = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Mage Speller")

# frame rate stuff
clock = pygame.time.Clock()
fps = 60


# world variablkes
world_gravity = 0.75


# player actions
moving_left = False
moving_right = False

# define colours
BG = '#00008B'
RED = (255, 0, 0)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 400), (s_width, 400))


# projectile class

# load images

# - arrow
arrow_img = pygame.image.load(
    './characters/Skeleton_Archer/Arrow.png').convert_alpha()


class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direciton = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        temp_list = []

# 0 - idle / 1 - run/ 2 - deaths
        # find a time stamp of time of creation
        self.update_time = pygame.time.get_ticks()
        # idle
        for i in range(2):
            img = pygame.image.load(
                f"./characters/{self.char_type}/Idle/{i}.png").convert_alpha()
            img = pygame.transform.scale(
                img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        # run
        for i in range(3):
            img = pygame.image.load(
                f"./characters/{self.char_type}/Run/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        # jumpy
        for i in range(2):
            img = pygame.image.load(
                f"./characters/{self.char_type}/jump/{i}.png")
            img = pygame.transform.scale(
                img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # reset movement vars
        dx = 0
        dy = 0

        # assign movement if left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        # jumping
        if self.jump and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity somehow after this
        self.vel_y += world_gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check collision with the floor
        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
            self.in_air = False

        # udpdate the position of the character
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation for the timer of the thign
        ANIMATION_CD = 200
        # udpat eht eimage
        self.image = self.animation_list[self.action][self.frame_index]
        # check the time that has passed since the last time
        if pygame.time.get_ticks() - self.update_time > ANIMATION_CD:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            # make sure that it properly loops
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check the difference in actions from the previous state
        if self.action != new_action:
            self.action = new_action
            # udpate the animation index
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = arrow_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = 1


x = 200
y = 200
scale = 1

player = Player("Skeleton_Spearman", x, y, scale, 5)

run = True
while run:

    # start the clock ticker
    clock.tick(fps)
    # basically erases the screen and redraws the character every time
    draw_bg()

    player.draw()
    player.update_animation()

    # update player actions
    if player.alive:
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)  # 1: run
        else:
            player.update_action(0)  # 0: idle
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False

        # account for keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # account for button releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                player.jump = False
    pygame.display.update()

pygame.quit()
