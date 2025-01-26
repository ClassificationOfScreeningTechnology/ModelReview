from PIL import Image
from torchvision.transforms import v2
from app.model import MovieFrame
import torch

# Funkcja ładowania i transformacji zdjęcia przed predykcją
def load_and_preprocess_image(img_path, target_size=(200, 200)):
    transform = v2.Compose([
                        v2.ToImage(),
                        v2.Resize(256),
                        v2.CenterCrop(224),
                        v2.ToDtype(torch.float32, scale=True),
                        v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                        ])
    # Wczytaj obraz
    img = Image.open(img_path).convert("RGB")
    # Zastosuj transformację
    img = transform(img)
    # Dodaj wymiar partii
    img = img.unsqueeze(0)
    return img
   


# Ładowanie modelu
CKPT_PATH = "app/model_version/checkpoints/modelparams.ckpt"
model = MovieFrame.load_from_checkpoint(checkpoint_path=CKPT_PATH,num_classes = 4,layer1_size = 256,dropout_rate = 0.7,lr = 0.00022838551102598225)
model.eval()

# Typy klasyfikacji
classes = [
    '2d_animation',
    '3d_animation',
    'live_action',
    'stop_motion'
]
