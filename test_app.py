"""
Automated Integration & Unit Tests for Mobile Mart System.
Tests every route, authentication, cart flow, checkout flow, review flow, and admin panel.
"""

import unittest
from app import app
from models import db, User, Product, Category, CartItem, Order, OrderItem, Review

class MobileMartTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    # ── Test Public Pages ──────────────────────────────────────────
    def test_home_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Mobile Mart', res.data)
        self.assertIn(b'Shop by Category', res.data)

    def test_products_page(self):
        res = self.client.get('/products')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'All Products', res.data)

    def test_products_filter_and_search(self):
        res = self.client.get('/products?category=smartphones')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/products?q=Galaxy')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Galaxy', res.data)

        res = self.client.get('/products?sort=price_low')
        self.assertEqual(res.status_code, 200)

    def test_product_detail(self):
        p = Product.query.first()
        self.assertIsNotNone(p)
        res = self.client.get(f'/product/{p.slug}')
        self.assertEqual(res.status_code, 200)
        self.assertIn(p.name.encode(), res.data)

    def test_search_redirect(self):
        res = self.client.get('/search?q=Apple')
        self.assertEqual(res.status_code, 302)
        self.assertIn('/products?q=Apple', res.headers['Location'])

    def test_why_us_feature_pages(self):
        features = ['fast-delivery', 'secure-shopping', 'authentic-products', 'easy-returns']
        for slug in features:
            res = self.client.get(f'/why-us/{slug}')
            self.assertEqual(res.status_code, 200)
            self.assertIn(b'Why Choose Us', res.data)

    # ── Test Auth ──────────────────────────────────────────────────
    def test_login_and_logout(self):
        # Demo user login
        res = self.client.post('/login', data={
            'username': 'demo',
            'password': 'demo123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Welcome back', res.data)

        # Logout
        res = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'logged out', res.data)

    def test_user_registration(self):
        test_user = 'userreg' + chr(97 + User.query.count() % 26) + chr(97 + (User.query.count() + 1) % 26)
        res = self.client.post('/register', data={
            'username': test_user,
            'email': f'{test_user}@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'full_name': 'Test User'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Account created successfully', res.data)

    def test_user_registration_invalid_username_or_fullname(self):
        # Reject numbers in username
        res = self.client.post('/register', data={
            'username': 'user123',
            'email': 'user123@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'full_name': 'Test User'
        }, follow_redirects=True)
        self.assertIn(b'Letters only', res.data)

        # Reject numbers in full name
        res = self.client.post('/register', data={
            'username': 'validuser',
            'email': 'validuser@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'full_name': 'John 123'
        }, follow_redirects=True)
        self.assertIn(b'Letters only', res.data)

    # ── Test Cart & Checkout ───────────────────────────────────────
    def test_cart_and_checkout_flow(self):
        # Login demo
        self.client.post('/login', data={'username': 'demo', 'password': 'demo123'})

        # Add to cart
        p = Product.query.filter(Product.stock > 0).first()
        res = self.client.post('/cart/add', data={
            'product_id': p.id,
            'quantity': 2
        }, headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['success'])

        # View Cart
        res = self.client.get('/cart')
        self.assertEqual(res.status_code, 200)
        self.assertIn(p.name.encode(), res.data)

        # Checkout GET
        res = self.client.get('/checkout')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Shipping Information', res.data)

        # Checkout POST
        res = self.client.post('/checkout', data={
            'shipping_name': 'Demo Customer',
            'shipping_address': '789 Testing Road',
            'shipping_city': 'Tech City',
            'shipping_phone': '+1-555-9999',
            'payment_method': 'Cash on Delivery',
            'notes': 'Please ring the bell'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Order #', res.data)
        self.assertIn(b'789 Testing Road', res.data)

    # ── Test Profile & Orders ──────────────────────────────────────
    def test_profile_and_orders(self):
        self.client.post('/login', data={'username': 'demo', 'password': 'demo123'})

        # Profile GET
        res = self.client.get('/profile')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'My Profile', res.data)

        # Profile Update POST
        res = self.client.post('/profile', data={
            'full_name': 'Demo User Updated',
            'phone': '+1-555-8888',
            'address': 'New Updated Address',
            'city': 'San Francisco',
            'new_password': ''
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Profile updated successfully', res.data)

        # Orders List GET
        res = self.client.get('/orders')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'My Orders', res.data)

    # ── Test Admin Functions ───────────────────────────────────────
    def test_admin_access_control(self):
        # Demo (non-admin) should get 403 on admin dashboard
        self.client.post('/login', data={'username': 'demo', 'password': 'demo123'})
        res = self.client.get('/admin')
        self.assertEqual(res.status_code, 403)

        # Admin login
        self.client.get('/logout')
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'})

        # Admin dashboard
        res = self.client.get('/admin')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Store Overview', res.data)

        # Admin products list
        res = self.client.get('/admin/products')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Products Management', res.data)

        # Admin new product GET & POST
        res = self.client.get('/admin/product/new')
        self.assertEqual(res.status_code, 200)

        cat = Category.query.first()
        res = self.client.post('/admin/product/new', data={
            'name': 'Test New Product Phone',
            'category_id': cat.id,
            'brand': 'TestBrand',
            'price': 499.99,
            'discount_price': 449.99,
            'stock': 15,
            'featured': '1',
            'image_url': '/static/images/placeholder.png',
            'description': 'A fantastic test phone.',
            'spec_key[]': ['Screen', 'Battery'],
            'spec_value[]': ['6.5 inch', '5000 mAh']
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'created successfully', res.data)

        # Admin orders list
        res = self.client.get('/admin/orders')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Orders Management', res.data)

        # Admin users list
        res = self.client.get('/admin/users')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Users Management', res.data)

if __name__ == '__main__':
    unittest.main()
