import torch 
from torch.autograd import Variable
from torchvision.datasets import MNIST
import torch.optim as optim
import pandas as pd 
import numpy as np
from ast import literal_eval

def pad_component_arrays(x, upper_lim):
    input_x = np.array(x)
    output_x = []
    for array in input_x:
        array += [0]*(upper_lim-len(array))
        output_x.append(array)
    return np.array(output_x)

def load_data(train=True):
    if train:
        data = pd.read_csv('ImageTopologyDataset.csv')
    else:
        data = pd.read_csv('ImageTopologyTesting.csv')
    train_x = data['ImageStructure'].values
    train_y = Variable(torch.from_numpy(data['ImageLabels'].values), requires_grad=False)
    train_x = list(map(literal_eval, train_x))
    # upper_lim = max([len(x) for x in train_x])
    upper_lim = 750
    train_x = list(map(torch.from_numpy, pad_component_arrays(train_x, upper_lim)))
    train_x = list(map(Variable, [x.float() for x in train_x]))
    return train_x, train_y, upper_lim

train_x, train_y, upper_lim = load_data(train=True)
# test_data = MNIST(root='.', train=False, transform=ToTensor(), download=False)
# load_test = DataLoader(test_data, batch_size=100, shuffle=True)
N, D_in, H, D_out = len(train_x), upper_lim, int(upper_lim/2), 10 
model = torch.nn.Sequential(torch.nn.Linear(D_in, H), torch.nn.ReLU(), torch.nn.Linear(H, D_out))
# model = torch.load('firsttry.pt')
loss = torch.nn.CrossEntropyLoss()
learning_rate = 1e3
optim = optim.Adam(model.parameters(), lr=learning_rate)
for i in range(2000):
    for ind, image in enumerate(train_x):
        image = image.view(1, upper_lim)
        y_pred = model(image)
        lossed = loss(y_pred, train_y[ind])
        print(i, lossed.data[0])
        optim.zero_grad()
        lossed.backward()
        optim.step()
        for param in model.parameters():
            param.data -= learning_rate * param.grad.data
    	        
        if i%200 == 0:
            print("Error:" + str(lossed))
torch.save(model, 'firsttry.pt')

test_x, test_y, _ = load_data(train=False)
test_x, test_y = test_x[:10], test_y[:10] # test only the first ten images
for index, img in enumerate(test_x):
    y_pred = model(img)
    y_true = test_y[ind]
    print(y_pred, y_true)
