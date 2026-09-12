"""
Download / copy high-resolution realistic product images for all Mobile Mart items.
"""
import os
import shutil
import urllib.request
import urllib.error

STATIC_IMG = os.path.join(os.path.dirname(__file__), 'static', 'images')
BRAIN_DIR = r"C:\Users\acer\.gemini\antigravity-ide\brain\2c789e00-2f34-4023-9307-22e5c3f573e6"

# 1. Copy the AI studio generated images first
ai_images = {
    'galaxy-s26-ultra.png': 'galaxy_s26_ultra_1789022705063.jpg',
    'iphone-18-pro-max.png': 'iphone_18_pro_max_1789022724566.jpg',
    'pixel-12-pro.png': 'pixel_12_pro_1789023047413.jpg',
    'macbook-pro-16-m5-max.png': 'macbook_pro_16_1789023070645.jpg',
    'ipad-pro-m5.png': 'ipad_pro_m5_1789023229277.jpg',
    'apple-watch-ultra-3.png': 'apple_watch_ultra_1789023258303.jpg',
}

for dest_name, src_name in ai_images.items():
    src_path = os.path.join(BRAIN_DIR, src_name)
    dest_path = os.path.join(STATIC_IMG, dest_name)
    if os.path.exists(src_path):
        shutil.copyfile(src_path, dest_path)
        print(f"[AI Photo Copied] {dest_name}")

# 2. Curated high quality gadget images from Unsplash / Wikimedia for remaining gadgets
curated_urls = {
    'oneplus-14-pro.png': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800&auto=format&fit=crop&q=80',
    'xiaomi-16-ultra.png': 'https://images.unsplash.com/photo-1580910051074-3eb694886505?w=800&auto=format&fit=crop&q=80',
    'nothing-phone-4.png': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&auto=format&fit=crop&q=80',
    'galaxy-tab-s10-ultra.png': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&auto=format&fit=crop&q=80',
    'dell-xps-15.png': 'https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=800&auto=format&fit=crop&q=80',
    'thinkpad-x1-carbon.png': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=800&auto=format&fit=crop&q=80',
    'magsafe-duo.png': 'https://images.unsplash.com/photo-1622445262464-84b1456045b6?w=800&auto=format&fit=crop&q=80',
    'samsung-45w-charger.png': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&auto=format&fit=crop&q=80',
    'anker-powercore.png': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=800&auto=format&fit=crop&q=80',
    'galaxy-watch-7-pro.png': 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=800&auto=format&fit=crop&q=80',
    'airpods-pro-3.png': 'https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=800&auto=format&fit=crop&q=80',
    'sony-wh-1000xm7.png': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80',
    'galaxy-buds-4-pro.png': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800&auto=format&fit=crop&q=80',
    'jbl-charge-6.png': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?w=800&auto=format&fit=crop&q=80',
    'placeholder.png': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&auto=format&fit=crop&q=80',
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for filename, url in curated_urls.items():
    dest_path = os.path.join(STATIC_IMG, filename)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response, open(dest_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"[Downloaded Gadget Photo] {filename}")
    except Exception as e:
        print(f"[Error downloading {filename}]: {e}")

print("All product images updated!")
