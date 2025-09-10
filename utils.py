from io import BytesIO
from PIL import Image

def fallback_upscale(image_bytes: bytes, scale: int = 2, preserve: bool = True):
    """High-quality PIL resampling fallback."""
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    w, h = img.size
    new_size = (int(w * scale), int(h * scale))
    up = img.resize(new_size, resample=Image.LANCZOS)
    return up

def real_esrgan_upscale(image_bytes: bytes, scale: int = 2, use_gpu: bool = True):
    """Replace with Real-ESRGAN model inference from your notebook."""
    try:
        from realesrgan import RealESRGAN
    except Exception as e:
        raise ImportError('Real-ESRGAN not installed: ' + str(e))

    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    device = 'cuda' if use_gpu else 'cpu'
    model = RealESRGAN(device=device, scale=scale)
    out = model.predict(img)
    return out
