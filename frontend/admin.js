const token = localStorage.getItem("token");
const role = localStorage.getItem("role");
const adminCategoriesContainer = document.getElementById("admin-categories-container");

if (!token || role !== "admin") {
    alert("Access denied");
    window.location.href = "login.html";
}

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

const usersContainer = document.getElementById("users-container");
const adminOrdersContainer = document.getElementById("admin-orders-container");
const adminProductsContainer = document.getElementById("admin-products-container");

// =========================
// USERS
// =========================

async function loadUsers() {
    try {
        const response = await fetch("http://127.0.0.1:8000/users/", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const users = await response.json();

        if (!response.ok) {
            usersContainer.innerHTML =
                `<p class="empty-orders">${users.detail || "Failed to load users"}</p>`;
            return;
        }

        renderUsers(users);

    } catch (error) {
        console.error(error);
        usersContainer.innerHTML =
            `<p class="empty-orders">Server error</p>`;
    }
}

function renderUsers(users) {
    usersContainer.innerHTML = "";

    if (!users || users.length === 0) {
        usersContainer.innerHTML =
            `<p class="empty-orders">No users found.</p>`;
        return;
    }

    users.forEach(user => {
        const item = document.createElement("div");
        item.className = "admin-item";

        item.innerHTML = `
            <div>
                <h3>${user.username}</h3>
                <p>Email: ${user.email}</p>
                <p>ID: ${user.id}</p>
                <span>Role: ${user.role}</span>
            </div>

            <button class="delete-btn" onclick="deleteUser(${user.id})">
                Delete
            </button>
        `;

        usersContainer.appendChild(item);
    });
}

async function deleteUser(userId) {
    if (!confirm("Delete this user?")) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/users/${userId}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            alert("User deleted successfully");
            loadUsers();
        } else {
            alert(data.detail || "Failed to delete user");
        }

    } catch (error) {
        console.error(error);
        alert("Server error");
    }
}

// =========================
// ORDERS
// =========================

async function loadAdminOrders() {
    try {
        const response = await fetch("http://127.0.0.1:8000/orders/all", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const orders = await response.json();

        if (!response.ok) {
            adminOrdersContainer.innerHTML =
                `<p class="empty-orders">${orders.detail || "Failed to load orders"}</p>`;
            return;
        }

        renderAdminOrders(orders);

    } catch (error) {
        console.error(error);
        adminOrdersContainer.innerHTML =
            `<p class="empty-orders">Server error</p>`;
    }
}

function renderAdminOrders(orders) {
    adminOrdersContainer.innerHTML = "";

    if (!orders || orders.length === 0) {
        adminOrdersContainer.innerHTML =
            `<p class="empty-orders">No orders found.</p>`;
        return;
    }

    orders.forEach(order => {
        const item = document.createElement("div");
        item.className = "admin-item";

        item.innerHTML = `
            <div>
                <h3>Order #${order.id}</h3>
                <p>User ID: ${order.user_id}</p>
                <p>Total: $${Number(order.total_price).toFixed(2)}</p>
                <span>Status: ${order.status || "pending"}</span>
            </div>

            <div class="admin-actions">
                <select class="status-select" id="status-${order.id}">
                    <option value="pending" ${order.status === "pending" ? "selected" : ""}>
                        Pending
                    </option>

                    <option value="processing" ${order.status === "processing" ? "selected" : ""}>
                        Processing
                    </option>

                    <option value="shipped" ${order.status === "shipped" ? "selected" : ""}>
                        Shipped
                    </option>

                    <option value="delivered" ${order.status === "delivered" ? "selected" : ""}>
                        Delivered
                    </option>

                    <option value="cancelled" ${order.status === "cancelled" ? "selected" : ""}>
                        Cancelled
                    </option>
                </select>

                <button onclick="updateOrderStatus(${order.id})">
                    Update
                </button>

                <button class="delete-btn" onclick="deleteOrder(${order.id})">
                    Delete
                </button>
            </div>
        `;

        adminOrdersContainer.appendChild(item);
    });
}

async function updateOrderStatus(orderId) {
    const status = document.getElementById(`status-${orderId}`).value;

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/orders/${orderId}/status?status=${status}`,
            {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (response.ok) {
            alert("Order status updated successfully");
            loadAdminOrders();
        } else {
            alert(data.detail || "Failed to update order status");
        }

    } catch (error) {
        console.error(error);
        alert("Server error");
    }
}

async function deleteOrder(orderId) {
    if (!confirm("Delete this order?")) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/orders/${orderId}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            alert("Order deleted successfully");
            loadAdminOrders();
        } else {
            alert(data.detail || "Failed to delete order");
        }

    } catch (error) {
        console.error(error);
        alert("Server error");
    }
}

// =========================
// CATEGORIES
// =========================

async function loadAdminCategories() {
    try {
        const response = await fetch("http://127.0.0.1:8000/categories/", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const categories = await response.json();

        if (!response.ok) {
            adminCategoriesContainer.innerHTML =
                `<p class="empty-orders">${categories.detail || "Failed to load categories"}</p>`;
            return;
        }

        renderAdminCategories(categories);

    } catch (error) {
        console.error(error);
        adminCategoriesContainer.innerHTML =
            `<p class="empty-orders">Server error</p>`;
    }
}

function renderAdminCategories(categories) {
    adminCategoriesContainer.innerHTML = "";

    if (!categories || categories.length === 0) {
        adminCategoriesContainer.innerHTML =
            `<p class="empty-orders">No categories found.</p>`;
        return;
    }

    categories.forEach(category => {
        const item = document.createElement("div");
        item.className = "admin-item";

        item.innerHTML = `
            <div>
                <h3>${category.name}</h3>
                <p>ID: ${category.id}</p>
            </div>

            <button class="delete-btn" onclick="deleteCategory(${category.id})">
                Delete
            </button>
        `;

        adminCategoriesContainer.appendChild(item);
    });
}

async function createCategory(event) {
    event.preventDefault();

    const categoryData = {
        name: document.getElementById("category-name").value
    };

    const response = await fetch("http://127.0.0.1:8000/categories/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(categoryData)
    });

    const data = await response.json();

    if (response.ok) {
        alert("Category created successfully");
        event.target.reset();
        loadAdminCategories();
    } else {
        alert(data.detail || "Failed to create category");
    }
}

async function deleteCategory(categoryId) {
    if (!confirm("Delete this category?")) return;

    const response = await fetch(`http://127.0.0.1:8000/categories/${categoryId}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();

    if (response.ok) {
        alert("Category deleted successfully");
        loadAdminCategories();
    } else {
        alert(data.detail || "Failed to delete category");
    }
}

// =========================
// PRODUCTS
// =========================

async function loadAdminProducts() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/products/search/?page=1&limit=100",
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const products = await response.json();

        if (!response.ok) {
            adminProductsContainer.innerHTML =
                `<p class="empty-orders">${products.detail || "Failed to load products"}</p>`;
            return;
        }

        renderAdminProducts(products);

    } catch (error) {
        console.error(error);
        adminProductsContainer.innerHTML =
            `<p class="empty-orders">Server error</p>`;
    }
}

function renderAdminProducts(products) {
    adminProductsContainer.innerHTML = "";

    if (!products || products.length === 0) {
        adminProductsContainer.innerHTML =
            `<p class="empty-orders">No products found.</p>`;
        return;
    }

    products.forEach(product => {
        const item = document.createElement("div");
        item.className = "admin-item";

        item.innerHTML = `
            <div>
                <h3>${product.name}</h3>
                <p>ID: ${product.id}</p>
                <p>Price: $${Number(product.price).toFixed(2)}</p>
                <p>Stock: ${product.stock}</p>
                <p>${product.description || "No description"}</p>
            </div>

            <div class="admin-actions">
                <button onclick="fillUpdateForm(
                    ${product.id},
                    '${product.name}',
                    '${product.description || ""}',
                    ${product.price},
                    ${product.stock},
                    ${product.category_id}
                )">
                    Edit
                </button>

                <button class="delete-btn" onclick="deleteProduct(${product.id})">
                    Delete
                </button>
            </div>
        `;

        adminProductsContainer.appendChild(item);
    });
}

async function createProduct(event) {
    event.preventDefault();

    const form = document.querySelector(".admin-form");
    const editId = form.dataset.editId;

    if (editId) {
        await updateProduct(editId);
        return;
    }

    const productData = {
        name: document.getElementById("product-name").value,
        description: document.getElementById("product-description").value,
        price: Number(document.getElementById("product-price").value),
        stock: Number(document.getElementById("product-stock").value),
        category_id: Number(document.getElementById("product-category").value)
    };

    const response = await fetch("http://127.0.0.1:8000/products/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(productData)
    });

    const data = await response.json();

    if (response.ok) {
        alert("Product created successfully");
        form.reset();
        loadAdminProducts();
    } else {
        alert(data.detail || "Failed to create product");
    }
}

function fillUpdateForm(id, name, description, price, stock, categoryId) {
    document.getElementById("product-name").value = name;
    document.getElementById("product-description").value = description;
    document.getElementById("product-price").value = price;
    document.getElementById("product-stock").value = stock;
    document.getElementById("product-category").value = categoryId;

    const form = document.querySelector(".admin-form");
    form.dataset.editId = id;

    window.scrollTo({
        top: document.getElementById("products-section").offsetTop - 100,
        behavior: "smooth"
    });
}

async function updateProduct(productId) {
    const productData = {
        name: document.getElementById("product-name").value,
        description: document.getElementById("product-description").value,
        price: Number(document.getElementById("product-price").value),
        stock: Number(document.getElementById("product-stock").value),
        category_id: Number(document.getElementById("product-category").value)
    };

    const response = await fetch(`http://127.0.0.1:8000/products/${productId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(productData)
    });

    const data = await response.json();

    if (response.ok) {
        alert("Product updated successfully");

        const form = document.querySelector(".admin-form");
        form.reset();
        delete form.dataset.editId;

        loadAdminProducts();
    } else {
        alert(data.detail || "Failed to update product");
    }
}

async function deleteProduct(productId) {
    if (!confirm("Delete this product?")) return;

    const response = await fetch(`http://127.0.0.1:8000/products/${productId}`, {
        method: "DELETE",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const data = await response.json();

    if (response.ok) {
        alert("Product deleted successfully");
        loadAdminProducts();
    } else {
        alert(data.detail || "Failed to delete product");
    }
}


// =========================
// MONITORING
// =========================

async function loadMonitoring() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/monitoring/dashboard",
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        document.getElementById("total-requests").innerText =
            data.total_requests;

        document.getElementById("avg-response-time").innerText =
            `${data.average_response_time}s`;

        document.getElementById("error-count").innerText =
            data.error_count;

        document.getElementById("error-rate").innerText =
            `${data.error_rate}%`;

        document.getElementById("system-health").innerText =
            data.system_health;

        const errorsList = document.getElementById("recent-errors-list");
        errorsList.innerHTML = "";

        if (!data.recent_errors || data.recent_errors.length === 0) {
            errorsList.innerHTML = "<li>No recent errors</li>";
            return;
        }

        data.recent_errors.forEach(error => {
            const li = document.createElement("li");
            li.innerText = error;
            errorsList.appendChild(li);
        });

    } catch (error) {
        console.error(error);
        alert("Failed to load monitoring data");
    }
}

// =========================
// INITIAL LOAD
// =========================

loadUsers();
loadAdminOrders();
loadAdminProducts();
loadMonitoring();
loadAdminCategories();