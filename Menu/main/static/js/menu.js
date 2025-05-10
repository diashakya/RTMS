/* 
Table of Contents:
1. DOM Ready Handler
2. Category Filtering
3. Search Functionality
4. Add to Cart Functionality
5. Today's Special Section
6. Helper Functions
7. Cart System
*/

// Main DOM Ready Handler
document.addEventListener("DOMContentLoaded", function() {
    initCategoryFiltering();
    initSearchFunctionality();
    initAddToCart();
    initTodaysSpecial();
    initCartSystem();
});

/* ---------------------------------------- Category Filtering ---------------------------------------- */
function initCategoryFiltering() {
    const categoryBtns = document.querySelectorAll(".category-btn");
    const menuItems = document.querySelectorAll(".menu-item-card");

    categoryBtns.forEach((btn) => {
        btn.addEventListener("click", function() {
            // Update active state
            categoryBtns.forEach((b) => b.classList.remove("active"));
            this.classList.add("active");

            // Filter items
            const category = this.dataset.category;
            menuItems.forEach((item) => {
                const shouldShow = category === "all" || item.dataset.category === category;
                item.style.display = shouldShow ? "block" : "none";
            });
        });
    });
}

/* ---------------------------------------- Search Functionality ---------------------------------------- */
function initSearchFunctionality() {
    const searchInput = document.getElementById("menu-search");
    const searchBtn = document.querySelector(".search-btn");
    const searchFeedback = document.getElementById("search-feedback");
    const menuItems = document.querySelectorAll(".menu-item-card");

    if (!searchInput) return;

    const filterMenuItems = (searchTerm) => {
        const term = searchTerm.toLowerCase().trim();
        let visibleItems = 0;

        menuItems.forEach(item => {
            const title = item.querySelector("h3").textContent.toLowerCase();
            const description = item.querySelector(".item-description")?.textContent.toLowerCase() || "";
            const isMatch = title.includes(term) || description.includes(term);
            
            item.style.display = isMatch ? "block" : "none";
            if (isMatch) visibleItems++;
        });

        // Update feedback messages
        if (searchFeedback) {
            searchFeedback.style.display = visibleItems === 0 && term !== "" ? "block" : "none";
        }

        const noItems = document.querySelector(".no-items");
        if (noItems) {
            noItems.style.display = visibleItems === 0 ? "block" : "none";
        }
    };

    // Event listeners
    searchInput.addEventListener("input", () => filterMenuItems(searchInput.value));
    searchInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") filterMenuItems(searchInput.value);
    });

    if (searchBtn) {
        searchBtn.addEventListener("click", () => filterMenuItems(searchInput.value));
    }
}

/* ---------------------------------------- Add to Cart Functionality ---------------------------------------- */
function initAddToCart() {
    const addToCartBtns = document.querySelectorAll(".add-to-cart-btn");

    addToCartBtns.forEach(btn => {
        btn.addEventListener("click", function() {
            const itemCard = this.closest(".menu-item-card, .special-item-card");
            const itemId = this.dataset.id;
            const itemName = itemCard.querySelector("h3").textContent;
            const itemPrice = itemCard.querySelector(".item-price").textContent;
            const quantity = itemCard.querySelector(".quantity")?.textContent || "1";

            console.log(`Added to cart: ${quantity}x ${itemName} - ${itemPrice}`);
            // TODO: Implement actual cart functionality
        });
    });
}

/* ---------------------------------------- Today's Special Section ---------------------------------------- */
function initTodaysSpecial() {
    // Quantity controls
    document.querySelectorAll(".quantity-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            const container = this.closest(".quantity-controls");
            const quantityElement = container.querySelector(".quantity");
            let quantity = parseInt(quantityElement.textContent);

            if (this.classList.contains("minus") && quantity > 1) {
                quantity--;
            } else if (this.classList.contains("plus")) {
                quantity++;
            }

            quantityElement.textContent = quantity;
        });
    });

    // Special items add to cart
    document.querySelectorAll(".special-item-card .add-to-cart-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            const card = this.closest(".special-item-card");
            const itemId = this.dataset.id;
            const itemName = card.querySelector("h3").textContent;
            const quantity = parseInt(card.querySelector(".quantity").textContent);
            const price = parseFloat(card.querySelector(".item-price").textContent.replace("Rs ", ""));

            console.log(`Added to cart: ${quantity}x ${itemName} - Rs ${(price * quantity).toFixed(2)}`);
            // TODO: Implement actual cart functionality
        });
    });
}

/* ---------------------------------------- Helper Functions ---------------------------------------- */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Back to Top Button
const backToTopBtn = document.getElementById('back-to-top');

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopBtn.style.display = 'flex';
    } else {
        backToTopBtn.style.display = 'none';
    }
});

backToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Quick View Functionality
document.querySelectorAll('.quick-view-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const itemId = btn.dataset.id;
        // Implement quick view modal functionality
        showQuickViewModal(itemId);
    });
});

// Favorite Button Functionality
document.querySelectorAll('.favorite-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const itemId = btn.dataset.id;
        const icon = btn.querySelector('i');
        
        if (icon.classList.contains('far')) {
            icon.classList.remove('far');
            icon.classList.add('fas');
            // Add to favorites
            addToFavorites(itemId);
        } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
            // Remove from favorites
            removeFromFavorites(itemId);
        }
    });
});

// Share Button Functionality
document.querySelectorAll('.share-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const itemId = btn.dataset.id;
        shareItem(itemId);
    });
});

// Quick Actions Buttons
document.getElementById('reservation-btn').addEventListener('click', () => {
    // Implement reservation functionality
    window.location.href = '/reservation/';
});

document.getElementById('catering-btn').addEventListener('click', () => {
    // Implement catering services functionality
    window.location.href = '/catering/';
});

document.getElementById('gift-card-btn').addEventListener('click', () => {
    // Implement gift card functionality
    window.location.href = '/gift-cards/';
});

// Helper Functions
function showQuickViewModal(itemId) {
    // Implement quick view modal
    console.log('Quick view for item:', itemId);
}

function addToFavorites(itemId) {
    // Implement add to favorites
    console.log('Added to favorites:', itemId);
}

function removeFromFavorites(itemId) {
    // Implement remove from favorites
    console.log('Removed from favorites:', itemId);
}

function shareItem(itemId) {
    // Implement share functionality
    if (navigator.share) {
        navigator.share({
            title: 'Check out this delicious item!',
            text: 'I found this amazing dish on our restaurant website!',
            url: window.location.href
        })
        .catch(error => console.log('Error sharing:', error));
    } else {
        // Fallback for browsers that don't support Web Share API
        const dummy = document.createElement('input');
        document.body.appendChild(dummy);
        dummy.value = window.location.href;
        dummy.select();
        document.execCommand('copy');
        document.body.removeChild(dummy);
        alert('Link copied to clipboard!');
    }
}

// Category Filter Animation
document.querySelectorAll('.category-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');
    });
});

// Search Animation
const searchInput = document.getElementById('menu-search');
const searchFeedback = document.getElementById('search-feedback');

searchInput.addEventListener('input', () => {
    if (searchInput.value.length > 0) {
        searchFeedback.style.display = 'block';
    } else {
        searchFeedback.style.display = 'none';
    }
});

// === CART SYSTEM ===

function initCartSystem() {
    // Cart button and dropdown
    const cartBtn = document.getElementById('cart-btn');
    const cartDropdown = document.getElementById('cart-dropdown');
    const cartCount = document.getElementById('cart-count');
    const cartItemsList = document.getElementById('cart-items-list');
    const cartTotalSection = document.getElementById('cart-total-section');
    const cartTotal = document.getElementById('cart-total');

    // Toggle cart dropdown
    if (cartBtn && cartDropdown) {
        cartBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            cartDropdown.style.display = cartDropdown.style.display === 'block' ? 'none' : 'block';
            renderCartDropdown();
        });
        // Hide dropdown on outside click
        document.addEventListener('click', function(e) {
            if (!cartDropdown.contains(e.target) && e.target !== cartBtn) {
                cartDropdown.style.display = 'none';
            }
        });
    }

    // Render cart dropdown
    function renderCartDropdown() {
        const cart = getCart();
        if (cart.length === 0) {
            cartItemsList.innerHTML = '<p style="color: #888;">Cart is empty.</p>';
            cartTotalSection.style.display = 'none';
            cartCount.textContent = '0';
            return;
        }
        let html = '';
        let total = 0;
        cart.forEach((item, idx) => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            html += `
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
                    <div style="flex: 1;">
                        <div style="font-weight: bold; color: #222;">${item.name}</div>
                        <div style="font-size: 0.95em; color: #888;">Rs ${item.price} x 
                            <button class="cart-qty-btn" data-idx="${idx}" data-action="minus" style="border:none;background:none;font-weight:bold;color:#f76d37;">-</button>
                            <span style="margin:0 6px;">${item.quantity}</span>
                            <button class="cart-qty-btn" data-idx="${idx}" data-action="plus" style="border:none;background:none;font-weight:bold;color:#f76d37;">+</button>
                        </div>
                    </div>
                    <div style="margin-left: 10px; font-weight: bold; color: #f76d37;">Rs ${itemTotal}</div>
                    <button class="cart-remove-btn" data-idx="${idx}" style="margin-left: 10px; background: none; border: none; color: #d32f2f; font-size: 1.2em;">&times;</button>
                </div>
            `;
        });
        cartItemsList.innerHTML = html;
        cartTotal.textContent = `Rs ${total}`;
        cartTotalSection.style.display = 'block';
        cartCount.textContent = cart.reduce((sum, item) => sum + item.quantity, 0);

        // Remove item
        cartItemsList.querySelectorAll('.cart-remove-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const idx = parseInt(this.dataset.idx);
                removeFromCart(idx);
                renderCartDropdown();
            });
        });
        // Quantity change
        cartItemsList.querySelectorAll('.cart-qty-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const idx = parseInt(this.dataset.idx);
                const action = this.dataset.action;
                updateCartQuantity(idx, action);
                renderCartDropdown();
            });
        });
    }

    // Add to cart from menu or specials
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const itemCard = this.closest('.menu-item-card, .special-item-card');
            const itemId = this.dataset.id;
            const itemName = itemCard.querySelector('h3').textContent;
            const itemPrice = parseFloat(itemCard.querySelector('.item-price').textContent.replace('Rs ', ''));
            const quantity = parseInt(itemCard.querySelector('.quantity')?.textContent || '1');
            addToCart({ id: itemId, name: itemName, price: itemPrice, quantity });
            renderCartDropdown && renderCartDropdown();
            showCartNotification(itemName, quantity);
            shakeCartIcon();
            launchConfetti();
        });
    });

    // Cart logic
    function getCart() {
        return JSON.parse(localStorage.getItem('cart') || '[]');
    }
    function setCart(cart) {
        localStorage.setItem('cart', JSON.stringify(cart));
    }
    function addToCart(item) {
        let cart = getCart();
        const idx = cart.findIndex(i => i.id === item.id);
        if (idx > -1) {
            cart[idx].quantity += item.quantity;
        } else {
            cart.push(item);
        }
        setCart(cart);
    }
    function removeFromCart(idx) {
        let cart = getCart();
        cart.splice(idx, 1);
        setCart(cart);
    }
    function updateCartQuantity(idx, action) {
        let cart = getCart();
        if (action === 'plus') {
            cart[idx].quantity += 1;
        } else if (action === 'minus' && cart[idx].quantity > 1) {
            cart[idx].quantity -= 1;
        }
        setCart(cart);
    }

    // Update cart badge on page load
    function updateCartBadge() {
        const cart = getCart();
        cartCount.textContent = cart.reduce((sum, item) => sum + item.quantity, 0);
    }
    updateCartBadge();

    // Hide dropdown on scroll or navigation
    window.addEventListener('scroll', () => { cartDropdown.style.display = 'none'; });
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => { cartDropdown.style.display = 'none'; });
    });

    // Notification popup
    function showCartNotification(itemName, quantity) {
        const notif = document.getElementById('cart-notification');
        const msg = document.getElementById('cart-notification-msg');
        if (!notif || !msg) return;
        msg.textContent = `Added ${quantity} × ${itemName} to cart!`;
        notif.style.display = 'block';
        notif.style.opacity = '1';
        setTimeout(() => {
            notif.style.opacity = '0';
            setTimeout(() => { notif.style.display = 'none'; }, 400);
        }, 1500);
    }
    // Cart icon shake
    function shakeCartIcon() {
        const cartBtn = document.getElementById('cart-btn');
        if (!cartBtn) return;
        cartBtn.classList.add('cart-shake');
        setTimeout(() => { cartBtn.classList.remove('cart-shake'); }, 500);
    }
    // Confetti effect
    function launchConfetti() {
        const canvas = document.getElementById('confetti-canvas');
        if (!canvas) return;
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        canvas.style.display = 'block';
        const ctx = canvas.getContext('2d');
        const confetti = [];
        for (let i = 0; i < 40; i++) {
            confetti.push({
                x: Math.random() * canvas.width,
                y: Math.random() * -canvas.height,
                r: 6 + Math.random() * 8,
                d: 2 + Math.random() * 4,
                color: `hsl(${Math.random()*360},90%,60%)`,
                tilt: Math.random() * 10 - 5
            });
        }
        let frame = 0;
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            confetti.forEach(c => {
                ctx.beginPath();
                ctx.arc(c.x, c.y, c.r, 0, 2 * Math.PI);
                ctx.fillStyle = c.color;
                ctx.fill();
            });
        }
        function update() {
            confetti.forEach(c => {
                c.y += c.d;
                c.x += Math.sin(frame/10 + c.tilt) * 2;
                if (c.y > canvas.height) c.y = -10;
            });
            frame++;
        }
        let count = 0;
        function animate() {
            draw();
            update();
            count++;
            if (count < 40) {
                requestAnimationFrame(animate);
            } else {
                canvas.style.display = 'none';
            }
        }
        animate();
    }
    // Add shake animation CSS
    const style = document.createElement('style');
    style.innerHTML = `.cart-shake { animation: cartshake 0.5s; } @keyframes cartshake { 0% { transform: translateX(0); } 20% { transform: translateX(-6px); } 40% { transform: translateX(6px); } 60% { transform: translateX(-4px); } 80% { transform: translateX(4px); } 100% { transform: translateX(0); } }`;
    document.head.appendChild(style);
}