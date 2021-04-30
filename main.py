import pygame
from pygame.font import Font

import ai
import sys
import time

pygame.init()

# set size, colors, and fonts
size = width, height = 600, 400
gray = (224, 224, 224)
black = (64, 64, 64)
background_color = (0, 76, 153)
title_color = (0, 0, 0)
screen = pygame.display.set_mode(size)
largeFont = pygame.font.Font('Ubuntu-Bold.ttf', 40)
regularFont = pygame.font.Font('Ubuntu-Regular.ttf', 30)


def play():
    user = None
    board = ai.initial()
    ai_turn = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(background_color)

        # start game
        if user is None:
            # title
            title = largeFont.render("Play Tic-Tac-Toe", True, (255, 255, 255))
            title_rect = title.get_rect()
            title_rect.center = ((width / 2), (height / 3))
            screen.blit(title, title_rect)

            # buttons
            X_button = pygame.Rect((width/8), (height/2), width/4, 50)
            X_text = regularFont.render("Play X", True, gray)
            X_rect = X_text.get_rect()
            X_rect.center = X_button.center
            pygame.draw.rect(screen, black, X_button)
            screen.blit(X_text, X_rect)

            O_button = pygame.Rect(5*(width / 8), (height / 2), width / 4, 50)
            O_text = regularFont.render("Play O", True, gray)
            O_rect = O_text.get_rect()
            O_rect.center = O_button.center
            pygame.draw.rect(screen, black, O_button)
            screen.blit(O_text, O_rect)

            # Check for user choice
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if X_button.collidepoint(mouse_pos):
                    time.sleep(0.5)
                    user = ai.X
                elif O_button.collidepoint(mouse_pos):
                    time.sleep(0.5)
                    user = ai.O
        else:
            # game board
            tile_size = 80
            tile_origin = (width/2-(1.5*tile_size), height/2-(1.5*tile_size))

            # make board
            tiles = []
            for i in range(3):
                row = []
                for j in range(3):
                    rect = pygame.Rect(
                        tile_origin[0] + j * tile_size,
                        tile_origin[1] + i * tile_size,
                        tile_size, tile_size
                    )
                    pygame.draw.rect(screen, black, rect, 3)
                    if board[i][j] is not None:
                        color = black
                        if board[i][j] == ai.O:
                            color = gray
                        else:
                            color = black
                        character = regularFont.render(board[i][j], True, color)
                        characterRect = character.get_rect()
                        characterRect.center = rect.center
                        screen.blit(character, characterRect)
                    row.append(rect)
                tiles.append(row)

            end_game = ai.terminal(board)
            player = ai.player(board)

            # draw title
            if end_game:
                # if game has ended
                winningPlayer = ai.winner(board)
                if winningPlayer is None:
                    title = f"Game Over: Tie"
                else:
                    title = f"Game Over: {winningPlayer} wins"
            elif user == player:
                # player's turn
                title = f"Play as {user}"
            else:
                # ai's turn
                title = f"AI is thinking..."
            title = largeFont.render(title, True, title_color)
            titleRect = title.get_rect()
            titleRect.center = ((width/2), 30)
            screen.blit(title, titleRect)

            # AI's turn
            if user != player and not end_game:
                if ai_turn:
                    time.sleep(0.5)
                    move = ai.minimax(board)
                    board = ai.result(board, move)
                    ai_turn = False
                else:
                    ai_turn = True

            # Player's turn
            if pygame.mouse.get_pressed()[0] and user == player and not end_game:
                mouse = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == ai.EMPTY and tiles[i][j].collidepoint(mouse):
                            board = ai.result(board, (i, j))

            if end_game:
                againButton = pygame.Rect(width/3, height - 65, width/3, 50)
                againText = regularFont.render("Play Again", True, title_color)
                againRect = againText.get_rect()
                againRect.center = againButton.center
                pygame.draw.rect(screen, gray, againButton)
                screen.blit(againText, againRect)
                if pygame.mouse.get_pressed()[0]:
                    mouse = pygame.mouse.get_pos()
                    if againButton.collidepoint(mouse):
                        time.sleep(0.3)
                        user = None
                        board = ai.initial()
                        ai_turn = False

        pygame.display.flip()


if __name__ == '__main__':
    play()
