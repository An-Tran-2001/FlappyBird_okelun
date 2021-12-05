import pygame
import random
from pygame.font import Font
from pygame.locals import*
pygame.init()
screen= pygame.display.set_mode((400,700))
pygame.display.set_caption("Flappy Bird")
# 
clock=pygame.time.Clock()
# 
background_img0 = pygame.image.load('pic/png/background/1.png').convert()
background_img0 = pygame.transform.scale(background_img0, (800, 700))
floor0=pygame.image.load('pic/png/obstacle/0.png').convert()
floor0 = pygame.transform.scale(floor0, (800, 60))
background_img1 = pygame.image.load('pic/png/background/0.png').convert()
background_img1 = pygame.transform.scale(background_img1, (400, 700))
background_img1.get_rect()
floor1=pygame.image.load('pic/png/obstacle/0.png').convert()
floor1 = pygame.transform.scale(floor1, (400, 60))
cloud_img=pygame.image.load('pic/png/background/3.png')
cloud_img = pygame.transform.scale(cloud_img, (400, 200))
frames=pygame.image.load('pic/png/background/4.png')
frames=pygame.transform.scale(frames, (400,700))
next_map=pygame.image.load('pic/png/background/5.png')
next_map=pygame.transform.scale(next_map, (50,50))
next_map_animation=[0, 0]
bg_animation=[0, 0]
select_bg=True
select_map=False
# 
play_img=pygame.image.load('pic/png/menu/0.png')
rating_img=pygame.image.load('pic/png/menu/1.png')
str_ready=pygame.image.load('pic/png/menu/2.png')
click_img=pygame.image.load('pic/png/menu/3.png')
click_img_animation=[195, 400]
suggestions1=pygame.image.load('pic/png/menu/4.png')
suggestions1_animation = [145, 400]
suggestions2=pygame.image.load('pic/png/menu/5.png')
suggestions2_animation=[225, 400]
suggestions3=pygame.image.load('pic/png/menu/6.png')
suggestions3_animation=[197, 350]
logo_img=pygame.image.load('pic/png/menu/7.png')
logo_img=pygame.transform.scale(logo_img, (420, 100))
# 
pygame.mixer.music.load('music/1.mp3')

#
gameover_img=pygame.image.load('pic/png/game_over/0.png')
gameover_img=pygame.transform.scale(gameover_img, (300,60))
transcript_img=pygame.image.load('pic/png/game_over/1.png')
transcript_img=pygame.transform.scale(transcript_img, (350,200))
new_img=pygame.image.load('pic/png/game_over/2.png')
new_img=pygame.transform.scale(new_img, (36,18))
share_img=pygame.image.load('pic/png/game_over/3.png')
scal_buttom=[80,40]
share_img=pygame.transform.scale(share_img, scal_buttom)
menu_img=pygame.image.load('pic/png/game_over/4.png')
menu_img=pygame.transform.scale(menu_img, scal_buttom)
ok_img=pygame.image.load('pic/png/game_over/5.png')
ok_img=pygame.transform.scale(ok_img, scal_buttom)
# 
pygame.mixer.music.play(-1) 
def stop_mp3():
    pygame.mixer.music.stop()
# 

def draw_background():
    bg_animation[0] -= 1
    if select_bg:
        screen.blit(background_img0, bg_animation)
        screen.blit(background_img0, (bg_animation[0] + 800, 0))
        screen.blit(cloud_img, (bg_animation[0], 0))
        screen.blit(cloud_img, (bg_animation[0]+400, 0))
        screen.blit(cloud_img, (bg_animation[0]+800, 0))
        screen.blit(cloud_img, (bg_animation[0]+1200, 0))
        screen.blit(floor0, (bg_animation[0], 640))
        screen.blit(floor0, (bg_animation[0] + 799, 640))
        if bg_animation[0] <= -800:
            bg_animation[0] = 0
    else:
        bg_animation[0] -= 1
        screen.blit(background_img1, bg_animation)
        screen.blit(background_img1, (bg_animation[0] + 400, 0))
        screen.blit(cloud_img, (bg_animation[0], 0))
        screen.blit(cloud_img, (bg_animation[0]+400, 0))
        screen.blit(floor1, (bg_animation[0], 640))
        screen.blit(floor1, (bg_animation[0] + 399, 640))
        if bg_animation[0] <= -400:
            bg_animation[0] = 0
# 
def draw_menu(i):
    screen.blit(play_img, (20, 600))
    screen.blit(rating_img, (230, 600))
    screen.blit(str_ready, (90, 500))
    screen.blit(click_img, click_img_animation)
    click_img_animation[1] += 1
    if click_img_animation[1] >= 415:
        click_img_animation[1] = 400
    screen.blit(suggestions1, suggestions1_animation)
    suggestions1_animation[0] -= 1
    if suggestions1_animation[0] <= 140:
        suggestions1_animation[0] = 145
    screen.blit(suggestions2, suggestions2_animation)
    suggestions2_animation[0] += 1
    if suggestions2_animation[0] >= 230:
        suggestions2_animation[0] = 225
    suggestions3_animation[1] += 1
    if suggestions3_animation[1] >= 360:
        suggestions3_animation[1] = 350
    screen.blit(suggestions3, suggestions3_animation)
    screen.blit(logo_img, (-15, 50))
    # 
    logo_bird=pygame.image.load(f'pic/png/bird/animations/bird2/{i}.png')
    loggo_bird=pygame.transform.scale(logo_bird, (50, 50))
    screen.blit(loggo_bird,(170, 300))
    if i==3:
        i=0
    return i+1
# 
def draw_gameover():
    screen.blit(gameover_img, (50, 150))
    screen.blit(transcript_img, (25, 250))
    screen.blit(new_img, (60, 247))
    screen.blit(share_img, (60, 430))
    screen.blit(menu_img, (160, 430))
    screen.blit(ok_img, (260, 430))
# 
def draw_selectbg(background_img0, background_img1):
    screen.blit(frames, (0,0))
    if select_map:
        next_map_animation[0] -=1
        screen.blit(next_map, (next_map_animation[0]+300,320))
        background_img0=pygame.transform.scale(background_img0, (200,300))
        screen.blit(background_img0, (100, 200))
        if next_map_animation[0] <= -5:
            next_map_animation[0] = 0
    else:
        next_map_animation[0] +=1    
        background_img1=pygame.transform.scale(background_img1, (200,300))
        screen.blit(background_img1, (100, 200))
        screen.blit(pygame.transform.flip(next_map, True, False),(next_map_animation[0]+50,320))
        if next_map_animation[0] >= 5:
            next_map_animation[0] = 0
# 
def click_button(orther):
    pos=pygame.mouse.get_pos()
    if orther.rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0]==1:
            print('click')
#   
ready=True
run=True
over=False
bg_select=False
i=0
while run:
    if ready:
        clock.tick(15) 
        draw_background()
        i=draw_menu(i)
        click_button(background_img1)
    if over:
        stop_mp3()
        clock.tick(20)
        draw_background()
        draw_gameover()
    if bg_select:
        clock.tick(20)
        draw_background()
        draw_selectbg(background_img0, background_img1)
    for event in pygame.event.get():
        if event.type==QUIT:
            run=False
        if event.type==KEYDOWN:
            if event.key==K_SPACE:
                ready=False
                over=True
                # bg_select=True
    pygame.display.flip()
pygame.quit()