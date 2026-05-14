const ordersContainer = document.getElementById("orders-container");

async function loadOrders() {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Please login first");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/orders/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const orders = await response.json();

        if (!response.ok) {
            ordersContainer.innerHTML =
                `<p class="empty-orders">${orders.detail || "Failed to load orders"}</p>`;
            return;
        }

        renderOrders(orders);

    } catch (error) {
        console.error(error);
        ordersContainer.innerHTML =
            `<p class="empty-orders">Server error</p>`;
    }
}

function renderOrders(orders) {
    ordersContainer.innerHTML = "";

    if (!orders || orders.length === 0) {
        ordersContainer.innerHTML =
            `<p class="empty-orders">No orders yet.</p>`;
        return;
    }

    orders.forEach(order => {
        const card = document.createElement("div");
        card.className = "order-card";

        card.innerHTML = `
            <div>
                <h3>Order #${order.id}</h3>
                <p>Status: ${order.status || "Pending"}</p>
            </div>

            <div class="order-price">
                $${Number(order.total_price).toFixed(2)}
            </div>
        `;

        ordersContainer.appendChild(card);
    });
}

loadOrders();