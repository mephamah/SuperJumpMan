import pygame, sys, os
from pygame.locals import *
from character_functions import *
from loading_functions import *
from gameloop_functions import *

# initiates pygame
pygame.init() 

# initiates screen and 1/2 scale 'display'
pygame.display.set_caption('Super Jump Man')
WINDOW_SIZE = (600,400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300,200))

# initialize scoll tracker
true_scroll = [0,0]

# load tile images and map array
grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
game_map = load_map('map')
tile_rects = []
for y, layer in enumerate(game_map):
    for x, tile in enumerate(layer):
        if tile != '0':
            tile_rects.append(pygame.Rect(x*16,y*16,16,16))

# create background objects
# background_object = [scrollrate, [xpos, ypos], surface]

background_objects = [
    [0.25, [120, 10], pygame.Surface((70, 400))],
    [0.25, [280,30], pygame.Surface((40, 400))],
    [0.5, [30,40], pygame.Surface((40, 400))],
    [0.5,[130,90], pygame.Surface((100, 400))],
    [0.5,[300,80], pygame.Surface((120, 400))]
    ]

for background_object in background_objects:
    background_object[2].fill((9,91,85))


# initialize all character variables
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
player_action = 'idle'
player_frame = 0
player_flip = False

# prepare character hitbox and animations
player_rect = pygame.Rect(100,100,5,13)
animation_frames = {}
animation_database = {}
animation_database['run'] = load_animation(animation_frames,'player_animations/run',[7,7])
animation_database['idle'] = load_animation(animation_frames,'player_animations/idle',[7,7,40])

# create clock object for controlling framerate
clock = pygame.time.Clock()



# ------------------------------Game Loop-------------------------------------
while True: 
    
    #update scroll tracker
    true_scroll, scroll = update_scrolls(player_rect, true_scroll)

    # create solid background
    display.fill((146,244,255))

    # add unmoving (infinite distance) background objects
    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))

    # add middle-distance background objects
    for background_object in background_objects:
        display.blit(background_object[2], (background_object[1][0] - background_object[0]*scroll[0], background_object[1][1] - background_object[0]*scroll[1]))

    for y, layer in enumerate(game_map):
        for x, tile in enumerate(layer):
            if tile == '1':
                display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
            if tile == '2':
                display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))


    # determine player speed for this frame
    player_movement, vertical_momentum = update_player_movement(moving_right, moving_left, vertical_momentum)

    # update player facing
    if player_movement[0] > 0:
        player_flip = False
    if player_movement[0] < 0:
        player_flip = True

    # update player action
    player_action, player_frame = update_player_action(player_movement, player_action, player_frame)

    # move player and determine collisions
    player_rect,collisions = move(player_rect,player_movement,tile_rects)

    # check if player is on the ground or in the air, update relevant variables
    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    # determine correct character animation frame    
    player_frame = update_framecount(player_frame, animation_database[player_action])

    # update character onto display
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))

    # check for user input
    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    vertical_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
    
    # update screen
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()

    # wait in order to ensure 60 fps
    clock.tick(60)
