# Game Version: Ver 1.1

import pygame
import time

# Imports pygame and time modules.

pygame.mixer.pre_init(44100, -16, 2, 512)
# pre-initializes the mixer, this is done to prevent delayed sounds.

pygame.init()
# Initializes pygame

clock = pygame.time.Clock()
# Sets the clock for pygame which will maintain a steady FPS of 60.

screen_size = (1200, 800)
# defines the screen size as a variable
screen = pygame.display.set_mode(screen_size, 0, 32)
# sets screen size using above variable, also sets flags and depth?
display = pygame.Surface((600, 400))
# surface that is going to be scaled up to make everything bigger. (size is half of that of the window.)

pygame.display.update()
# updates display
pygame.display.set_caption("Wanderlust")
icon = pygame.image.load("sprites/Game_Icon.png")
pygame.display.set_icon(icon)
# sets caption, loads and sets icon.

player_image = pygame.image.load("sprites/idle/idle_0.png")
# Loads placeholder player image
grass_image = pygame.image.load("sprites/tiles/small grass block.png")
# loads grass tile image
dirt_image = pygame.image.load("sprites/tiles/small dirt block.png")
# loads dirt tile image
sky_image = pygame.image.load("sprites/sky.png")
# loads sky image
tile_size = grass_image.get_width()
# this will be used for blitting values in the map to the correct spots on screen.
fullHeart = pygame.image.load("sprites/hearts/other half.png")
# loads right half of heart image
halfHeart = pygame.image.load("sprites/hearts/Half Heart.png")
# loads left half of heart image
halfHeart = pygame.transform.scale(halfHeart, (halfHeart.get_width() * 2, halfHeart.get_height() * 2))
fullHeart = pygame.transform.scale(fullHeart, (fullHeart.get_width() * 2, fullHeart.get_height() * 2))
# doubles the size of the half and full hearts.
pygame.mixer.music.load("audio/Amynedd - Hero's Run.wav")
# loads the music
pygame.mixer.music.set_volume(0.015)
# sets the volume very low since it was quite loud
pygame.mixer.music.play(-1)
# music plays infinitely.
falling_sound = pygame.mixer.Sound("audio/sfx/falling sound effect.wav")
# falling sound is loaded.
pygame.mixer.Sound.set_volume(falling_sound, 0.15)
# sets the volume very low since it was quite loud
footstep_sound = pygame.mixer.Sound("audio/sfx/footstep_1.wav")
# footstep sound is loaded.
pygame.mixer.Sound.set_volume(footstep_sound, 0.015)
# sets the volume very low since it was quite loud
jump_sound = pygame.mixer.Sound("audio/sfx/jump_1.wav")
# jump sound is loaded.
pygame.mixer.Sound.set_volume(jump_sound, 0.02)
# sets the volume very low since it was quite loud
game_over_font = pygame.font.SysFont("arial", 42)
# game over font is loaded.
game_over = game_over_font.render("Game Over", True, (255, 255, 255))
# game over text is rendered.
congratulations_font = pygame.font.SysFont("arial", 42)
# congratulations font is loaded,
congratulations = congratulations_font.render("You Win!", True, (0, 0, 0))
# congratulations text is rendered.
# (game over and win texts are loaded.)
global frames
# creates a global frame variable, will be used for later.
frames = {}
# it will be a dictionary.


def animation_load(path, duration):
    # loads animations. The path would be the folder name, and the duration is a list of how many frames each image goes for.
    global frames
    # loads the global variable
    animation_name = path.split("/")[-1]
    # the animation's name is made,
    # splits the path by the slash.
    frame_data = []
    # a list of the frame data is created. ex: [idle_1, idle_1, idle_1, idle_2, idle_2, idle_2]
    n = 0
    # the n variable is used for frame IDs. It is added to in the for loop, and is a numerical marker that is added to the end of the IDs.
    for frame in duration:
        # iterates through the duration parameter. ex: [30, 30] would be 30 frames for each image in the sequence, before it is repeated.
        frame_id = animation_name + "_" + str(n)
        # creates an ID for the frame, to be used later.
        image_location = "sprites/" + path + "/" + frame_id + ".png"
        # full image location is made, to be used in loading.
        image = pygame.image.load(image_location)
        # loads the individual image from the image's location.
        image.set_colorkey((150, 150, 150))
        # all of the images have a gray background that will be keyed out. Had to add this because of a visual bug with transparent images.
        frames[frame_id] = image.copy()
        # this dictionary contains the frame IDs.
        for z in range(frame):
            # creates the actual list that contains the sequence of frames.
            frame_data.append(frame_id)
        n += 1
    return frame_data
# frame data is returned.


def changeState(action, frame, new):
    # this function allows the state of the player to be changed. (the state is defined later.)
    if action != new:
        # if the state is a new one, it gets replaced with the new one, and the frame is set to 0.
        action = new
        frame = 0
    return action, frame
# the new action and frame is returned.


anim_database = {'idle': animation_load("idle", [30, 30]), 'runRight': animation_load("runRight", [10, 10, 10, 10]),
                 'jump_idle_down': animation_load("jump_idle_down", [5]),
                 'jump_idle_up': animation_load("jump_idle_up", [5]),
                 'jump_right_down': animation_load("jump_right_down", [5]),
                 'jump_right_up': animation_load("jump_right_up", [5])}
# the database with all of the animations inside of it is created. It uses the function to load all of the animation and give them proper frame data.

flipped = False
# the variable specifying if the player's sprite is flipped to face the left or not is defined.
player_state = "idle"
# the player's default state is idle.
player_frame = 0
# the player's frame is set to 0.


def displayHealth(value):
    for n in range(value):
        # basically, displays the 2 halves of the heart multiple times depending on what the player's health (the value parameter) is equal to.
        if n == 0:
            display.blit(halfHeart, (5, 5))
        if n == 1:
            display.blit(fullHeart, (19, 5))
        if n == 2:
            display.blit(halfHeart, (39, 5))
        if n == 3:
            display.blit(fullHeart, (53, 5))
        if n == 4:
            display.blit(halfHeart, (73, 5))
        if n == 5:
            display.blit(fullHeart, (87, 5))


def loadMap(path):
    # loads the game map from a .txt file. The path includes the first part of the file's name.
    f = open(path + '.txt')
    # the txt file is opened. The .txt suffix is added to it.
    data = f.read()
    # the text file is read, this data is stored in a variable called data.
    f.close()
    # the txt file is closed, now that we have the data we need.
    data = data.split('\n')
    # the txt file is split from one string into multiple strings, one for each line.
    game_map = []
    for row in data:
        game_map.append(list(row))
    # the data is made into a list of lists; one list for each line of values.
    return game_map


game_map = loadMap('map')
# parameter is 'map' because the map file is called map.txt
# this allows me to potentially implement multiple levels in the future if I wanted to load a certain map.
# 0 = nothing, 1 = dirt, 2 = grass.
# in future, I plan on making the tiles 16x16 pixels instead of 32x32 pixels so that I can create a more detailed map.


def collision_test(rect, tiles):
    # function to test collision
    collision_list = []
    # list that stores all collisions is created.
    for tile in tiles:
        # goes through all tiles and checks if the rect in the parameters is colliding with any tiles. If so, they are appended on the list.
        # done in this way so that enemy collisions can also be detected in a similar manner.
        if rect.colliderect(tile):
            collision_list.append(tile)
    return collision_list


# the final, updated collision list is returned.


def move(rect, movement, tiles):
    # function that will move the player. It will first go through x collisions and then y collisions, handling one axis at a time.
    collision_types = {
        'top': False,
        'bottom': False,
        'right': False,
        'left': False
    }
    # a dictionary containing the types of collisions is created. These values will be changed to True if the entity is colliding in a certain direction.
    rect.x += movement[0]
    # The entity's rect (indicated in parameters) is moved based on the first value in the list, the x change.
    collision_list = collision_test(rect, tiles)
    # collision list is updated based on the result of a collision test, performed by the previous function.
    for tile in collision_list:
        if movement[0] > 0:
            # if the rect is moving right, the dictionary is updated so that the collision type 'right' is true.
            # we now know which way to move the rect if we need to account for a collision. (left)
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            # if the rect is moving left, the dictionary is updated so that the collision type 'left' is true.
            # to account for a collision, we can move the rect in the opposite direction. (right)
            rect.left = tile.right
            collision_types['left'] = True
    rect.y = int(rect.y + movement[1])
    # now moves the rect based on y change.
    # converted to an integer to avoid implicit conversion and to prevent visual bugs from occurring.
    collision_list = collision_test(rect, tiles)
    for tile in collision_list:
        if movement[1] > 0:
            # if the rect is moving downwards, the dictionary is updated so that the collision type 'bottom' is true.
            # to account for a collision, we can move the rect in the opposite direction. (upwards)
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            # elif the rect is moving downwards, the dictionary is updated so that the collision type 'top' is true.
            # to account for a collision, we can move the rect in the opposite direction. (downwards)
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def oobTest(rect, data):
    # tests if the player is out of bounds. parameters are specified rect and the list of out of bounds tiles.
    oob_collision_list = []
    # list of all points where the player collides with an out of bounds tile.
    global out_of_bounds
    # creates a global out of bounds boolean variable.
    out_of_bounds = False
    for tiles in data:
        # iterates through tiles
        if rect.colliderect(tiles):
            # appends the collision list (the list is obsolete now since I only need the boolean but it is still useful for understanding the code and such)
            oob_collision_list.append(tiles)
            out_of_bounds = True
            # out of bounds becomes true.
    return oob_collision_list
# returns the list


moving_right = False
moving_left = False
# these 2 variables will determine if the player is moving left or right.
scroll = [0, 0]
# scroll variable is defined.
playerVisible = True
# the boolean determining if the player should be visible is defined.
player_yMomentum = 0
# vertical momentum variable is defined.
airTimer = 0
# Tracks how long the player has been in the air, allowing them to jump slightly after falling off of a platform. (QoL feature)
health = 6
# player health is defined.
player_Rect = pygame.Rect(350, 100, player_image.get_width(), player_image.get_height())
# Updates hitbox locations
boundary_list = []
# empty boundary list is created.
displayHealth(health)
# display health function is called.
checkpoint = [350, 100]
# default checkpoint is set.
out_of_bounds = False
# out of bounds is set to false.
invisibleFrames = 0
# the amount of frames the player has been invisible for is set to 0.
invincibilityFrames = 0
# unused so far
invisibilityPeriod = False
# the invisibilityPeriod boolean is used to toggle the period after falling out of the stage where the player becomes visible and invisible briefly.
footstep_timer = 0
# timer for footsteps timing is set to 0.
gameEnd = False
# when true, the game ends.
lose = False
# determines if the player has died.
win = False
# determines if the player reaches the end.
# game loop
while not gameEnd:
    display.blit(sky_image, (0, 0))
    # sky background image is blitted to screen.
    scroll[0] -= (player_Rect.x + scroll[0] - 286) / 12
    # x scroll is set so that it mostly focuses in on the player, with a little delay until it centers fully after the player has stopped moving.
    # allows for dynamic camera movement, makes the game more fluid.
    scroll[1] -= (player_Rect.y + scroll[1] - 190) / 12
    # same is done with y scroll.
    tile_Rects = []
    # a rect list is created, will store hitbox locations.
    boundary_list = []
    y = 0
    # sets y to 0
    for row in game_map:
        x = 0
        # resets X since we have moved to the next row.
        for tile in row:
            # goes through the row horizontally.
            if tile == "1":
                # the value 1 in the list represents a dirt block.
                display.blit(dirt_image, (x * tile_size + int(scroll[0]), y * tile_size + int(scroll[1])))
                # blits the dirt block at the x and y coordinates * the width and height of the image, with the scroll added to it.
                # the scroll values become integers to avoid implicit conversion, as well as to avoid visual bugs.
            if tile == "2":
                # the value 2 in the list represents a grass block.
                display.blit(grass_image, (x * tile_size + int(scroll[0]), y * tile_size + int(scroll[1])))
                # blits the grass block at the x and y coordinates * the width and height of the image, with the scroll added to it.
                # the scroll values become integers to avoid implicit conversion, as well as to avoid visual bugs.
            if tile == "5":
                boundary_list.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            if tile != "0" and tile != "5":
                # if the tile isn't equal to nothing, the rect list is appended.
                tile_Rects.append(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size))
            x += 1
        # adds 1 to the x, so that the next column is read.
        y += 1
    # adds 1 to the y, so that the next row down is read.
    if footstep_timer > 0:
        # if the footstep sound is playing at the moment, it decreases by 1 each frame.
        footstep_timer -= 1
    if airTimer > 5:
        # if the player's air timer exceeds 5 (it is set to 5 every time the player jumps due to the fact that you can still jump 5 frames after leaving a platform),
        # the footstep sound is stopped.
        footstep_timer = 0
        pygame.mixer.Sound.stop(footstep_sound)

    player_movement = [0, 0]
    # keeps track of intended movement for the player.
    if moving_right:
        player_movement[0] += 3
    if moving_left:
        player_movement[0] -= 3
    # x movement is handled: x value decreases when moving left, increases when moving right
    player_movement[1] += player_yMomentum
    # player's y momentum is added to the second coordinate of player movement, the y value.
    player_yMomentum += 0.23
    # gravity is added to
    if player_yMomentum > 5:
        player_yMomentum = 5
    # maximum velocity (gravity) is set so that if the player is falling faster than 4 pixels per frame, it is automatically changed to 4 pixels per frame.
    if player_movement[0] > 0:
        # if the player is moving right, the state is changed to runRight.
        player_state, player_frame = changeState(player_state, player_frame, "runRight")
        flipped = False
    elif player_movement[0] < 0:
        # if the player is moving left, the state is changed to runRight, and it is flipped.
        player_state, player_frame = changeState(player_state, player_frame, "runRight")
        flipped = True
    elif player_movement[0] == 0:
        # if the player is not moving left or right, the state is changed to idle.
        player_state, player_frame = changeState(player_state, player_frame, "idle")
        flipped = False
    if airTimer > 5:
        if player_movement[0] > 0:
            # if the player is moving right, and they are also moving right...
            if player_movement[1] < 0:
                # if they are moving upwards, the state is changed to jump_right_up
                player_state, player_frame = changeState(player_state, player_frame, "jump_right_up")
                flipped = False
            else:
                # if they are moving downwards, the state is changed to jump_right_up
                player_state, player_frame = changeState(player_state, player_frame, "jump_right_down")
                flipped = False
        if player_movement[0] == 0:
            # if the player is not moving left or right...
            if player_movement[1] < 0:
                # if they are moving upwards, the state is changed to jump_idle_up
                player_state, player_frame = changeState(player_state, player_frame, "jump_idle_up")
                flipped = False
            else:
                # if they are moving downwards, the state is changed to jump_idle_down
                player_state, player_frame = changeState(player_state, player_frame, "jump_idle_down")
                flipped = False
        if player_movement[0] < 0:
            # if the player is moving left...
            if player_movement[1] < 0:
                # if they are moving upwards, the state is changed to jump_right_up, and flipped = True
                player_state, player_frame = changeState(player_state, player_frame, "jump_right_up")
                flipped = True
            else:
                # if they are moving upwards, the state is changed to jump_right_down, and flipped = True
                player_state, player_frame = changeState(player_state, player_frame, "jump_right_down")
                flipped = True
    player_frame += 1
    # one new frame is added to the animation processing.
    if player_frame >= len(anim_database[player_state]):
        player_frame = 0
        # if the player has finished a certain animation, is is reset and they perform the animation again
    frame_id = anim_database[player_state][player_frame]
    # the frame ID is set to the current frame.
    player_image = frames[frame_id]
    # the player's image, which is blitted to the scree, is determined by the frame ID of the current frame.
    player_Rect, collisions = move(player_Rect, player_movement, tile_Rects)
    # the move function is called upon to handle collisions with solid tiles and move the player.
    oobTest(player_Rect, boundary_list)
    # the oobTest function tests if the player is colliding with any of the out-of-bounds tiles.
    if out_of_bounds:
        # the player loses 1 health.
        health -= 1
        player_Rect.x = checkpoint[0]
        # the player is teleported to the x and y of the checkpoint. (the last place they were grounded)
        player_Rect.y = checkpoint[1]
        falling_sound.play()
        # plays the falling sound effect.
        invisibilityPeriod = True
        # invisibility period starts.
        invisibleFrames = 0
        # frames of invisibility is set to 0. This is to ensure that if the player falls off of the world again before the animation is done, that it will still work.
        playerVisible = False
        # player is set to invisible (will not be blitted.)
    if invisibilityPeriod and invisibleFrames < 60:
        # if the player invisibility period is occurring, and the frames of invisibility is less than 60...
        playerVisible = False
        # the player is not blitted to the screen.
        invisibleFrames += 1
        # 1 invisibility frame is added.
        # what is happening below is that every 10 frames, the player is becoming visible (flashing in and out of visibility)
        if 10 < invisibleFrames <= 20:
            playerVisible = True
        elif 30 < invisibleFrames <= 40:
            playerVisible = True
        elif 50 < invisibleFrames <= 60:
            playerVisible = True
        else:
            playerVisible = False
            # if it is not one of those visibility periods, the player is invisible again.
    else:
        invisibilityPeriod = False
        # the invisibility period is ended.
        playerVisible = True
        # the player becomes visible again.
        invisibleFrames = 0
    if collisions['bottom']:
        airTimer = 0
        # air timer is reset when player touches the ground.
        player_yMomentum = 0
        # player's y momentum is set to 0; they stop falling.
        checkpoint = [player_Rect.x, player_Rect.y]
        # the checkpoint is set for the player. It is set every time that the player is safely grounded.
        if player_movement[0] != 0:
            if footstep_timer == 0:
                # if the player is moving left or right and the footstep timer is set to 51 (it counts down)
                # this is because the sound takes about 50.5 frames to play
                footstep_sound.play()
                footstep_timer = 51
        else:
            pygame.mixer.Sound.stop(footstep_sound)
            # if not, it stops the sound (when the player is not moving left or right.)
            footstep_timer = 0
    else:
        airTimer += 1
        # air timer is incremented if the player is in the air.
    if collisions['top']:
        # if the player hits the ceiling, they will begin to fall. Their upward momentum is cancelled.
        player_yMomentum = 0
    if playerVisible:
        display.blit(pygame.transform.flip(player_image, flipped, False),
                     (player_Rect.x + int(scroll[0]), player_Rect.y + int(scroll[1])))
    # renders player image onto screen, flips them if the flipped variable is true.
    # the scroll values become integers to avoid implicit conversion, as well as to avoid visual bugs.
    keys = pygame.key.get_pressed()
    # sees what keys are pressed to determine if the space bar is being held.
    if keys[pygame.K_SPACE]:
        if airTimer < 5:
            player_yMomentum = -6
            # allows the player 5 frames after falling off of a platform where they can still jump if they are late in their timing.
            jump_sound.play()
            airTimer = 5
            # sets the air timer to 5 so that they cannot get any extra boost to their jump by holding the button.
    for event in pygame.event.get():
        # processes all events.
        if event.type == pygame.QUIT:
            # quits pygame and the program if the X is pressed on window.
            pygame.quit()
            quit()
        # handles keyboard inputs, changes the directions in which the player is moving based on input.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False
    displayHealth(health)
    # health is displayed.
    if player_Rect.x > 2750:
        win = True
    if health == 0:
        # if the player, dies, game over is set to true, and the game loop stops.
        lose = True
        gameEnd = True
    if win:
        gameEnd = True
        # if the player wins, the game is ended.
    surf = pygame.transform.scale(display, screen_size)
    # scales the "display" to the screen size
    screen.blit(surf, (0, 0))
    # blits the upscaled display to the window.
    pygame.display.update()
    # updates display.
    clock.tick(60)
    # one frame is processed.

# after the game is over:
if lose:
    # if they lost, screen turns black, player image is blitted, and the game over text is displayed.
    display.fill((0, 0, 0))
    display.blit(player_image, (379, 271))
    display.blit(game_over, (100, 100))
    surf = pygame.transform.scale(display, screen_size)
    # scales the "display" to the screen size
    screen.blit(surf, (0, 0))
    # blits the upscaled display to the window.
    pygame.display.update()
    # updates display.
    time.sleep(3)
    # waits 3 seconds and ends the program.
if win:
    # if they lost, screen turns white, player image is blitted, and the congratulations text is displayed.
    display.fill((255, 255, 255))
    display.blit(player_image, (379, 271))
    display.blit(congratulations, (100, 100))
    surf = pygame.transform.scale(display, screen_size)
    # scales the "display" to the screen size
    screen.blit(surf, (0, 0))
    # blits the upscaled display to the window.
    pygame.display.update()
    # updates display.
    time.sleep(3)
    # waits 3 seconds, then ends the program.
