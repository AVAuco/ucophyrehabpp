import os

from torch.utils.tensorboard import SummaryWriter
from datetime import datetime
from typing import Optional, Dict, Any


class TBLogger:
    def __init__(self, cfg):
        """
        log_dir: carpeta base donde guardar los logs (por defecto 'runs')
        run_name: subcarpeta para este experimento (por defecto timestamp)
        """
        self.cfg = cfg
    
        now = datetime.now().strftime("%Y%m%d-%H%M%S")

        log_dir = os.path.join("output", cfg.project.name, cfg.data.modality, cfg.data.split_name, cfg.project.run_name, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{now}_tb_log")

        self.writer = SummaryWriter(log_file)
        print(f"[TBLogger] Output_file: {log_file}")

    def log_epoch(
        self,
        cfg,
        epoch: int,
        train_loss: Optional[float] = None,
        metrics: Dict[str, Any] = {}
    ):
        """Logging Loss"""
        self.writer.add_scalar("Loss/train", train_loss, epoch)

        """Logging Evaluation Metrics"""
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                self.writer.add_scalar(key, value, epoch)
            else:
                # Solo se registran valores escalares
                print(f"[TBLogger] Métrica ignorada (no escalar): {key}={value}")

        self.writer.add_scalar("LR", cfg.training.lr, epoch)

    def log_batch_loss(self, step: int, loss: float):
        """Opcional: para loggear la loss por iteración/batch."""
        self.writer.add_scalar("Loss/train_batch", loss, step)

    def close(self):
        self.writer.close()
