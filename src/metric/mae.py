import torch

def mae(y, yhat):
    return torch.mean(torch.abs(yhat - y))