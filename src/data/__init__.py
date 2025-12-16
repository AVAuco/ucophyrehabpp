from .sils_folder_dataset import SilsFolderDataset
from .rgb_folder_dataset import RGBFolderDataset

def get_dataset_loader(cfg):
    """Devuelve el dataset según su nombre"""
    name = cfg.dataset_loader.lower()
    if name == "silsfolderdataset":
        return SilsFolderDataset
    if name == "rgbfolderdataset":
        return RGBFolderDataset
    else:
        raise ValueError(f"Unknown dataset loader or not implemented: {name}")