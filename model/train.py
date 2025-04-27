import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.data_loader import get_dataloaders, save_class_mapping
from utils.model_setup import create_model
from utils.training_loop import train_and_validate
import torch

def main():
    torch.backends.cudnn.benchmark = True  #  AMP 최적화

    train_loader, valid_loader, class_names = get_dataloaders()
    save_class_mapping(class_names)

    model, criterion, optimizer, device = create_model(
        num_classes=len(class_names),
        learning_rate=1e-4,
        freeze_feature=False  # 
    )

    start_epoch = 0
    best_val_acc = 0.0

    # === AMP 학습 ===
    scaler = torch.cuda.amp.GradScaler()

    train_and_validate(
        model, optimizer, criterion,
        train_loader, valid_loader,
        device,
        start_epoch=start_epoch,
        num_epochs=10,
        best_val_acc=best_val_acc,
        early_stopping=True,
        patience=3,
        delta=0.001,
        scaler=scaler  #  AMP 스케일러 전달
    )

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    main()
