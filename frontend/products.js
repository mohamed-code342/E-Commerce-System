const productsContainer =
    document.getElementById("products-container");

const pageNumber =
    document.getElementById("page-number");

const prevPageBtn =
    document.getElementById("prev-page");

const nextPageBtn =
    document.getElementById("next-page");

const searchInput =
    document.getElementById("search-input");

const minPriceInput =
    document.getElementById("min-price");

const maxPriceInput =
    document.getElementById("max-price");

const applyFiltersBtn =
    document.getElementById("apply-filters");

let currentPage = 1;
let selectedCategory = "";
let currentSearch = "";
let currentMinPrice = "";
let currentMaxPrice = "";
let limit = 8;

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


// Load products from API
async function loadProducts() {

    const params = new URLSearchParams();

    params.append("page", currentPage);
    params.append("limit", limit);

    if (currentSearch) {
        params.append("name", currentSearch);
    }

    if (selectedCategory) {
        params.append("category_id", selectedCategory);
    }

    if (currentMinPrice) {
        params.append("min_price", currentMinPrice);
    }

    if (currentMaxPrice) {
        params.append("max_price", currentMaxPrice);
    }

    const url =
        `http://127.0.0.1:8000/products/search/?${params.toString()}`;

    try {
        const response = await fetch(url);

        const products = await response.json();

        renderProducts(products);

        pageNumber.textContent = currentPage;

    } catch (error) {
        console.error(error);

        productsContainer.innerHTML =
            "<p>Failed to load products.</p>";
    }
}


// Render product cards
function renderProducts(products) {

    productsContainer.innerHTML = "";

    if (!products || products.length === 0) {
        productsContainer.innerHTML =
            "<p>No products found.</p>";
        return;
    }

    products.forEach((product) => {

        const card = document.createElement("div");

        card.className = "shop-card";

        const productImage =
    productImages[product.name]
    || defaultProductImage;
    
        card.innerHTML = `
            <button class="wishlist-btn">
                <i class="far fa-heart"></i>
            </button>

            <div class="shop-image-box">
                <img src="${productImage}" alt="${product.name}">
            </div>

            <div class="shop-info">

                <div class="shop-row">
                    <h3>${product.name}</h3>
                    <div class="shop-price">
                        $${Number(product.price).toFixed(2)}
                    </div>
                </div>

                <p class="shop-desc">
                    ${product.description || "No description available"}
                </p>

                <div class="shop-rating">
                    ★★★★★ <span>(121)</span>
                </div>

                <button class="shop-add-btn" onclick="addToCart(${product.id})">
                    Add to Cart
                </button>

            </div>
        `;

        productsContainer.appendChild(card);
    });
}


// Apply search and price filters
function applyFilters() {

    currentSearch = searchInput.value.trim();
    currentMinPrice = minPriceInput.value;
    currentMaxPrice = maxPriceInput.value;

    currentPage = 1;

    loadProducts();
}


// Add product to cart
async function addToCart(productId) {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Please login first");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/cart/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Product added to cart!");
        } else {
            alert(data.detail || "Failed to add product");
        }

    } catch (error) {
        console.error(error);
        alert("Server error");
    }
}


// Category filter
document.querySelectorAll("[data-category]").forEach((btn) => {

    btn.addEventListener("click", () => {

        selectedCategory = btn.dataset.category;

        currentPage = 1;

        loadProducts();
    });
});


// Search while typing
searchInput.addEventListener("input", () => {
    applyFilters();
});


// Apply price button
applyFiltersBtn.addEventListener("click", () => {
    applyFilters();
});


// Pagination
nextPageBtn.addEventListener("click", () => {
    currentPage++;
    loadProducts();
});

prevPageBtn.addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        loadProducts();
    }
});


// First load
loadProducts();