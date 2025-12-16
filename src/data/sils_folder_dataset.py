# src/data/sils_folder_dataset.py
import os
from typing import Callable, Dict, Optional, Tuple

import pandas as pd
from PIL import Image

import torch
from torch.utils.data import Dataset
import torchvision.transforms as tv


class SilsFolderDataset(Dataset):
    """
    Dataset para siluetas (1 canal) basado en los CSVs de manifest.

    Espera CSVs con al menos estas columnas:
      - subject, exercise, camera, frame_id, img_path, angle_deg
      - (opcional) angle_norm  → si no pasas normalizador, puedes usar esa columna

    Parámetros
    ----------
    split : str
        "train" | "val" | "test".
    manifests_map : dict[str, str], opcional
        Mapeo explícito { "train": "..._train.csv", "val": "..._val.csv", "test": "..._test.csv" }.
    manifests_dir : str, opcional
        Directorio donde están los CSVs (si usas base_name).
    base_name : str, opcional
        Prefijo común de los CSVs (p.ej., "80_10_10" → resolverá "80_10_10_train.csv", etc.).
        Se ignora si `manifests_map` está definido.
    image_size : (int, int)
        Tamaño de redimensionado (H, W).
    mean_std_gray : (float|list, float|list)
        Media y std para normalización de imagen en gris. Acepta float o [float].
    angle_column : str
        Nombre de la columna de ángulo **a usar como objetivo**. Por defecto "angle_deg".
        Si quieres entrenar en normalizado, pon "angle_norm".
    angle_normalizer : Callable[[torch.Tensor], torch.Tensor], opcional
        Función que transforme ángulo en grados → espacio normalizado (p.ej. z-score).
        Si se proporciona, se aplica sobre la columna `angle_deg` y **se ignora `angle_column`**.
        Útil para garantizar que *train/val/test* usan exactamente los stats de *train*.
    drop_na : bool
        Si True, descarta filas con NaN en `img_path` o `angle_column` (o `angle_deg` si normalizas on-the-fly).
    """

    def __init__(self, cfg, active_split):
        super().__init__()
        assert active_split in {"train", "val", "test"}, f"split inválido: {active_split}"
        self.split = active_split
    
        # Resolver ruta del CSV
        manifests_dir = 'data/manifests'

        # assert manifests_dir and cfg.data.split_name, "Si no pasas manifests_map, especifica manifests_dir y base_name"
        # csv_path = os.path.join(manifests_dir, f"{cfg.data.split_name}_{active_split}.csv")
        csv_path = os.path.join(manifests_dir, cfg.project.name, cfg.data.modality, cfg.data.split_name, cfg.project.run_name)
        active_split_csv = os.path.join(csv_path, f"{cfg.data.split_name}_{active_split}.csv")
        assert os.path.exists(active_split_csv), f"Manifest CSV no encontrado: {active_split_csv}"

        # if not os.path.exists(csv_path):
        #     raise FileNotFoundError(f"CSV de manifest no encontrado: {csv_path}")

        df = pd.read_csv(active_split_csv)

        # Decidir qué columna de ángulo se usará como objetivo
        self._target_col = "angle_norm" # Columna con ángulos normalizados   

        # Guardar DataFrame ya filtrado
        self.df = df

        # Transformaciones de imagen
        H, W = cfg.data.image_size
        mean, std = (0.5,0.5)
        n_channels = cfg.data.channels
        if n_channels == 3:
            mean = [mean]*3
            std = [std]*3
        else:
            mean = [mean]
            std = [std]

        if isinstance(mean, (int, float)):
            mean = [float(mean)]
        if isinstance(std, (int, float)):
            std = [float(std)]

        self.tf = tv.Compose([
            tv.Resize((H, W), interpolation=tv.InterpolationMode.NEAREST),
            tv.ToTensor(),                   # PIL(L) → [1,H,W] en [0,1]
            # tv.Normalize(mean=mean, std=std)
        ])

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx: int):
        r = self.df.iloc[idx]

        # Imagen en gris
        img_path = r.img_path
        x = Image.open(img_path).convert("L")
        x = self.tf(x)  # [1,H,W] float32

        # Ángulo (deg o norm). 
        y = float(r[self._target_col])
        y = torch.tensor(y, dtype=torch.float32)

        meta = {
            "subject": r.get("subject", None),
            "exercise": r.get("exercise", None),
            "camera": r.get("camera", None),
            "frame_id": int(r.get("frame_id", -1)) if pd.notna(r.get("frame_id", None)) else -1,
            "img_path": img_path,
            "angle_deg": float(r["angle_deg"]) if "angle_deg" in r and pd.notna(r["angle_deg"]) else None,
            "angle_norm": float(r["angle_norm"]) if "angle_norm" in r and pd.notna(r["angle_norm"]) else None,
        }

        return x, y, meta
