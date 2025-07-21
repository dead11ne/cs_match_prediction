# imports
import torch
import pandas as pd
import torch.nn as nn
import torch.optim as opt
import torchvision.transforms as transforms
import torch.utils.data.dataloader as dataloader

# transformer
transform = transforms.Compose(
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) 
)

# dataset
dataloader = dataloader.DataLoader(
    dataset='final_cleared.csv',
    batch_size=128,
    shuffle=True
)

# claas of NN
class MyNet(nn.Module):
    # def of initialization 
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(64, 32),
            nn.Sigmoid(),
            nn.Dropout(p=0.2),
            nn.Linear(32, 16),
            nn.Sigmoid(),
            nn.Dropout(p=0.1),
            nn.Linear(16, 1)
        )
    # def of forward pass    
    def forward(self, x):
        return self.layers(x)
    
model = MyNet()
criterion = nn.BCELoss()
optimizer = opt.Adam(params=model.parameters(), lr=0.0003)