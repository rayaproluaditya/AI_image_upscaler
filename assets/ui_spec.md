Title: Upscaler — simple, fast, friendly

Color palette:
- Primary: #0F62FE (Bright blue)
- Accent: #0F9D58 (Green)
- Background: #F6F8FA
- Text: #0B1226

Typography: Inter or system-ui, medium weights for titles.

Wireframe (top-down):

[Header] "Upscaler" | small about icon

[Main area — two columns]
- Left column (controls, 30% width):
  - Upload image (drag & drop)
  - Select scale: Radio (2x, 4x, 8x)
  - Model: Selectbox (Auto-detect, Real-ESRGAN, Fallback)
  - Toggle: Preserve aspect ratio (on)
  - Button: "Upscale"
  - Button: "Reset"
  - Info: model size, GPU / CPU indicator

- Right column (preview, 70%):
  - Original image (thumbnail)
  - Upscaled preview (with lazy loading)
  - Slider to zoom preview
  - Download button (PNG/JPEG)

[Footer]
- small text with usage tips and link to README

Accessibility: large touch targets, high-contrast labels, keyboard accessible controls.
