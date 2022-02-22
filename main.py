import os
import pygame
import math
import random
from pygame import mixer
from enemy import Enemy
from boss import Boss
import button

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castle Defender')
clock = pygame.time.Clock()
FPS = 60

# ---------CASTLE-AND-TOWER-START ------------------------------------------

max_towers = 4 
TOWER_COST = 5000  
star_number = int(0)
tower_positions = [
    [SCREEN_WIDTH - 243, SCREEN_HEIGHT - 270],
    [SCREEN_WIDTH - 193, SCREEN_HEIGHT - 230],
    [SCREEN_WIDTH - 125, SCREEN_HEIGHT - 230],
    [SCREEN_WIDTH - 65, SCREEN_HEIGHT - 230]
]
# -------------
star_types = ['1_star', '2_star', '3_star']
castle_list = []
tower_list = []
# enemy animations
for star in star_types:
    types_castle_list = [pygame.image.load(f'img/castle/{star}/castle_100.png'),
                         pygame.image.load(f'img/castle/{star}/castle_50.png'),
                         pygame.image.load(f'img/castle/{star}/castle_25.png')]
    types_tower_list = [pygame.image.load(f'img/tower/{star}/tower_100.png'),
                        pygame.image.load(f'img/tower/{star}/tower_50.png'),
                        pygame.image.load(f'img/tower/{star}/tower_25.png')]
    castle_list.append(types_castle_list)
    tower_list.append(types_tower_list)
# -------------CASTLE-AND-TOWER-END----------------------------------------------

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)

font_20 = pygame.font.SysFont('algerian', 20)
font_30 = pygame.font.SysFont('algerian', 30)
font_40 = pygame.font.SysFont('algerian', 40)
font_70 = pygame.font.SysFont('jokerman', 70)

# MAP
bg = pygame.image.load('img/map/map_0.png').convert_alpha()
map_types = ['img/map/map_1.png', 'img/map/map_2.png', 'img/map/map_3.png']
m = 0  

animation_types = ['walk', 'attack', 'death']

# ------------ENEMY-START -------------------------------------------------------------------------
enemy_animations = []
enemy_types = ['knight', 'goblin', 'purple_goblin', 'red_goblin']
enemy_health = [75, 100, 125, 150]
enemy_alive = 0
ENEMY_TIMER = 1000 
last_enemy = pygame.time.get_ticks()
enemies_alive = 0
# thêm hành động cho enemy
for enemy in enemy_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        number_of_frames = 20
        for i in range(number_of_frames):
            img = pygame.image.load(f'img/enemies/{enemy}/{animation}/{i}.png').convert_alpha()
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w * 0.2), int(e_h * 0.2)))
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)

# ---------------ENEMY-END --------------------------------------------------------------------------

# ---------------BOSS-START --------------------------------------------------------------------------
boss_animations = []
boss_types = ['green_goblin']
boss_health = [500]
boss_alive = 0
check = True
create_boss = False
number_boss = 0
BOSS_TIMER = 5000  
last_boss = pygame.time.get_ticks()
for boss in boss_types:
    animation_list = []
    for animation in animation_types:
        temp_list = []
        number_of_frames = 20
        for i in range(number_of_frames):
            img = pygame.image.load(f'img/boss/{boss}/{animation}/{i}.png').convert_alpha()
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w * 0.2), int(e_h * 0.2)))
            temp_list.append(img)
        animation_list.append(temp_list)
    boss_animations.append(animation_list)

# ----------button ----------------------------------
music_on_img = pygame.image.load('img/button/music.png').convert_alpha()
music_off_img = pygame.image.load('img/button/music_off.png').convert_alpha()
repair_img = pygame.image.load('img/button/repair.png').convert_alpha()
armour_img = pygame.image.load('img/button/armour.png').convert_alpha()
exit_img = pygame.image.load('img/button/exit.png').convert_alpha()
save_img = pygame.image.load('img/button/save.png').convert_alpha()
restart_img = pygame.image.load('img/button/restart.png').convert_alpha()
start_img = pygame.image.load('img/button/start.png').convert_alpha()
resume_img = pygame.image.load('img/button/resume.png').convert_alpha()
pause_img2 = pygame.image.load('img/button/pause_2.png').convert_alpha()
pause_img = pygame.image.load("img/button/pause.png").convert_alpha()
tower_img = pygame.image.load("img/button/tower.png").convert_alpha()
update_castle_img = pygame.image.load("img/button/update_castle.png").convert_alpha()
tmp_img = pygame.image.load(f"img/button/star_1.png").convert_alpha()
t_w = img.get_width()
t_h = img.get_height()
star_1_img = pygame.transform.scale(tmp_img, (int(t_w * 0.3), int(t_h * 0.15)))
tmp_img = pygame.image.load(f"img/button/star_2.png").convert_alpha()
t_w = img.get_width()
t_h = img.get_height()
star_2_img = pygame.transform.scale(tmp_img, (int(t_w * 0.3), int(t_h * 0.15)))
tmp_img = pygame.image.load(f"img/button/star_3.png").convert_alpha()
t_w = img.get_width()
t_h = img.get_height()
star_3_img = pygame.transform.scale(tmp_img, (int(t_w * 0.3), int(t_h * 0.15)))
star_img = star_1_img


# ---------------METHOD--------------------------------
def draw_text(text, font, text_col, x, y):
    img_text = font.render(text, True, text_col)
    screen.blit(img_text, (x, y))


def show_info():
    draw_text('Money: ' + str(castle.money) + '$', font_20, BLACK, 10, 10)
    draw_text('Score: ' + str(castle.score), font_20, BLACK, 10, 35)
    draw_text('High_score: ' + str(high_score), font_20, BLACK, 10, 60)
    draw_text('LEVEL: ' + str(level), font_20, BLACK, (SCREEN_WIDTH // 2 - 60), 10)
    draw_text('HP: ' + str(castle.health) + "/" + str(castle.max_health), font_30, BLACK, SCREEN_WIDTH - 230,
              SCREEN_HEIGHT - 50)
    draw_text('1000', font_20, BLACK, SCREEN_WIDTH - 200, 70)
    draw_text('500', font_20, BLACK, SCREEN_WIDTH - 70, 70)
    if len(tower_group) < max_towers:
        draw_text(str(TOWER_COST), font_20, BLACK, SCREEN_WIDTH - 135, 70)
    else:
        draw_text('MAX', font_20, BLACK, SCREEN_WIDTH - 135, 70)
    if star_number < 2:
        draw_text(str((star_number + 1) * 10000), font_20, BLACK, SCREEN_WIDTH - 273, 70)
        draw_text('Lv >' + str((star_number + 1) * 5), font_20, BLACK, SCREEN_WIDTH - 268, 90)
    else:
        draw_text('MAX', font_20, BLACK, SCREEN_WIDTH - 268, 70)


# Castle class
class Castle:

    def __init__(self, image100, image50, image25, x, y, scale, star_nb):
        self.health = 1000 + star_nb * 1000
        self.max_health = self.health
        self.fired = False
        # Nếu là nâng cấp thì các chỉ số sẽ ko đc khởi tạo lại mà tính toán dựa trên đã có
        if star_nb != 0:
            self.money = castle.money - (star_nb + 1) * 10000
            self.score = castle.score
        else:
            self.money = 5000000
            self.score = 0

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (
            int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self):
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0]
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1] > 70:
            self.fired = True
            bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
            bullet_group.add(bullet)
        if not pygame.mouse.get_pressed()[0]:
            self.fired = False

    def draw(self):
        if self.health <= 250:
            self.image = self.image25
        elif self.health <= 500:
            self.image = self.image50
        else:
            self.image = self.image100

        screen.blit(self.image, self.rect)

    def repair(self):
        if self.money >= 1000 and self.health < self.max_health:
            self.health += 500
            self.money -= 1000
            if castle.health > castle.max_health:
                castle.health = castle.max_health

    def update_castle(self, star_nb):
        if self.money >= 10000:
            self.health += 1000
            self.money -= 10000 * (star_nb + 1)
            castle.health = castle.max_health
            self.max_health = self.health

    def armour(self):
        if self.money >= 500:
            self.max_health += 250
            self.money -= 500


class Tower(pygame.sprite.Sprite):
    def __init__(self, image100, image50, image25, x, y, scale):
        pygame.sprite.Sprite.__init__(self)

        self.got_target = False
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
        self.image = self.image100
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, group):
        self.got_target = False
        for monter in group:
            if monter.alive:
                target_x, target_y = monter.rect.midbottom
                self.got_target = True
                break

        if self.got_target:
            x_dist = target_x - self.rect.midleft[0]
            y_dist = -(target_y - self.rect.midleft[1])
            self.angle = math.degrees(math.atan2(y_dist, x_dist))

            shot_cooldown = 1000
            if pygame.time.get_ticks() - self.last_shot > shot_cooldown:
                bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
                bullet_group.add(bullet)
                self.last_shot = pygame.time.get_ticks()

        if castle.health <= 250:
            self.image = self.image25
        elif castle.health <= 500:
            self.image = self.image50
        else:
            self.image = self.image100


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 8

        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    def update(self):
        if self.rect.right < 0 \
                or self.rect.left > SCREEN_WIDTH \
                or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        self.rect.x += self.dx
        self.rect.y += self.dy


class Crosshair:
    def __init__(self, scale):
        image = pygame.image.load('img/button/crosshair.png')
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        self.rect.center = (mx, my)
        screen.blit(self.image, self.rect)


# castle

castle = Castle(castle_list[star_number][0], castle_list[star_number][1],
                castle_list[star_number][2], SCREEN_WIDTH - 250, SCREEN_HEIGHT - 400, 0.2, star_number)
# Creat crosshair
crosshair = Crosshair(0.025)
# button
repair_button = button.Button(SCREEN_WIDTH - 140, 10, repair_img, 0.5)
tower_button = button.Button(SCREEN_WIDTH - 200, 10, tower_img, 0.5)
armour_button = button.Button(SCREEN_WIDTH - 75, 10, armour_img, 0.5)
music_button = button.Button(9, SCREEN_HEIGHT - 110, music_on_img, 0.5)
start_button = button.Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20, start_img, 0.4)
exit_button = button.Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 100, exit_img, 0.4)
resume_button = button.Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 20, resume_img, 0.4)
restart_button = button.Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 60, restart_img, 0.4)
save_button = button.Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 20, save_img, 0.4)
pause_button = button.Button(8, SCREEN_HEIGHT - 60, pause_img2, 0.5)
update_castle_button = button.Button(SCREEN_WIDTH - 270, 10, update_castle_img, 0.5)
# Create groups
tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
# bullet
bullet_img = pygame.image.load('img/button/bullet.png').convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 0.075), int(b_h * 0.075)))

# gameplay
high_score = 0
level = 1
level_difficulty = 0
DIFFICULTY_MULTIPLIER = 1.3
target_difficulty = 1000
game_over = True
game_pause = False
game_menu = True
game_music = True
next_level = False
last_score = 0
run = True
if os.path.exists('score.txt'):
    with open('score.txt', 'r+') as file:
        high_score = int(file.read())
if not os.path.exists('data.txt'):
    with open('data.txt', 'w+') as file:
        file.write(str(1) + '\n')
        file.write(str(0) + '\n')
        file.write(str(0) + '\n')
        file.write(str(1000) + '\n')
        file.write(str(0) + '\n')
        file.write(str(0) + '\n')
# MUSIC------------------------------------
music_types = ['music/battle_bg1.mp3', 'music/battle_bg2.mp3', 'music/battle_bg3.mp3']
mixer.music.load('music/background0.mp3')
mixer.music.play(-1)
# -----------------------------------------------------------------------------------------------------
while run:
    clock.tick(FPS)
    if game_menu:
        screen.blit(bg, (0, 0))
        crosshair.draw()
        draw_text("CASTLE", font_70, BLACK, SCREEN_WIDTH // 2 - 150, 50)
        draw_text("DEFENSER", font_70, BLACK, SCREEN_WIDTH // 2 - 190, 150)
        if start_button.draw(screen):
            bg = pygame.image.load(map_types[m]).convert_alpha()
            mixer.music.load('music/battle_bg1.mp3')
            mixer.music.play(-1)
            game_menu = False
            game_over = False
        if resume_button.draw(screen):
            if os.path.exists('data.txt'):
                with open('data.txt', 'r') as file:
                    level = int(file.readline())
                    castle.money = int(file.readline())
                    castle.score = int(file.readline())
                    target_difficulty = int(file.readline())
                    m = int(file.readline())
                    star_number = int(file.readline())
            bg = pygame.image.load(map_types[m]).convert_alpha()
            mixer.music.load('music/battle_bg1.mp3')
            mixer.music.play(-1)
            castle = Castle(castle_list[star_number][0], castle_list[star_number][1],
                            castle_list[star_number][2], SCREEN_WIDTH - 250, SCREEN_HEIGHT - 400, 0.2, star_number)
            if star_number == 1:
                star_img = star_2_img
            if star_number == 2:
                star_img = star_3_img
            game_menu = False
            game_over = False
        if restart_button.draw(screen):
            level = 1
            m = 0
            target_difficulty = 1000
            level_difficulty = 0
            last_enemy = pygame.time.get_ticks()
            enemy_group.empty()
            boss_group.empty()
            tower_group.empty()
            castle.score = 0
            castle.health = 1000
            castle.max_health = castle.health
            castle.money = 0
            number_boss = 0
            create_boss = False
            check = False
            # pygame.mouse.set_visible(False)
            bg = pygame.image.load(map_types[m]).convert_alpha()
            mixer.music.load(music_types[m])
            mixer.music.play(-1)
            game_menu = False
            game_over = False
        if exit_button.draw(screen):
            run = False
    #         ---------------------------------------------------------
    if not game_over and not game_pause:
        # screen
        screen.blit(bg, (0, 0))
        # draw castle
        castle.draw()
        castle.shoot()
        # draw tower
        tower_group.draw(screen)
        # cập nhật tính hình của tower
        tower_group.update(enemy_group)
        tower_group.update(boss_group)
        # vẽ crosshair
        crosshair.draw()
        # draw bullets
        bullet_group.update()
        bullet_group.draw(screen)
        # enemise
        enemy_group.update(screen, castle, bullet_group)
        # xuất boss ra màn hình
        boss_group.update(screen, castle, bullet_group)
        # hiển thị các thông tin
        show_info()
        screen.blit(star_img, (330, 40))
        # update castle
        if update_castle_button.draw(screen):
            if castle.money > 10000 * (star_number + 1) and star_number < 2 and level >= 5 * (star_number + 1):
                star_number += 1
                castle.update_castle(star_number)
                if star_number == 1:
                    star_img = star_2_img
                if star_number == 2:
                    star_img = star_3_img
                castle = Castle(castle_list[star_number][0], castle_list[star_number][1],
                                castle_list[star_number][2], SCREEN_WIDTH - 250, SCREEN_HEIGHT - 400, 0.2, star_number)
        #
        if pause_button.draw(screen):
            pygame.mixer.music.pause()
            game_pause = True
        #
        if music_button.draw(screen):
            if game_music:
                music_button = button.Button(9, SCREEN_HEIGHT - 110, music_off_img, 0.5)
                game_music = False
                pygame.mixer.music.pause()
            else:
                game_music = True
                music_button = button.Button(9, SCREEN_HEIGHT - 110, music_on_img, 0.5)
                pygame.mixer.music.unpause()
        #
        if repair_button.draw(screen):
            castle.repair()
        #
        if tower_button.draw(screen):
            if castle.money >= TOWER_COST and len(tower_group) < max_towers:
                tower = Tower(
                    tower_list[star_number][0],
                    tower_list[star_number][1],
                    tower_list[star_number][2],
                    tower_positions[len(tower_group)][0],
                    tower_positions[len(tower_group)][1],
                    0.2
                )
                tower_group.add(tower)
                TOWER_COST = len(tower_group) * 1000 + 5000
                castle.money -= TOWER_COST
        #
        if armour_button.draw(screen):
            castle.armour()

        # quá trình tạo enemy
        if level_difficulty < target_difficulty:
            if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
                e = random.randint(0, len(enemy_types) - 1)
                enemy = Enemy(enemy_health[e], enemy_animations[e], - 100, SCREEN_HEIGHT - 230, 1)
                enemy_group.add(enemy)
                last_enemy = pygame.time.get_ticks()
                level_difficulty += enemy_health[e]

        if level % 3 == 0 and level_difficulty >= target_difficulty and check == True and create_boss == False:
            number_boss = level // 3
            check = False
        if not check:
            enemies_alive = len(enemy_group)
            for e in enemy_group:
                if not e.alive:
                    enemies_alive -= 1
            draw_text(str(enemies_alive), font_30, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            if enemies_alive == 0:
                mixer.music.load('music/battle_boss.mp3')
                mixer.music.play(-1)
                create_boss = True
                check = True
                last_boss = pygame.time.get_ticks()
        # spawn boss
        if create_boss and number_boss > 0:
            draw_text('WARNING!', font_30, BLACK, 290, 300)
            if pygame.time.get_ticks() - last_boss > BOSS_TIMER:
                b = 0
                boss = Boss(boss_health[b], boss_animations[b], -  100, SCREEN_HEIGHT - 330, 1)
                boss_group.add(boss)
                number_boss -= 1
                last_boss = pygame.time.get_ticks()
                
        if create_boss and number_boss == 0:
            tmp = 0
            boss_alive = 0
            for b in boss_group:
                if b.alive:
                    boss_alive += 1
            if boss_alive == 0:
                create_boss = False
                boss_group.empty()
        # next level
        if create_boss == False and level_difficulty >= target_difficulty:
            enemies_alive = 0
            for e in enemy_group:
                if e.alive:
                    enemies_alive += 1
            if enemies_alive == 0 and next_level == False:
                next_level = True
                level_reset_time = pygame.time.get_ticks()
        if next_level:
            create_boss = False
            number_boss = 0
            draw_text("LEVEL COMPLETED", font_30, BLACK, 220, 250)
            draw_text("NEXT LEVEL!", font_30, BLACK, 270, 300)
            last_score = castle.score
            if castle.score > high_score:
                high_score = castle.score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            if pygame.time.get_ticks() - level_reset_time > 1500:
                next_level = False
                level += 1
                last_enemy = pygame.time.get_ticks()
                target_difficulty = int(target_difficulty * DIFFICULTY_MULTIPLIER)
                level_difficulty = 0
                enemy_group.empty()
                if m > 1:
                    m = random.randint(0, len(map_types) - 1)
                else:
                    m += 1
                bg = pygame.image.load(map_types[m]).convert_alpha()
                mixer.music.load(music_types[m])
                mixer.music.play(-1)
                
        if castle.health <= 0:
            game_over = True
    elif game_over and not game_menu:
        draw_text('GAME OVER!', font_30, BLACK, 270, 280)
        draw_text('PRESS "A" TO PLAY AGAIN!', font_30, BLACK, 150, 350)
        pygame.mouse.set_visible(True)
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            game_over = False
            level = 1
            target_difficulty = 1000
            level_difficulty = 0
            last_enemy = pygame.time.get_ticks()
            enemy_group.empty()
            boss_group.empty()
            tower_group.empty()
            castle.score = 0
            castle.health = 1000
            castle.max_health = castle.health
            castle.money = 0
            number_boss = 0
            create_boss = False
            check = False
            star = 0
    elif game_pause:
        # screen
        screen.blit(bg, (0, 0))
        screen.blit(star_img, (330, 40))
        # draw button and ------
        castle.draw()
        tower_group.draw(screen)
        crosshair.draw()
        bullet_group.draw(screen)
        repair_button.draw(screen)
        tower_button.draw(screen)
        update_castle_button.draw(screen)
        pause_button = button.Button(8, SCREEN_HEIGHT - 60, pause_img, 0.5)
        if pause_button.draw(screen):
            pause_button = button.Button(8, SCREEN_HEIGHT - 60, pause_img2, 0.5)
            pygame.mixer.music.unpause()
            game_pause = False
        armour_button.draw(screen)
        music_button.draw(screen)
        show_info()
        # ----------------------
        if resume_button.draw(screen):
            pygame.mixer.music.unpause()
            game_pause = False
        if restart_button.draw(screen):
            game_pause = False
            pause_button = button.Button(8, SCREEN_HEIGHT - 60, pause_img2, 0.5)
            level = 1
            target_difficulty = 1000
            level_difficulty = 0
            last_enemy = pygame.time.get_ticks()
            enemy_group.empty()
            boss_group.empty()
            tower_group.empty()
            castle.score = 0
            castle.health = 1000
            castle.max_health = castle.health
            castle.money = 0
            number_boss = 0
            create_boss = False
            check = False
            star_number = 0
            
        if exit_button.draw(screen):
            run = False
        if save_button.draw(screen):
            with open('data.txt', 'w+') as file:
                file.write(str(level) + '\n')
                file.write(str(castle.money) + '\n')
                file.write(str(last_score) + '\n')
                file.write(str(target_difficulty) + '\n')
                file.write(str(m) + '\n')
                file.write(str(star_number) + '\n')
            draw_text("SAVED", font_30, BLACK, 340, 240)
    # event in game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and not game_menu:
                if not game_pause:
                    pygame.mixer.music.pause()
                if game_pause:
                    pause_button = button.Button(8, SCREEN_HEIGHT - 60, pause_img2, 0.5)
                    pygame.mixer.music.unpause()
                if game_pause:
                    game_pause = False
                else:
                    game_pause = True

            if event.key == pygame.K_m:
                if game_music:
                    game_music = False
                    music_button = button.Button(9, SCREEN_HEIGHT - 110, music_off_img, 0.5)
                    pygame.mixer.music.pause()
                else:
                    game_music = True
                    pygame.mixer.music.unpause()
                    music_button = button.Button(9, SCREEN_HEIGHT - 110, music_on_img, 0.5)
    pygame.display.update()
pygame.quit()
