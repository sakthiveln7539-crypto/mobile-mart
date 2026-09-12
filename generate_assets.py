"""
Generate modern vector SVG graphic assets for all products in Mobile Mart.
"""
import os

images_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
os.makedirs(images_dir, exist_ok=True)

# Helper function to generate SVG
def make_svg(title, subtitle, category_icon, bg_gradient, accent_color, device_type="phone"):
    """
    Creates an ultra-modern 600x600 SVG product illustration with glowing gradients and device frames.
    """
    if device_type == "phone":
        device_svg = f"""
        <!-- Phone Body -->
        <rect x="210" y="100" width="180" height="360" rx="36" fill="#181824" stroke="{accent_color}" stroke-width="4" filter="url(#glow)"/>
        <rect x="218" y="108" width="164" height="344" rx="28" fill="#0c0c14"/>
        <!-- Screen Gradient -->
        <rect x="222" y="112" width="156" height="336" rx="24" fill="url(#screenGrad)"/>
        <!-- Dynamic Island / Punch Hole -->
        <rect x="270" y="122" width="60" height="14" rx="7" fill="#000000"/>
        <!-- Screen Content Graphic -->
        <circle cx="300" cy="240" r="45" fill="{accent_color}" opacity="0.25"/>
        <text x="300" y="250" font-family="system-ui, -apple-system, sans-serif" font-size="36" font-weight="900" fill="#ffffff" text-anchor="middle">{category_icon}</text>
        <text x="300" y="320" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle" opacity="0.9">{title}</text>
        <text x="300" y="340" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="500" fill="#a0a0b8" text-anchor="middle">{subtitle}</text>
        <!-- Home bar -->
        <rect x="270" y="432" width="60" height="4" rx="2" fill="#ffffff" opacity="0.6"/>
        """
    elif device_type == "tablet":
        device_svg = f"""
        <!-- Tablet Body -->
        <rect x="150" y="120" width="300" height="340" rx="24" fill="#181824" stroke="{accent_color}" stroke-width="4" filter="url(#glow)"/>
        <rect x="160" y="130" width="280" height="320" rx="18" fill="url(#screenGrad)"/>
        <!-- Camera -->
        <circle cx="300" cy="140" r="4" fill="#000000"/>
        <!-- Content Graphic -->
        <circle cx="300" cy="260" r="50" fill="{accent_color}" opacity="0.25"/>
        <text x="300" y="275" font-family="system-ui, -apple-system, sans-serif" font-size="44" font-weight="900" fill="#ffffff" text-anchor="middle">{category_icon}</text>
        <text x="300" y="340" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">{title}</text>
        <text x="300" y="365" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="500" fill="#a0a0b8" text-anchor="middle">{subtitle}</text>
        """
    elif device_type == "laptop":
        device_svg = f"""
        <!-- Laptop Screen -->
        <rect x="150" y="140" width="300" height="200" rx="12" fill="#181824" stroke="{accent_color}" stroke-width="3" filter="url(#glow)"/>
        <rect x="160" y="150" width="280" height="180" rx="8" fill="url(#screenGrad)"/>
        <circle cx="300" cy="225" r="40" fill="{accent_color}" opacity="0.25"/>
        <text x="300" y="238" font-family="system-ui, -apple-system, sans-serif" font-size="36" font-weight="900" fill="#ffffff" text-anchor="middle">{category_icon}</text>
        <text x="300" y="285" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">{title}</text>
        <!-- Laptop Base -->
        <path d="M 120 340 L 480 340 L 500 370 L 100 370 Z" fill="#242436" stroke="{accent_color}" stroke-width="2"/>
        <rect x="260" y="344" width="80" height="6" rx="3" fill="#12121a"/>
        """
    elif device_type == "watch":
        device_svg = f"""
        <!-- Watch Straps -->
        <rect x="265" y="60" width="70" height="120" rx="12" fill="#2a2a3e"/>
        <rect x="265" y="380" width="70" height="120" rx="12" fill="#2a2a3e"/>
        <!-- Watch Case -->
        <rect x="220" y="160" width="160" height="200" rx="44" fill="#181826" stroke="{accent_color}" stroke-width="5" filter="url(#glow)"/>
        <rect x="230" y="170" width="140" height="180" rx="36" fill="url(#screenGrad)"/>
        <!-- Crown button -->
        <rect x="382" y="210" width="8" height="30" rx="3" fill="{accent_color}"/>
        <!-- Watch Face Content -->
        <text x="300" y="240" font-family="system-ui, -apple-system, sans-serif" font-size="40" font-weight="900" fill="#ffffff" text-anchor="middle">{category_icon}</text>
        <text x="300" y="285" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="{accent_color}" text-anchor="middle">10:09 AM</text>
        <text x="300" y="315" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600" fill="#ffffff" text-anchor="middle">{title}</text>
        """
    elif device_type == "audio":
        device_svg = f"""
        <!-- Audio / Headphone Graphic -->
        <circle cx="300" cy="270" r="120" fill="none" stroke="{accent_color}" stroke-width="12" stroke-linecap="round" filter="url(#glow)"/>
        <!-- Left Ear Cup -->
        <rect x="170" y="240" width="45" height="90" rx="22" fill="#242438" stroke="{accent_color}" stroke-width="4"/>
        <!-- Right Ear Cup -->
        <rect x="385" y="240" width="45" height="90" rx="22" fill="#242438" stroke="{accent_color}" stroke-width="4"/>
        <!-- Center Icon -->
        <circle cx="300" cy="285" r="45" fill="{accent_color}" opacity="0.2"/>
        <text x="300" y="300" font-family="system-ui, -apple-system, sans-serif" font-size="44" font-weight="900" fill="#ffffff" text-anchor="middle">{category_icon}</text>
        <text x="300" y="410" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="700" fill="#ffffff" text-anchor="middle">{title}</text>
        <text x="300" y="435" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="500" fill="#a0a0b8" text-anchor="middle">{subtitle}</text>
        """
    else: # accessory / generic
        device_svg = f"""
        <rect x="200" y="160" width="200" height="220" rx="28" fill="#1c1c2c" stroke="{accent_color}" stroke-width="4" filter="url(#glow)"/>
        <circle cx="300" cy="250" r="50" fill="{accent_color}" opacity="0.25"/>
        <text x="300" y="265" font-family="system-ui, -apple-system, sans-serif" font-size="48" font-weight="900" fill="#ffffff" text-anchor="middle">{category_icon}</text>
        <text x="300" y="335" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="700" fill="#ffffff" text-anchor="middle">{title}</text>
        <text x="300" y="360" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="500" fill="#a0a0b8" text-anchor="middle">{subtitle}</text>
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="100%" height="100%">
    <defs>
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="{bg_gradient[0]}"/>
            <stop offset="100%" stop-color="{bg_gradient[1]}"/>
        </linearGradient>
        <linearGradient id="screenGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#141424"/>
            <stop offset="50%" stop-color="#1e1e38"/>
            <stop offset="100%" stop-color="#0f0f1c"/>
        </linearGradient>
        <radialGradient id="glowGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="{accent_color}" stop-opacity="0.35"/>
            <stop offset="100%" stop-color="{accent_color}" stop-opacity="0"/>
        </radialGradient>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="8" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
    </defs>
    
    <!-- Background -->
    <rect width="600" height="600" rx="32" fill="url(#bgGrad)"/>
    <circle cx="300" cy="270" r="220" fill="url(#glowGrad)"/>

    {device_svg}

    <!-- Brand Badge Top Right -->
    <g transform="translate(480, 40)">
        <rect width="80" height="30" rx="15" fill="#ffffff" fill-opacity="0.08" stroke="#ffffff" stroke-opacity="0.15"/>
        <text x="40" y="20" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="800" fill="#ffffff" text-anchor="middle">OFFICIAL</text>
    </g>
</svg>"""
    return svg

products = [
    # Smartphones
    ('galaxy-s26-ultra.png', 'Galaxy S26 Ultra', 'Samsung Flagship 200MP', '📱', ('#0f172a', '#1e1b4b'), '#818cf8', 'phone'),
    ('iphone-18-pro-max.png', 'iPhone 18 Pro Max', 'Apple Titanium A20', '📱', ('#18181b', '#27272a'), '#a78bfa', 'phone'),
    ('pixel-12-pro.png', 'Pixel 12 Pro', 'Google Tensor G6 AI', '📱', ('#0c1a24', '#132f3c'), '#38bdf8', 'phone'),
    ('oneplus-14-pro.png', 'OnePlus 14 Pro', 'Hasselblad 100W Fast', '📱', ('#1f1315', '#38161a'), '#f87171', 'phone'),
    ('xiaomi-16-ultra.png', 'Xiaomi 16 Ultra', 'Leica 1-inch Sensor', '📱', ('#1a1510', '#3b2814'), '#fb923c', 'phone'),
    ('nothing-phone-4.png', 'Nothing Phone 4', 'Glyph Interface 2.0', '📱', ('#141419', '#24242e'), '#e2e8f0', 'phone'),
    
    # Tablets
    ('ipad-pro-m5.png', 'iPad Pro M5', 'Apple Liquid Retina XDR', '📟', ('#111827', '#1f2937'), '#60a5fa', 'tablet'),
    ('galaxy-tab-s10-ultra.png', 'Galaxy Tab S10 Ultra', 'Samsung 14.6" AMOLED', '📟', ('#0f172a', '#1e1b4b'), '#c084fc', 'tablet'),
    
    # Laptops
    ('macbook-pro-16-m5-max.png', 'MacBook Pro 16"', 'M5 Max Extreme Performance', '💻', ('#18181b', '#2e1065'), '#a855f7', 'laptop'),
    ('dell-xps-15.png', 'Dell XPS 15', 'Intel Core Ultra 9 OLED', '💻', ('#0f172a', '#1e293b'), '#38bdf8', 'laptop'),
    ('thinkpad-x1-carbon.png', 'ThinkPad X1 Carbon', 'Lenovo Carbon Lightweight', '💻', ('#1a1012', '#2d181c'), '#ef4444', 'laptop'),
    
    # Accessories
    ('magsafe-duo.png', 'MagSafe Duo Charger', 'Apple Fast Wireless 15W', '⚡', ('#1e1b4b', '#312e81'), '#818cf8', 'accessory'),
    ('samsung-45w-charger.png', '45W GaN Travel Adapter', 'Samsung USB-C Super Fast', '🔌', ('#18181b', '#27272a'), '#34d399', 'accessory'),
    ('anker-powercore.png', 'PowerCore 26800 PD', 'Anker 65W High Capacity', '🔋', ('#0f172a', '#1e293b'), '#38bdf8', 'accessory'),
    
    # Smartwatches
    ('apple-watch-ultra-3.png', 'Apple Watch Ultra 3', 'Rugged Titanium 52mm', '⌚', ('#1c1917', '#292524'), '#fb923c', 'watch'),
    ('galaxy-watch-7-pro.png', 'Galaxy Watch 7 Pro', 'Samsung BioActive LTE', '⌚', ('#0f172a', '#1e1b4b'), '#818cf8', 'watch'),
    
    # Audio
    ('airpods-pro-3.png', 'AirPods Pro 3', 'Apple Spatial Audio ANC', '🎧', ('#18181b', '#27272a'), '#f43f5e', 'audio'),
    ('sony-wh-1000xm7.png', 'Sony WH-1000XM7', 'Industry-Leading ANC Hi-Res', '🎧', ('#1e1b4b', '#172554'), '#3b82f6', 'audio'),
    ('galaxy-buds-4-pro.png', 'Galaxy Buds 4 Pro', 'Samsung 360 Audio Hi-Fi', '🎧', ('#0f172a', '#1e1b4b'), '#a855f7', 'audio'),
    ('jbl-charge-6.png', 'JBL Charge 6', 'Waterproof IP67 Speaker', '🔊', ('#1f140e', '#3c1d10'), '#f97316', 'audio'),

    # Generic Placeholder
    ('placeholder.png', 'Mobile Mart', 'Premium Tech Device', '📦', ('#111827', '#1f2937'), '#6366f1', 'phone')
]

for filename, title, subtitle, icon, bg, accent, dev_type in products:
    content = make_svg(title, subtitle, icon, bg, accent, dev_type)
    filepath = os.path.join(images_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {filename}")

print(f"Successfully generated {len(products)} image assets in {images_dir}")
