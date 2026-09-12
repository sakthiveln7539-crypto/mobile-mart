/**
 * Mobile Mart System — Frontend JavaScript
 * Cart AJAX, search, quantity controls, animations, flash messages
 */

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initFlashMessages();
    initQuantityControls();
    initCartActions();
    initStarRating();
    initSearchForm();
    initAnimations();
    initSpecsForm();
    initFilterForm();
    initHeroCarousel();
});


// ── Mobile Navigation Toggle ──────────────────────────────────
function initMobileMenu() {
    const toggle = document.querySelector('.mobile-toggle');
    const nav = document.querySelector('.navbar-nav');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', () => {
        nav.classList.toggle('active');
        toggle.textContent = nav.classList.contains('active') ? '✕' : '☰';
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!toggle.contains(e.target) && !nav.contains(e.target)) {
            nav.classList.remove('active');
            toggle.textContent = '☰';
        }
    });
}


// ── Flash Messages ────────────────────────────────────────────
function initFlashMessages() {
    const container = document.querySelector('.flash-container');
    if (!container) return;

    // Auto-dismiss after 5 seconds
    container.querySelectorAll('.flash-message').forEach((msg, i) => {
        setTimeout(() => {
            msg.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => msg.remove(), 300);
        }, 5000 + (i * 500));

        msg.addEventListener('click', () => {
            msg.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => msg.remove(), 300);
        });
    });

    // Add slideOut animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideOutRight {
            to { transform: translateX(120%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}

function showFlash(message, type = 'success') {
    let container = document.querySelector('.flash-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'flash-container';
        document.body.appendChild(container);
    }

    const icons = { success: '✓', error: '✕', info: 'ℹ', warning: '⚠' };
    const flash = document.createElement('div');
    flash.className = `flash-message ${type}`;
    flash.innerHTML = `<span>${icons[type] || 'ℹ'}</span> ${message}`;

    container.appendChild(flash);

    setTimeout(() => {
        flash.style.animation = 'slideOutRight 0.3s ease forwards';
        setTimeout(() => flash.remove(), 300);
    }, 4000);

    flash.addEventListener('click', () => {
        flash.style.animation = 'slideOutRight 0.3s ease forwards';
        setTimeout(() => flash.remove(), 300);
    });
}


// ── Quantity Controls ─────────────────────────────────────────
function initQuantityControls() {
    document.querySelectorAll('.quantity-controls').forEach(ctrl => {
        const input = ctrl.querySelector('input');
        const minusBtn = ctrl.querySelector('.qty-minus');
        const plusBtn = ctrl.querySelector('.qty-plus');
        if (!input) return;

        const min = parseInt(input.min) || 1;
        const max = parseInt(input.max) || 99;

        if (minusBtn) {
            minusBtn.addEventListener('click', () => {
                let val = parseInt(input.value) || min;
                if (val > min) {
                    input.value = val - 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
        }

        if (plusBtn) {
            plusBtn.addEventListener('click', () => {
                let val = parseInt(input.value) || min;
                if (val < max) {
                    input.value = val + 1;
                    input.dispatchEvent(new Event('change'));
                }
            });
        }
    });
}


// ── Cart AJAX Actions ─────────────────────────────────────────
function initCartActions() {
    // Add to cart buttons (AJAX)
    document.querySelectorAll('.ajax-add-cart').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('button[type="submit"]');
            const origText = btn.innerHTML;

            btn.disabled = true;
            btn.innerHTML = '<span class="spinner" style="width:16px;height:16px;border-width:2px;margin:0;"></span>';

            try {
                const formData = new FormData(form);
                const res = await fetch(form.action, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    body: formData
                });
                const data = await res.json();

                if (data.success) {
                    updateCartBadge(data.cart_count);
                    showFlash(data.message || 'Added to cart!', 'success');
                    btn.innerHTML = '✓ Added';
                    setTimeout(() => { btn.innerHTML = origText; btn.disabled = false; }, 1500);
                } else {
                    showFlash(data.message || 'Error adding to cart', 'error');
                    btn.innerHTML = origText;
                    btn.disabled = false;
                }
            } catch (err) {
                showFlash('Something went wrong. Please try again.', 'error');
                btn.innerHTML = origText;
                btn.disabled = false;
            }
        });
    });

    // Cart quantity update
    document.querySelectorAll('.cart-qty-form').forEach(form => {
        const input = form.querySelector('input[name="quantity"]');
        if (!input) return;

        input.addEventListener('change', async () => {
            const formData = new FormData(form);
            formData.set('quantity', input.value);

            try {
                const res = await fetch(form.action, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    body: formData
                });
                const data = await res.json();
                if (data.success) {
                    updateCartBadge(data.cart_count);
                    // Update subtotal display
                    const row = form.closest('.cart-item');
                    if (row) {
                        const priceEl = row.querySelector('.cart-item-price');
                        if (priceEl) priceEl.textContent = '$' + data.item_subtotal.toFixed(2);
                    }
                    // Update total
                    const totalEl = document.querySelector('.cart-total-value');
                    if (totalEl) totalEl.textContent = '$' + data.cart_total.toFixed(2);
                }
            } catch (err) {
                console.error('Error updating cart:', err);
            }
        });
    });

    // Cart remove item
    document.querySelectorAll('.cart-remove-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const row = form.closest('.cart-item');

            try {
                const formData = new FormData(form);
                const res = await fetch(form.action, {
                    method: 'POST',
                    headers: { 'X-Requested-With': 'XMLHttpRequest' },
                    body: formData
                });
                const data = await res.json();

                if (data.success) {
                    updateCartBadge(data.cart_count);
                    if (row) {
                        row.style.animation = 'slideOutRight 0.3s ease forwards';
                        setTimeout(() => {
                            row.remove();
                            // Check if cart is empty
                            if (!document.querySelector('.cart-item')) {
                                location.reload();
                            }
                        }, 300);
                    }
                    const totalEl = document.querySelector('.cart-total-value');
                    if (totalEl) totalEl.textContent = '$' + data.cart_total.toFixed(2);
                    showFlash('Item removed from cart.', 'info');
                }
            } catch (err) {
                form.submit(); // Fallback to regular submit
            }
        });
    });
}

function updateCartBadge(count) {
    const badges = document.querySelectorAll('.cart-badge');
    badges.forEach(badge => {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'flex' : 'none';
        badge.style.animation = 'none';
        badge.offsetHeight; // Trigger reflow
        badge.style.animation = 'badgePop 0.3s ease';
    });
}


// ── Star Rating Widget ────────────────────────────────────────
function initStarRating() {
    const ratingContainer = document.querySelector('.star-rating');
    if (!ratingContainer) return;

    const inputs = ratingContainer.querySelectorAll('input');
    const labels = ratingContainer.querySelectorAll('label');

    labels.forEach(label => {
        label.addEventListener('mouseenter', () => {
            const val = label.getAttribute('for').replace('star', '');
            highlightStars(labels, val);
        });
    });

    ratingContainer.addEventListener('mouseleave', () => {
        const checked = ratingContainer.querySelector('input:checked');
        if (checked) {
            highlightStars(labels, checked.value);
        } else {
            labels.forEach(l => l.style.color = '');
        }
    });
}

function highlightStars(labels, value) {
    labels.forEach(label => {
        const starVal = label.getAttribute('for').replace('star', '');
        label.style.color = starVal <= value ? '#fbbf24' : '';
    });
}


// ── Search ────────────────────────────────────────────────────
function initSearchForm() {
    const searchInput = document.querySelector('.nav-search input');
    if (!searchInput) return;

    // Debounced search on enter
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const q = searchInput.value.trim();
            if (q) {
                window.location.href = `/products?q=${encodeURIComponent(q)}`;
            }
        }
    });
}


// ── Scroll Animations ─────────────────────────────────────────
function initAnimations() {
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '';
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.05 });

    document.querySelectorAll('.product-card, .category-card, .stat-card').forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
}


// ── Admin: Dynamic Spec Rows ──────────────────────────────────
function initSpecsForm() {
    const addBtn = document.getElementById('add-spec-row');
    const container = document.getElementById('specs-container');
    if (!addBtn || !container) return;

    addBtn.addEventListener('click', () => {
        const row = document.createElement('div');
        row.className = 'spec-row';
        row.innerHTML = `
            <input type="text" name="spec_key[]" class="form-control" placeholder="Spec name">
            <input type="text" name="spec_value[]" class="form-control" placeholder="Value">
            <button type="button" class="btn-remove-spec" onclick="this.parentElement.remove()">✕</button>
        `;
        container.appendChild(row);
    });
}


// ── Filter Form Auto-Submit ───────────────────────────────────
function initFilterForm() {
    const filterForm = document.getElementById('filter-form');
    if (!filterForm) return;

    filterForm.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', () => {
            filterForm.submit();
        });
    });
}


// ── Hero Carousel / Rotating Banner ───────────────────────────
function initHeroCarousel() {
    const carousel = document.getElementById('hero-carousel');
    if (!carousel) return;

    const slides = carousel.querySelectorAll('.carousel-slide');
    const dots = carousel.querySelectorAll('.carousel-dot');
    const prevBtn = document.getElementById('carousel-prev');
    const nextBtn = document.getElementById('carousel-next');

    if (slides.length === 0) return;

    let currentIndex = 0;
    let autoplayTimer = null;
    let isPaused = false;
    const INTERVAL = 5000; // 5 seconds

    function goToSlide(index, skipAnimation = false) {
        // Clamp index
        if (index < 0) index = slides.length - 1;
        if (index >= slides.length) index = 0;

        // Don't re-trigger if same slide
        if (index === currentIndex && !skipAnimation) return;

        // Deactivate current
        slides[currentIndex].classList.remove('active');
        dots[currentIndex].classList.remove('active');

        // Reset progress animation on old dot
        const oldProgress = dots[currentIndex].querySelector('.dot-progress');
        if (oldProgress) {
            oldProgress.style.animation = 'none';
            oldProgress.offsetHeight; // Reflow
            oldProgress.style.width = '0';
        }

        // Activate new
        currentIndex = index;
        slides[currentIndex].classList.add('active');
        dots[currentIndex].classList.add('active');

        // Restart progress animation on new dot
        const newProgress = dots[currentIndex].querySelector('.dot-progress');
        if (newProgress) {
            newProgress.style.animation = 'none';
            newProgress.offsetHeight; // Reflow
            newProgress.style.animation = 'dotFill ' + INTERVAL + 'ms linear forwards';
        }
    }

    function nextSlide() {
        goToSlide(currentIndex + 1);
    }

    function prevSlide() {
        goToSlide(currentIndex - 1);
    }

    function startAutoplay() {
        stopAutoplay();
        autoplayTimer = setInterval(() => {
            if (!isPaused) nextSlide();
        }, INTERVAL);
    }

    function stopAutoplay() {
        if (autoplayTimer) {
            clearInterval(autoplayTimer);
            autoplayTimer = null;
        }
    }

    // Dot click handlers
    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            const idx = parseInt(dot.dataset.index, 10);
            goToSlide(idx);
            startAutoplay(); // Reset timer on manual interaction
        });
    });

    // Arrow buttons
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            prevSlide();
            startAutoplay();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            nextSlide();
            startAutoplay();
        });
    }

    // Pause on hover
    carousel.addEventListener('mouseenter', () => {
        isPaused = true;
    });

    carousel.addEventListener('mouseleave', () => {
        isPaused = false;
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        // Only respond if carousel is visible in viewport
        const rect = carousel.getBoundingClientRect();
        const inView = rect.top < window.innerHeight && rect.bottom > 0;
        if (!inView) return;

        if (e.key === 'ArrowLeft') {
            prevSlide();
            startAutoplay();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
            startAutoplay();
        }
    });

    // Touch/swipe support
    let touchStartX = 0;
    let touchEndX = 0;
    const SWIPE_THRESHOLD = 50;

    carousel.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    carousel.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        const diff = touchStartX - touchEndX;
        if (Math.abs(diff) > SWIPE_THRESHOLD) {
            if (diff > 0) {
                nextSlide(); // Swipe left → next
            } else {
                prevSlide(); // Swipe right → prev
            }
            startAutoplay();
        }
    }, { passive: true });

    // Pause autoplay when tab is hidden (save resources)
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            stopAutoplay();
        } else {
            startAutoplay();
        }
    });

    // Initialize: trigger progress animation on first dot
    goToSlide(0, true);

    // Start auto-rotation
    startAutoplay();
}
