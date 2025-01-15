from PIL import Image
from torchvision import transforms
from app.model import MovieFrame

# Funkcja ładowania i transformacji zdjęcia przed predykcją
def load_and_preprocess_image(img_path, target_size=(200, 200)):
    transform = transforms.Compose([
                                    transforms.Resize(200),
                                    transforms.CenterCrop(200),
                                    transforms.ToTensor(),
                                    transforms.Normalize((0), (1))
                                ])
    # Wczytaj obraz
    img = Image.open(img_path).convert("RGB")
    # Zastosuj transformację
    img = transform(img)
    # Dodaj wymiar partii
    img = img.unsqueeze(0)
    return img
   


# Ładowanie modelu
model = MovieFrame.load_from_checkpoint("app/model_version/checkpoints/epoch=29-step=6870.ckpt", num_classes=4)
model.eval()

# Typy klasyfikacji
classes = [
    '2d_animation',
    '3d_animation',
    'live_action',
    'stop_motion'
]
