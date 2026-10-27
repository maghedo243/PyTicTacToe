import pygame
import torch

import AI.Agent as agent
from AI.Agent import DQN

from table import Table
from util import tablePos, turnState

agent.initAgent()


pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("TicTacToe")
clock = pygame.time.Clock()

running = True
dt = 0

table = Table()
turn = turnState.X
i = 0

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i,x in enumerate(table.posRects):
                if x.collidepoint(event.pos):
                    if turn == turnState.X and table.markTable("X",tablePos.fromTableIndex(i)):
                        turn = turnState.O
                        i = 0

    winner = table.winCheck()

    if winner != "unfinished":
        running = False

    if turn == turnState.O and running:
        i += 1
        state = table.get_obs()
        state = torch.tensor(state, dtype=torch.float32, device="cpu").unsqueeze(0)
        if i < 200 and table.markTable("O",agent.smartMove("X",state)):
            turn = turnState.X
        elif table.markTable("O",agent.nextMove("X",state)) or table.markTable("O",agent.nextMove("X",state,"smart")):
            turn = turnState.X

    winner = table.winCheck()

    if winner != "unfinished":
        running = False

    screen.fill("darkgray")

    table.drawTable(screen)

    pygame.display.flip()



    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

print("WINNER IS", winner)
pygame.quit()