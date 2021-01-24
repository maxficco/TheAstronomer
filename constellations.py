import pygame, sys

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Constellations")
WINDOW_SIZE = (1000, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
CANVAS_SIZE = (500, 300)
display = pygame.Surface((CANVAS_SIZE))
print(CANVAS_SIZE[0])

gameRunning = True

tile1 = pygame.image.load("tile1.png")
tile2 = pygame.image.load("tile2.png")
tile5 = pygame.image.load("tile5.png")
tile6 = pygame.image.load("tile6.png")
sprite1 = pygame.image.load("sprite1.png")
sprite2 = pygame.image.load("sprite2.png")
spritebox = pygame.Rect(300,175, 12,16)
mainframe = sprite1

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

moving_left = False
moving_right = False
vertical_momentum = 0
airtimer = 0

scroll = [0,0]

def test_collisions(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles, vertical_momentum):
    collision_types = {"top": False, "bottom": False, "left": False, "right": False}
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
            rect.x = 300
            rect.y = 175
            break
    return rect, collision_types, vertical_momentum

while gameRunning:
# Reset display surface to gray
    display.fill((160,150,255))

# Change Scroll
    scrollchangex = int((spritebox.x-scroll[0])-(CANVAS_SIZE[0]/2))/20
    scrollchangey = int((spritebox.y-scroll[1])-(CANVAS_SIZE[1]/2))/20
    scroll[0] += scrollchangex
    scroll[1] += scrollchangey
    print(scrollchangex)

# Pygame Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
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
                if airtimer < 10:
                    vertical_momentum = -3.125
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
    

# Draw Background Objects
    pygame.draw.circle(display, (200,179,2), (190-scroll[0]/25,125+scroll[1]/20), 50) #(The Sun)
    pygame.draw.rect(display, (52,45,145), (0,150,500,150))
    pygame.draw.rect(display, (100,100,100), (0,220,500,150))



# Draw Tiles and Map Rects
    tile_rects = []
    y = 0
    for row in game_map:
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
        player_movement[0] -= 1
    if moving_right == True:
        player_movement[0] += 1
    # gravity
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.125
    if vertical_momentum > 3:
        vertical_momentum = 3


    spritebox, collision_types, vertical_momentum = move(spritebox, player_movement, tile_rects, vertical_momentum)
    
    if collision_types["bottom"] == True:
        vertical_momentum = 0
        airtimer = 0
    else:
        airtimer += 1

    display.blit(mainframe, (spritebox.x-scroll[0], spritebox.y-scroll[1]))

# Draw and update display
    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0,0))
    pygame.display.update()
# Time Delay
    clock.tick(105)
    print(int(clock.get_fps()))
