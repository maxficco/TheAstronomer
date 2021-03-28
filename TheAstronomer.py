import pygame, sys, time, math, random
from impact_animations import *
ifeellikeit = True
# Setup
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("The Astronomer")
WINDOW_SIZE = (1000, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
CANVAS_SIZE = (500, 300)
display = pygame.Surface((CANVAS_SIZE))


titlescreen = True
gameRunning = False
endgame = False


# Images / Sprites
tile1 = pygame.image.load("tiles/tile1.png")
tile2 = pygame.image.load("tiles/tile2.png")
tile5 = pygame.image.load("tiles/tile5.png")
tile6 = pygame.image.load("tiles/tile6.png")
sprite1 = pygame.image.load("sprites/sprite1.png")
sprite2 = pygame.image.load("sprites/sprite2.png")
spritebox = pygame.Rect(300,175, 12,16)
mainframe = sprite1
checkpoint = [300, 256]

# Delta Time
prev_time = time.time()
dt = 0
TARGET_FPS = 80

tickcounter = 0

# Create Map from map.txt
def load_map():
    f = open("map.txt","r")
    data = f.read()
    f.close()
    data = data.split("\n")
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
game_map = load_map()

def make_stars(howmany,x1,x2,y1,y2):
    stars = []
    for star in range(howmany):
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)
        stars.append((x,y))
    return stars
stars = make_stars(500, 0, 500, 300, 1200)

moving_left = False
moving_right = False
vertical_momentum = 0
collision_types = {"top": False, "bottom": False, "left": False, "right": False, "death": False}
airtimer = 0
jumpcounter = 0
doublejump = True
explosion_list = []
particle_list = []
torches = []

scroll = [0,0]

def test_collisions(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles, vertical_momentum):
    collision_types = {"top": False, "bottom": False, "left": False, "right": False, "death": False}
    rect.x += movement[0]
    hit_list = test_collisions(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True 
        if movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True
    rect.y += movement[1]
    hit_list = test_collisions(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True
            vertical_momentum = 0
        if tile.height == 15:
            collision_types["death"] = True
            rect.x = checkpoint[0]
            rect.y = checkpoint[1]
            break
    return rect, collision_types, vertical_momentum 


while titlescreen:
        display.fill((100,100,100))
        for title_event in pygame.event.get():
            if title_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if title_event.type == pygame.KEYDOWN:
                titlescreen = False
                gameRunning = True

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
        pygame.display.update()
        clock.tick(200)

while gameRunning: ############################### GAME LOOP ###############################

# Reset display surface to sky color
    multiplier = spritebox.y/1500
    if multiplier <= 0:
        multiplier = 0
    if multiplier >= 1:
        multiplier = 1
    multiplier = 1 - multiplier
    display.fill((78*multiplier,122*multiplier,200*multiplier))

# Delta Time
    now = time.time()
    dt = now - prev_time
    prev_time = now

    if tickcounter == 0:
        tickcounter += 1
    else:
        tickcounter -= 1

# Change Scroll
    scroll[0] += int((spritebox.x-scroll[0])-(CANVAS_SIZE[0]/2))/20*(math.ceil(dt*TARGET_FPS))
    scroll[1] += int((spritebox.y-scroll[1])-(CANVAS_SIZE[1]/2))/20*(math.ceil(dt*TARGET_FPS))

    isonscreen = False
    if spritebox.x - scroll[0] > 0 and spritebox.x - scroll[0] < 500:
        isonscreen = True

    if collision_types["death"] == True: #If just died, stop player movement
        moving_right = False
        moving_left = False
        vertical_momentum = 0
        player_movement = [0,0]

# Pygame Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(checkpoint)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
                mainframe = sprite1
            if event.key == pygame.K_RIGHT:
                moving_right = True
                mainframe = sprite2
            if event.key == pygame.K_UP:
                if (airtimer < 25 and jumpcounter < 1)  or (doublejump == True and jumpcounter == 1 and airtimer > 25):
                    jumpcounter += 1
                    vertical_momentum = -3
                    if jumpcounter == 2:
                        particle_list.append(DoubleJump(spritebox.x+6, spritebox.y+12))
            if event.key == pygame.K_m:
                checkpoint[0] = spritebox.x
                checkpoint[1] = spritebox.y
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
# Draw Stars:
    for s in stars:
        blink = random.randint(0, 100)
        if blink != 26:
            pygame.draw.rect(display, (255,255,255), (s[0]-scroll[0]/100, s[1]-scroll[1]/4, 1, 1))

# Draw Background Objects
    pygame.draw.circle(display, (251, 90, 82), (190-scroll[0]/50,150+scroll[1]/40), 50)
    pygame.draw.rect(display, (110*multiplier, 115*multiplier, 125*multiplier), (0,150-scroll[1]/40,500,300))
    pygame.draw.rect(display, (43*multiplier, 49*multiplier, 61*multiplier), (0,220-scroll[1]/17.5,500,500))

# Draw Tiles and Map Rects
    tile_rects = []
    y = 0
    for row in game_map:
        if (y*16-scroll[1] > -16) and (y*16-scroll[1] < CANVAS_SIZE[1]):
            x = 0
            for tile in row:
                if ((x*16-scroll[0] > -16) and (x*16-scroll[0] < CANVAS_SIZE[0])) and ((y*16-scroll[1] > -16) and (y*16-scroll[1] < CANVAS_SIZE[1])):
                    if tile == "1":
                        display.blit(tile1, (x*16-scroll[0],y*16-scroll[1]))
                        tile_rects.append(pygame.Rect(x*16,y*16, 16,16))
                    if tile == "2":
                        display.blit(tile2, (x*16-scroll[0],y*16-scroll[1]))
                        tile_rects.append(pygame.Rect(x*16,y*16, 16,16))
                    if tile == "5":
                        display.blit(tile5, (x*16-scroll[0],y*16-scroll[1]))
                        tile_rects.append(pygame.Rect(x*16,y*16+1, 16,15))
                    if tile == "6":
                        display.blit(tile6, (x*16-scroll[0],y*16-scroll[1]))
                        tile_rects.append(pygame.Rect(x*16,y*16+1, 16,15))
                x += 1
        y += 1
    
# Player Movement
    player_movement = [0,0]
    if moving_left == True:
        player_movement[0] -= math.ceil(dt*TARGET_FPS)
    if moving_right == True:
        player_movement[0] += math.ceil(dt*TARGET_FPS)
    
    # gravity
    player_movement[1] += (vertical_momentum*dt*TARGET_FPS)
    vertical_momentum += 0.125*(dt*TARGET_FPS)
    if vertical_momentum > 3:
        vertical_momentum = 3

    spritebox, collision_types, vertical_momentum = move(spritebox, player_movement, tile_rects, vertical_momentum)
    
    if collision_types["bottom"] == True:
        vertical_momentum = 0
        airtimer = 0
        jumpcounter = 0
    else:
        airtimer += math.ceil(dt*TARGET_FPS)

    display.blit(mainframe, (spritebox.x-scroll[0], spritebox.y-scroll[1]))


# Torches / Lighting

    if len(torches) < 1:
        torches.append(Torch(spritebox.x, spritebox.y, random.randint(0,5)))

    for torch in torches:
        torch.shrink()
        torch.move()
        if mainframe == sprite1:
            torch.draw(display, scroll, spritebox, True, True)
        else:
            torch.draw(display, scroll, spritebox, False, True)

        if len(torch.particles) < 1:
                torches.remove(torch)

# Animations
    if collision_types["left"] == True:
        if len(explosion_list) < 1:
            explosion_list.append(Explosion(spritebox.x, spritebox.y+8))
    if collision_types["right"] == True:
        if len(explosion_list) < 1:
            explosion_list.append(Explosion(spritebox.x+12, spritebox.y+8))

    if collision_types["death"] == True:
        if len(particle_list) < 1:
            particle_list.append(Disappeario(spritebox.x+6, spritebox.y+8))
        
    if isonscreen:
        for pars in particle_list:
            pars.draw(display, scroll)
            pars.shrink()
            pars.move()
            if len(pars.particles) < 1:
                particle_list.remove(pars)
    for exp in explosion_list:
        if tickcounter == 1:
            exp.grow()
        if exp.radius > 12:
            explosion_list.remove(exp)
        else:
            exp.draw(display, scroll)

# Draw display (scaled) and update screen
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    pygame.display.update()


# Time Delay
    clock.tick(110)
    print(int(clock.get_fps()))

# Check for endgame
    if spritebox.y > 4777:
        gameRunning = False
        endgame = True

while endgame:
    display.fill((0, 0, 0))
    for title_event in pygame.event.get():
        if title_event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if title_event.type == pygame.KEYDOWN:
            endgame = False

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    pygame.display.update()
    clock.tick(110)

    