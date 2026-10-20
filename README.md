# LogoSculpt

**English** | [繁體中文](README.zh-TW.md)

---

Batch convert noisy, low-resolution, or bordered raster logos (PNG, JPG, SVG, WEBP, etc.) into tightly cropped, clean white vector SVGs and transparent 4K PNGs.

---

## Quick Start

### 1. Install dependencies
Requires Python 3.10+:
```bash
pip install -r requirements.txt
```

### 2. Drop files in
Put your images directly into the `input/` folder (supports SVG, PNG, JPG, WEBP, AVIF, GIF, etc.).

### 3. Run conversion
* **Windows**: Double-click `run.bat`.
* **Command line**:
  ```bash
  python convert.py
  ```

### 4. Grab your outputs
Processed files are saved in `output/`, organized into folders per logo. Open `output/preview.html` in your browser to preview against dark backgrounds and download assets.

---

## Common CLI Options

```bash
# Force re-process already converted files
python convert.py --force

# Custom vector fill color (defaults to pure white #FFFFFF, e.g. brand gold #FFD700)
python convert.py --color "#FFD700"

# Adjust edge padding (default 2.0px, tightly cropped)
python convert.py --padding 3.0

# Disable auto-splitting into icon and text (full lockup only)
python convert.py --no-split

# Custom input and output paths
python convert.py -i "/path/to/input" -o "/path/to/output"
```

---

## Real-World Edge Cases Solved Automatically

Skip manual pen-tool tracing in Illustrator. The script fixes common raster defects under the hood:

1. **Screenshot black borders**: Detects and neutralizes outer 1~2px screenshot lines so backgrounds aren't misread as dark or boxed in.
2. **Font bloat and closed counters**: Uses dual-peak Otsu and alpha midpoint tuning to stop letters like `A`, `R`, `P` and dense CJK strokes from blowing up and closing shut.
3. **JPEG compression noise**: Bilateral filtering paired with connected-component area filters cleans stray background specks while keeping punctuation and lowercase `i` dots intact.
4. **Physical stamps & ink bleed**: Color saturation gating removes fuzzy paper bleed inside hollow stamp grooves.
5. **Bright gradient preservation**: HSV saturation sensing keeps bright colored accents (yellows, cyans) from vanishing into white backgrounds.
6. **Auto Icon / Text split**: Wide logos are automatically split into "Full", standalone "Icon", and standalone "Text".

---

## Output Files

Each logo generates:

| File | Description |
| :--- | :--- |
| `*_white_full.svg` | Full vector asset (tight viewBox, infinitely scalable) |
| `*_white_full.png` | 1x transparent PNG (resvg subpixel rasterization) |
| `*_white_full_4k.png` | 4K transparent PNG (longest side >= 4000px) |
| `*_white_icon.svg / .png` | Standalone icon (when aspect ratio and gap match) |
| `*_white_text.svg / .png` | Standalone typography (when aspect ratio and gap match) |
| `output/preview.html` | Offline preview board with dark, navy, and checkerboard toggles |

---

## License

[MIT License](./LICENSE)
