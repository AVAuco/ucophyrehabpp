import torch.nn as nn
import torchvision.models as tvm

# ───────────────────────────── Modelo: ResNet18 1-canal → escalar ─────────────────────────────
class BaselineSilsModel(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        net = tvm.resnet18(weights=None)
        net.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
        feat_dim = net.fc.in_features
        net.fc = nn.Identity()
        self.backbone = net
        self.head = nn.Sequential(
            nn.Linear(feat_dim, cfg.hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(cfg.hidden_dim, 1),
        )

    def forward(self, x):              # x: [B,1,H,W]
        f = self.backbone(x)           # [B, D]
        y = self.head(f).squeeze(-1)   # [B]
        return y