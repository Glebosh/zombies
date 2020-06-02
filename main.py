import pygame as pg
import sys
from settings import *
from sprites import *
from tilemap import *
from os import path


def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = GREEN
    if pct <= 0.6:
        col = YELLOW
    if pct <= 0.3:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.level = 0
        self.next_level = False
        self.win = False
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map_folder = path.join(game_folder, 'maps')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        #self.map = Map(path.join(game_folder, 'map3.txt'))
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.start_screen = pg.image.load(path.join(img_folder, START_SCREEN)).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_images = {}
        for wpn in WEAPONS:
            self.player_images[wpn] = pg.image.load(path.join(img_folder, WEAPONS[wpn]['image_wpn'])).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_imges = {}
        self.bullet_imges['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_imges['sm'] = pg.transform.scale(self.bullet_imges['lg'], (8, 8))
        self.mm9_img = pg.image.load(path.join(img_folder, '9mm_ammo_32.png')).convert_alpha()
        #self.mm9_img = pg.transform.scale(self.mm9_img, (16, 16))
        self.mm12_img = pg.image.load(path.join(img_folder, 'shotgun_ammo_32.png')).convert_alpha()
        #self.mm12_img = pg.transform.scale(self.mm12_img, (16, 16))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img1 = pg.image.load(path.join(img_folder, MOB_IMG1)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # Эффект ночного освещения
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # Загрузка музыки
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effect_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effect_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.3)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.3)
            self.player_hit_sounds.append(s)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.3)
            self.zombie_hit_sounds.append(s)

    def new(self):
        # инициализируйте все переменные и выполните все настройки для новой игры
        self.map = TiledMap(path.join(self.map_folder, LEVELS[self.level]))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        player_x = 10
        player_y = 10
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == "1":
        #             Wall(self, col, row)
        #         if tile == "M":
        #             Mob(self, col, row)
        #         if tile == "P":
        #             self.player = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                if not self.next_level:
                    self.player = Player(self, obj_center.x, obj_center.y)
                else:
                    self.player._layer = PLAYER_LAYER
                    self.player.groups = self.all_sprites
                    pg.sprite.Sprite.__init__(self.player, self.player.groups)
                    self.player.game = self
                    self.player.image = self.player_img
                    self.player.rect = self.player.image.get_rect()
                    self.player.rect.center = (obj_center.x, obj_center.y)
                    self.player.hit_rect = PLAYER_HIT_RECT
                    self.player.hit_rect.center = self.player.rect.center
                    self.player.vel = vec(0, 0)
                    self.player.pos = vec(obj_center.x, obj_center.y)  # * TILESIZE
                    self.player.rot = 0
                    self.player.last_shot = 0
                    self.player.health = PLAYER_HEALTH
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name in ITEM_LIST:
                Item(self, obj_center, tile_object.name)

        #self.player = Player(self, 5, 5)
        print(self.map.width, self.map.height)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.pause = False
        self.night = False
        self.night_spawn = pg.time.get_ticks()
        self.effect_sounds['level_start'].play()

    def run(self):
        # игровой цикл - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.pause:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # обновление всех элементов игры
        self.all_sprites.update()
        self.camera.update(self.player)
        # game over
        if len(self.mobs) == 0:
            self.playing = False
            self.level += 1
            self.next_level = True
            if self.level > len(LEVELS) - 1:
                self.next_level = False
                self.win = True
        # подбираем предметы
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effect_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effect_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
                if 2 in self.player.take_weapon:
                    self.player.take_weapon[2] += WEAPONS[self.player.weapon]['ammo_count']
                else:
                    self.player.take_weapon[2] = WEAPONS[self.player.weapon]['ammo_count']
                self.player.weapon_type = 2
                #self.player.take_weapon.append(2)
            if hit.type == '9mm':
                if 1 in self.player.take_weapon:
                    hit.kill()
                    self.effect_sounds['gun_pickup'].play()
                    self.player.take_weapon[1] += 40
            if hit.type == '12mm':
                if 2 in self.player.take_weapon:
                    hit.kill()
                    self.effect_sounds['gun_pickup'].play()
                    self.player.take_weapon[2] += 32
            if hit.type == 'portal':
                self.playing = False
                self.level += 1
                self.next_level = True
                if self.level > len(LEVELS) - 1:
                    self.next_level = False
                    self.win = True
        # повреждение игрока
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # убийство мобов
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            hit.vel = vec(0, 0)
        if pg.time.get_ticks() - self.night_spawn > LIGHT_SPAUN:
            self.night = not self.night
            self.night_spawn = pg.time.get_ticks()

        self.player_img = self.player_images[self.player.weapon]

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # рисование затемнения и света
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0,0), special_flags=pg.BLEND_MULT)


    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(wall.rect), 1)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # pg.draw.rect(self.screen, WHITE, self.camera.apply(....), 2)
        # self.all_sprites.draw(self.screen)
        if self.night:
            self.render_fog()
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text("Zombie: {}".format(len(self.mobs)), self.hud_font, 30, WHITE, WIDTH - 10, 10, align="ne")
        i = 0
        for tp, ammo in self.player.take_weapon.items():
            if tp == 1:
                self.screen.blit(self.mm9_img, (10, 50 + i))
            if tp == 2:
                self.screen.blit(self.mm12_img, (10, 50 + i))
            self.draw_text(str(ammo), self.hud_font, 20, WHITE, 18, 50 + i)
            i += 30
        if self.pause:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    def events(self):
        # обработка событий - мышь, клавиатура
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.pause = not self.pause
                if event.key == pg.K_n:
                    self.night = not self.night
                    self.night_spawn = pg.time.get_ticks()
                if event.key == pg.K_1:
                    if 1 in self.player.take_weapon:
                        self.player.weapon_type = 1
                        self.player.weapon = 'pistol'
                if event.key == pg.K_2:
                    if 2 in self.player.take_weapon:
                        self.player.weapon = 'shotgun'
                        self.player.weapon_type = 2

    def show_start_screen(self):
        self.screen.blit(self.start_screen, (0,0))
        self.draw_text("ZOMBIE GAME!!!", self.title_font, 105, RED, WIDTH / 2, HEIGHT * 1 / 8, align='center')
        self.draw_text("Press a key to start new game. esc - EXIT", self.title_font, 45, WHITE, WIDTH / 2,
                       HEIGHT * 7 / 8, align='center')
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        if self.win:
            self.draw_text("YOU WIN!!!!", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 3, align='center')
            self.level = 0
        else:
            self.draw_text("GAME OVER", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 3, align='center')
        self.draw_text("Press a key to start new game. esc - EXIT", self.title_font, 45, WHITE, WIDTH / 2, HEIGHT * 3/4, align='center')
        pg.display.flip()
        self.wait_for_key()

    def show_level(self):
        self.screen.fill(BLACK)
        self.draw_text(f"Level {self.level + 1}", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 3, align="center")
        self.draw_text("Press a key to start. ESC - exit", self.title_font, 45, WHITE, WIDTH / 2,
                       HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                if event.type == pg.KEYUP:
                    waiting = False



if __name__ == '__main__':
    # создаем новый объект - Игра
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.show_level()
        g.run()
        if not g.next_level:
            g.show_go_screen()
