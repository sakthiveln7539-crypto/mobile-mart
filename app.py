"""
Mobile Mart System — Main Flask Application
Routes, authentication, cart, checkout, admin, and API endpoints.
"""

import os
import json
import re
from datetime import datetime, timezone
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, jsonify, abort
)
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)

from models import db, User, Category, Product, CartItem, Order, OrderItem, Review

# ---------------------------------------------------------------------------
# App factory & configuration
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mobile-mart-dev-secret-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mobile_mart.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure database tables exist when running under a production WSGI server.
with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def admin_required(f):
    """Decorator that requires admin privileges."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Context processor — inject data available to all templates
# ---------------------------------------------------------------------------

@app.context_processor
def inject_globals():
    categories = Category.query.order_by(Category.name).all()
    cart_count = 0
    if current_user.is_authenticated:
        cart_count = current_user.cart_count
    return dict(
        all_categories=categories,
        cart_count=cart_count,
        current_year=datetime.now().year
    )


# ---------------------------------------------------------------------------
# PUBLIC ROUTES
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Home page with featured products and categories."""
    featured = Product.query.filter_by(featured=True).limit(8).all()
    latest = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    categories = Category.query.all()
    total_products = Product.query.count()
    total_brands = db.session.query(Product.brand).distinct().count()
    return render_template('index.html',
                           featured=featured,
                           latest=latest,
                           categories=categories,
                           total_products=total_products,
                           total_brands=total_brands)


@app.route('/products')
def products():
    """Product listing with search, category filter, and sorting."""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    category_slug = request.args.get('category', '')
    search_query = request.args.get('q', '')
    sort = request.args.get('sort', 'newest')
    brand_filter = request.args.get('brand', '')

    query = Product.query

    # Category filter
    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first()
        if cat:
            query = query.filter_by(category_id=cat.id)

    # Search
    if search_query:
        query = query.filter(
            db.or_(
                Product.name.ilike(f'%{search_query}%'),
                Product.description.ilike(f'%{search_query}%'),
                Product.brand.ilike(f'%{search_query}%')
            )
        )

    # Brand filter
    if brand_filter:
        query = query.filter_by(brand=brand_filter)

    # Sorting
    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort == 'name':
        query = query.order_by(Product.name.asc())
    elif sort == 'rating':
        query = query.order_by(Product.rating.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    brands = db.session.query(Product.brand).distinct().order_by(Product.brand).all()
    brands = [b[0] for b in brands if b[0]]

    return render_template('products.html',
                           products=pagination.items,
                           pagination=pagination,
                           category_slug=category_slug,
                           search_query=search_query,
                           sort=sort,
                           brand_filter=brand_filter,
                           brands=brands)


@app.route('/product/<slug>')
def product_detail(slug):
    """Single product detail page."""
    product = Product.query.filter_by(slug=slug).first_or_404()
    related = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(4).all()
    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()

    # Check if current user already reviewed
    user_reviewed = False
    if current_user.is_authenticated:
        user_reviewed = Review.query.filter_by(
            user_id=current_user.id, product_id=product.id
        ).first() is not None

    specs = {}
    try:
        specs = json.loads(product.specs) if product.specs else {}
    except (json.JSONDecodeError, TypeError):
        specs = {}

    return render_template('product_detail.html',
                           product=product,
                           related=related,
                           reviews=reviews,
                           user_reviewed=user_reviewed,
                           specs=specs)


@app.route('/search')
def search():
    """Redirect search to products page."""
    q = request.args.get('q', '')
    return redirect(url_for('products', q=q))


# ---------------------------------------------------------------------------
# WHY CHOOSE US / FEATURE DETAIL PAGES
# ---------------------------------------------------------------------------

WHY_US_FEATURES = {
    'fast-delivery': {
        'slug': 'fast-delivery',
        'title': 'Fast & Free Delivery',
        'badge': '🚀 EXPRESS SHIPPING',
        'icon_class': 'cat-icon-feature-1',
        'icon_svg': '<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>',
        'short_desc': 'Free shipping on all orders with real-time live tracking.',
        'hero_subtitle': 'Experience blazing-fast doorstep delivery with end-to-end package tracking and guaranteed zero shipping fees.',
        'highlights': [
            {'icon': '⚡', 'title': 'Same-Day Dispatch', 'desc': 'Orders placed before 2:00 PM are processed, quality-checked, and dispatched on the exact same day.'},
            {'icon': '🚚', 'title': '100% Free Shipping', 'desc': 'No hidden fees or minimum cart values. Enjoy free standard shipping across all regions.'},
            {'icon': '📍', 'title': 'Live Order Tracking', 'desc': 'Track your shipment step-by-step from our warehouse to your doorstep with SMS and email updates.'},
            {'icon': '🛡️', 'title': 'Insured In-Transit', 'desc': 'Every package is 100% insured against loss or transit damage for total peace of mind.'}
        ],
        'details': [
            'We partner with top-tier courier networks (FedEx, DHL, UPS) to guarantee fast, safe delivery.',
            'All items are packed in shock-proof, anti-static sealed boxes with tamper-evident security tape.',
            'Optional Priority Express overnight shipping available at checkout for urgent orders.'
        ],
        'faqs': [
            {'q': 'How quickly will my order be dispatched?', 'a': 'Orders placed before 2 PM local time ship out the same day. Orders placed after 2 PM ship out the next business morning.'},
            {'q': 'Are there any hidden delivery charges?', 'a': 'None at all! All standard delivery options are 100% free on every order.'},
            {'q': 'How do I track my package?', 'a': 'Once shipped, you will receive a tracking link via email and can also view live updates directly from your Profile > Orders page.'}
        ]
    },
    'secure-shopping': {
        'slug': 'secure-shopping',
        'title': '100% Secure Shopping',
        'badge': '🛡️ BANK-GRADE SECURITY',
        'icon_class': 'cat-icon-feature-2',
        'icon_svg': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
        'short_desc': 'End-to-end 256-bit SSL encryption protecting every transaction.',
        'hero_subtitle': 'Your privacy, card details, and personal data are safeguarded by enterprise-grade payment encryption protocols.',
        'highlights': [
            {'icon': '🔒', 'title': '256-Bit SSL Encryption', 'desc': 'All communications and checkout data are encrypted with military-grade TLS 1.3 protocol.'},
            {'icon': '💳', 'title': 'PCI-DSS Level 1 Compliant', 'desc': 'We adhere to the highest international security standards. Raw card numbers are never stored.'},
            {'icon': '🤝', 'title': 'Buyer Protection Plan', 'desc': 'Guaranteed full refund if your item is not delivered as described or fails inspection.'},
            {'icon': '👁️', 'title': 'Zero Data Sharing', 'desc': 'Your personal details are strictly private. We never sell or share user data with third parties.'}
        ],
        'details': [
            'Every checkout uses 3D-Secure 2.0 authentication to verify your identity and protect against fraud.',
            'We accept verified payment channels including Credit/Debit Cards, Stripe, PayPal, Apple Pay, and Google Pay.',
            'Our system undergoes routine automated security audits and vulnerability scans to keep your data safe.'
        ],
        'faqs': [
            {'q': 'Is my payment information stored on your servers?', 'a': 'No. We process payments via PCI-DSS certified payment gateways. Your raw card details are never stored on our servers.'},
            {'q': 'What protection do I have if an order goes missing?', 'a': 'Our Buyer Protection Plan covers 100% of your payment with a full refund or instant replacement.'},
            {'q': 'Which payment methods are accepted?', 'a': 'We accept Visa, MasterCard, American Express, PayPal, Apple Pay, Google Pay, and major digital wallets.'}
        ]
    },
    'authentic-products': {
        'slug': 'authentic-products',
        'title': '100% Genuine & Authentic',
        'badge': '💎 BRAND AUTHENTICITY',
        'icon_class': 'cat-icon-feature-3',
        'icon_svg': '<path d="M6 3h12l4 6-10 12L2 9z"/>',
        'short_desc': 'Direct authorized sourcing with full manufacturer warranty.',
        'hero_subtitle': 'Zero compromise on quality. Sourced straight from authorized brand partners with original retail seals.',
        'highlights': [
            {'icon': '🏷️', 'title': 'Direct Brand Sourcing', 'desc': 'We partner directly with Apple, Samsung, Google, Dell, and Sony authorized channels.'},
            {'icon': '📜', 'title': 'Official Manufacturer Warranty', 'desc': 'Every device comes with full brand warranty valid at official brand service centers.'},
            {'icon': '🔍', 'title': 'Serial Number Verification', 'desc': 'Verify your product serial number directly on official manufacturer portals.'},
            {'icon': '✨', 'title': 'Factory Sealed Packaging', 'desc': 'Guaranteed brand new items delivered in original pristine retail boxes with factory seals.'}
        ],
        'details': [
            'We maintain a strict zero-counterfeit policy. Grey market and refurbished items are never sold as new.',
            'Products undergo serial registration checks prior to dispatch to ensure valid warranty activation.',
            'Formal tax invoices and official brand warranty documents are provided with every order.'
        ],
        'faqs': [
            {'q': 'Are all products 100% genuine and original?', 'a': 'Yes, 100%. All items sold on Mobile Mart are brand new, original, and sourced from authorized brand distributors.'},
            {'q': 'Does my purchase come with an official warranty?', 'a': 'Yes. Every device includes full manufacturer warranty valid at authorized service centers globally.'},
            {'q': 'How can I verify authenticity?', 'a': 'You can verify the serial number printed on the product box directly on the official brand manufacturer website.'}
        ]
    },
    'easy-returns': {
        'slug': 'easy-returns',
        'title': '30-Day Easy Returns',
        'badge': '🔄 HASSLE-FREE RETURNS',
        'icon_class': 'cat-icon-feature-4',
        'icon_svg': '<polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>',
        'short_desc': '30-day return policy with hassle-free pickup and instant refunds.',
        'hero_subtitle': 'Enjoy stress-free shopping with our generous 30-day return window, free doorstep pickups, and fast refunds.',
        'highlights': [
            {'icon': '📅', 'title': '30-Day Return Window', 'desc': 'Take your time. Return or exchange any item within 30 days of delivery.'},
            {'icon': '🚗', 'title': 'Free Doorstep Pickup', 'desc': 'We arrange courier pickup right from your home or office at zero extra charge.'},
            {'icon': '⚡', 'title': 'Fast Refund Credit', 'desc': 'Refunds are processed to your original payment method within 24 hours of package return inspection.'},
            {'icon': '🔁', 'title': 'Instant Replacements', 'desc': 'Encounter a transit defect? Request a brand-new unit replacement with express dispatch.'}
        ],
        'details': [
            'Easily request returns with one click from your user account profile page.',
            'Prepaid return labels and packaging instructions are provided immediately upon request.',
            'Our support team is available 24/7 to guide you through any return or exchange queries.'
        ],
        'faqs': [
            {'q': 'How do I start a return?', 'a': 'Go to your Account Profile > Orders, select the order item, and click "Request Return". Our team handles the rest!'},
            {'q': 'Do I have to pay for return shipping?', 'a': 'No! We provide free doorstep courier pickups and prepaid return shipping labels.'},
            {'q': 'When will I receive my refund?', 'a': 'Refunds are processed within 24 hours of the returned item arriving at our warehouse.'}
        ]
    }
}


@app.route('/why-us/<feature_slug>')
def why_us_detail(feature_slug):
    """Dedicated detailed page for Why Choose Us features."""
    feature = WHY_US_FEATURES.get(feature_slug)
    if not feature:
        return render_template('base.html', error_code=404, error_message='Feature page not found.'), 404
    
    other_features = [f for s, f in WHY_US_FEATURES.items() if s != feature_slug]
    
    return render_template('why_us_detail.html',
                           feature=feature,
                           other_features=other_features)


# ---------------------------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user = User.query.filter(
            db.or_(User.username == username, User.email == username)
        ).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Welcome back! You have logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        full_name = request.form.get('full_name', '').strip()

        errors = []
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        elif not re.match(r'^[A-Za-z]+$', username):
            errors.append('Letters only — username must contain only letters (A-Z, a-z).')
        if full_name and not re.match(r'^[A-Za-z\s]+$', full_name):
            errors.append('Letters only — full name must contain only letters (A-Z, a-z).')
        if not email or '@' not in email:
            errors.append('Please enter a valid email.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm:
            errors.append('Passwords do not match.')
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken.')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')

        if errors:
            for e in errors:
                flash(e, 'error')
        else:
            user = User(username=username, email=email, full_name=full_name)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Account created successfully! Welcome to Mobile Mart.', 'success')
            return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ---------------------------------------------------------------------------
# USER PROFILE & ORDERS
# ---------------------------------------------------------------------------

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name', '').strip()
        current_user.phone = request.form.get('phone', '').strip()
        current_user.address = request.form.get('address', '').strip()
        current_user.city = request.form.get('city', '').strip()

        new_password = request.form.get('new_password', '')
        if new_password:
            if len(new_password) < 6:
                flash('New password must be at least 6 characters.', 'error')
                return redirect(url_for('profile'))
            current_user.set_password(new_password)

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html')


@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id)\
        .order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)


@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = db.get_or_404(Order, order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    return render_template('order_detail.html', order=order)


# ---------------------------------------------------------------------------
# CART (AJAX + page)
# ---------------------------------------------------------------------------

@app.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', items=items)


@app.route('/cart/add', methods=['POST'])
@login_required
def cart_add():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)

    if not product_id or quantity < 1:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(success=False, message='Invalid request'), 400
        flash('Invalid request.', 'error')
        return redirect(request.referrer or url_for('products'))

    product = db.get_or_404(Product, product_id)
    if not product.in_stock:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(success=False, message='Product out of stock'), 400
        flash('Product is out of stock.', 'error')
        return redirect(request.referrer or url_for('products'))

    existing = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        existing.quantity = min(existing.quantity + quantity, product.stock)
    else:
        item = CartItem(user_id=current_user.id, product_id=product_id, quantity=min(quantity, product.stock))
        db.session.add(item)

    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(success=True, cart_count=current_user.cart_count, message='Added to cart!')
    flash(f'{product.name} added to cart!', 'success')
    return redirect(request.referrer or url_for('products'))


@app.route('/cart/update', methods=['POST'])
@login_required
def cart_update():
    item_id = request.form.get('item_id', type=int)
    quantity = request.form.get('quantity', type=int)

    item = db.get_or_404(CartItem, item_id)
    if item.user_id != current_user.id:
        abort(403)

    if quantity and quantity > 0:
        item.quantity = min(quantity, item.product.stock)
        db.session.commit()
    else:
        db.session.delete(item)
        db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(
            success=True,
            cart_count=current_user.cart_count,
            cart_total=current_user.cart_total,
            item_subtotal=round(item.product.effective_price * item.quantity, 2) if quantity and quantity > 0 else 0
        )
    return redirect(url_for('cart'))


@app.route('/cart/remove', methods=['POST'])
@login_required
def cart_remove():
    item_id = request.form.get('item_id', type=int)
    item = db.get_or_404(CartItem, item_id)
    if item.user_id != current_user.id:
        abort(403)

    db.session.delete(item)
    db.session.commit()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(success=True, cart_count=current_user.cart_count, cart_total=current_user.cart_total)
    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))


# ---------------------------------------------------------------------------
# CHECKOUT
# ---------------------------------------------------------------------------

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('products'))

    if request.method == 'POST':
        shipping_name = request.form.get('shipping_name', '').strip()
        shipping_address = request.form.get('shipping_address', '').strip()
        shipping_city = request.form.get('shipping_city', '').strip()
        shipping_phone = request.form.get('shipping_phone', '').strip()
        payment_method = request.form.get('payment_method', 'Cash on Delivery')
        notes = request.form.get('notes', '').strip()

        if not all([shipping_name, shipping_address, shipping_city, shipping_phone]):
            flash('Please fill in all required shipping fields.', 'error')
            return render_template('checkout.html', items=items)

        # Calculate total
        total = 0
        for ci in items:
            total += ci.product.effective_price * ci.quantity

        # Create order
        order = Order(
            user_id=current_user.id,
            total=round(total, 2),
            shipping_name=shipping_name,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_phone=shipping_phone,
            payment_method=payment_method,
            notes=notes
        )
        db.session.add(order)
        db.session.flush()  # get order.id

        # Create order items & reduce stock
        for ci in items:
            oi = OrderItem(
                order_id=order.id,
                product_id=ci.product_id,
                quantity=ci.quantity,
                price=ci.product.effective_price
            )
            db.session.add(oi)
            ci.product.stock = max(0, ci.product.stock - ci.quantity)

        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        flash(f'Order #{order.id} placed successfully!', 'success')
        return redirect(url_for('order_detail', order_id=order.id))

    return render_template('checkout.html', items=items)


# ---------------------------------------------------------------------------
# REVIEWS
# ---------------------------------------------------------------------------

@app.route('/review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    product = db.get_or_404(Product, product_id)

    existing = Review.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        flash('You have already reviewed this product.', 'info')
        return redirect(url_for('product_detail', slug=product.slug))

    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment', '').strip()

    if not rating or rating < 1 or rating > 5:
        flash('Please select a rating (1-5).', 'error')
        return redirect(url_for('product_detail', slug=product.slug))

    review = Review(
        user_id=current_user.id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    product.update_rating()
    db.session.commit()

    flash('Thank you for your review!', 'success')
    return redirect(url_for('product_detail', slug=product.slug))


# ---------------------------------------------------------------------------
# ADMIN ROUTES
# ---------------------------------------------------------------------------

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total)).filter(
        Order.status != 'Cancelled'
    ).scalar() or 0

    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    low_stock = Product.query.filter(Product.stock < 5).order_by(Product.stock.asc()).all()

    # Orders by status for chart
    status_counts = {}
    for status in ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']:
        status_counts[status] = Order.query.filter_by(status=status).count()

    return render_template('admin/dashboard.html',
                           total_products=total_products,
                           total_orders=total_orders,
                           total_users=total_users,
                           total_revenue=round(total_revenue, 2),
                           recent_orders=recent_orders,
                           low_stock=low_stock,
                           status_counts=status_counts)


@app.route('/admin/products')
@login_required
@admin_required
def admin_products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/products.html', products=products)


@app.route('/admin/product/new', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_product_new():
    categories = Category.query.order_by(Category.name).all()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        slug = name.lower().replace(' ', '-').replace('/', '-')
        description = request.form.get('description', '').strip()
        price = request.form.get('price', type=float)
        discount_price = request.form.get('discount_price', type=float)
        stock = request.form.get('stock', 0, type=int)
        category_id = request.form.get('category_id', type=int)
        brand = request.form.get('brand', '').strip()
        featured = bool(request.form.get('featured'))
        image_url = request.form.get('image_url', '/static/images/placeholder.png').strip()

        # Collect specs
        spec_keys = request.form.getlist('spec_key[]')
        spec_vals = request.form.getlist('spec_value[]')
        specs = {}
        for k, v in zip(spec_keys, spec_vals):
            if k.strip() and v.strip():
                specs[k.strip()] = v.strip()

        if not name or not price or not category_id:
            flash('Name, price, and category are required.', 'error')
            return render_template('admin/product_form.html', categories=categories, product=None)

        # Make slug unique
        existing = Product.query.filter_by(slug=slug).first()
        if existing:
            slug = slug + '-' + str(Product.query.count() + 1)

        product = Product(
            name=name, slug=slug, description=description,
            price=price, discount_price=discount_price if discount_price else None,
            stock=stock, category_id=category_id, brand=brand,
            featured=featured, image_url=image_url,
            specs=json.dumps(specs)
        )
        db.session.add(product)
        db.session.commit()
        flash(f'Product "{name}" created successfully!', 'success')
        return redirect(url_for('admin_products'))

    return render_template('admin/product_form.html', categories=categories, product=None)


@app.route('/admin/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_product_edit(product_id):
    product = db.get_or_404(Product, product_id)
    categories = Category.query.order_by(Category.name).all()

    if request.method == 'POST':
        product.name = request.form.get('name', '').strip()
        product.description = request.form.get('description', '').strip()
        product.price = request.form.get('price', type=float)
        discount_price = request.form.get('discount_price', type=float)
        product.discount_price = discount_price if discount_price else None
        product.stock = request.form.get('stock', 0, type=int)
        product.category_id = request.form.get('category_id', type=int)
        product.brand = request.form.get('brand', '').strip()
        product.featured = bool(request.form.get('featured'))
        product.image_url = request.form.get('image_url', product.image_url).strip()

        spec_keys = request.form.getlist('spec_key[]')
        spec_vals = request.form.getlist('spec_value[]')
        specs = {}
        for k, v in zip(spec_keys, spec_vals):
            if k.strip() and v.strip():
                specs[k.strip()] = v.strip()
        product.specs = json.dumps(specs)

        db.session.commit()
        flash(f'Product "{product.name}" updated!', 'success')
        return redirect(url_for('admin_products'))

    specs = {}
    try:
        specs = json.loads(product.specs) if product.specs else {}
    except (json.JSONDecodeError, TypeError):
        specs = {}
    product._parsed_specs = specs

    return render_template('admin/product_form.html', categories=categories, product=product)


@app.route('/admin/product/<int:product_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_product_delete(product_id):
    product = db.get_or_404(Product, product_id)
    name = product.name
    db.session.delete(product)
    db.session.commit()
    flash(f'Product "{name}" deleted.', 'info')
    return redirect(url_for('admin_products'))


@app.route('/admin/orders')
@login_required
@admin_required
def admin_orders():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    query = Order.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/orders.html', orders=orders, status_filter=status_filter)


@app.route('/admin/order/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def admin_order_status(order_id):
    order = db.get_or_404(Order, order_id)
    new_status = request.form.get('status', '')
    if new_status in ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.id} status updated to {new_status}.', 'success')
    return redirect(request.referrer or url_for('admin_orders'))


@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


# ---------------------------------------------------------------------------
# ERROR HANDLERS
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template('base.html', error_code=404, error_message='Page not found'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('base.html', error_code=403, error_message='Access denied'), 403


# ---------------------------------------------------------------------------
# RUN
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', '0') == '1'
    )
