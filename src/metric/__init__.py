def get_metric(cfg):
    """Devuelve la función de pérdida según su nombre"""
    name = cfg.lower()
    if name == "mae":
        from .mae import mae 
        return mae
    if name == "rmse":
        from .rmse import rmse
        return rmse
    else:
        raise ValueError(f"Unknown loss function or not implemented: {name}")