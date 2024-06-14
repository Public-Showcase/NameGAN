# PyTorch
import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np
import string

# Hyperparameters
max_length = 12
num_layers = 1
hidden_size = 50
num_chars = 27

# Utils
char_to_id = {c:i for i, c in enumerate(string.ascii_lowercase + ".")}
id_to_char = {v:k for k, v in char_to_id.items()}

class Model(nn.Module):
    
    def __init__(self, input_size, hidden_size, output_size, num_layers):
        super(Model, self).__init__() # initializing inherited class Module

        # sizes
        self.input_size = input_size
        self.hidden_size = hidden_size # number of neurons in LSTM, (higher val => higher overfitting)
        self.num_layers = num_layers # # number of recurrent (LSTM) layers

        # LSTM layer
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)

        # fully connected layers
        self.fc_1 = nn.Linear(hidden_size, output_size)
        self.fc_2 = nn.Linear(output_size, output_size)
        
    def forward(self, X, states):
        ht, ct = states # hidden state and the cell state of LSTM

        batch_size = X.size(0)

        out, (ht, ct) = self.lstm(X, (ht, ct))

        out = self.fc_1(out)
        out = F.relu(out) # ReLU is used to avoid vanishing gradient problem
        out = self.fc_2(out)

        return out, (ht, ct) # out: Size([batch_size, max_length, num_chars])

#
# Loading saved model
#
path = "name_generator_LSTM.pth"
model = Model(input_size=num_chars, hidden_size=hidden_size, output_size=num_chars, num_layers=num_layers)
model = nn.DataParallel(model)
model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))


def generate_new_name(start='j', k=5):
    """
    model: trained model
    start: string to start name with, bydefaule it's 'j'
    k: the model selects the top 'k' probable characters from the output and randomly selects one from them as the next character
    """
    
    # Not generating names longer than max_length (here 12)
    if len(start) >= max_length:
        return name
    
    with torch.no_grad(): # since no need to compute gradients for following operations
        
        # initializing hidden and cell states
        ht = torch.zeros((num_layers, 1, hidden_size))
        ct = torch.zeros((num_layers, 1, hidden_size))

        length = 0
        name = start
        
        for char in start:
            X = torch.zeros((1, 1, num_chars)) # initializing one-hot encoded vector, [batch_size, timestep, num_chars]
            X[0, 0, char_to_id[char]] = 1 # one-hot encoding

            out, (ht, ct) = model(X, (ht, ct)) # generating next character

            length += 1

        vals, idxs = torch.topk(out[0], k) # top k most probable characters

        idx = np.random.choice(idxs.cpu().numpy()[0]) # selecting 1 of top k character randomnly
        char = id_to_char[idx]
        
        while char != "." and length <= max_length-1:
            X = torch.zeros((1, 1, num_chars)) # [batch_size, timestep, num_chars]
            X[0, 0, char_to_id[char]] = 1
            
            out, (ht, ct) = model(X, (ht, ct))
            
            vals, idxs = torch.topk(out[0], k) # 0 -> first eg in a batch
            idx = np.random.choice(idxs.cpu().numpy()[0]) # 0 -> first...
            char = id_to_char[idx]
            
            length += 1
            name += char
    
        # if name[-1] != ".":
        #     name += "."
    
    return name
