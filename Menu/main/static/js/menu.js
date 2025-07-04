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
    initFavorites();
    updateCartBadge();
    updateFavoritesBadge();
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
    // Forms will submit normally to the server, no AJAX needed
    // Quantity controls are handled by the updateQuantity function
}

function addToCartAjax(itemType, itemId, quantity) {
    const csrfToken = getCookie('csrftoken');
    
    fetch('/api/add-to-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({
            type: itemType,
            id: itemId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            updateCartBadge(data.cart_count);
            shakeCartIcon();
        } else {
            showNotification('Error adding to cart: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error adding to cart', 'error');
    });
}

function updateCartBadge(count) {
    const badge = document.getElementById('cart-count');
    if (badge) {
        badge.textContent = count || 0;
    }
}
function showCartNotification(message, quantity) {
    const notif = document.getElementById('cart-notification');
    const msg = document.getElementById('cart-notification-msg');
    if (notif && msg) {
        msg.textContent = message;
        notif.style.display = 'block';
        setTimeout(() => { notif.style.display = 'none'; }, 1500);
    }
}

/* ---------------------------------------- Quantity Controls ---------------------------------------- */
function updateQuantity(button, change) {
    const container = button.closest(".quantity-controls");
    if (!container) return;
    
    const quantityInput = container.querySelector(".quantity");
    if (!quantityInput) return;
    
    let currentQuantity = parseInt(quantityInput.value) || 1;
    let newQuantity = currentQuantity + change;
    
    // Ensure quantity stays within bounds
    if (newQuantity < 1) newQuantity = 1;
    if (newQuantity > 50) newQuantity = 50;
    
    quantityInput.value = newQuantity;
}

/* ---------------------------------------- Today's Special Section ---------------------------------------- */
function initTodaysSpecial() {
    // Quantity controls
    document.querySelectorAll(".quantity-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            const container = this.closest(".quantity-controls");
            if (!container) return; // Exit if no container found
            
            const quantityElement = container.querySelector(".quantity");
            if (!quantityElement) return; // Exit if no quantity element found
            
            let quantity = parseInt(quantityElement.textContent);

            if (this.classList.contains("minus") && quantity > 1) {
                quantity--;
            } else if (this.classList.contains("plus")) {
                quantity++;
            }

            quantityElement.textContent = quantity;
        });
    });

    // Special items add to cart - now handled by server-side forms
    // This section has been updated to use Django forms instead of JavaScript
    document.querySelectorAll(".special-item-card .add-to-cart-btn").forEach(btn => {
        btn.addEventListener("click", function() {
            // Cart addition is now handled by Django forms in the template
            // This event listener is kept for any additional UI feedback
            const card = this.closest(".special-item-card");
            const itemName = card.querySelector("h3").textContent;
            console.log(`Adding to cart: ${itemName} (handled by Django form)`);
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

if (backToTopBtn) {
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
}

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
const reservationBtn = document.getElementById('reservation-btn');
if (reservationBtn) {
    reservationBtn.addEventListener('click', () => {
        // Implement reservation functionality
        window.location.href = '/reservation/';
    });
}

const cateringBtn = document.getElementById('catering-btn');
if (cateringBtn) {
    cateringBtn.addEventListener('click', () => {
        // Implement catering services functionality
        window.location.href = '/catering/';
    });
}

const giftCardBtn = document.getElementById('gift-card-btn');
if (giftCardBtn) {
    giftCardBtn.addEventListener('click', () => {
        // Implement gift card functionality
        window.location.href = '/gift-cards/';
    });
}

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

if (searchInput && searchFeedback) {
    searchInput.addEventListener('input', () => {
        if (searchInput.value.length > 0) {
            searchFeedback.style.display = 'block';
        } else {
            searchFeedback.style.display = 'none';
        }
    });
}

// === CART SYSTEM ===

function initCartSystem() {
    // Initialize cart badge update
    updateCartBadge();
    
    // Add shake animation CSS for cart icon
    const style = document.createElement('style');
    style.innerHTML = `.cart-shake { animation: cartshake 0.5s; } @keyframes cartshake { 0% { transform: translateX(0); } 20% { transform: translateX(-6px); } 40% { transform: translateX(6px); } 60% { transform: translateX(-4px); } 80% { transform: translateX(4px); } 100% { transform: translateX(0); } }`;
    document.head.appendChild(style);
}

// Cart icon shake animation
function shakeCartIcon() {
    const cartBtn = document.getElementById('cart-btn');
    if (!cartBtn) return;
    cartBtn.classList.add('cart-shake');
    setTimeout(() => { cartBtn.classList.remove('cart-shake'); }, 500);
}

// Confetti effect for cart additions
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

function setupCartItemHandlers() {
    // Cart logic has been moved to server-side Django views
    // This function is kept for compatibility but cart operations
    // are now handled via Django forms and AJAX endpoints
    
    // Update cart badge on page load
    updateCartBadge();
}

function initFavorites() {
    const favoriteBtns = document.querySelectorAll('.favorite-btn');
    const csrftoken = getCookie('csrftoken');

    // Fetch user's favorites and update icons
    fetch('/api/favorites/', {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => {
        if (!response.ok) throw new Error('Not authenticated or error fetching favorites');
        return response.json();
    })
    .then(data => {
        const favoriteIds = data.map(fav => fav.food);
        updateFavoritesBadge(data.length); // Update badge count
        favoriteBtns.forEach(btn => {
            const icon = btn.querySelector('i');
            if (favoriteIds.includes(parseInt(btn.dataset.id))) {
                icon.classList.remove('fa-regular');
                icon.classList.add('fa-solid');
                btn.classList.add('favorited');
            } else {
                icon.classList.remove('fa-solid');
                icon.classList.add('fa-regular');
                btn.classList.remove('favorited');
            }
        });
    })
    .catch(() => {
        // Not logged in or error, just leave as is
        updateFavoritesBadge(0);
    });

    // Click handler
    favoriteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = btn.dataset.id;
            const icon = btn.querySelector('i');
            const isFavorited = btn.classList.contains('favorited');
            const url = isFavorited ? '/api/favorites/remove/' : '/api/favorites/add/';
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ food_id: itemId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    icon.classList.toggle('fa-solid');
                    icon.classList.toggle('fa-regular');
                    btn.classList.toggle('favorited');
                    // Update favorites badge count
                    updateFavoritesBadge();
                } else {
                    alert(data.error || 'Could not update favorite.');
                }
            })
            .catch(() => {
                alert('Error updating favorite.');
            });
        });
    });
}

function updateFavoritesBadge(count = null) {
    const favCount = document.getElementById('favorites-count');
    if (!favCount) return;
    
    if (count !== null) {
        favCount.textContent = count;
        return;
    }
    
    // Fetch current count
    fetch('/api/favorites/', {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => {
        if (!response.ok) throw new Error('Not authenticated');
        return response.json();
    })
    .then(data => {
        favCount.textContent = data.length;
    })
    .catch(() => {
        favCount.textContent = '0';
    });
}

// Notification system
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        z-index: 10000;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        ${type === 'success' ? 'background: #28a745;' : 'background: #dc3545;'}
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}