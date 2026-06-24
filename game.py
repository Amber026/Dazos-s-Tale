# import the PyGame library
import pygame
import random
from pygame.locals import *

# initialise PyGame
pygame.init()
pygame.display.set_caption("Platformer")

# settings
HEIGHT = 750
WIDTH = 1200
FPS = 60
LEFT_RIGHT_MOVE = 5

# the clock and display surface
FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))

# the Target Sprite
class Target(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((30, 184, 30))
        self.rect = self.surf.get_rect(center = position)

# the Player Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 15,15 is the width and height
        self.surf = pygame.Surface((15, 15))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()
        self.rect.midbottom = (200, 225)

# the Platform Sprite
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, position, colour = (255,0,0)):
        super().__init__()
        self.surf = pygame.Surface((width, 20))
        self.surf.fill(colour)
        self.rect = self.surf.get_rect(center = position)

platform_1 = Platform(100, (200, 500))
platform_2 = Platform(50, (400, 600))
platform_3 = Platform(120, (600, 600))
platform_4 = Platform(190, (800, 550))
platform_5 = Platform(160, (1000, 500))
platform_6 = Platform(WIDTH, (WIDTH/2, HEIGHT), (0, 0, 255))

# has it landed?
def has_landed(player:Player, platform:Platform)->bool:
    return (
        player.rect.right > platform.rect.left and
        player.rect.bottom >= platform.rect.top and
        player.rect.top < platform.rect.top and
        player.rect.left < platform.rect.right
    )

# has it bumped?
def has_bumped(player:Player, platform:Platform)->bool:
    return (
        player.rect.right > platform.rect.left and
        player.rect.top < platform.rect.bottom and
        player.rect.bottom > platform.rect.bottom and
        player.rect.left < platform.rect.right
    )

# visible elements
all_sprites = pygame.sprite.Group()

T = Target((1000, 450))
all_sprites.add(T)

P1 = Player()
all_sprites.add(P1)
all_sprites.add(platform_1)
all_sprites.add(platform_2)
all_sprites.add(platform_3)
all_sprites.add(platform_4)
all_sprites.add(platform_5)
all_sprites.add(platform_6)

all_platforms = pygame.sprite.Group()
all_platforms.add(platform_1)
all_platforms.add(platform_2)
all_platforms.add(platform_3)
all_platforms.add(platform_4)
all_platforms.add(platform_5)
all_platforms.add(platform_6)

speed_y = 0
on_target = False

timer_interval = 60000 # 0.5 seconds
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event , timer_interval)

txt = police.render
running = True

# the game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == timer_event:
            print("test")
            running = False

    if on_target:
        background_colour = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    else:
        background_colour = (0, 0, 0)

    displaysurface.fill(background_colour)

    # move the player left/right
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        P1.rect.left -= LEFT_RIGHT_MOVE
    if keys[K_RIGHT]:
        P1.rect.right += LEFT_RIGHT_MOVE

    # stop at the edge
    if P1.rect.left < 0:
        P1.rect.left = 0
    if P1.rect.right > WIDTH:
        P1.rect.right = WIDTH

    # has it landed on a platform?
    player_has_landed = False
    for platform in all_platforms:
        if has_bumped(P1, platform):
            P1.rect.top = platform.rect.bottom
            speed_y = 0
            break
        if has_landed(P1, platform):
            P1.rect.bottom = platform.rect.top
            speed_y = 0
            player_has_landed = True
            break

    if player_has_landed:
        # if player has landed we can also jump
        if keys[K_UP]:
            speed_y = -8
            P1.rect.bottom -= 1
    else:
        # if player hasn't landed they are effected by gravity
        P1.rect.bottom += speed_y
        speed_y += 0.5

    # reached the target?
    on_target = T.rect.contains(P1.rect)

    # draw all visible elements
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    pygame.display.update()
    FramePerSec.tick(FPS)