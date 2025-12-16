from .baseline_sils import BaselineSilsModel
from .baseline_rgb import BaselineRGBModel

def get_model(cfg):
    """Devuelve el modelo según su nombre"""
    name = cfg.name.lower()
    if name == "none":
        return None
    if name == "baselinesilsmodel":
        return BaselineSilsModel
    if name == "baselinergbmodel":
        return BaselineRGBModel
    else:
        raise ValueError(f"Unknown model or not implemented: {name}")