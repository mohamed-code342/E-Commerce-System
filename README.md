# E-Commerce System Backend with FastAPI

## Project Description

This project is a scalable backend system for an online store using FastAPI.  
It supports user authentication, role-based authorization, product and category management, shopping cart functionality, order placement, Redis caching, logging, monitoring dashboard APIs, and API testing.

---

## Technologies Used

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- JWT Authentication
- Redis
- Pytest
- HTML / CSS / JavaScript Frontend

---

## Project Features

### Authentication
- User registration
- User login
- JWT token generation
- Token validation
- Protected routes

### Role-Based Authorization
- Admin can manage products and categories
- Admin can view all orders
- Customer can browse products, manage cart, and place orders

### Products
- Create product
- Get all products
- Get product by ID
- Update product
- Delete product
- Search products
- Filter by category and price
- Pagination

### Categories
- Create category
- Get all categories

### Cart
- Add product to cart
- View cart
- Remove item from cart

### Orders
- Create order from cart
- View user orders
- Admin view all orders
- Stock validation
- Total price calculation

### Redis Caching
- Cache frequently accessed product data
- Cache-aside pattern
- Cache invalidation after create, update, and delete
- Performance test endpoint to compare database and cache response times

### Logging and Monitoring
- Structured logging using Python logging module
- Request and response logging
- Authentication logs
- Token validation logs
- CRUD operation logs
- Error logs
- Monitoring dashboard endpoint

### Frontend
- Simple frontend using HTML, CSS, and JavaScript
- Login and register pages
- Products page
- Cart page
- Orders page
- Admin dashboard page

---

## Project Structure

```text
ecommerce-fastapi/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── cache.py
│   ├── crud.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── monitoring.py
│   │
│   └── routes/
│       ├── users.py
│       ├── products.py
│       ├── categories.py
│       ├── cart.py
│       ├── orders.py
│       ├── monitoring.py
│       └── performance.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── products.html
│   ├── cart.html
│   ├── orders.html
│   ├── admin.html
│   ├── dashboard.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── main.js
│       ├── login.js
│       ├── register.js
│       ├── products.js
│       ├── cart.js
│       ├── orders.js
│       └── admin.js
│
├── tests/
│   ├── test_auth.py
│   ├── test_cart.py
│   ├── test_crud.py
│   ├── test_orders.py
│   ├── test_products.py
│   └── test_validation.py
│
├── ecommerce.db
├── app.log
├── requirements.txt
└── README.md
````

---

## Installation

### 1. Clone the project

```bash
git clone <repository-link>
cd ecommerce-fastapi
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Redis

Make sure Redis is running locally on:

```text
localhost:6379
```

### 4. Run the FastAPI server

```bash
uvicorn app.main:app --reload
```

The API will run on:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Main API Endpoints

### Users

```text
POST /users/register
POST /users/login
POST /users/token
```

### Products

```text
GET /products/
GET /products/{product_id}
POST /products/
PUT /products/{product_id}
DELETE /products/{product_id}
GET /products/search/
```

### Categories

```text
GET /categories/
POST /categories/
```

### Cart

```text
POST /cart/
GET /cart/
DELETE /cart/{cart_item_id}
```

### Orders

```text
POST /orders/
GET /orders/
GET /orders/all
```

### Monitoring

```text
GET /monitoring/dashboard
```

### Performance

```text
GET /performance/cache-test
```

---

## Running Tests

```bash
pytest
```

---

## Notes

* Admin-only routes require JWT authentication with an admin account.
* Redis must be running to enable caching.
* If Redis is not available, the application continues running without cache.

```
```
