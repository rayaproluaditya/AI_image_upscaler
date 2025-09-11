from io import BytesIO
from PIL import Image
import torch
import os
import requests

_model_cache = {}

def _download_weights(scale: int):
    """
    Download Real-ESRGAN pretrained weights if not already present.
    Saves to ./weights/RealESRGAN_x{scale}.pth
    """
    os.makedirs("weights", exist_ok=True)
    weight_path = f"weights/RealESRGAN_x{scale}.pth"

    if not os.path.exists(weight_path):
        url = f"https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x{scale}.pth"
        print(f"Downloading weights from {url} ...")
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(weight_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✅ Weights saved to {weight_path}")
    return weight_path


def _get_model(scale=2, use_gpu=True):
    """
    Lazy-load the official Real-ESRGAN model and cache it.
    """
    global _model_cache
    if scale in _model_cache:
        return _model_cache[scale]

    try:
        from realesrgan import RealESRGANer
        from basicsr.archs.rrdbnet_arch import RRDBNet
    except ImportError as e:
        raise ImportError(
            "Real-ESRGAN not installed. Make sure you added it in requirements.txt:\n"
            "git+https://github.com/xinntao/Real-ESRGAN.git\n"
            "basicsr\nfacexlib\ngfpgan"
        ) from e

    # Download weights if missing
    weight_path = _download_weights(scale)

    # RRDBNet architecture
    model = RRDBNet(
        num_in_ch=3, num_out_ch=3, num_feat=64,
        num_block=23, num_grow_ch=32, scale=4
    )

    device = "cuda" if (use_gpu and torch.cuda.is_available()) else "cpu"

    # Create ESRGANer
    upsampler = RealESRGANer(
        scale=scale,
        model_path=weight_path,
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=use_gpu,  # use FP16 if GPU
        device=device,
    )

    _model_cache[scale] = upsampler
    return upsampler


def real_esrgan_upscale(image_bytes: bytes, scale: int = 2, use_gpu: bool = True):
    """
    Run inference with official Real-ESRGAN implementation.
    """
    model = _get_model(scale=scale, use_gpu=use_gpu)

    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    import numpy as np
    img_np = np.array(img)

    output, _ = model.enhance(img_np, outscale=scale)
    out_img = Image.fromarray(output)
    return out_img


def fallback_upscale(image_bytes: bytes, scale: int = 2, preserve: bool = True):
    """
    High-quality PIL resampling fallback (if Real-ESRGAN unavailable).
    """
    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    w, h = img.size
    new_size = (int(w * scale), int(h * scale))
    up = img.resize(new_size, resample=Image.LANCZOS)
    return up