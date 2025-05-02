// menu.js

document.addEventListener("DOMContentLoaded", function () {
  // Category filtering
  const categoryBtns = document.querySelectorAll(".category-btn");
  const menuItems = document.querySelectorAll(".menu-item-card");

  categoryBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      // Remove active class from all buttons
      categoryBtns.forEach((b) => b.classList.remove("active"));
      // Add active class to clicked button
      this.classList.add("active");

      const category = this.dataset.category;

      // Filter menu items
      menuItems.forEach((item) => {
        if (category === "all" || item.dataset.category === category) {
          item.style.display = "block";
        } else {
          item.style.display = "none";
        }
      });
    });
  });

  // Search functionality
  const searchInput = document.getElementById("menu-search");

  searchInput.addEventListener("input", function () {
    const searchTerm = this.value.toLowerCase();

    menuItems.forEach((item) => {
      const itemName = item.querySelector("h3").textContent.toLowerCase();
      const itemDesc = item
        .querySelector(".item-description")
        .textContent.toLowerCase();

      if (itemName.includes(searchTerm) || itemDesc.includes(searchTerm)) {
        item.style.display = "block";
      } else {
        item.style.display = "none";
      }
    });
  });

  // Add to cart functionality
  const addToCartBtns = document.querySelectorAll(".add-to-cart-btn");

  addToCartBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const itemCard = this.closest(".menu-item-card");
      const itemName = itemCard.querySelector("h3").textContent;
      const itemPrice = itemCard.querySelector(".item-price").textContent;

      // Here you would typically send this data to your backend
      // For now, we'll just show an alert
      alert(`Added to cart: ${itemName} - ${itemPrice}`);

      // You can implement actual cart functionality here
      // For example, adding to a cart array or making an AJAX call
    });
  });
});

// todays special section
document.addEventListener("DOMContentLoaded", function () {
  // Quantity controls
  document.querySelectorAll(".quantity-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const container = this.closest(".quantity-controls");
      const quantityElement = container.querySelector(".quantity");
      let quantity = parseInt(quantityElement.textContent);

      if (this.classList.contains("minus")) {
        if (quantity > 1) {
          quantity--;
        }
      } else if (this.classList.contains("plus")) {
        quantity++;
      }

      quantityElement.textContent = quantity;
    });
  });

  // Add to cart functionality for special items
  document
    .querySelectorAll(".special-item-card .add-to-cart-btn")
    .forEach((btn) => {
      btn.addEventListener("click", function () {
        const card = this.closest(".special-item-card");
        const itemId = this.dataset.id;
        const itemName = card.querySelector("h3").textContent;
        const quantity = parseInt(card.querySelector(".quantity").textContent);
        let priceText = card.querySelector(".item-price").textContent;
        const price = parseFloat(priceText.replace("Rs ", ""));

        // Here you would typically send this data to your backend
        const itemData = {
          id: itemId,
          name: itemName,
          price: price,
          quantity: quantity,
        };

        // For now, we'll just show an alert
        alert(
          `Added to cart: ${quantity}x ${itemName} - Rs ${(
            price * quantity
          ).toFixed(2)}`
        );

        // You would typically make an AJAX call here to add to cart
        // Example:
        /*
                      fetch('/add-to-cart/', {
                          method: 'POST',
                          headers: {
                              'Content-Type': 'application/json',
                              'X-CSRFToken': getCookie('csrftoken'),
                          },
                          body: JSON.stringify(itemData)
                      })
                      .then(response => response.json())
                      .then(data => {
                          // Update cart count in navbar, etc.
                      });
                      */
      });
    });
});

// Helper function for CSRF token (needed for AJAX calls)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
