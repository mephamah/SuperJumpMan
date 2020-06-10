def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame

def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

def update_player_movement(moving_right, moving_left, vertical_momentum):
    player_movement = [0,0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3
    return player_movement, vertical_momentum

def update_player_action(player_movement, player_action, player_frame):
    if player_movement[0] == 0:
        return change_action(player_action,player_frame,'idle')
    if player_movement[0] > 0:
        player_flip = False
        return change_action(player_action,player_frame,'run')
    if player_movement[0] < 0:
        player_flip = True
        return change_action(player_action,player_frame,'run')

def update_framecount(player_frame, number_of_frames_in_action):
    player_frame += 1
    if player_frame >= len(number_of_frames_in_action ):
        player_frame = 0
    return player_frame