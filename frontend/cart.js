const cartContainer = document.getElementById("cart-container");

const defaultProductImage =
    "images/default.png";

// Product images map
const productImages = {

    "Nike Air Shoes White":
        "images/nike-white.png",

    "Black Shoes":
        "images/black-shoes.png",

    "Red Shoes":
        "images/red-shoes.png",
    
    "Blue Shoes":
        "images/blue-shoes.png",

};

let cartTotal = 0;


// Load cart
async function loadCart() {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Please login first");
        window.location.href = "login.html";
        return;
    }

    const response = await fetch("http://127.0.0.1:8000/cart/", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();

    if (response.ok) {
        renderCart(data);
    } else {
        alert(data.detail || "Failed to load cart");
    }
}


// Render cart
async function renderCart(cartItems) {
    cartContainer.innerHTML = "";
    cartTotal = 0;

    if (!cartItems || cartItems.length === 0) {
        cartContainer.innerHTML = "<p>Your cart is empty.</p>";
        updateTotal();
        return;
    }

    for (const item of cartItems) {
        const product = await getProduct(item.product_id);

        const productImage =
            productImages[product.name] || defaultProductImage;

        const itemTotal =
            Number(product.price) * Number(item.quantity);

        cartTotal += itemTotal;

        const cartItem = document.createElement("div");
        cartItem.className = "cart-item";

        cartItem.innerHTML = `
            <img src="${productImage}" alt="${product.name}">

            <div class="cart-info">
                <h3>${product.name}</h3>
                <p>${product.description || "No description available"}</p>
                <p class="cart-price">$${Number(product.price).toFixed(2)}</p>
            </div>

            <div class="qty-box">
                <button onclick="changeQuantity(${item.id}, ${item.quantity - 1})">-</button>

                <span>${item.quantity}</span>

                <button onclick="changeQuantity(${item.id}, ${item.quantity + 1})">+</button>
            </div>

            <div class="item-total">
                $${itemTotal.toFixed(2)}
            </div>

            <button class="remove-btn" onclick="removeCartItem(${item.id})">
                Remove
            </button>
        `;

        cartContainer.appendChild(cartItem);
    }

    updateTotal();
}


// Get product details
async function getProduct(productId) {
    const response =
        await fetch(`http://127.0.0.1:8000/products/${productId}`);

    return await response.json();
}


// Update quantity
async function changeQuantity(cartItemId, newQuantity) {
    const token = localStorage.getItem("token");

    const response = await fetch(
        `http://127.0.0.1:8000/cart/${cartItemId}?quantity=${newQuantity}`,
        {
            method: "PUT",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    if (response.ok) {
        loadCart();
    } else {
        const data = await response.json();
        alert(data.detail || "Failed to update quantity");
    }
}


// Remove item
async function removeCartItem(cartItemId) {
    const token = localStorage.getItem("token");

    const response = await fetch(
        `http://127.0.0.1:8000/cart/${cartItemId}`,
        {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );

    if (response.ok) {
        loadCart();
    } else {
        const data = await response.json();
        alert(data.detail || "Failed to remove item");
    }
}


// Update total price
function updateTotal() {
    const totalBox = document.getElementById("cart-total");

    if (totalBox) {
        totalBox.textContent = `$${cartTotal.toFixed(2)}`;
    }
}


// Ordering
async function checkout() {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Please login first");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/orders/", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            alert("Order created successfully!");
            window.location.href = "orders.html";
        } else {
            alert(data.detail || "Checkout failed");
        }

    } catch (error) {
        console.error(error);
        alert("Server error");
    }
}

loadCart();

