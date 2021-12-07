import pygame
import random
from pygame.locals import*
pygame.init()
screen = pygame.display.set_mode((400, 700))
pygame.display.set_caption("Flappy Bird")
#
clock = pygame.time.Clock()
#
# conditions
select_bird = 1
run = True
die = False
first_open = True


class background(pygame.sprite.Sprite):
    def __init__(self, width, height, speed, file_name, cloud, floor):
        self.file_name = file_name
        self.speed = speed
        self.floor = floor
        self.cloud = cloud
        img = pygame.image.load(
            f'pic/png/background/{self.file_name}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (width, height))
        cloud_img = pygame.image.load(
            f'pic/png/cloud/{self.cloud}.png').convert_alpha()
        self.cloud_image = pygame.transform.scale(cloud_img, (width, height/3))
        floor_img = pygame.image.load(
            f'pic/png/floor/{self.floor}.png').convert_alpha()
        self.floor_image = pygame.transform.scale(
            floor_img, (width, height/12))
        self.rect = self.image.get_rect()

    def draw_bg_animations(self):
        self.rect.x += self.speed
        screen.blit(self.image, self.rect)
        screen.blit(self.image, (self.rect.x+self.rect.width, self.rect.y))
        screen.blit(self.cloud_image, self.rect)
        screen.blit(self.cloud_image, (self.rect.x +
                    self.rect.width, self.rect.y))
        screen.blit(self.floor_image, (self.rect.x, self.rect.y +
                    self.rect.height-self.floor_image.get_height()))
        screen.blit(self.floor_image, (self.rect.x+self.rect.width,
                    self.rect.y+self.rect.height-self.floor_image.get_height()))
        if self.rect.x < -self.rect.width:
            self.rect.x = 0
#


class menu(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, folder_name, file_name):
        self.file_name = file_name
        self.folder_name = folder_name
        self.width = width
        self.height = height
        img = pygame.image.load(
            f'pic/png/{self.folder_name}/{self.file_name}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.click = False

    def draw_menu(self):
        screen.blit(self.image, self.rect)

    def draw_button(self):
        actions = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and self.click == False:
                self.click = True
                actions = True
            if pygame.mouse.get_pressed()[0] == False and self.click == True:
                self.click = False
        screen.blit(self.image, self.rect)
        return actions

    def bird_bg(self):
        self.file_name += 1
        img = pygame.image.load(
            f'pic/png/{self.folder_name}/{self.file_name}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (self.width, self.height))
        if self.file_name == 3:
            self.file_name = 0

    def sugestion_animations_01(self):
        self.rect.y += 1
        img = pygame.image.load(
            f'pic/png/{self.folder_name}/{self.file_name}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (self.width, self.height))
        if self.file_name == '3':
            if self.rect.y >= 380:
                self.rect.y = 350
        if self.file_name == '6':
            if self.rect.y >= 330:
                self.rect.y = 320

    def sugestion_animations_02(self):
        img = pygame.image.load(
            f'pic/png/{self.folder_name}/{self.file_name}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (self.width, self.height))
        if self.file_name == '4':
            self.rect.x -= 1
            if self.rect.x <= 120:
                self.rect.x = 125
        if self.file_name == '5':
            self.rect.x += 1
            if self.rect.x >= 235:
                self.rect.x = 230

    def next01_select_map(self):
        img = pygame.image.load(
            f'pic/png/{self.folder_name}/{self.file_name}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (self.width, self.height))
        self.rect.x -= 1
        if self.rect.x <= 315:
            self.rect.x = 320

    def next02_select_map(self):
        img = pygame.image.load(
            f'pic/png/{self.folder_name}/{self.file_name}.png').convert_alpha()
        self.image = pygame.transform.scale(pygame.transform.flip(
            img, True, False), (self.width, self.height))
        self.rect.x -= 1
        if self.rect.x <= 45:
            self.rect.x = 50
#


class bird(menu):
    def __init__(self, x, y, width, height, folder_name, file_name, gravity, movement):
        super().__init__(x, y, width, height, folder_name, file_name)
        self.gravity = gravity
        self.movement = movement

    def bird_animations(self):
        if self.movement >= 0:
            img = pygame.image.load(
                f'pic/png/{self.folder_name}/{self.file_name}.png').convert_alpha()
            self.image = pygame.transform.scale(
                pygame.transform.rotate(img, -45), (self.width, self.height))
        else:
            self.file_name += 1
            if self.file_name == 3:
                self.file_name = 0
            img = pygame.image.load(
                f'pic/png/{self.folder_name}/{self.file_name}.png').convert_alpha()
            self.image = pygame.transform.scale(
                pygame.transform.rotate(img, 45), (self.width, self.height))
        self.rect.y -= self.gravity
        self.movement += self.gravity
        self.rect.y += self.movement

    def jump(self):
        self.movement = -8
        jump_mp3 = pygame.mixer.Sound('music/wing.mp3')
        jump_mp3.play()

    def collide(self, other):
        return (other.rect.collidepoint(self.rect.topleft[0]+15, self.rect.topright[1]+10) or
                other.rect.collidepoint(self.rect.topright[0]-15, self.rect.topright[1]+10) or
                other.rect.collidepoint(self.rect.bottomleft[0]+15, self.rect.bottomleft[1]-10) or
                other.rect.collidepoint(self.rect.bottomright[0]-15, self.rect.bottomright[1]-10) or
                other.rect01.collidepoint(self.rect.topleft[0]+15, self.rect.topright[1]-10) or
                other.rect01.collidepoint(self.rect.topright[0]-15, self.rect.topright[1]-10) or
                other.rect01.collidepoint(self.rect.bottomleft[0]+30, self.rect.bottomleft[1]-15) or
                other.rect01.collidepoint(self.rect.bottomright[0]-15, self.rect.bottomright[1]-15))

    def socer(self, other):
        return self.rect.x == (other.rect.x+other.width)
#


class tube(menu):
    def __init__(self, x, y, width, height, folder_name, file_name):
        super().__init__(x, y, width, height, folder_name, file_name)
        self.x = x
        self.y = y
        img1 = pygame.image.load(
            f'pic/png/{self.folder_name}/{self.file_name+1}.png').convert_alpha()
        self.img1 = pygame.transform.scale(img1, (self.width, 600))
        self.rect01 = self.img1.get_rect()

    def tub_animations(self):
        self.rect.x -= 1
        if self.rect.x < -self.width:
            self.height = random.randint(200, 1000)
            img = pygame.image.load(
                f'pic/png/{self.folder_name}/{self.file_name}.png').convert_alpha()
            self.image = pygame.transform.scale(img, (self.width, self.height))
            self.x = 600-self.width
            self.rect = self.image.get_rect()
            self.rect.center = (self.x, self.y)

    def draw_tube(self):
        self.rect01.topleft = (self.rect.x, self.rect.midbottom[1]+150)
        screen.blit(self.image, self.rect)
        screen.blit(self.img1, self.rect01)
# print first menu


def first_menu():
    title.draw_menu()
    getready.draw_menu()
    bird_bg.bird_bg()
    bird_bg.draw_menu()
    suggetions01.sugestion_animations_01()
    suggetions01.draw_menu()
    suggetions02.sugestion_animations_01()
    suggetions02.draw_menu()
    tap1.sugestion_animations_02()
    tap1.draw_menu()
    tap2.sugestion_animations_02()
    tap2.draw_menu()


def first_menu02():
    clock.tick(25)
    background02.draw_bg_animations()
    first_menu()


def first_menu01():
    clock.tick(25)
    background01.draw_bg_animations()
    first_menu()
# print game over


def game_over_menu():
    clock.tick(25)
    game_over_title.draw_menu()
    game_over_table.draw_menu()
    game_over_newicon.draw_menu()
    game_over_button01.draw_menu()
    game_over_button02.draw_menu()
    game_over_button03.draw_menu()
# print map


def select_map_01():
    clock.tick(25)
    background01.draw_bg_animations()
    select_background01.draw_menu()
    oke_select_background.draw_menu()
    next01_selcet_background.draw_menu()
    next01_selcet_background.next01_select_map()
    border02_select_background.draw_menu()


def select_map_02():
    clock.tick(25)
    background02.draw_bg_animations()
    select_background02.draw_menu()
    oke_select_background.draw_menu()
    next02_selcet_background.draw_menu()
    next02_selcet_background.next02_select_map()
    border02_select_background.draw_menu()


# music
pygame.mixer.music.load('music/1.mp3')
pygame.mixer.music.play(-1)


def stop_mp3():
    pygame.mixer.music.stop()
# in game


def draw_tube_of_bird_1_3():
    tube01.draw_tube()
    tube01.tub_animations()
    tube02.draw_tube()
    tube02.tub_animations()
    tube03.draw_tube()
    tube03.tub_animations()


def draw_tube_of_bird_2_4():
    tube01_1.draw_tube()
    tube01_1.tub_animations()
    tube02_1.draw_tube()
    tube02_1.tub_animations()
    tube03_1.draw_tube()
    tube03_1.tub_animations()


def ingame_bird01():
    stop_mp3()
    clock.tick(60)
    background01.draw_bg_animations()
    bird01.draw_menu()
    bird01.bird_animations()
    draw_tube_of_bird_1_3()


def ingame_bird02():
    stop_mp3()
    clock.tick(60)
    background02.draw_bg_animations()
    bird02.draw_menu()
    bird02.bird_animations()
    draw_tube_of_bird_2_4()


def ingame_bird03():
    stop_mp3()
    clock.tick(60)
    background01.draw_bg_animations()
    bird03.draw_menu()
    bird03.bird_animations()
    draw_tube_of_bird_1_3()


def ingame_bird04():
    stop_mp3()
    clock.tick(60)
    background02.draw_bg_animations()
    bird04.draw_menu()
    bird04.bird_animations()
    draw_tube_of_bird_2_4()
# socer


def socring_system():
    socer.draw_menu()
    socer_last.draw_menu()
    if bird01.socer(tube01) == True or bird01.socer(tube02) == True or bird01.socer(tube03) == True or bird02.socer(tube01_1) == True or bird02.socer(tube02_1) == True or bird02.socer(tube03_1) == True or bird03.socer(tube01) == True or bird03.socer(tube02) == True or bird03.socer(tube03) == True or bird04.socer(tube01_1) == True or bird04.socer(tube02_1) == True or bird04.socer(tube03_1) == True:
        socer.file_name += 1
        if socer.file_name == 9:
            socer.file_name = 0
            socer_last.file_name += 1
        img = pygame.image.load(
            f'pic/png/{socer.folder_name}/{socer.file_name}.png').convert_alpha()
        socer.image = pygame.transform.scale(img, (socer.width, socer.height))
        img1 = pygame.image.load(
            f'pic/png/{socer_last.folder_name}/{socer_last.file_name}.png').convert_alpha()
        socer_last.image = pygame.transform.scale(
            img1, (socer_last.width, socer_last.height))
        point_mp3 = pygame.mixer.Sound('music/point.mp3')
        point_mp3.play()
# choose bird


def Sound_die():
    die_mp3 = pygame.mixer.Sound('music/game_over_real.mp3')
    die_mp3.play()


def choose_bird(die):
    if select_bird == 1:
        ingame_bird01()
        if bird01.collide(tube01) or bird01.collide(tube02) or bird01.collide(tube03):
            Sound_die()
            die = True
        if bird01.collide(tube01_1) or bird01.collide(tube02_1) or bird01.collide(tube03_1):
            die = True
    if select_bird == 2:
        ingame_bird02()
        if bird02.collide(tube01) or bird02.collide(tube02) or bird02.collide(tube03):
            Sound_die()
            die = True
        if bird02.collide(tube01_1) or bird02.collide(tube02_1) or bird02.collide(tube03_1):
            die = True
    if select_bird == 3:
        ingame_bird03()
        if bird03.collide(tube01) or bird03.collide(tube02) or bird03.collide(tube03):
            Sound_die()
            die = True
        if bird03.collide(tube01_1) or bird03.collide(tube02_1) or bird03.collide(tube03_1):
            die = True
    if select_bird == 4:
        ingame_bird04()
        if bird04.collide(tube01) or bird04.collide(tube02) or bird04.collide(tube03):
            Sound_die()
            die = True
        if bird04.collide(tube01_1) or bird04.collide(tube02_1) or bird04.collide(tube03_1):
            die = True
    return die


#
click = False


def click_every_where(click):
    if pygame.mouse.get_pressed()[0] and click == False:
        click = True
    return click


# background
background01 = background(400, 700, -2, '0', '0', '0')
background02 = background(800, 700, -2, '1', '1', '1')
# frist menu
title = menu(200, 100, 400, 100, 'menu', '7')
getready = menu(200, 500, 250, 50, 'menu', '2')
bird_bg = menu(200, 300, 50, 50, 'bird', 0)
rate = menu(310, 600, 190, 90, 'menu', '1')
menu_map = menu(100, 600, 190, 90, 'menu', '0')
suggetions01 = menu(202, 380, 40, 60, 'menu', '3')
suggetions02 = menu(200, 325, 15, 20, 'menu', '6')
tap1 = menu(150, 380, 50, 25, 'menu', '4')
tap2 = menu(250, 380, 50, 25, 'menu', '5')
# select map
select_background01 = menu(200, 322, 228, 410, 'background', '0')
select_background02 = menu(200, 322, 228, 410, 'background', '1')
oke_select_background = menu(200, 600, 90, 45, 'select', '0')
next01_selcet_background = menu(335, 325, 30, 40, 'select', '1')
next02_selcet_background = menu(65, 325, 30, 40, 'select', '1')
border01_select_background = menu(199, 343, 220, 441, 'border', '0')
border02_select_background = menu(200, 350, 400, 700, 'border', '1')
# game over
game_over_title = menu(200, 200, 350, 60, 'game_over', '0')
game_over_table = menu(200, 350, 350, 200, 'game_over', '1')
game_over_newicon = menu(80, 250, 50, 20, 'game_over', '2')
game_over_button01 = menu(100, 450, 90, 45, 'game_over', '3')
game_over_button02 = menu(200, 450, 90, 45, 'game_over', '4')
game_over_button03 = menu(300, 450, 90, 45, 'game_over', '5')
# bird
bird01 = bird(100, 350, 50, 50, 'bird', 0, 0.5, 0)
bird02 = bird(100, 350, 50, 50, 'bird2', 0, 0.5, 0)
bird03 = bird(100, 350, 50, 50, 'bird3', 0, 0.5, 0)
bird04 = bird(100, 350, 50, 50, 'bird4', 0, 0.5, 0)
# tub
height = random.randint(100, 600)
tube01 = tube(200, 0, 50, height, 'tube', 0)
tube01_1 = tube(200, 0, 50, height, 'tube', 2)
height = random.randint(100, 600)
tube02 = tube(400, 0, 50, height, 'tube', 0)
tube02_1 = tube(400, 0, 50, height, 'tube', 2)
height = random.randint(100, 600)
tube03 = tube(600, 0, 50, height, 'tube', 0)
tube03_1 = tube(600, 0, 50, height, 'tube', 2)
# socer
socer = menu(210, 25, 20, 25, 'socer', 0)
socer_last = menu(190, 25, 20, 25, 'socer', 0)
# check border
RED = (255, 0, 0)
while run:
    # chọn background thì tháo background trong con chym ra
    if first_open:
        #
        click = click_every_where(click)
        #
        first_menu01()
        #
        rate_online = rate.draw_button()
        choose_map = menu_map.draw_button()

    # first_menu02(first_open,choose_map)
    #
    if choose_map:
        select_map_01()
        # select_map_02()
        first_open = False
    print(click)
    if click:
        first_open = False
        if die == False:
            die = choose_bird(die)
            socring_system()
        if die == True:
            game_over_menu()
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                click = True
                if click:
                    if die == False:
                        bird01.jump()
                        bird02.jump()
                        bird03.jump()
                        bird04.jump()
    # dòng phía dưới để vẽ ra dễ hình dung ống phía dưới
    # pygame.draw.rect(screen, RED, bird01.rect, 2)
    # pygame.draw.rect(screen, RED, tube01.rect, 2)
    # pygame.draw.rect(screen, RED, tube01.rect01, 2)
    pygame.display.flip()
pygame.quit()
#
