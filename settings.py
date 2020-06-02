import pygame as pg
vec = pg.math.Vector2


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (100, 64, 15)

# game settings
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Зомби атакуют"
BGCOLOR = BROWN   #  DARKGREY

# установки tile
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'

# установки для Player
PLAYER_SPEED = 250
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 40, 40)
BARREL_OFFSET = vec(30,10)
PLAYER_HEALTH = 100

# установки для мобов-зомби
MOB_IMG = 'zombie1_hold.png'
MOB_IMG1 = 'robot1_hold.png'
MOB_SPEED = [200, 150, 125, 100, 75]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 10
AVOID_RADIUS = 50
DETECTED_RADIUS = 400

# уровни
LEVELS = ['level1.tmx', 'level2.tmx']

# установки для оружия (выстрел)
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1,
                     'ammo_count': 15,
                     'image_wpn': 'manBlue_gun.png'}
WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12,
                      'ammo_count': 8,
                      'image_wpn': 'manBlue_machine.png'}

# BULLET_LIFETIME = 1000
# BULLET_SPEED = 500
# BULLET_RATE = 150
# KICKBACK = 100
# GUN_SPREAD = 5
# BULLET_DAMAGE = 10

# Эффекты
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
FLASH_DURATION = 40
SPLAT = 'splat green.png'
DAMAGE_ALPHA = [i for i in range(0,255,55)]

NIGHT_COLOR = (10, 10, 10)
LIGHT_RADIUS = (600, 500)
LIGHT_MASK = "light_350_soft.png"
LIGHT_SPAUN = 30000
START_SCREEN = 'PdUIuh.jpg'
# Слои спрайтов
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEM_LAYER = 1

# Предметы
ITEM_IMAGES = {'health': 'health_pack.png',
               'shotgun': 'obj_shotgun.png',
               '9mm': '9mm_ammo_32.png',
               '12mm': 'shotgun_ammo_32.png',
               'portal': 'portal.png'}
ITEM_LIST = ['health', 'shotgun', '9mm', '12mm', 'portal']
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 20
BOB_SPEED = 0.6

# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS_GUN = ['pistol.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                'shotgun': ['shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav'}


