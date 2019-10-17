import pygame
from pygame.locals import *
from Classes import *

pygame.init()

##### SCREEN #####
SCREEN_DIMEN = 500
MAX_SCREEN_EDGE = SCREEN_DIMEN - 20
MARGIN = 10
screen = pygame.display.set_mode((SCREEN_DIMEN, SCREEN_DIMEN))

##### COLOR CONSTANTS #####
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
RED = (255, 0, 0)

##### BOOLEANS #####
running = True          #Program is running?
roomChange = True       #Scene was changed?
playerOneWin = False    #Player 1 won?

##### OBJECTS #####
food = Food(GREEN)
player_1 = Player(BLACK, 0, 0, "right")
player_2 = Player(RED, MAX_SCREEN_EDGE, MAX_SCREEN_EDGE, "left")

##### IMAGE VARIABLES #####
one_play = Image("button_1.png", 100, 270, 125)
two_play = Image("button_2.png",
                 one_play.y + one_play.boundingRect.height + 3 * MARGIN,
                 270, 125)
game_over = Image("game_over.jpg", 50, SCREEN_DIMEN,
                  int(SCREEN_DIMEN * 2 / 5))
restart = Image("restart.png", 250, 100, 100)

##### TEXT VARIABLES
fontObj = pygame.font.Font('minecraft.ttf', 32)
one_text = fontObj.render("One", True, WHITE)
two_text = fontObj.render("Two", True, WHITE)
player_text = fontObj.render("Player", True, WHITE)
play_one_win_text = fontObj.render("Player 1 Wins!", False, WHITE)
play_two_win_text = fontObj.render("Player 2 Wins!", False, WHITE)

##### MISC VARIABLES #####
room = 0        #What scene to display
numPlayer = 0   #The number of players
timer = 300     #A timer to slow down the snake's movement


##### GAME LOOP #####
while running:
    
    #For all possible events (keyboard input, mouse input, etc.)
    for event in pygame.event.get():
            
        #Close the pygame window if the X was pressed.
        if event.type == pygame.QUIT:
            running = False
            continue
        
        #If a keyboard key was pressed
        elif event.type == pygame.KEYDOWN:

            #If ESC was pressed, close the pygame window
            if event.key == pygame.K_ESCAPE:
                running = False
                continue

            #If playing game
            if room == 1:

                #Player 1 controls
                if event.key == pygame.K_UP and player_1.direction != "down":
                    player_1.direction = "up"
                elif event.key == pygame.K_DOWN and player_1.direction != "up":
                    player_1.direction = "down"
                elif event.key == pygame.K_LEFT and player_1.direction != "right":
                    player_1.direction = "left"
                elif event.key == pygame.K_RIGHT and player_1.direction != "left":
                    player_1.direction = "right"

                #Player 2 controls
                if event.key == pygame.K_w and player_2.direction != "down":
                    player_2.direction = "up"
                elif event.key == pygame.K_s and player_2.direction != "up":
                    player_2.direction = "down"
                elif event.key == pygame.K_a and player_2.direction != "right":
                    player_2.direction = "left"
                elif event.key == pygame.K_d and player_2.direction != "left":
                    player_2.direction = "right"

        #If the left mouse button was clicked
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            #If currently in game intro screen
            if room == 0:

                #If the one player button was clicked
                if one_play.checkClicked(event.pos[0], event.pos[1]):
                    numPlayer = 1
                    room = 1

                #If the two player button was clicked
                elif two_play.checkClicked(event.pos[0], event.pos[1]):
                    numPlayer = 2
                    room = 1
                
            #If currently in game over screen
            elif room == 2:

                #If the restart button was clicked
                if restart.checkClicked(event.pos[0], event.pos[1]):
                    food.resetPos()
                    player_1.resetPlayer()
                    player_2.resetPlayer()
                    timer = 300
                    numPlayer = 0
                    room = 0
                    roomChange = True

    #If in the game intro scene (only need to update scene once)
    if room == 0 and roomChange:

        #Draw the background and the buttons
        screen.fill(BLACK)
        one_play.draw(screen)
        two_play.draw(screen)

        #Draw "One"
        textBoundingRect = one_text.get_rect()
        textX = ((one_play.boundingRect.width - textBoundingRect.width) / 2) + one_play.x
        oneTextY = one_play.y + 3 * MARGIN
        screen.blit(one_text, (textX, oneTextY))

        #Draw "Two"
        textBoundingRect = two_text.get_rect()
        textX = ((two_play.boundingRect.width - textBoundingRect.width) / 2) + two_play.x
        twoTextY = two_play.y + 3 * MARGIN
        screen.blit(two_text, (textX, twoTextY))
        
        #Draw "Player
        textBoundingRect = player_text.get_rect()

        #Draw for One Player
        textX = ((one_play.boundingRect.width - textBoundingRect.width) / 2) + one_play.x
        screen.blit(player_text, (textX, oneTextY + 4 * MARGIN))

        #Draw for One Player
        textX = ((two_play.boundingRect.width - textBoundingRect.width) / 2) + two_play.x
        screen.blit(player_text, (textX, twoTextY + 4 * MARGIN))

        #Update the screen
        pygame.display.update()
        roomChange = False

    #If in playing game
    elif room == 1:
        
        '''Another keyboard solution, not for repl.it
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            move = "up"
        elif pressed[pygame.K_DOWN]:
            move = "down"
        elif pressed[pygame.K_LEFT]:
            move = "left"
        elif pressed[pygame.K_RIGHT]:
            move = "right"
        '''

        #Player 1 died?
        died = False

        #Check if player 1 went out of bounds
        died = player_1.checkBoundary(0, MAX_SCREEN_EDGE, 0, MAX_SCREEN_EDGE)
        if died:
            room = 2
            roomChange = True
            playerOneWin = False
            continue

        #Check if player 1 collided with its body
        died = player_1.checkSelfDestroy()
        if died:
            room = 2
            roomChange = True
            playerOneWin = False
            continue

        #Check if player 1 ate the food
        eat = player_1.eatFood(food.getPos())
        if eat:
            food.resetPos()

            #Make the game run faster
            if timer > 200:
                timer -= 20
            elif timer > 100:
                timer -= 10
                
        #Move player 1
        player_1.moveBody()

        #If there are two players
        if numPlayer == 2:

            #Player 2 died?
            died = False

            #Check if player 2 went out of bounds
            died = player_2.checkBoundary(0, MAX_SCREEN_EDGE, 0, MAX_SCREEN_EDGE)
            if died:
                room = 2
                roomChange = True
                playerOneWin = True
                continue

            #Check if player 2 collided with its body
            died = player_2.checkSelfDestroy()
            if died:
                room = 2
                roomChange = True
                playerOneWin = True
                continue

            #Check if player 1 ate the food
            eat = player_2.eatFood(food.getPos())
            if eat:
                food.resetPos()

                #Make the game run faster
                if timer > 200:
                    timer -= 20
                elif timer > 100:
                    timer -= 10

            #Move player 1
            player_2.moveBody()

        #All drawing code
        screen.fill(WHITE)
        food.draw(screen)
        player_1.draw(screen)

        #If there are two players
        if numPlayer == 2:
            player_2.draw(screen)
            
        pygame.display.update()
        pygame.time.wait(timer)

    #If in game over screen
    elif room == 2 and roomChange:
        screen.fill(BLACK)
        game_over.draw(screen)
        restart.draw(screen)

        #If there are two players, draw the text for the winning player
        if numPlayer == 2:

            #If player 1 won
            if playerOneWin:
                textBoundingRect = play_one_win_text.get_rect()
                textX = (SCREEN_DIMEN - textBoundingRect.width) / 2
                screen.blit(play_one_win_text, (textX, 200))

            #If player 2 won
            else:
                textBoundingRect = play_two_win_text.get_rect()
                textX = (SCREEN_DIMEN - textBoundingRect.width) / 2
                screen.blit(play_two_win_text, (textX, 200))
        
        pygame.display.update()
        roomChange = False
        
pygame.quit()            
