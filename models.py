"""
Mobile Mart System — Database Models
SQLAlchemy models for Users, Products, Categories, Cart, Orders, Reviews
"""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User account model with authentication support."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), default='')
    phone = db.Column(db.String(20), default='')
    address = db.Column(db.Text, default='')
    city = db.Column(db.String(100), default='')
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def cart_count(self):
        return sum(item.quantity for item in self.cart_items)

    @property
    def cart_total(self):
        total = 0
        for item in self.cart_items:
            price = item.product.discount_price if item.product.discount_price else item.product.price
            total += price * item.quantity
        return round(total, 2)


class Category(db.Model):
    """Product category model."""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    icon = db.Column(db.String(50), default='📱')
    description = db.Column(db.Text, default='')

    products = db.relationship('Product', backref='category', lazy=True)

    @property
    def product_count(self):
        return len(self.products)


class Product(db.Model):
    """Product model with pricing, stock, and metadata."""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, default='')
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500), default='/static/images/placeholder.png')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    brand = db.Column(db.String(100), default='')
    specs = db.Column(db.Text, default='{}')  # JSON string
    featured = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percent(self):
        if self.discount_price and self.price > 0:
            return round((1 - self.discount_price / self.price) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0

    def update_rating(self):
        """Recalculate average rating from reviews."""
        reviews = Review.query.filter_by(product_id=self.id).all()
        if reviews:
            self.rating = round(sum(r.rating for r in reviews) / len(reviews), 1)
            self.review_count = len(reviews)
        else:
            self.rating = 0.0
            self.review_count = 0


class CartItem(db.Model):
    """Shopping cart item linking user to product with quantity."""
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    product = db.relationship('Product', lazy=True)


class Order(db.Model):
    """Customer order model."""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), default='Pending')  # Pending, Processing, Shipped, Delivered, Cancelled
    shipping_name = db.Column(db.String(150), default='')
    shipping_address = db.Column(db.Text, default='')
    shipping_city = db.Column(db.String(100), default='')
    shipping_phone = db.Column(db.String(20), default='')
    payment_method = db.Column(db.String(50), default='Cash on Delivery')
    notes = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items)

    @property
    def status_color(self):
        colors = {
            'Pending': '#f59e0b',
            'Processing': '#3b82f6',
            'Shipped': '#8b5cf6',
            'Delivered': '#10b981',
            'Cancelled': '#ef4444'
        }
        return colors.get(self.status, '#6b7280')


class OrderItem(db.Model):
    """Individual item within an order."""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)  # Price at time of purchase

    @property
    def subtotal(self):
        return round(self.price * self.quantity, 2)


class Review(db.Model):
    """Product review with rating and comment."""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
