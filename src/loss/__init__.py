

def get_loss(cfg):
    """Devuelve la función de pérdida según su nombre"""
    name = cfg.loss.lower()
    if name == "mse":
        import torch.nn.functional as F
        return F.mse_loss
    if name == "mae":
        import torch.nn.functional as F
        return F.l1_loss
    else:
        raise ValueError(f"Unknown loss function or not implemented: {name}")