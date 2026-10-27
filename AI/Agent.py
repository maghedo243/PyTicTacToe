import math
import random
import time

import numpy

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class DQN(nn.Module):
    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)


xModel = None
xSmartModel = None
xMergedModel = None
oModel = None
oSmartModel = None
oMergedModel = None

BATCH_SIZE = 128
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 1000
TAU = 0.005

_action_to_location = {
    0: "1A",
    1: "1B",
    2: "1C",
    3: "2A",
    4: "2B",
    5: "2C",
    6: "3A",
    7: "3B",
    8: "3C"
}


def initAgent():
    print("Initializing Models...")
    global xModel, xSmartModel, xMergedModel, oModel, oSmartModel, oMergedModel
    checkpointX = torch.load('AI/TicTacModelX.pth')
    checkpointO = torch.load('AI/TicTacModelO.pth')
    checkpointXE = torch.load('AI/TicTacModelSmartTrainX.pth')
    checkpointOE = torch.load('AI/TicTacModelSmartTrainO.pth')
    checkpointXM = torch.load('AI/TicTacModelXMerged.pth')
    checkpointOM = torch.load('AI/TicTacModelOMerged.pth')

    # Instantiate the model using the saved architecture
    xModel = checkpointX['model_architecture']
    oModel = checkpointO['model_architecture']
    xSmartModel = checkpointXE['model_architecture']
    oSmartModel = checkpointOE['model_architecture']
    xMergedModel = checkpointXM['model_architecture']
    oMergedModel = checkpointOM['model_architecture']

    # Load the saved state_dict to populate the model's weights
    xModel.load_state_dict(checkpointX['model_state_dict'])
    oModel.load_state_dict(checkpointO['model_state_dict'])
    xSmartModel.load_state_dict(checkpointXE['model_state_dict'])
    oSmartModel.load_state_dict(checkpointOE['model_state_dict'])
    xMergedModel.load_state_dict(checkpointXM['model_state_dict'])
    oMergedModel.load_state_dict(checkpointOM['model_state_dict'])
    xModel.eval()
    xModel.to("cpu")
    xSmartModel.eval()
    xSmartModel.to("cpu")
    xMergedModel.eval()
    xMergedModel.to("cpu")
    oModel.eval()
    oModel.to("cpu")
    oSmartModel.eval()
    oSmartModel.to("cpu")
    oMergedModel.eval()
    oMergedModel.to("cpu")
    print("Models Loaded")


def nextMove(playerSymbol: str, state, mode="normal"):
    with torch.no_grad():
        match playerSymbol:
            case "X":
                return _action_to_location[oModel(state).max(1)[1].view(1, 1).item()] if mode == "normal" else _action_to_location[oSmartModel(state).max(1)[1].view(1, 1).item()]
            case "O":
                return _action_to_location[xModel(state).max(1)[1].view(1, 1).item()] if mode == "normal" else _action_to_location[xSmartModel(state).max(1)[1].view(1, 1).item()]


def smartMove(playerSymbol: str, state):
    with torch.no_grad():
        match playerSymbol:
            case "X":
                return _action_to_location[oMergedModel(state).max(1)[1].view(1,1).item()]
