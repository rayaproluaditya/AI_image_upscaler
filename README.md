# Streamlit Upscaler

## Quick start (local)

1. Create virtualenv: python -m venv .venv && source .venv/bin/activate
2. Install: pip install -r requirements.txt
3. Run: streamlit run app.py

Notes: If you have a Real-ESRGAN model or other upscaler code in your `Upscaler.ipynb`, copy the model-loading & upscaling function into `utils.py` under `real_esrgan_upscale()` (see TODO comments).

Docker and Heroku deploy options included.
