"""
Prepare and crop image assets to precise aspect ratios for the PowerPoint presentation.
"""

from pathlib import Path
from PIL import Image, ImageOps

ASSETS_DIR = Path("11_Presentation/assets")
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def crop_to_aspect(src_path: Path, dest_path: Path, target_ratio: float):
    with Image.open(src_path) as img:
        img = img.convert("RGB")
        w, h = img.size
        current_ratio = w / h

        if current_ratio > target_ratio:
            # Too wide: crop width
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            box = (left, 0, left + new_w, h)
        else:
            # Too tall: crop height
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            box = (0, top, w, top + new_h)

        cropped = img.crop(box)
        cropped.save(dest_path, quality=92)
        print(f"Generated: {dest_path.name} ({cropped.size})")

def main():
    crops = [
        # (src, dest, target_width/target_height)
        ("12_Frontend/static/images/culture/ayurveda_kettuvallam.jpg", "cover_hero.jpg", 4.2 / 5.8),
        ("12_Frontend/static/images/destinations/kochi_city.jpg", "card_kochi.jpg", 3.2 / 1.7),
        ("12_Frontend/static/images/destinations/vagamon.jpg", "card_vagamon.jpg", 3.2 / 1.7),
        ("12_Frontend/static/images/destinations/munnar.jpg", "growth_munnar.jpg", 3.8 / 2.3),
        ("12_Frontend/static/images/destinations/kochi_city.jpg", "cluster_urban.jpg", 3.4 / 1.1),
        ("12_Frontend/static/images/destinations/silent_valley.jpg", "cluster_nature.jpg", 3.4 / 1.1),
        ("12_Frontend/static/images/destinations/thekkady.jpg", "cluster_resort.jpg", 3.4 / 1.1),
        ("12_Frontend/static/images/destinations/varkala.jpg", "trends_varkala.jpg", 3.5 / 2.0),
        ("12_Frontend/static/images/culture/malabar_food.jpg", "trends_food.jpg", 3.5 / 2.0),
        ("12_Frontend/static/images/destinations/kumarakom.jpg", "blueprint_kumarakom.jpg", 2.6 / 1.6),
        ("12_Frontend/static/images/destinations/vagamon.jpg", "blueprint_vagamon.jpg", 2.6 / 1.6),
        ("12_Frontend/static/images/destinations/munnar.jpg", "blueprint_munnar.jpg", 2.6 / 1.6),
        ("12_Frontend/static/images/destinations/bekal.jpg", "blueprint_bekal.jpg", 2.6 / 1.6),
        ("12_Frontend/static/images/culture/theyyam.jpg", "closing_theyyam.jpg", 4.0 / 5.4),
    ]

    for src, dest, ratio in crops:
        src_p = Path(src)
        dest_p = ASSETS_DIR / dest
        if src_p.exists():
            crop_to_aspect(src_p, dest_p, ratio)
        else:
            print(f"Warning: {src_p} does not exist.")

if __name__ == "__main__":
    main()
