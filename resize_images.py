import os
import re
from PIL import Image

input_folder = "images"
output_folder = "images"

# small: shown in gallery grid (fast to load)
small_width = 800
small_quality = 70

# large: shown in lightbox when clicking an image (good quality)
large_width = 1600
large_quality = 80

def clean_filename(name):
    # lowercase
    name = name.lower()
    # replace spaces, brackets, plus with dash
    name = re.sub(r"[ ()+]", "-", name)
    # collapse multiple dashes
    name = re.sub(r"-+", "-", name)
    # strip trailing dashes
    name = name.strip("-")
    return name

def resize_and_save(path, base_name):
    img = Image.open(path)
    w, h = img.size

    for width, suffix, quality in [
        (small_width, "small", small_quality),
        (large_width, "large", large_quality),
    ]:
        new_h = int(h * (width / w)) if w > width else h
        resized = img.resize((min(w, width), new_h), Image.LANCZOS)
        new_name = f"{base_name}-{suffix}.jpg"
        save_path = os.path.join(output_folder, new_name)
        resized.convert("RGB").save(save_path, "JPEG", quality=quality, optimize=True)
        print(f"✅ Created {save_path}")

def process_images():
    for filename in os.listdir(input_folder):
        low = filename.lower()
        if low.endswith((".jpg", ".jpeg", ".png")) and "-small." not in low and "-large." not in low:
            filepath = os.path.join(input_folder, filename)
            base, _ = os.path.splitext(filename)
            clean_base = clean_filename(base)

            # Resize to small & large (no original copy kept)
            try:
                resize_and_save(filepath, clean_base)
                os.remove(filepath)
                print(f"🔄 Processed & removed original: {filename}")
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

process_images()
print("\n🎉 All images processed — small (gallery) and large (lightbox) versions created!")
