from pathlib import Path
import io
import streamlit as st
from PIL import Image
import utils

st.set_page_config(page_title='Upscaler', layout='wide', initial_sidebar_state='expanded')

# Header
st.title('🖼️ Upscaler')
st.markdown('Upload an image, choose a scale, and get a high-quality upscaled result. Works with Real-ESRGAN if installed, otherwise falls back to a high-quality resample for demo.')

# Layout: controls left, preview right
col1, col2 = st.columns([1, 2])

with col1:
    uploaded = st.file_uploader('Upload image', type=['png', 'jpg', 'jpeg', 'webp', 'bmp'], accept_multiple_files=False)
    scale = st.radio('Scale', [2, 4, 8], index=0, help='Choose upscaling factor')
    model_choice = st.selectbox('Model', ['auto', 'realesrgan', 'fallback'], index=0)
    preserve = st.checkbox('Preserve aspect ratio', value=True)
    run_btn = st.button('Upscale')
    st.divider()
    st.markdown('**Advanced**')
    use_gpu = st.checkbox('Use GPU (if available)', value=True)
    st.write('Tip: For best results, run with GPU and install Real-ESRGAN models.')

with col2:
    orig_placeholder = st.empty()
    result_placeholder = st.empty()

# Helper: display original whenever uploaded
if uploaded:
    img = Image.open(uploaded).convert('RGB')
    orig_placeholder.subheader('Original')
    orig_placeholder.image(img, use_column_width=True)
else:
    orig_placeholder.info('No image uploaded yet — upload above to begin')

# Run upscaling
if run_btn:
    if not uploaded:
        st.warning('Please upload an image first.')
    else:
        with st.spinner('Upscaling — this can take a few seconds'):
            img_bytes = uploaded.read()
            try:
                # Try to run a Real-ESRGAN upscaler if user has it installed and chosen
                if model_choice in ('auto', 'realesrgan'):
                    result_img = utils.real_esrgan_upscale(img_bytes, scale=scale, use_gpu=use_gpu)
                else:
                    result_img = utils.fallback_upscale(img_bytes, scale=scale, preserve=preserve)
            except Exception as e:
                st.error(f'Upscaling failed: {e}')
                # attempt fallback
                result_img = utils.fallback_upscale(img_bytes, scale=scale, preserve=preserve)

        # show result
        result_placeholder.subheader('Upscaled')
        result_placeholder.image(result_img, use_column_width=True)

        # download
        buf = io.BytesIO()
        result_img.save(buf, format='PNG')
        buf.seek(0)
        st.download_button('Download PNG', data=buf, file_name=f'upscaled_x{scale}.png', mime='image/png')

# small footer
st.markdown('---')
st.caption('Built with Streamlit — adapt model code from your Upscaler.ipynb into utils.real_esrgan_upscale()')
