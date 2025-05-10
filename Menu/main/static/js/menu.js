/* 
Table of Contents:
1. DOM Ready Handler
2. Category Filtering
3. Search Functionality
4. Add to Cart Functionality
5. Today's Special Section
6. Helper Functions
*/

// Main DOM Ready Handler
document.addEventListener("DOMContentLoaded", function() {
    initCategoryFiltering();
    initSearchFunctionality();
    initAddToCart();
    initTodaysSpecial();
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