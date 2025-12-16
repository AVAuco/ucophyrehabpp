import torch

def rmse(y, yhat):
    return torch.sqrt(torch.mean((yhat - y) ** 2))