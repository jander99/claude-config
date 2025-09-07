# Database Schema Design and Architecture

## Overview

Database schema design encompasses the systematic planning and implementation of database structures, including table design, relationship modeling, indexing strategies, and data architecture patterns that ensure optimal performance, maintainability, and scalability across relational and NoSQL database systems.

## Relational Database Design

### Entity Relationship Modeling

**Conceptual Modeling:**
- **Entity Identification**: Business object identification and definition
- **Attribute Definition**: Entity property specification and constraints
- **Relationship Mapping**: Inter-entity relationship identification and cardinality
- **Business Rule Integration**: Domain-specific constraint modeling

**Logical Design Principles:**
```sql
-- Example: E-commerce schema design
-- Customer entity with proper normalization
CREATE TABLE customers (
    customer_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Constraints
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT name_not_empty CHECK (
        LENGTH(TRIM(first_name)) > 0 AND 
        LENGTH(TRIM(last_name)) > 0
    )
);

-- Address entity with proper separation
CREATE TABLE addresses (
    address_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    address_type VARCHAR(20) NOT NULL CHECK (address_type IN ('billing', 'shipping', 'both')),
    street_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state_province VARCHAR(100),
    postal_code VARCHAR(20) NOT NULL,
    country_code CHAR(2) NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure only one default address per type per customer
    UNIQUE(customer_id, address_type, is_default) DEFERRABLE INITIALLY DEFERRED
);

-- Product catalog with hierarchical categories
CREATE TABLE categories (
    category_id BIGSERIAL PRIMARY KEY,
    parent_category_id BIGINT REFERENCES categories(category_id),
    category_name VARCHAR(100) NOT NULL,
    category_path LTREE, -- PostgreSQL hierarchical data type
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent self-referencing and circular references
    CONSTRAINT no_self_reference CHECK (category_id != parent_category_id)
);
```

### Normalization and Denormalization

**Normalization Strategies:**
- **First Normal Form (1NF)**: Atomic values and unique column names
- **Second Normal Form (2NF)**: Elimination of partial dependencies
- **Third Normal Form (3NF)**: Elimination of transitive dependencies
- **Boyce-Codd Normal Form (BCNF)**: Stricter dependency requirements

**Strategic Denormalization:**
```sql
-- Example: Order summary denormalization for performance
CREATE TABLE orders (
    order_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
    order_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    
    -- Denormalized summary fields for performance
    total_items INTEGER NOT NULL DEFAULT 0,
    subtotal DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    tax_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    shipping_cost DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    
    -- Maintaining referential data
    shipping_address_id BIGINT REFERENCES addresses(address_id),
    billing_address_id BIGINT REFERENCES addresses(address_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Triggers to maintain denormalized data consistency
    CONSTRAINT positive_amounts CHECK (
        subtotal >= 0 AND tax_amount >= 0 AND 
        shipping_cost >= 0 AND total_amount >= 0
    )
);

-- Trigger function to maintain order totals
CREATE OR REPLACE FUNCTION update_order_totals()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE orders SET
        total_items = (
            SELECT COALESCE(SUM(quantity), 0)
            FROM order_items 
            WHERE order_id = NEW.order_id
        ),
        subtotal = (
            SELECT COALESCE(SUM(quantity * unit_price), 0.00)
            FROM order_items 
            WHERE order_id = NEW.order_id
        ),
        updated_at = CURRENT_TIMESTAMP
    WHERE order_id = NEW.order_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_items_update_totals
    AFTER INSERT OR UPDATE OR DELETE ON order_items
    FOR EACH ROW EXECUTE FUNCTION update_order_totals();
```

### Data Type Optimization

**Appropriate Data Type Selection:**
```sql
-- Optimized data types for different use cases
CREATE TABLE products (
    product_id BIGSERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL, -- Limited length for SKUs
    name VARCHAR(255) NOT NULL,
    description TEXT, -- Unlimited text for descriptions
    
    -- Price storage with appropriate precision
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    cost DECIMAL(10,2) CHECK (cost >= 0),
    
    -- Weight in grams (integer for precision)
    weight_grams INTEGER CHECK (weight_grams > 0),
    
    -- Dimensions in millimeters
    length_mm INTEGER CHECK (length_mm > 0),
    width_mm INTEGER CHECK (width_mm > 0),
    height_mm INTEGER CHECK (height_mm > 0),
    
    -- Inventory management
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
    reserved_quantity INTEGER NOT NULL DEFAULT 0 CHECK (reserved_quantity >= 0),
    
    -- Status fields
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- JSON for flexible attributes (PostgreSQL)
    attributes JSONB,
    
    -- Search optimization
    search_vector TSVECTOR GENERATED ALWAYS AS (
        to_tsvector('english', name || ' ' || COALESCE(description, ''))
    ) STORED
);
```

## NoSQL Database Design

### Document Database Design

**MongoDB Schema Patterns:**
```javascript
// User profile with embedded documents
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "profile": {
    "firstName": "John",
    "lastName": "Doe",
    "avatar": {
      "url": "https://cdn.example.com/avatars/user123.jpg",
      "thumbnails": {
        "small": "https://cdn.example.com/avatars/user123_sm.jpg",
        "medium": "https://cdn.example.com/avatars/user123_md.jpg"
      }
    }
  },
  "preferences": {
    "notifications": {
      "email": true,
      "sms": false,
      "push": true
    },
    "privacy": {
      "profileVisible": true,
      "showOnlineStatus": false
    }
  },
  "addresses": [
    {
      "type": "home",
      "street": "123 Main St",
      "city": "Anytown",
      "country": "US",
      "postalCode": "12345",
      "isDefault": true
    }
  ],
  "createdAt": ISODate("2024-01-01T00:00:00Z"),
  "updatedAt": ISODate("2024-01-01T00:00:00Z")
}

// Product catalog with references and embeddings
{
  "_id": ObjectId("..."),
  "sku": "PROD-001",
  "name": "Premium Laptop",
  "description": "High-performance laptop for professionals",
  "category": {
    "id": ObjectId("..."),
    "name": "Electronics",
    "path": "electronics/computers/laptops"
  },
  "pricing": {
    "currency": "USD",
    "listPrice": 1299.99,
    "salePrice": 1199.99,
    "costPrice": 800.00
  },
  "inventory": {
    "stockQuantity": 45,
    "reservedQuantity": 5,
    "reorderLevel": 10,
    "supplier": {
      "id": ObjectId("..."),
      "name": "Tech Supplier Inc"
    }
  },
  "specifications": {
    "processor": "Intel i7-12700H",
    "memory": "16GB DDR4",
    "storage": "512GB SSD",
    "display": "15.6\" FHD"
  },
  "reviews": {
    "averageRating": 4.5,
    "totalReviews": 127,
    "ratingDistribution": {
      "5": 78,
      "4": 32,
      "3": 12,
      "2": 3,
      "1": 2
    }
  },
  "isActive": true,
  "createdAt": ISODate("2024-01-01T00:00:00Z"),
  "updatedAt": ISODate("2024-01-01T00:00:00Z")
}
```

**Design Patterns for MongoDB:**
- **Embedding vs. Referencing**: Decision criteria for data modeling
- **One-to-Few**: Embedding small arrays of related documents
- **One-to-Many**: Reference pattern for large related collections
- **Many-to-Many**: Two-way referencing with junction collections

### Key-Value Store Design

**Redis Data Structure Patterns:**
```python
# User session management
class RedisSessionManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.session_prefix = "session:"
        self.user_sessions_prefix = "user_sessions:"
    
    def create_session(self, user_id, session_data, ttl=3600):
        session_id = str(uuid.uuid4())
        session_key = f"{self.session_prefix}{session_id}"
        user_sessions_key = f"{self.user_sessions_prefix}{user_id}"
        
        # Store session data with expiration
        session_payload = {
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat(),
            **session_data
        }
        
        # Use pipeline for atomic operations
        pipe = self.redis.pipeline()
        pipe.hmset(session_key, session_payload)
        pipe.expire(session_key, ttl)
        pipe.sadd(user_sessions_key, session_id)
        pipe.expire(user_sessions_key, ttl + 300)  # Slightly longer TTL
        pipe.execute()
        
        return session_id
    
    def get_session(self, session_id):
        session_key = f"{self.session_prefix}{session_id}"
        session_data = self.redis.hgetall(session_key)
        
        if session_data:
            # Update last activity
            self.redis.hset(session_key, 'last_activity', 
                          datetime.utcnow().isoformat())
            return session_data
        
        return None

# Cache management with intelligent invalidation
class IntelligentCacheManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.cache_tags_prefix = "cache_tags:"
        
    def set_with_tags(self, key, value, tags, ttl=3600):
        # Store the cached value
        self.redis.setex(key, ttl, value)
        
        # Associate with tags for bulk invalidation
        pipe = self.redis.pipeline()
        for tag in tags:
            tag_key = f"{self.cache_tags_prefix}{tag}"
            pipe.sadd(tag_key, key)
            pipe.expire(tag_key, ttl + 300)
        pipe.execute()
    
    def invalidate_by_tag(self, tag):
        tag_key = f"{self.cache_tags_prefix}{tag}"
        cached_keys = self.redis.smembers(tag_key)
        
        if cached_keys:
            # Remove all cached entries with this tag
            pipe = self.redis.pipeline()
            for key in cached_keys:
                pipe.delete(key)
            pipe.delete(tag_key)
            pipe.execute()
```

## Indexing Strategies

### Relational Database Indexing

**Strategic Index Design:**
```sql
-- Primary and unique indexes
CREATE UNIQUE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_active ON customers(is_active) WHERE is_active = true;

-- Composite indexes for common query patterns
CREATE INDEX idx_orders_customer_status_date ON orders(customer_id, order_status, created_at DESC);
CREATE INDEX idx_products_category_active ON products(category_id, is_active, price) WHERE is_active = true;

-- Partial indexes for specific conditions
CREATE INDEX idx_orders_pending ON orders(created_at DESC) WHERE order_status = 'pending';
CREATE INDEX idx_products_featured ON products(display_order, name) WHERE is_featured = true;

-- Full-text search indexes
CREATE INDEX idx_products_search ON products USING GIN(search_vector);
CREATE INDEX idx_products_attributes ON products USING GIN(attributes) WHERE attributes IS NOT NULL;

-- Expression indexes for computed values
CREATE INDEX idx_customers_full_name ON customers(LOWER(first_name || ' ' || last_name));
CREATE INDEX idx_orders_total_range ON orders((
    CASE 
        WHEN total_amount < 100 THEN 'low'
        WHEN total_amount < 500 THEN 'medium'
        ELSE 'high'
    END
));
```

**Index Maintenance Strategies:**
```sql
-- Index usage monitoring query
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan::float / GREATEST(seq_scan + idx_scan, 1) AS index_usage_ratio
FROM pg_stat_user_indexes 
ORDER BY idx_scan DESC;

-- Unused index identification
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes 
WHERE idx_scan = 0
AND schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### NoSQL Indexing Patterns

**MongoDB Index Strategies:**
```javascript
// Compound indexes for query patterns
db.products.createIndex(
  { category: 1, isActive: 1, price: 1 },
  { name: "idx_category_active_price" }
);

// Text search indexes
db.products.createIndex(
  { name: "text", description: "text" },
  { 
    name: "idx_product_search",
    weights: { name: 10, description: 1 },
    default_language: "english"
  }
);

// Geospatial indexes for location-based queries
db.stores.createIndex(
  { location: "2dsphere" },
  { name: "idx_store_location" }
);

// Partial indexes with conditions
db.orders.createIndex(
  { customerId: 1, createdAt: -1 },
  { 
    partialFilterExpression: { status: "active" },
    name: "idx_active_orders"
  }
);

// TTL indexes for automatic document expiration
db.sessions.createIndex(
  { lastActivity: 1 },
  { expireAfterSeconds: 3600, name: "idx_session_ttl" }
);
```

## Performance Optimization

### Query Performance Tuning

**Query Analysis and Optimization:**
```sql
-- Query performance analysis
EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
SELECT 
    c.first_name,
    c.last_name,
    c.email,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id 
    AND o.order_status = 'completed'
    AND o.created_at >= '2024-01-01'
WHERE c.is_active = true
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
HAVING COUNT(o.order_id) > 0
ORDER BY total_spent DESC, c.last_name
LIMIT 100;

-- Optimized version with better indexing strategy
CREATE INDEX CONCURRENTLY idx_orders_customer_completed_date 
ON orders(customer_id, created_at DESC) 
WHERE order_status = 'completed';

-- Window functions for efficient ranking
SELECT 
    product_id,
    name,
    price,
    category_id,
    ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price DESC) as price_rank,
    PERCENT_RANK() OVER (PARTITION BY category_id ORDER BY price) as price_percentile
FROM products 
WHERE is_active = true;
```

**Caching Strategies:**
```python
class DatabaseCacheLayer:
    def __init__(self, db_connection, cache_client):
        self.db = db_connection
        self.cache = cache_client
        self.default_ttl = 3600
    
    def get_product_with_cache(self, product_id):
        cache_key = f"product:{product_id}"
        
        # Try cache first
        cached_product = self.cache.get(cache_key)
        if cached_product:
            return json.loads(cached_product)
        
        # Fetch from database
        product = self.db.execute("""
            SELECT p.*, c.name as category_name
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            WHERE p.product_id = %s AND p.is_active = true
        """, (product_id,)).fetchone()
        
        if product:
            # Cache with tags for intelligent invalidation
            product_data = dict(product)
            self.cache.setex(
                cache_key, 
                self.default_ttl, 
                json.dumps(product_data)
            )
            
            # Add to cache tags for invalidation
            self.cache.sadd(f"tag:product_updates", cache_key)
            self.cache.sadd(f"tag:category:{product['category_id']}", cache_key)
            
            return product_data
        
        return None
    
    def invalidate_product_cache(self, product_id):
        # Direct cache invalidation
        self.cache.delete(f"product:{product_id}")
        
        # Tag-based invalidation for related data
        self.cache.delete(f"tag:product_updates")
```

This comprehensive schema design framework ensures optimal database structure, performance, and maintainability across both relational and NoSQL database systems while providing clear patterns for indexing and optimization strategies.