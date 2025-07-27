# Database Schema for E-commerce Application

## Overview

### 1. Users Table

```sql
CREATE TABLE users (
    id VARCHAR(26) PRIMARY KEY,  -- ULID format
    uid VARCHAR(255) NULL,
    provider VARCHAR(255) NULL,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    street VARCHAR(70) NULL,
    city VARCHAR(40) NULL,
    state VARCHAR(40) NULL,
    country VARCHAR(40) NULL,
    postal_code VARCHAR(10) NULL,
    phone VARCHAR(24) NULL,
    dob DATE NULL,
    email VARCHAR(256) NOT NULL UNIQUE,
    password VARCHAR(255) NULL,
    role VARCHAR(255) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

```

### 2. Categories Table

```sql
CREATE TABLE categories (
    id VARCHAR(26) PRIMARY KEY,  -- ULID format
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,
    parent_id VARCHAR(26) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
);

```

### 3. Brands Table

```sql
CREATE TABLE brands (
    id VARCHAR(26) PRIMARY KEY,  -- ULID format
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

```

### 4. Product Images Table

```sql
CREATE TABLE product_images (
    id VARCHAR(26) PRIMARY KEY,  -- ULID format
    by_name VARCHAR(120) NOT NULL,
    by_url VARCHAR(255) NOT NULL,
    source_name VARCHAR(120) NOT NULL,
    source_url VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    title VARCHAR(120) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

```

### 5. Products Table

```sql
CREATE TABLE products (
    id VARCHAR(26) PRIMARY KEY,  -- ULID format
    name VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    is_location_offer BOOLEAN DEFAULT FALSE,
    is_rental BOOLEAN DEFAULT FALSE,
    category_id VARCHAR(26) NOT NULL,
    brand_id VARCHAR(26) NOT NULL,
    product_image_id VARCHAR(26) NOT NULL,
    in_stock BOOLEAN DEFAULT TRUE,
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE,
    FOREIGN KEY (product_image_id) REFERENCES product_images(id) ON DELETE CASCADE
);

```

### 6. Favorites Table

```sql
CREATE TABLE favorites (
    id VARCHAR(26) PRIMARY KEY,  -- ULID format
    user_id VARCHAR(26) NOT NULL,
    product_id VARCHAR(26) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_product (user_id, product_id)
);

```

### 7. Invoices Table

```sql
CREATE TABLE invoices (
    id VARCHAR(26) PRIMARY KEY,  -- ULID format
    invoice_number VARCHAR(255) NOT NULL UNIQUE,
    invoice_date DATE NOT NULL,
    billing_address TEXT NOT NULL,
    billing_city VARCHAR(40) NOT NULL,
    billing_state VARCHAR(40) NULL,
    billing_country VARCHAR(40) NOT NULL,
    billing_postcode VARCHAR(10) NULL,
    user_id VARCHAR(26) NOT NULL,
    total DECIMAL(8,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

```

### 8. Invoice Items Table

```sql
CREATE TABLE invoice_items (
    id VARCHAR(26) PRIMARY KEY,  -- ULID format
    invoice_id VARCHAR(26) NOT NULL,
    product_id VARCHAR(26) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(8,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

```

### 9. Payments Table

```sql
CREATE TABLE payments (
    id VARCHAR(26) PRIMARY KEY,  -- ULID format
    invoice_id VARCHAR(26) NOT NULL,
    method ENUM('CREDIT_CARD', 'BANK_TRANSFER', 'CASH_ON_DELIVERY', 'BUY_NOW_PAY_LATER') NOT NULL,
    status ENUM('PENDING', 'SUCCESS', 'FAILED') NOT NULL,
    payment_reference_id VARCHAR(26) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE
);

```
