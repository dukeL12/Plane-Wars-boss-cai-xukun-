#添加敌机函数
from Shell import *

figure = 0

#设置玩家血量条属性函数
def draw_shield_bar(surf,x,y,pct):
    pct = max(pct,0)
    fill = (pct/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

#设置玩家生命数量属性函数
def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x+30*i
        img_rect.y = y
        surf.blit(img,img_rect)


# #设置boss血量条属性函数
def draw_boss_bar(surf,x,y,pct):
    pct = max(pct,0)
    fill = (pct/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BOSS1_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,RED,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

#添加敌机函数
def newmob():
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)



#添加火山石函数
def newlava():
    lava_element = Lava()
    all_sprites.add(lava_element)
    lavas.add(lava_element)


class Player(pygame.sprite.Sprite):
    '''创建玩家类'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 10
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30
        self.speedx = 0
        self.speedy = 0
        # 方向控制：A控制左、D控制右、W控制上、S控制下、A+W控制左上、A+S控制左下、D+W控制右上、D+S控制右下
        keystate = pygame.key.get_pressed()
        if keystate[K_a]:
            self.speedx = -5
        if keystate[K_d]:
            self.speedx = 5
        if keystate[K_w]:
            self.speedy = -5
        if keystate[K_s]:
            self.speedy = 5
        # 发射控制：空格
        if keystate[pygame.K_SPACE]:
            self.shoot()
        # 设置玩家移动边界
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 10:
            self.rect.top = 10
        if self.rect.bottom > HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # 单火力
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
            # 双火力
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.play()
            # 三火力
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                missile1 = Missile(self.rect.centerx, self.rect.top)  # 导弹
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)
                shooting_sound.play()
                missile_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    '''创建敌机类'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(enemies_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 2)   #飞机下降
        self.speedx = random.randrange(-3, 3)  #飞机左右
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if random.randrange(10) >= 6:
            self.enemies_shoot()
        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

    def enemies_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            enemies_bullet = EnemiesBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(enemies_bullet)
            enemies_bullets.add(enemies_bullet)
            shooting_sound.play()


# 创建Boss
class Mob_boss2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss2_img,(296, 225))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-400
        self.radius = 20
        self.shield = 450
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.speedx = random.randrange(-2, 2)  # 飞机左右
        self.shoot_delay = 2000
        self.last_shot = pygame.time.get_ticks()
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        if random.randrange(10) >= 2:
            self.enemies_shoot()
        # if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
        self.rect.x = random.randrange(-1, 150)



    def enemies_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            boss_bullet1 = BossBullet(self.rect.left, self.rect.centery,figure)
            boss_bullet4 = BossBullet(self.rect.left + 40, self.rect.centery - 40,figure)
            boss_bullet5 = BossBullet(self.rect.left + 80, self.rect.centery - 80,figure)
            boss_bullet2 = BossBullet(self.rect.right, self.rect.centery,figure)
            boss_bullet6 = BossBullet(self.rect.right - 40, self.rect.centery - 40,figure)
            boss_bullet7 = BossBullet(self.rect.right - 80, self.rect.centery - 80,figure)
            boss_bullet3 = BossBullet(self.rect.centerx, self.rect.top,figure)
            all_sprites.add(boss_bullet1)
            all_sprites.add(boss_bullet4)
            all_sprites.add(boss_bullet5)
            all_sprites.add(boss_bullet6)
            all_sprites.add(boss_bullet7)
            all_sprites.add(boss_bullet2)
            all_sprites.add(boss_bullet3)
            boss_bullets.add(boss_bullet1)
            boss_bullets.add(boss_bullet4)
            boss_bullets.add(boss_bullet5)
            boss_bullets.add(boss_bullet6)
            boss_bullets.add(boss_bullet7)
            boss_bullets.add(boss_bullet2)
            boss_bullets.add(boss_bullet3)
            shooting_sound.play()
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
class Mob_boss3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss3_img,(296, 225))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-400
        self.radius = 20
        self.shield = 450
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.speedx = random.randrange(-2, 2)  # 飞机左右
        self.shoot_delay = 2000
        self.last_shot = pygame.time.get_ticks()
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        if random.randrange(10) >= 2:
            self.enemies_shoot()
        # if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > WIDTH + 20):
        self.rect.x = random.randrange(-1, 150)



    def enemies_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            boss_bullet1 = BossBullet(self.rect.left, self.rect.centery,figure)
            boss_bullet4 = BossBullet(self.rect.left + 40, self.rect.centery - 40,figure)
            boss_bullet5 = BossBullet(self.rect.left + 80, self.rect.centery - 80,figure)
            boss_bullet2 = BossBullet(self.rect.right, self.rect.centery,figure)
            boss_bullet6 = BossBullet(self.rect.right - 40, self.rect.centery - 40,figure)
            boss_bullet7 = BossBullet(self.rect.right - 80, self.rect.centery - 80,figure)
            boss_bullet3 = BossBullet(self.rect.centerx, self.rect.top,figure)
            all_sprites.add(boss_bullet1)
            all_sprites.add(boss_bullet4)
            all_sprites.add(boss_bullet5)
            all_sprites.add(boss_bullet6)
            all_sprites.add(boss_bullet7)
            all_sprites.add(boss_bullet2)
            all_sprites.add(boss_bullet3)
            boss_bullets.add(boss_bullet1)
            boss_bullets.add(boss_bullet4)
            boss_bullets.add(boss_bullet5)
            boss_bullets.add(boss_bullet6)
            boss_bullets.add(boss_bullet7)
            boss_bullets.add(boss_bullet2)
            boss_bullets.add(boss_bullet3)
            shooting_sound.play()
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

#######################################主循环#######################################

# 定义游戏开始界面标识
running = True
menu_display = True

while running:
    if menu_display:
        main_menu()  # 游戏初始界面和准备开始界面函数
        pygame.time.wait(3000)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.play(-1)  # -1：循环播放
        menu_display = False

        all_sprites = pygame.sprite.Group()
        player = Player()
        # boss1 = Mob_boss2()
        # all_sprites.add(boss1)
        all_sprites.add(player)
        mobs = pygame.sprite.Group()
        for i in range(4):
            newmob()
        lavas = pygame.sprite.Group()
        for i in range(4):
            newlava()
        bullets = pygame.sprite.Group()
        enemies_bullets = pygame.sprite.Group()
        boss_bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        # boss1=pygame.sprite.Group()
        # all_sprites.add(boss1)
        # newboss()
        # mob_boss =Mob_boss2()
        # all_sprites.add(mob_boss)
        score = 0
        mob_boss = Mob_boss2()
        mob_boss3 = Mob_boss3()
    clock.tick(FPS)




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    all_sprites.update()

    if score > 100:
        # draw_boss_bar(screen, 5, 5, mob_boss.shield)
        figure = 1
        all_sprites.add(mob_boss)
        # 玩家与boss炮弹碰撞检测
        hits = pygame.sprite.spritecollide(player, boss_bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius * 3
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if mob_boss.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(mob_boss.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                figure = 2
                player.lives -= 1
                player.shield = 100

        # boss与玩家炮弹碰撞检测
        hits = pygame.sprite.spritecollide(mob_boss, bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            mob_boss.shield -= hit.radius * 1
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if mob_boss.shield <= 0:
                player_die_sound.play()
                all_sprites.remove(mob_boss)
                # death_explosion = Explosion(player.rect.center, 'boss')
                # all_sprites.add(death_explosion)
                mob_boss.hide()
#boss3
    if score > 800:
        # draw_boss_bar(screen, 5, 5, mob_boss.shield)
        figure = 3
        all_sprites.add(mob_boss3)
        # 玩家与boss炮弹碰撞检测
        hits = pygame.sprite.spritecollide(player, boss_bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius * 3
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if mob_boss3.shield <= 0:
                player_die_sound.play()
                death_explosion = Explosion(mob_boss3.rect.center, 'player')
                all_sprites.add(death_explosion)
                player.hide()
                figure = 2
                player.lives -= 1
                player.shield = 100

        # boss与玩家炮弹碰撞检测
        hits = pygame.sprite.spritecollide(mob_boss3, bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            mob_boss3.shield -= hit.radius * 1
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if mob_boss3.shield <= 0:
                player_die_sound.play()
                all_sprites.remove(mob_boss3)
                # death_explosion = Explosion(player.rect.center, 'boss')
                # all_sprites.add(death_explosion)
                mob_boss3.hide()

    # # 玩家与boss炮弹碰撞检测
    # hits = pygame.sprite.spritecollide(player, boss_bullets, True, pygame.sprite.collide_circle)
    # for hit in hits:
    #     player.shield -= hit.radius * 3
    #     expl = Explosion(hit.rect.center, 'sm')
    #     all_sprites.add(expl)
    #     if mob_boss.shield <= 0:
    #         player_die_sound.play()
    #         death_explosion = Explosion(mob_boss.rect.center, 'player')
    #         all_sprites.add(death_explosion)
    #         player.hide()
    #         player.lives -= 1
    #         player.shield = 100
    #
    # # boss与玩家炮弹碰撞检测
    # hits = pygame.sprite.spritecollide(mob_boss, bullets, True, pygame.sprite.collide_circle)
    # for hit in hits:
    #     mob_boss.shield -= hit.radius * 4
    #     expl = Explosion(hit.rect.center, 'sm')
    #     all_sprites.add(expl)
    #     if mob_boss.shield <= 0:
    #         player_die_sound.play()
    #         all_sprites.remove(mob_boss)
    #         # death_explosion = Explosion(player.rect.center, 'boss')
    #         # all_sprites.add(death_explosion)
    #         # mob_boss.hide()

    # 敌机与玩家炮弹碰撞检测
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # 火山石与玩家炮弹碰撞检测
    hits = pygame.sprite.groupcollide(lavas, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newlava()

    # 玩家与敌机碰撞检测
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100


    # 玩家与火山石碰撞检测
    hits = pygame.sprite.spritecollide(player, lavas, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newlava()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # 玩家与敌机炮弹碰撞检测
    hits = pygame.sprite.spritecollide(player, enemies_bullets, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100





    # 玩家与补给碰撞检测
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()



    if player.lives == 0 and not death_explosion.alive():
        pygame.time.wait(1000)
        screen.fill(BLACK)
        draw_text(screen, "Game Over", 40, WIDTH / 2, HEIGHT / 3)
        pygame.display.update()
        pygame.time.wait(3000)
        menu_display = True


    # 背景画卷向下滚动
    screen.fill(BLACK)
    screen.blit(background, (0, height))
    height += 2
    if height >= -168:
        height = -936

    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 30)
    draw_shield_bar(screen, 5, 20, player.shield)
    draw_lives(screen, WIDTH - 100, 20, player.lives, player_mini_img)

    '''
    根据判断更换boss血条，用draw_boss_bar函数画血条框
    '''
    if figure == 1:
        draw_boss_bar(screen, 5, 5,mob_boss.shield)
    if figure == 3:
        draw_boss_bar(screen, 5, 5, mob_boss3.shield)
    pygame.display.flip()

pygame.quit()