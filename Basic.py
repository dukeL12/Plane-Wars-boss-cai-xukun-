#导入模块
import pygame
import random
from pygame.locals import *
from os import path



#######################################基本参数配置#######################################

'''
Bullet:我方炮弹
EnemiesBullet：敌机炮弹
'''


#获取图片库和声音库路径
img_dir = path.join(path.dirname(__file__),'pic')
sound_folder = path.join(path.dirname(__file__),'sounds')

#定义游戏窗口、玩家血量条尺寸，游戏运行速度、炮火持续时间等参数
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BOSS1_LENGTH=450    #B0SS
BAR_HEIGHT = 10

#定义白、黑、红、绿、蓝、黄的RGB参数
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#初始化pygame模块，创建游戏窗口、游戏窗口命名、创建跟踪时间对象
pygame.init()
pygame.mixer.init()  #初始化音效
screen = pygame.display.set_mode((WIDTH,HEIGHT))  # 创建游戏窗口
pygame.display.set_caption("飞机大战")
clock = pygame.time.Clock()

#定义文本字体
font_name = pygame.font.match_font('SimHei')

#######################################加载图片#######################################

#加载游戏进行中背景图片
background = pygame.image.load(path.join(img_dir,'starfield.png')).convert()
background = pygame.transform.scale(background,(WIDTH,1536))
height = -936

#加载玩家图片
# player_img = pygame.image.load(path.join(img_dir,'player.png')).convert()
player_img = pygame.image.load('pic/player.png')
player_mini_img = pygame.transform.scale(player_img,(25, 19))
player_mini_img.set_colorkey(BLACK)

#加载玩家炮弹、导弹图片
bullet_img = pygame.image.load(path.join(img_dir,'bullet.png')).convert()
missile_img = pygame.image.load(path.join(img_dir,'missile.png')).convert_alpha()

#加载敌机炮弹图片
enemies_bullet_img = pygame.image.load(path.join(img_dir,'enemies_bullet.png')).convert()
boss_bullet_img = pygame.image.load(path.join(img_dir,'boss_zidan3.png'))
boss_bullet_img3 = pygame.image.load(path.join(img_dir,'lanqiu.png'))
#boss1
boss2_img = pygame.image.load(path.join('pic/Boss2.png'))
boss2_mini_img = pygame.transform.scale(boss2_img,(200, 152))
boss2_mini_img.set_colorkey(BLACK)
#boss2
boss3_img = pygame.image.load(path.join('pic/Boss3.png'))
boss3_mini_img = pygame.transform.scale(boss3_img,(200, 152))
boss3_mini_img.set_colorkey(BLACK)
#加载盾牌、闪电图片
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt.png')).convert()

#加载敌机和火山石图片
enemies_images = []
lava_images = []
#敌机
enemies_list = [
    'enemies1.png',
    'enemies2.png',
    'enemies3.png'
]
#火山石
lava_list = [
    'lava_med.png',
    'lava_small1.png',
    'lava_small2.png',
    'lava_tiny.png'
]
for image in enemies_list:
    enemies_img = pygame.image.load(path.join(img_dir,image)).convert()
    enemies_img = pygame.transform.scale(enemies_img,(80, 60))
    enemies_images.append(enemies_img)
for image in lava_list:
    lava_images.append(pygame.image.load(path.join(img_dir,image)).convert())

#加载爆炸图片
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    #敌机、火山石爆炸
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    #大爆炸
    img_lg = pygame.transform.scale(img,(75,75))
    explosion_anim['lg'].append(img_lg)
    #小爆炸
    img_sm = pygame.transform.scale(img,(32,32))
    explosion_anim['sm'].append(img_sm)
    #玩家爆炸
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

#######################################加载声音#######################################

#加载炮弹、导弹发射声音
shooting_sound = pygame.mixer.Sound(path.join(sound_folder,'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder,'rocket.ogg'))

#加载敌机、火山石爆炸声音
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder,sound)))
#调低音量
pygame.mixer.music.set_volume(0.2)

#加载玩家爆炸声音
player_die_sound = pygame.mixer.Sound(path.join(sound_folder,'rumble1.ogg'))
