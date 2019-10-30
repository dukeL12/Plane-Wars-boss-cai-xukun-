#######################################函数区#######################################

#游戏初始界面和准备开始界面函数
from Basic import *


def main_menu():
    global screen
    #加载游戏初始界面背景音乐
    menu_song = pygame.mixer.music.load(path.join(sound_folder,"menu.ogg"))
    #循环播放
    pygame.mixer.music.play(-1)
    #加载游戏初始界面背景图片
    title = pygame.image.load(path.join(img_dir,"main.png")).convert()
    title = pygame.transform.scale(title,(WIDTH, HEIGHT),screen)  #   (width, height): 缩放的大小
    screen.blit(title,(0,0))          # 显示背景图
    pygame.display.update()           #更新需要显示的内容
    #检测玩家操作事件
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:  # 按下enter键
                break
        elif ev.type == pygame.QUIT:   # 点击窗口的x关闭游戏
                pygame.quit()
                quit()
        else:
            draw_text(screen, "按下 [ENTER] 开始游戏", 30, WIDTH/2, HEIGHT/2)
            draw_text(screen, "[A] ←  [S] ↓  [D] →  [W] ↑", 30, WIDTH/2, 2*HEIGHT/3)
            draw_text(screen, "[Space] 开火", 30, WIDTH/2, 3*HEIGHT/4)
            pygame.display.update()
    #加载准备声音
    ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
    ready.play()
    #加载准备开始界面背景颜色和文本
    screen.fill(BLACK)
    draw_text(screen, "GET READY!", 40, WIDTH/2, HEIGHT/3)
    pygame.display.update()

#设置文本属性函数
def draw_text(surf,text,size,x,y):
    #定义文本参数
    font = pygame.font.Font(font_name,size)
    # font = pygame.font.SysFont('SimHei',32)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)