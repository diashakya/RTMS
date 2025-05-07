/* 
Table of Contents:
1. Category Filtering
2. Search Functionality
3. Add to Cart Functionality
4. Today's Special Section
5. Helper Functions
*/

/* ----------------------------------------Category Filtering starts ---------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  const categoryBtns = document.querySelectorAll(".category-btn");
  const menuItems = document.querySelectorAll(".menu-item-card");

  categoryBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      categoryBtns.forEach((b) => b.classList.remove("active"));
      this.classList.add("active");

      const category = this.dataset.category;
      menuItems.forEach((item) => {
        item.style.display = (category === "all" || item.dataset.category === category) ? "block" : "none";
      });
    });
  });
/* ----------------------------------------Category Filtering ends ---------------------------------------- */

/* ----------------------------------------Search Functionality starts ---------------------------------------- */
  const searchInput = document.getElementById("menu-search");

  searchInput.addEventListener("input", function () {
    const searchTerm = this.value.toLowerCase();
    menuItems.forEach((item) => {
      const itemName = item.querySelector("h3").textContent.toLowerCase();
      const itemDesc = item.querySelector(".item-description").textContent.toLowerCase();
      item.style.display = (itemName.includes(searchTerm) || itemDesc.includes(searchTerm)) ? "block" : "none";
    });
  });
/* ----------------------------------------Search Functionality ends ---------------------------------------- */

/* ----------------------------------------Add to Cart Functionality starts ---------------------------------------- */
  const addToCartBtns = document.querySelectorAll(".add-to-cart-btn");

  addToCartBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      const itemCard = this.closest(".menu-item-card");
      const itemName = itemCard.querySelector("h3").textContent;
      const itemPrice = itemCard.querySelector(".item-price").textContent;
      
      // TODO: Implement actual cart functionality
      console.log(`Added to cart: ${itemName} - ${itemPrice}`);
    });
  });
});
/* ----------------------------------------Add to Cart Functionality ends ---------------------------------------- */

/* ----------------------------------------Today's Special Section starts ---------------------------------------- */
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".quantity-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
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

  document.querySelectorAll(".special-item-card .add-to-cart-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const card = this.closest(".special-item-card");
      const itemId = this.dataset.id;
      const itemName = card.querySelector("h3").textContent;
      const quantity = parseInt(card.querySelector(".quantity").textContent);
      const price = parseFloat(card.querySelector(".item-price").textContent.replace("Rs ", ""));

      // TODO: Implement actual cart functionality
      console.log(`Added to cart: ${quantity}x ${itemName} - Rs ${(price * quantity).toFixed(2)}`);
    });
  });
});
/* ----------------------------------------Today's Special Section ends ---------------------------------------- */

/* ----------------------------------------Helper Functions starts ---------------------------------------- */
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
/* ----------------------------------------Helper Functions ends ---------------------------------------- */
