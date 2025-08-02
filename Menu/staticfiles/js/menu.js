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
    initQuickView();
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
    // Add click handlers for AJAX add to cart buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-to-cart-btn') || e.target.closest('.add-to-cart-btn')) {
            const button = e.target.classList.contains('add-to-cart-btn') ? e.target : e.target.closest('.add-to-cart-btn');
            const form = button.closest('form');
            
            // Check if this should be AJAX (you can add a data attribute to enable AJAX)
            if (button.dataset.ajax === 'true' || form.dataset.ajax === 'true') {
                e.preventDefault();
                
                const formData = new FormData(form);
                const itemType = formData.get('item_type');
                const itemId = formData.get('item_id');
                const quantity = formData.get('quantity') || 1;
                
                addToCartAjax(itemType, itemId, quantity, button);
            }
        }
    });
}

function addToCartAjax(itemType, itemId, quantity, button = null) {
    const csrfToken = getCookie('csrftoken');
    
    makeAjaxCall('/api/add-to-cart/', {
        method: 'POST',
        data: {
            type: itemType,
            id: itemId,
            quantity: quantity
        },
        button: button,
        loadingMessage: 'Adding item to cart...',
        onSuccess: (data) => {
            if (data.success) {
                showNotification(data.message, 'success');
                updateCartBadge(data.cart_count);
                shakeCartIcon();
            } else {
                showNotification('Error adding to cart: ' + data.message, 'error');
            }
        },
        onError: (error) => {
            console.error('Error:', error);
            showNotification('Error adding to cart', 'error');
        }
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

/* ---------------------------------------- Quick View Functionality ---------------------------------------- */
function initQuickView() {
    document.querySelectorAll('.quick-view-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const itemId = btn.dataset.id;
            showQuickViewModal(itemId);
        });
    });
}

/* ---------------------------------------- Favorite Button Functionality ---------------------------------------- */
function initFavorites() {
    document.querySelectorAll('.favorite-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const itemId = btn.dataset.id;
            const icon = btn.querySelector('i');
            
            if (icon.classList.contains('far')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                // Add to favorites with loading
                addToFavorites(itemId, btn);
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                // Remove from favorites with loading
                removeFromFavorites(itemId, btn);
            }
        });
    });
}

/* ---------------------------------------- Share Button Functionality ---------------------------------------- */
function initShareButtons() {
    document.querySelectorAll('.share-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const itemId = btn.dataset.id;
            shareItem(itemId);
        });
    });
}

/* ---------------------------------------- Quick Actions Buttons ---------------------------------------- */
function initQuickActions() {
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
}

/* ---------------------------------------- Helper Functions ---------------------------------------- */
function showQuickViewModal(itemId) {
    // Fetch item details from server
    fetch(`/api/foods/${itemId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showNotification('Error loading item details', 'error');
                return;
            }
            populateQuickViewModal(data);
            // Show the modal
            const modal = new bootstrap.Modal(document.getElementById('quickViewModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Error fetching item details:', error);
            showNotification('Error loading item details', 'error');
        });
}

function populateQuickViewModal(itemData) {
    // Populate modal with item data
    document.getElementById('quick-view-title').textContent = itemData.title;
    document.getElementById('quick-view-description').textContent = itemData.description || 'No description available';
    document.getElementById('quick-view-price').textContent = `Rs ${itemData.price}`;
    document.getElementById('quick-view-item-id').value = itemData.id;
    
    // Set image
    const imageElement = document.getElementById('quick-view-image');
    if (itemData.image) {
        imageElement.src = itemData.image;
        imageElement.alt = itemData.title;
    } else {
        // Use a CSS-based placeholder
        imageElement.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjQwMCIgdmlld0JveD0iMCAwIDQwMCA0MDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iNDAwIiBmaWxsPSIjRjhGOUZBIi8+CjxwYXRoIGQ9Ik0xNjAgMTgwSDI0MFYyMjBIMTYwVjE4MFoiIGZpbGw9IiNERUUyRTYiLz4KPHBhdGggZD0iTTE4MCAyMDBIMjIwVjI0MEgxODBWMjAwWiIgZmlsbD0iI0RFRTJFNiIvPgo8dGV4dCB4PSIyMDAiIHk9IjI4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iIzZCNzI4MCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE2Ij5ObyBJbWFnZTwvdGV4dD4KPC9zdmc+';
        imageElement.alt = 'No image available';
    }
    
    // Set category
    const categoryElement = document.getElementById('quick-view-category');
    categoryElement.textContent = itemData.category || 'Uncategorized';
    
    // Set rating
    const ratingElement = document.getElementById('quick-view-rating');
    ratingElement.textContent = itemData.rating || '4.5';
    
    // Set calories if available
    const caloriesElement = document.getElementById('quick-view-calories');
    if (itemData.calories) {
        caloriesElement.textContent = `${itemData.calories} cal`;
        caloriesElement.style.display = 'inline';
    } else {
        caloriesElement.style.display = 'none';
    }
    
    // Set dietary badges
    const dietaryInfoElement = document.getElementById('quick-view-dietary-info');
    let dietaryBadges = '';
    if (itemData.is_vegetarian) {
        dietaryBadges += '<span class="badge bg-success me-2"><i class="fas fa-leaf"></i> Vegetarian</span>';
    }
    if (itemData.is_spicy) {
        dietaryBadges += '<span class="badge bg-warning me-2"><i class="fas fa-pepper-hot"></i> Spicy</span>';
    }
    dietaryInfoElement.innerHTML = dietaryBadges;
    
    // Reset quantity to 1
    document.getElementById('modal-quantity').value = 1;
    
    // Reset favorite status (you could enhance this to check actual favorite status)
    updateModalFavoriteButton(false);
}

function updateModalQuantity(change) {
    const quantityInput = document.getElementById('modal-quantity');
    let currentQuantity = parseInt(quantityInput.value) || 1;
    let newQuantity = currentQuantity + change;
    
    // Ensure quantity stays within bounds
    if (newQuantity < 1) newQuantity = 1;
    if (newQuantity > 50) newQuantity = 50;
    
    quantityInput.value = newQuantity;
}

function toggleModalFavorite() {
    const icon = document.getElementById('modal-favorite-icon');
    const text = document.getElementById('modal-favorite-text');
    const itemId = document.getElementById('quick-view-item-id').value;
    
    if (icon.classList.contains('far') || text.textContent === 'Add to Favorites') {
        // Add to favorites
        addToFavorites(itemId);
        updateModalFavoriteButton(true);
    } else {
        // Remove from favorites
        removeFromFavorites(itemId);
        updateModalFavoriteButton(false);
    }
}

function updateModalFavoriteButton(isFavorite) {
    const icon = document.getElementById('modal-favorite-icon');
    const text = document.getElementById('modal-favorite-text');
    
    if (isFavorite) {
        icon.className = 'fas fa-heart';
        text.textContent = 'Remove from Favorites';
    } else {
        icon.className = 'far fa-heart';
        text.textContent = 'Add to Favorites';
    }
}

function shareModalItem() {
    const title = document.getElementById('quick-view-title').textContent;
    const itemId = document.getElementById('quick-view-item-id').value;
    
    if (navigator.share) {
        navigator.share({
            title: `Check out ${title}!`,
            text: `I found this delicious ${title} on our restaurant website!`,
            url: `${window.location.origin}/menu/?item=${itemId}`
        }).catch(err => console.log('Error sharing:', err));
    } else {
        // Fallback: copy to clipboard
        const url = `${window.location.origin}/menu/?item=${itemId}`;
        navigator.clipboard.writeText(url).then(() => {
            showNotification('Link copied to clipboard!', 'success');
        }).catch(() => {
            showNotification('Unable to share. Try again later.', 'error');
        });
    }
}

function addToFavorites(itemId, button = null) {
    if (!checkAuthentication()) return;
    
    makeAjaxCall('/api/toggle-favorite/', {
        method: 'POST',
        data: {
            food_id: itemId
        },
        button: button,
        loadingMessage: 'Adding to favorites...',
        onSuccess: (data) => {
            if (data.success) {
                if (data.action === 'added') {
                    showNotification(data.message, 'success');
                    updateFavoritesBadge(data.favorites_count);
                }
            } else {
                showNotification('Error: ' + data.message, 'error');
            }
        },
        onError: (error) => {
            console.error('Error:', error);
            showNotification('Error adding to favorites', 'error');
        }
    });
}

function removeFromFavorites(itemId, button = null) {
    if (!checkAuthentication()) return;
    
    makeAjaxCall('/api/toggle-favorite/', {
        method: 'POST',
        data: {
            food_id: itemId
        },
        button: button,
        loadingMessage: 'Removing from favorites...',
        onSuccess: (data) => {
            if (data.success) {
                if (data.action === 'removed') {
                    showNotification(data.message, 'success');
                    updateFavoritesBadge(data.favorites_count);
                }
            } else {
                showNotification('Error: ' + data.message, 'error');
            }
        },
        onError: (error) => {
            console.error('Error:', error);
            showNotification('Error removing from favorites', 'error');
        }
    });
}

function checkAuthentication() {
    // Simple check - you could enhance this
    const userGreeting = document.querySelector('.user-greeting');
    if (!userGreeting) {
        showNotification('Please login to add favorites', 'warning');
        return false;
    }
    return true;
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

function updateFavoritesBadge(count) {
    const badge = document.getElementById('favorites-count');
    if (badge) {
        badge.textContent = count || 0;
    }
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

/* ----------------------------------------Loading Utilities ---------------------------------------- */

/**
 * Loading management system for AJAX calls
 */
class LoadingManager {
    constructor() {
        this.activeLoaders = new Set();
        this.createGlobalOverlay();
    }

    // Create global loading overlay
    createGlobalOverlay() {
        if (!document.getElementById('global-loading-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'global-loading-overlay';
            overlay.className = 'loading-overlay';
            overlay.innerHTML = `
                <div style="text-align: center; color: white;">
                    <div class="spinner"></div>
                    <div class="loading-text">Processing your request</div>
                </div>
            `;
            document.body.appendChild(overlay);
        }
    }

    // Show global loading
    showGlobalLoading(message = 'Processing your request') {
        const overlay = document.getElementById('global-loading-overlay');
        const text = overlay.querySelector('.loading-text');
        if (text) text.textContent = message;
        overlay.classList.add('show');
    }

    // Hide global loading
    hideGlobalLoading() {
        const overlay = document.getElementById('global-loading-overlay');
        overlay.classList.remove('show');
    }

    // Show button loading state
    showButtonLoading(button, originalText = null) {
        if (!button) return;
        
        const buttonId = button.id || button.className || 'unknown';
        this.activeLoaders.add(buttonId);
        
        // Store original text if provided
        if (originalText) {
            button.dataset.originalText = originalText;
        } else {
            button.dataset.originalText = button.textContent || button.innerHTML;
        }
        
        // Add loading class and spinner
        button.classList.add('btn-loading');
        button.disabled = true;
        
        // Change button text based on type
        if (button.classList.contains('cart-btn') || button.textContent.includes('Add to Cart')) {
            button.innerHTML = '<span class="spinner-small"></span>Adding...';
        } else if (button.classList.contains('favorite-btn')) {
            button.innerHTML = '<span class="spinner-small"></span>Updating...';
        } else {
            button.innerHTML = '<span class="spinner-small"></span>Loading...';
        }
    }

    // Hide button loading state
    hideButtonLoading(button) {
        if (!button) return;
        
        const buttonId = button.id || button.className || 'unknown';
        this.activeLoaders.delete(buttonId);
        
        // Remove loading class and restore original text
        button.classList.remove('btn-loading');
        button.disabled = false;
        
        const originalText = button.dataset.originalText;
        if (originalText) {
            button.innerHTML = originalText;
            delete button.dataset.originalText;
        }
    }

    // Show form loading state
    showFormLoading(form) {
        if (!form) return;
        form.classList.add('form-loading');
        
        // Disable all form inputs
        const inputs = form.querySelectorAll('input, button, textarea, select');
        inputs.forEach(input => {
            input.disabled = true;
        });
    }

    // Hide form loading state
    hideFormLoading(form) {
        if (!form) return;
        form.classList.remove('form-loading');
        
        // Re-enable all form inputs
        const inputs = form.querySelectorAll('input, button, textarea, select');
        inputs.forEach(input => {
            input.disabled = false;
        });
    }

    // Show section loading with skeleton
    showSectionLoading(container, type = 'default') {
        if (!container) return;
        
        let skeletonHTML = '';
        switch (type) {
            case 'menu-items':
                skeletonHTML = `
                    <div class="skeleton skeleton-image"></div>
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text" style="width: 70%;"></div>
                `;
                break;
            case 'cart':
                skeletonHTML = `
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text" style="width: 80%;"></div>
                    <div class="skeleton skeleton-text" style="width: 60%;"></div>
                `;
                break;
            default:
                skeletonHTML = `
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text" style="width: 85%;"></div>
                `;
        }
        
        container.innerHTML = `<div class="loading-skeleton">${skeletonHTML}</div>`;
    }

    // Clear all loading states
    clearAllLoading() {
        this.hideGlobalLoading();
        
        // Clear button loading states
        document.querySelectorAll('.btn-loading').forEach(btn => {
            this.hideButtonLoading(btn);
        });
        
        // Clear form loading states
        document.querySelectorAll('.form-loading').forEach(form => {
            this.hideFormLoading(form);
        });
        
        this.activeLoaders.clear();
    }

    // Flash success/error animations
    flashSuccess(element) {
        if (!element) return;
        element.classList.add('success-flash');
        setTimeout(() => element.classList.remove('success-flash'), 600);
    }

    flashError(element) {
        if (!element) return;
        element.classList.add('error-flash');
        setTimeout(() => element.classList.remove('error-flash'), 600);
    }
}

// Create global loading manager instance
const loadingManager = new LoadingManager();

// Enhanced AJAX wrapper with automatic loading states
function makeAjaxCall(url, options = {}) {
    const {
        method = 'GET',
        data = null,
        button = null,
        form = null,
        globalLoading = false,
        loadingMessage = 'Processing your request',
        onSuccess = () => {},
        onError = () => {},
        onComplete = () => {}
    } = options;

    // Show appropriate loading state
    if (globalLoading) {
        loadingManager.showGlobalLoading(loadingMessage);
    }
    if (button) {
        loadingManager.showButtonLoading(button);
    }
    if (form) {
        loadingManager.showFormLoading(form);
    }

    // Prepare fetch options
    const fetchOptions = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        }
    };

    if (data) {
        fetchOptions.body = JSON.stringify(data);
    }

    // Make the request
    return fetch(url, fetchOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Success handling
            if (button) loadingManager.flashSuccess(button);
            if (form) loadingManager.flashSuccess(form);
            onSuccess(data);
            return data;
        })
        .catch(error => {
            console.error('AJAX Error:', error);
            // Error handling
            if (button) loadingManager.flashError(button);
            if (form) loadingManager.flashError(form);
            onError(error);
            throw error;
        })
        .finally(() => {
            // Cleanup loading states
            if (globalLoading) {
                loadingManager.hideGlobalLoading();
            }
            if (button) {
                loadingManager.hideButtonLoading(button);
            }
            if (form) {
                loadingManager.hideFormLoading(form);
            }
            onComplete();
        });
}

// Enhanced notification system with loading integration
function showLoadingNotification(message, duration = 2000) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 24px;
        background: #f76d37;
        color: white;
        border-radius: 8px;
        z-index: 10001;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    `;
    
    notification.innerHTML = `
        <div class="spinner-small"></div>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, duration);
}

/* ----------------------------------------Loading Integration with Existing Functions ---------------------------------------- */

// Export for use in other files
window.loadingManager = loadingManager;
window.makeAjaxCall = makeAjaxCall;
window.showLoadingNotification = showLoadingNotification;