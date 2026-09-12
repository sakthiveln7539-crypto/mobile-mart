"""
Mobile Mart System — Database Seeder
Creates tables and populates with sample categories, products, and users.
Run: python init_db.py
"""

import json
import os
import sys

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User, Category, Product, Review


def seed():
    """Seed the database with sample data."""

    with app.app_context():
        db.create_all()

        # Skip if data exists
        if Product.query.first():
            print("Database already seeded. Skipping.")
            return

        print("Seeding database...")

        # ── Categories ─────────────────────────────────────────────
        categories_data = [
            {'name': 'Smartphones', 'slug': 'smartphones', 'icon': '📱', 'description': 'Latest smartphones from top brands'},
            {'name': 'Tablets', 'slug': 'tablets', 'icon': '📱', 'description': 'Powerful tablets for work and play'},
            {'name': 'Laptops', 'slug': 'laptops', 'icon': '💻', 'description': 'High-performance laptops and ultrabooks'},
            {'name': 'Accessories', 'slug': 'accessories', 'icon': '⚡', 'description': 'Cases, chargers, cables, and more'},
            {'name': 'Smartwatches', 'slug': 'smartwatches', 'icon': '⌚', 'description': 'Smart wearables and fitness trackers'},
            {'name': 'Audio', 'slug': 'audio', 'icon': '🎧', 'description': 'Headphones, earbuds, and speakers'},
        ]
        cats = {}
        for c in categories_data:
            cat = Category(**c)
            db.session.add(cat)
            cats[c['slug']] = cat

        db.session.flush()

        # ── Products ───────────────────────────────────────────────
        products_data = [
            # Smartphones
            {
                'name': 'Galaxy S26 Ultra',
                'slug': 'galaxy-s26-ultra',
                'description': 'Samsung\'s flagship with a stunning 6.9" Dynamic AMOLED 2X display, 200MP camera system, S Pen integration, and Snapdragon 8 Gen 5 processor. Features AI-powered photography, all-day battery life, and a premium titanium frame.',
                'price': 1399.99,
                'discount_price': 1249.99,
                'stock': 25,
                'category': 'smartphones',
                'brand': 'Samsung',
                'featured': True,
                'image_url': '/static/images/galaxy-s26-ultra.png',
                'specs': {'Display': '6.9" Dynamic AMOLED 2X', 'Processor': 'Snapdragon 8 Gen 5', 'RAM': '12GB', 'Storage': '256GB/512GB/1TB', 'Camera': '200MP + 50MP + 12MP + 10MP', 'Battery': '5500 mAh', 'OS': 'Android 16'},
            },
            {
                'name': 'iPhone 18 Pro Max',
                'slug': 'iphone-18-pro-max',
                'description': 'Apple\'s most advanced iPhone yet featuring the A20 Bionic chip, ProMotion XDR display, revolutionary 48MP quad-camera system with 10x optical zoom, and MagSafe 3.0. Experience unmatched performance and iOS 20.',
                'price': 1599.99,
                'discount_price': 1499.99,
                'stock': 30,
                'category': 'smartphones',
                'brand': 'Apple',
                'featured': True,
                'image_url': '/static/images/iphone-18-pro-max.png',
                'specs': {'Display': '6.9" Super Retina XDR', 'Processor': 'A20 Bionic', 'RAM': '12GB', 'Storage': '256GB/512GB/1TB', 'Camera': '48MP Quad System', 'Battery': '5000 mAh', 'OS': 'iOS 20'},
            },
            {
                'name': 'Pixel 12 Pro',
                'slug': 'pixel-12-pro',
                'description': 'Google\'s AI-first smartphone with the Tensor G6 chip, advanced computational photography, 7 years of updates, and seamless Google ecosystem integration. The best camera phone for everyday moments.',
                'price': 1099.99,
                'discount_price': 999.99,
                'stock': 20,
                'category': 'smartphones',
                'brand': 'Google',
                'featured': True,
                'image_url': '/static/images/pixel-12-pro.png',
                'specs': {'Display': '6.7" LTPO OLED', 'Processor': 'Tensor G6', 'RAM': '12GB', 'Storage': '128GB/256GB/512GB', 'Camera': '50MP + 48MP + 48MP', 'Battery': '5200 mAh', 'OS': 'Android 16'},
            },
            {
                'name': 'OnePlus 14 Pro',
                'slug': 'oneplus-14-pro',
                'description': 'Flagship killer with Snapdragon 8 Gen 5, Hasselblad camera partnership, 100W fast charging, and a stunning 2K display. Incredible performance at a competitive price.',
                'price': 899.99,
                'discount_price': 799.99,
                'stock': 15,
                'category': 'smartphones',
                'brand': 'OnePlus',
                'featured': False,
                'image_url': '/static/images/oneplus-14-pro.png',
                'specs': {'Display': '6.7" 2K AMOLED 120Hz', 'Processor': 'Snapdragon 8 Gen 5', 'RAM': '16GB', 'Storage': '256GB/512GB', 'Camera': '50MP + 48MP + 64MP', 'Battery': '5400 mAh', 'OS': 'OxygenOS 15'},
            },
            # Tablets
            {
                'name': 'iPad Pro M5',
                'slug': 'ipad-pro-m5',
                'description': 'The ultimate iPad with the M5 chip, Liquid Retina XDR display, Thunderbolt 4, and Apple Pencil Pro support. A powerhouse for creative professionals and productivity.',
                'price': 1299.99,
                'discount_price': 1199.99,
                'stock': 18,
                'category': 'tablets',
                'brand': 'Apple',
                'featured': True,
                'image_url': '/static/images/ipad-pro-m5.png',
                'specs': {'Display': '12.9" Liquid Retina XDR', 'Processor': 'Apple M5', 'RAM': '16GB', 'Storage': '256GB/512GB/1TB/2TB', 'Camera': '12MP + 10MP', 'Battery': '10 hours', 'OS': 'iPadOS 20'},
            },
            {
                'name': 'Galaxy Tab S10 Ultra',
                'slug': 'galaxy-tab-s10-ultra',
                'description': 'Samsung\'s largest and most powerful tablet with a 14.6" AMOLED display, S Pen included, DeX mode for desktop experience, and flagship-level cameras.',
                'price': 1199.99,
                'discount_price': None,
                'stock': 12,
                'category': 'tablets',
                'brand': 'Samsung',
                'featured': False,
                'image_url': '/static/images/galaxy-tab-s10-ultra.png',
                'specs': {'Display': '14.6" Super AMOLED', 'Processor': 'Snapdragon 8 Gen 5', 'RAM': '12GB/16GB', 'Storage': '256GB/512GB', 'Camera': '13MP + 8MP', 'Battery': '11200 mAh', 'OS': 'Android 16'},
            },
            # Laptops
            {
                'name': 'MacBook Pro 16" M5 Max',
                'slug': 'macbook-pro-16-m5-max',
                'description': 'Apple\'s most powerful laptop ever with M5 Max chip, up to 128GB unified memory, stunning Liquid Retina XDR display, 24 hours of battery life, and MagSafe charging.',
                'price': 3499.99,
                'discount_price': 3299.99,
                'stock': 10,
                'category': 'laptops',
                'brand': 'Apple',
                'featured': True,
                'image_url': '/static/images/macbook-pro-16-m5-max.png',
                'specs': {'Display': '16.2" Liquid Retina XDR', 'Processor': 'Apple M5 Max', 'RAM': '48GB/64GB/128GB', 'Storage': '1TB/2TB/4TB/8TB', 'Battery': '24 hours', 'Ports': 'Thunderbolt 5, HDMI, SD', 'OS': 'macOS'},
            },
            {
                'name': 'Dell XPS 15',
                'slug': 'dell-xps-15',
                'description': 'Premium ultrabook with Intel Core Ultra 9, OLED 3.5K display, sleek InfinityEdge design, and all-day battery life. Perfect for professionals and creators.',
                'price': 1899.99,
                'discount_price': 1699.99,
                'stock': 14,
                'category': 'laptops',
                'brand': 'Dell',
                'featured': True,
                'image_url': '/static/images/dell-xps-15.png',
                'specs': {'Display': '15.6" 3.5K OLED', 'Processor': 'Intel Core Ultra 9', 'RAM': '32GB DDR5', 'Storage': '1TB NVMe SSD', 'Graphics': 'NVIDIA RTX 4070', 'Battery': '13 hours', 'OS': 'Windows 11'},
            },
            {
                'name': 'ThinkPad X1 Carbon Gen 13',
                'slug': 'thinkpad-x1-carbon-gen-13',
                'description': 'Lenovo\'s legendary business ultrabook, now lighter and more powerful. Features a 14" 2.8K OLED display, Intel Core Ultra 7, legendary keyboard, and enterprise security.',
                'price': 1649.99,
                'discount_price': None,
                'stock': 8,
                'category': 'laptops',
                'brand': 'Lenovo',
                'featured': False,
                'image_url': '/static/images/thinkpad-x1-carbon.png',
                'specs': {'Display': '14" 2.8K OLED', 'Processor': 'Intel Core Ultra 7', 'RAM': '32GB LPDDR5x', 'Storage': '512GB/1TB SSD', 'Battery': '15 hours', 'Weight': '1.09 kg', 'OS': 'Windows 11 Pro'},
            },
            # Accessories
            {
                'name': 'MagSafe Duo Charger',
                'slug': 'magsafe-duo-charger',
                'description': 'Charge your iPhone and Apple Watch simultaneously with this elegant folding MagSafe Duo charger. 15W fast wireless charging in a compact design.',
                'price': 129.99,
                'discount_price': 99.99,
                'stock': 50,
                'category': 'accessories',
                'brand': 'Apple',
                'featured': False,
                'image_url': '/static/images/magsafe-duo.png',
                'specs': {'Type': 'Wireless Charger', 'Wattage': '15W', 'Compatibility': 'iPhone 14+, Apple Watch', 'Cable': 'USB-C', 'Color': 'White'},
            },
            {
                'name': 'Samsung 45W Travel Adapter',
                'slug': 'samsung-45w-travel-adapter',
                'description': 'Ultra-fast 45W USB-C charger with GaN technology. Compact, travel-friendly design that charges your Galaxy devices at maximum speed.',
                'price': 49.99,
                'discount_price': 39.99,
                'stock': 100,
                'category': 'accessories',
                'brand': 'Samsung',
                'featured': False,
                'image_url': '/static/images/samsung-45w-charger.png',
                'specs': {'Type': 'Wall Charger', 'Wattage': '45W', 'Technology': 'GaN', 'Port': 'USB-C PD 3.0', 'Color': 'Black'},
            },
            {
                'name': 'Anker PowerCore 26800 PD',
                'slug': 'anker-powercore-26800',
                'description': 'Massive 26800mAh portable charger with 65W USB-C PD output. Charge your laptop, tablet, and phone multiple times on a single charge.',
                'price': 79.99,
                'discount_price': 64.99,
                'stock': 40,
                'category': 'accessories',
                'brand': 'Anker',
                'featured': False,
                'image_url': '/static/images/anker-powercore.png',
                'specs': {'Capacity': '26800 mAh', 'Output': '65W USB-C PD', 'Ports': '1x USB-C + 2x USB-A', 'Weight': '580g', 'Charges': 'Laptop 1x, Phone 6x'},
            },
            # Smartwatches
            {
                'name': 'Apple Watch Ultra 3',
                'slug': 'apple-watch-ultra-3',
                'description': 'The most rugged and capable Apple Watch built for extreme environments. Features a 52mm titanium case, dual-frequency GPS, 72-hour battery life, and advanced health sensors.',
                'price': 899.99,
                'discount_price': 849.99,
                'stock': 20,
                'category': 'smartwatches',
                'brand': 'Apple',
                'featured': True,
                'image_url': '/static/images/apple-watch-ultra-3.png',
                'specs': {'Display': '52mm Always-On Retina', 'Case': 'Titanium', 'Battery': '72 hours', 'Water Resistance': '100m + EN13319', 'Sensors': 'Heart Rate, SpO2, Temp, Depth', 'GPS': 'Dual-frequency L1/L5'},
            },
            {
                'name': 'Galaxy Watch 7 Pro',
                'slug': 'galaxy-watch-7-pro',
                'description': 'Samsung\'s premium smartwatch with titanium build, advanced sleep coaching, body composition analysis, and up to 80 hours of battery life with LTE connectivity.',
                'price': 549.99,
                'discount_price': 499.99,
                'stock': 22,
                'category': 'smartwatches',
                'brand': 'Samsung',
                'featured': False,
                'image_url': '/static/images/galaxy-watch-7-pro.png',
                'specs': {'Display': '47mm Super AMOLED', 'Case': 'Titanium', 'Battery': '80 hours', 'OS': 'Wear OS 6', 'Sensors': 'BioActive, Temp, SpO2', 'Connectivity': 'LTE, WiFi, Bluetooth 5.3'},
            },
            # Audio
            {
                'name': 'AirPods Pro 3',
                'slug': 'airpods-pro-3',
                'description': 'Apple\'s best earbuds with H3 chip, adaptive audio, conversation awareness, personalized spatial audio, and clinical-grade hearing health features. USB-C with MagSafe case.',
                'price': 279.99,
                'discount_price': 249.99,
                'stock': 60,
                'category': 'audio',
                'brand': 'Apple',
                'featured': True,
                'image_url': '/static/images/airpods-pro-3.png',
                'specs': {'Driver': 'Custom H3 chip', 'ANC': 'Adaptive Active Noise Cancellation', 'Battery': '6h (30h with case)', 'Connectivity': 'Bluetooth 5.4', 'Water Resistance': 'IP54', 'Features': 'Spatial Audio, Conversation Awareness'},
            },
            {
                'name': 'Sony WH-1000XM7',
                'slug': 'sony-wh-1000xm7',
                'description': 'Industry-leading noise canceling headphones with 40-hour battery life, multipoint connection, LDAC Hi-Res audio, and AI-adaptive sound control.',
                'price': 399.99,
                'discount_price': 349.99,
                'stock': 35,
                'category': 'audio',
                'brand': 'Sony',
                'featured': False,
                'image_url': '/static/images/sony-wh-1000xm7.png',
                'specs': {'Driver': '40mm, LDAC', 'ANC': 'AI-Adaptive Noise Canceling', 'Battery': '40 hours', 'Connectivity': 'Bluetooth 5.4, Multipoint', 'Weight': '250g', 'Features': 'Speak-to-Chat, DSEE Extreme'},
            },
            {
                'name': 'Samsung Galaxy Buds 4 Pro',
                'slug': 'galaxy-buds-4-pro',
                'description': 'Premium wireless earbuds with intelligent ANC, 360 Audio, seamless Galaxy ecosystem integration, and hi-fi 24-bit audio. All-day comfort with IP57 rating.',
                'price': 229.99,
                'discount_price': 199.99,
                'stock': 45,
                'category': 'audio',
                'brand': 'Samsung',
                'featured': False,
                'image_url': '/static/images/galaxy-buds-4-pro.png',
                'specs': {'Driver': 'Dual dynamic', 'ANC': 'Intelligent Active Noise Canceling', 'Battery': '8h (30h with case)', 'Connectivity': 'Bluetooth 5.4', 'Water Resistance': 'IP57', 'Audio': '24-bit Hi-Fi, 360 Audio'},
            },
            {
                'name': 'JBL Charge 6',
                'slug': 'jbl-charge-6',
                'description': 'Portable Bluetooth speaker with massive sound, 24-hour playtime, built-in power bank, and IP67 waterproof rating. Perfect for outdoor adventures.',
                'price': 179.99,
                'discount_price': 149.99,
                'stock': 30,
                'category': 'audio',
                'brand': 'JBL',
                'featured': False,
                'image_url': '/static/images/jbl-charge-6.png',
                'specs': {'Type': 'Portable Speaker', 'Output': '30W', 'Battery': '24 hours', 'Waterproof': 'IP67', 'Connectivity': 'Bluetooth 5.3', 'Features': 'Power Bank, PartyBoost'},
            },
            # More smartphones
            {
                'name': 'Xiaomi 16 Ultra',
                'slug': 'xiaomi-16-ultra',
                'description': 'Xiaomi\'s photography flagship with Leica optics, 1-inch sensor, 200W HyperCharge, and a gorgeous 2K AMOLED display. Pro-grade photography at an incredible value.',
                'price': 799.99,
                'discount_price': 699.99,
                'stock': 18,
                'category': 'smartphones',
                'brand': 'Xiaomi',
                'featured': False,
                'image_url': '/static/images/xiaomi-16-ultra.png',
                'specs': {'Display': '6.73" 2K AMOLED 120Hz', 'Processor': 'Snapdragon 8 Gen 5', 'RAM': '16GB', 'Storage': '512GB/1TB', 'Camera': '50MP 1-inch Leica + 50MP + 50MP', 'Battery': '5300 mAh, 200W charge', 'OS': 'HyperOS 3'},
            },
            {
                'name': 'Nothing Phone 4',
                'slug': 'nothing-phone-4',
                'description': 'Bold and transparent design with iconic Glyph Interface 2.0. Features Snapdragon 8s Gen 5, clean Nothing OS, and a stunning dual 50MP camera with unique lighting effects.',
                'price': 599.99,
                'discount_price': 549.99,
                'stock': 12,
                'category': 'smartphones',
                'brand': 'Nothing',
                'featured': False,
                'image_url': '/static/images/nothing-phone-4.png',
                'specs': {'Display': '6.7" LTPO OLED 120Hz', 'Processor': 'Snapdragon 8s Gen 5', 'RAM': '12GB', 'Storage': '256GB/512GB', 'Camera': '50MP + 50MP', 'Battery': '5000 mAh, 65W', 'OS': 'Nothing OS 4'},
            },
        ]

        product_objects = []
        for p in products_data:
            cat_slug = p.pop('category')
            cat = cats[cat_slug]
            p['category_id'] = cat.id
            p['specs'] = json.dumps(p.get('specs', {}))
            prod = Product(**p)
            db.session.add(prod)
            product_objects.append(prod)

        db.session.flush()

        # ── Users ──────────────────────────────────────────────────
        admin = User(
            username='admin',
            email='admin@mobilemart.com',
            full_name='Admin User',
            is_admin=True,
            phone='+1-555-0100',
            address='123 Admin Street',
            city='New York'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        demo = User(
            username='demo',
            email='demo@mobilemart.com',
            full_name='Demo Customer',
            is_admin=False,
            phone='+1-555-0200',
            address='456 Demo Avenue',
            city='San Francisco'
        )
        demo.set_password('demo123')
        db.session.add(demo)

        db.session.flush()

        # ── Sample Reviews ─────────────────────────────────────────
        sample_reviews = [
            (product_objects[0], demo, 5, "Absolutely incredible phone! The camera is a game changer."),
            (product_objects[1], demo, 5, "Best iPhone ever made. The battery life is outstanding."),
            (product_objects[2], demo, 4, "Amazing camera and clean software. Love the AI features."),
            (product_objects[4], demo, 5, "Perfect for creative work. M5 chip is insanely fast."),
            (product_objects[6], demo, 5, "The best laptop I've ever owned. Worth every penny."),
            (product_objects[12], demo, 5, "Built like a tank. Perfect for hiking and outdoor activities."),
            (product_objects[14], demo, 4, "Great sound quality and the noise canceling is top-notch."),
        ]
        for prod, user, rating, comment in sample_reviews:
            review = Review(
                user_id=user.id,
                product_id=prod.id,
                rating=rating,
                comment=comment
            )
            db.session.add(review)

        db.session.flush()

        # Update ratings
        for prod, _, rating, _ in sample_reviews:
            prod.update_rating()

        db.session.commit()
        print(f"[OK] Seeded {len(categories_data)} categories")
        print(f"[OK] Seeded {len(products_data)} products")
        print(f"[OK] Seeded 2 users (admin/admin123, demo/demo123)")
        print(f"[OK] Seeded {len(sample_reviews)} reviews")
        print("[OK] Database ready!")


if __name__ == '__main__':
    seed()
