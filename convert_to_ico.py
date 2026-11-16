import os

# Set DLL path for Cairo on Windows (MSYS2) — must be before importing cairosvg
os.environ["PATH"] = r"C:\msys64\mingw64\bin" + os.pathsep + os.environ["PATH"]
os.add_dll_directory(r"C:\msys64\mingw64\bin")

from PIL import Image
import cairosvg
from io import BytesIO

src = os.path.join(os.path.dirname(__file__), "PNG")
dst = os.path.join(os.path.dirname(__file__), "icon")
os.makedirs(dst, exist_ok=True)

converted = 0
failed = 0

for f in sorted(os.listdir(src)):
    name, ext = os.path.splitext(f)
    ext = ext.lower()
    if ext not in ('.svg', '.webp', '.png', '.icns'):
        continue

    src_path = os.path.join(src, f)
    dst_path = os.path.join(dst, name + ".ico")

    try:
        if ext == '.svg':
            png_data = cairosvg.svg2png(url=src_path, output_width=256, output_height=256)
            img = Image.open(BytesIO(png_data)).convert("RGBA")
        else:
            img = Image.open(src_path)
            if ext == '.icns':
                # ICNS holds several sizes; load the largest to minimise upscaling
                w, h, scale = max(img.info['sizes'], key=lambda s: s[0] * s[2])
                img.size = (w, h)
                img.load(scale=scale)
            img = img.convert("RGBA")

        img = img.resize((256, 256), Image.LANCZOS)
        icon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        img.save(dst_path, format='ICO', sizes=icon_sizes)
        converted += 1
        print(f"OK: {f}")
    except Exception as e:
        failed += 1
        print(f"FAIL: {f} — {e}")

print(f"\nDone: {converted} converted, {failed} failed")
