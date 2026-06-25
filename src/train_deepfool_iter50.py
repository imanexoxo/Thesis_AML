"""
Adversarial Training DeepFool - max_iter=50
Da eseguire sul server con:
    tmux new -s deepfool50
    python src/train_deepfool_iter50.py
"""

import os
import sys
import time
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms, models
from torchvision.datasets import ImageFolder

# ── Configurazione ─────────────────────────────────────────────────────────────

RANDOM_SEED = 42
BATCH_SIZE = 32
IMG_SIZE = 224
N_CLASSES = 5

OVERSHOOT = 0.02
MAX_ITER_TRAINING = 50   # 5 in notebook locale; qui usiamo 50
NUM_EPOCHS = 30
PATIENCE = 10
LR = 0.0001

ROOT = Path(__file__).resolve().parent.parent
MODEL_IN  = ROOT / "models" / "best_resnet18.pt"
MODEL_OUT = ROOT / "models" / "best_df_0.02_iter50.pt"
LOG_FILE  = ROOT / "results" / "train_deepfool_iter50.log"

ROOT.joinpath("results").mkdir(exist_ok=True)

# ── Logging ────────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, mode="w"),
    ],
)
log = logging.getLogger(__name__)

# ── Riproducibilità ────────────────────────────────────────────────────────────

np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
log.info(f"Device: {device}")

# ── Transforms e DataLoader ────────────────────────────────────────────────────

NORMALIZE = transforms.Normalize(
    mean=[0.485, 0.456, 0.406],
    std=[0.229, 0.224, 0.225]
)

TRANSFORMS = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
])

dataset_path = ROOT / "data" / "fruits-classification-stratified"

train_dataset = ImageFolder(root=dataset_path / "train", transform=TRANSFORMS)
val_dataset   = ImageFolder(root=dataset_path / "valid", transform=TRANSFORMS)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True,  num_workers=4)
val_loader   = DataLoader(val_dataset,   batch_size=BATCH_SIZE, shuffle=False, num_workers=4)

log.info(f"Train: {len(train_dataset)} immagini  |  Val: {len(val_dataset)} immagini")

# ── Modello base ───────────────────────────────────────────────────────────────

base_model = models.resnet18(pretrained=False)
base_model.fc = nn.Linear(512, N_CLASSES)
base_model.load_state_dict(torch.load(MODEL_IN, map_location=device))
base_model = base_model.to(device)
base_model.eval()

log.info(f"Modello base caricato da {MODEL_IN}")

# ── DeepFool ───────────────────────────────────────────────────────────────────

def deepfool_attack(model, images, num_classes, overshoot, max_iter):
    """
    Attacco DeepFool su un batch di immagini (range [0, 1]).

    Returns:
        adv_images  : immagini adversarial clampate in [0, 1]
        perturbation: perturbazione applicata (adv - original)
    """
    adv_images = images.clone().detach()

    for image_id in range(images.size(0)):
        original_image = images[image_id : image_id + 1].clone().detach()

        with torch.no_grad():
            outputs = model(NORMALIZE(original_image))
            pred_original = torch.argmax(outputs, dim=1).item()

        total_perturbation = torch.zeros_like(original_image)

        for _ in range(max_iter):
            current_image = torch.clamp(
                original_image + total_perturbation, 0, 1
            ).detach()
            current_image.requires_grad_(True)

            outputs = model(NORMALIZE(current_image))
            pred_current = torch.argmax(outputs, dim=1).item()

            if pred_current != pred_original:
                break

            gradients = []
            for class_id in range(num_classes):
                model.zero_grad()
                if current_image.grad is not None:
                    current_image.grad.zero_()
                outputs[0, class_id].backward(retain_graph=True)
                gradients.append(current_image.grad.clone().detach())

            original_gradient = gradients[pred_original]
            original_score    = outputs[0, pred_original].detach()

            min_distance = float("inf")
            best_step    = torch.zeros_like(original_image)

            for class_id in range(num_classes):
                if class_id == pred_original:
                    continue

                grad_diff  = gradients[class_id] - original_gradient
                score_diff = outputs[0, class_id].detach() - original_score
                grad_norm  = grad_diff.norm()

                if grad_norm.item() == 0:
                    continue

                distance = torch.abs(score_diff) / grad_norm

                if distance.item() < min_distance:
                    min_distance = distance.item()
                    best_step = (
                        torch.abs(score_diff) / grad_norm.pow(2)
                    ) * grad_diff

            total_perturbation = total_perturbation + best_step

        adv_image = torch.clamp(
            original_image + (1 + overshoot) * total_perturbation, 0, 1
        ).detach()
        adv_images[image_id : image_id + 1] = adv_image

    perturbation = adv_images - images
    return adv_images, perturbation.detach()


# ── Adversarial Training ───────────────────────────────────────────────────────

log.info(
    f"Avvio adversarial training DeepFool — "
    f"overshoot={OVERSHOOT}, max_iter_training={MAX_ITER_TRAINING}, "
    f"epochs={NUM_EPOCHS}, patience={PATIENCE}"
)

df_model = models.resnet18(pretrained=False)
df_model.fc = nn.Linear(512, N_CLASSES)
df_model.load_state_dict(torch.load(MODEL_IN, map_location=device))
df_model = df_model.to(device)

loss_fn   = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(df_model.parameters(), lr=LR)

best_val_loss    = float("inf")
patience_counter = 0
history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

total_start = time.time()

for epoch in range(NUM_EPOCHS):
    epoch_start = time.time()

    # ── Train ──────────────────────────────────────────────────────────────────
    df_model.train()
    epoch_loss = 0
    correct_train = 0
    total_train   = 0

    for images, labels in tqdm(
        train_loader,
        desc=f"Epoch {epoch + 1}/{NUM_EPOCHS}",
        leave=False,
    ):
        images = images.to(device)
        labels = labels.to(device)

        half = images.size(0) // 2
        clean_images = images[:half]

        # genera immagini adversarial sulla seconda metà del batch
        df_model.eval()
        adv_images, _ = deepfool_attack(
            df_model,
            images[half:].clone().detach(),
            N_CLASSES,
            OVERSHOOT,
            MAX_ITER_TRAINING,
        )
        df_model.train()

        mixed_images = torch.cat([clean_images, adv_images], dim=0)

        optimizer.zero_grad()
        outputs = df_model(NORMALIZE(mixed_images))
        loss    = loss_fn(outputs, labels)
        loss.backward()
        optimizer.step()

        epoch_loss    += loss.item()
        preds          = torch.argmax(outputs, dim=1)
        correct_train += (preds == labels).sum().item()
        total_train   += labels.size(0)

    train_loss = epoch_loss / len(train_loader)
    train_acc  = correct_train / total_train

    # ── Validation ─────────────────────────────────────────────────────────────
    df_model.eval()
    val_loss = 0
    correct_val = 0
    total_val   = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            labels = labels.to(device)
            outputs  = df_model(NORMALIZE(images))
            val_loss += loss_fn(outputs, labels).item()
            preds     = torch.argmax(outputs, dim=1)
            correct_val += (preds == labels).sum().item()
            total_val   += labels.size(0)

    val_loss /= len(val_loader)
    val_acc   = correct_val / total_val

    history["train_loss"].append(train_loss)
    history["train_acc"].append(train_acc)
    history["val_loss"].append(val_loss)
    history["val_acc"].append(val_acc)

    elapsed = time.time() - epoch_start
    log.info(
        f"Epoch {epoch + 1:02d}/{NUM_EPOCHS} | "
        f"Train Loss={train_loss:.4f}  Acc={train_acc:.4f} | "
        f"Val Loss={val_loss:.4f}  Acc={val_acc:.4f} | "
        f"{elapsed:.0f}s"
    )

    # ── Early stopping ─────────────────────────────────────────────────────────
    if val_loss < best_val_loss:
        best_val_loss    = val_loss
        patience_counter = 0
        torch.save(df_model.state_dict(), MODEL_OUT)
        log.info(f"  → Miglior modello salvato ({MODEL_OUT.name})")
    else:
        patience_counter += 1
        if patience_counter >= PATIENCE:
            log.info(f"Early stopping all'epoca {epoch + 1}")
            break

# ── Riepilogo ──────────────────────────────────────────────────────────────────

total_time = time.time() - total_start
log.info(f"\nTraining completato in {total_time / 60:.1f} min")
log.info(f"Miglior val loss: {best_val_loss:.4f}")
log.info(f"Modello salvato: {MODEL_OUT}")

# salva la history
pd.DataFrame(history).to_csv(
    ROOT / "results" / "train_deepfool_iter50_history.csv",
    index=False
)
log.info("History salvata in results/train_deepfool_iter50_history.csv")
