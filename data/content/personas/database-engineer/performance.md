# Data Modeling and Architecture

## Overview

Data modeling encompasses the systematic design of data structures, relationships, and constraints that accurately represent business requirements while ensuring optimal performance, scalability, and maintainability across different database paradigms including relational, document, graph, and time-series databases.

## Conceptual Data Modeling

### Business Requirements Analysis

**Domain-Driven Design Approach:**
```python
# Domain entity identification and modeling
class BusinessDomainAnalyzer:
    def __init__(self):
        self.entities = {}
        self.relationships = {}
        self.business_rules = []
        self.constraints = {}
    
    def identify_core_entities(self, business_requirements):
        """
        Extract core business entities from requirements
        """
        entities = {}
        
        # E-commerce domain example
        entities['Customer'] = {
            'attributes': {
                'customer_id': {'type': 'identifier', 'required': True},
                'email': {'type': 'string', 'unique': True, 'required': True},
                'password_hash': {'type': 'string', 'required': True},
                'first_name': {'type': 'string', 'required': True},
                'last_name': {'type': 'string', 'required': True},
                'date_of_birth': {'type': 'date', 'required': False},
                'phone': {'type': 'string', 'required': False},
                'created_at': {'type': 'timestamp', 'auto': True},
                'is_active': {'type': 'boolean', 'default': True}
            },
            'business_rules': [
                'Email must be unique across all customers',
                'Password must meet security requirements',
                'Customer must be 18+ for certain product categories'
            ]
        }
        
        entities['Product'] = {
            'attributes': {
                'product_id': {'type': 'identifier', 'required': True},
                'sku': {'type': 'string', 'unique': True, 'required': True},
                'name': {'type': 'string', 'required': True},
                'description': {'type': 'text', 'required': False},
                'category_id': {'type': 'foreign_key', 'references': 'Category'},
                'price': {'type': 'decimal', 'precision': 10, 'scale': 2, 'required': True},
                'cost': {'type': 'decimal', 'precision': 10, 'scale': 2},
                'stock_quantity': {'type': 'integer', 'min': 0, 'required': True},
                'is_active': {'type': 'boolean', 'default': True}
            },
            'business_rules': [
                'SKU must be unique across all products',
                'Price must be greater than or equal to cost',
                'Stock quantity cannot be negative',
                'Products can only be sold if active and in stock'
            ]
        }
        
        entities['Order'] = {
            'attributes': {
                'order_id': {'type': 'identifier', 'required': True},
                'customer_id': {'type': 'foreign_key', 'references': 'Customer'},
                'order_status': {'type': 'enum', 'values': ['pending', 'processing', 'shipped', 'delivered', 'cancelled']},
                'order_date': {'type': 'timestamp', 'auto': True},
                'subtotal': {'type': 'decimal', 'precision': 12, 'scale': 2},
                'tax_amount': {'type': 'decimal', 'precision': 12, 'scale': 2},
                'shipping_cost': {'type': 'decimal', 'precision': 12, 'scale': 2},
                'total_amount': {'type': 'decimal', 'precision': 12, 'scale': 2, 'required': True}
            },
            'business_rules': [
                'Total amount must equal subtotal + tax + shipping',
                'Orders can only be modified in pending status',
                'Cancelled orders cannot change to other statuses'
            ]
        }
        
        return entities
    
    def define_entity_relationships(self, entities):
        """
        Define relationships between business entities
        """
        relationships = {
            'customer_addresses': {
                'type': 'one_to_many',
                'parent': 'Customer',
                'child': 'Address',
                'foreign_key': 'customer_id',
                'cascade': 'delete'
            },
            'customer_orders': {
                'type': 'one_to_many',
                'parent': 'Customer',
                'child': 'Order',
                'foreign_key': 'customer_id',
                'cascade': 'restrict'  # Don't delete customers with orders
            },
            'order_items': {
                'type': 'one_to_many',
                'parent': 'Order',
                'child': 'OrderItem',
                'foreign_key': 'order_id',
                'cascade': 'delete'
            },
            'product_categories': {
                'type': 'many_to_one',
                'child': 'Product',
                'parent': 'Category',
                'foreign_key': 'category_id',
                'cascade': 'restrict'
            },
            'product_reviews': {
                'type': 'one_to_many',
                'parent': 'Product',
                'child': 'Review',
                'foreign_key': 'product_id',
                'cascade': 'delete'
            }
        }
        
        return relationships
```

### Entity Relationship Diagrams

**Advanced ER Modeling:**
```sql
-- Comprehensive entity relationship implementation
-- Customer entity with full normalization
CREATE TABLE customers (
    customer_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Personal information
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    phone VARCHAR(20),
    
    -- Account management
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    phone_verified BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE,
    
    -- Constraints
    CONSTRAINT customer_email_format CHECK (
        email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    ),
    CONSTRAINT customer_names_not_empty CHECK (
        LENGTH(TRIM(first_name)) > 0 AND LENGTH(TRIM(last_name)) > 0
    ),
    CONSTRAINT customer_age_check CHECK (
        date_of_birth IS NULL OR 
        date_of_birth <= CURRENT_DATE - INTERVAL '13 years'
    )
);

-- Address entity with proper normalization and validation
CREATE TABLE addresses (
    address_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    
    -- Address classification
    address_type VARCHAR(20) NOT NULL CHECK (
        address_type IN ('billing', 'shipping', 'both')
    ),
    address_label VARCHAR(50), -- Home, Work, etc.
    
    -- Address components
    recipient_name VARCHAR(200),
    company_name VARCHAR(200),
    street_address_1 VARCHAR(255) NOT NULL,
    street_address_2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state_province VARCHAR(100),
    postal_code VARCHAR(20) NOT NULL,
    country_code CHAR(2) NOT NULL,
    
    -- Validation and preferences
    is_default BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure only one default address per type per customer
    UNIQUE(customer_id, address_type, is_default) DEFERRABLE INITIALLY DEFERRED
);

-- Category hierarchy with closure table pattern
CREATE TABLE categories (
    category_id BIGSERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    category_slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_category_id BIGINT REFERENCES categories(category_id),
    
    -- Display and management
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- SEO and metadata
    meta_title VARCHAR(255),
    meta_description TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent self-referencing
    CONSTRAINT no_self_reference CHECK (category_id != parent_category_id)
);

-- Category closure table for efficient hierarchy queries
CREATE TABLE category_hierarchy (
    ancestor_id BIGINT NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    descendant_id BIGINT NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    depth INTEGER NOT NULL DEFAULT 0,
    
    PRIMARY KEY (ancestor_id, descendant_id),
    CONSTRAINT hierarchy_depth_check CHECK (depth >= 0)
);

-- Product entity with comprehensive attributes
CREATE TABLE products (
    product_id BIGSERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id BIGINT NOT NULL REFERENCES categories(category_id),
    
    -- Pricing
    price DECIMAL(12,2) NOT NULL CHECK (price >= 0),
    compare_at_price DECIMAL(12,2) CHECK (compare_at_price >= price),
    cost DECIMAL(12,2) CHECK (cost >= 0),
    
    -- Physical attributes
    weight_grams INTEGER CHECK (weight_grams > 0),
    length_mm INTEGER CHECK (length_mm > 0),
    width_mm INTEGER CHECK (width_mm > 0),
    height_mm INTEGER CHECK (height_mm > 0),
    
    -- Inventory management
    inventory_quantity INTEGER NOT NULL DEFAULT 0 CHECK (inventory_quantity >= 0),
    inventory_policy VARCHAR(20) DEFAULT 'deny' CHECK (
        inventory_policy IN ('deny', 'continue')
    ),
    
    -- Product management
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    requires_shipping BOOLEAN DEFAULT TRUE,
    is_taxable BOOLEAN DEFAULT TRUE,
    
    -- SEO and searchability
    handle VARCHAR(255) UNIQUE,
    meta_title VARCHAR(255),
    meta_description TEXT,
    search_keywords TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Full-text search vector
    search_vector TSVECTOR GENERATED ALWAYS AS (
        setweight(to_tsvector('english', name), 'A') ||
        setweight(to_tsvector('english', COALESCE(description, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(search_keywords, '')), 'C')
    ) STORED
);
```

## Logical Data Models

### Relationship Patterns

**Advanced Relationship Modeling:**
```sql
-- Many-to-many relationship with attributes (Order-Product through OrderItem)
CREATE TABLE order_items (
    order_item_id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id BIGINT NOT NULL REFERENCES products(product_id),
    
    -- Quantity and pricing at time of order
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(12,2) NOT NULL CHECK (unit_price >= 0),
    total_price DECIMAL(12,2) NOT NULL CHECK (total_price >= 0),
    
    -- Product snapshot at time of order
    product_name VARCHAR(255) NOT NULL,
    product_sku VARCHAR(50) NOT NULL,
    
    -- Fulfillment tracking
    quantity_fulfilled INTEGER DEFAULT 0 CHECK (
        quantity_fulfilled >= 0 AND quantity_fulfilled <= quantity
    ),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure unique product per order
    UNIQUE(order_id, product_id),
    
    -- Ensure total price matches quantity * unit_price
    CONSTRAINT price_calculation_check CHECK (
        total_price = quantity * unit_price
    )
);

-- Self-referencing relationship (Category hierarchy)
CREATE TABLE category_relationships (
    parent_id BIGINT NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    child_id BIGINT NOT NULL REFERENCES categories(category_id) ON DELETE CASCADE,
    relationship_type VARCHAR(20) DEFAULT 'parent_child' CHECK (
        relationship_type IN ('parent_child', 'related', 'alternative')
    ),
    
    PRIMARY KEY (parent_id, child_id, relationship_type),
    
    -- Prevent self-referencing
    CONSTRAINT no_self_reference CHECK (parent_id != child_id)
);

-- Polymorphic relationships (Comments on different entity types)
CREATE TABLE comments (
    comment_id BIGSERIAL PRIMARY KEY,
    commentable_type VARCHAR(50) NOT NULL CHECK (
        commentable_type IN ('product', 'order', 'customer')
    ),
    commentable_id BIGINT NOT NULL,
    
    -- Comment content
    title VARCHAR(255),
    content TEXT NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    
    -- Author information
    author_id BIGINT REFERENCES customers(customer_id),
    author_name VARCHAR(100), -- For guest comments
    author_email VARCHAR(255), -- For guest comments
    
    -- Moderation
    is_approved BOOLEAN DEFAULT FALSE,
    is_featured BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure polymorphic integrity
    CONSTRAINT comment_author_check CHECK (
        (author_id IS NOT NULL) OR 
        (author_name IS NOT NULL AND author_email IS NOT NULL)
    )
);

-- Create indexes for polymorphic relationships
CREATE INDEX idx_comments_polymorphic ON comments(commentable_type, commentable_id);
CREATE INDEX idx_comments_approval_date ON comments(is_approved, created_at DESC);
```

### Data Integrity Constraints

**Advanced Constraint Implementation:**
```sql
-- Complex business rule constraints
CREATE OR REPLACE FUNCTION validate_order_business_rules()
RETURNS TRIGGER AS $$
BEGIN
    -- Validate order status transitions
    IF OLD.order_status IS NOT NULL AND NEW.order_status != OLD.order_status THEN
        -- Define valid status transitions
        IF NOT (
            (OLD.order_status = 'pending' AND NEW.order_status IN ('processing', 'cancelled')) OR
            (OLD.order_status = 'processing' AND NEW.order_status IN ('shipped', 'cancelled')) OR
            (OLD.order_status = 'shipped' AND NEW.order_status IN ('delivered', 'returned')) OR
            (OLD.order_status = 'delivered' AND NEW.order_status = 'returned')
        ) THEN
            RAISE EXCEPTION 'Invalid order status transition from % to %', 
                OLD.order_status, NEW.order_status;
        END IF;
    END IF;
    
    -- Validate order totals
    IF NEW.total_amount != (NEW.subtotal + NEW.tax_amount + NEW.shipping_cost) THEN
        RAISE EXCEPTION 'Order total amount does not match sum of components';
    END IF;
    
    -- Validate customer is active
    IF NOT EXISTS (
        SELECT 1 FROM customers 
        WHERE customer_id = NEW.customer_id AND is_active = TRUE
    ) THEN
        RAISE EXCEPTION 'Cannot create order for inactive customer';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_business_rules_trigger
    BEFORE INSERT OR UPDATE ON orders
    FOR EACH ROW EXECUTE FUNCTION validate_order_business_rules();

-- Inventory management constraints
CREATE OR REPLACE FUNCTION manage_product_inventory()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
        -- Check inventory availability
        IF NEW.quantity > 0 THEN
            DECLARE
                available_quantity INTEGER;
            BEGIN
                SELECT (inventory_quantity - reserved_quantity) 
                INTO available_quantity
                FROM products 
                WHERE product_id = NEW.product_id;
                
                IF available_quantity < NEW.quantity THEN
                    RAISE EXCEPTION 'Insufficient inventory for product ID %. Available: %, Requested: %',
                        NEW.product_id, available_quantity, NEW.quantity;
                END IF;
            END;
        END IF;
        
        RETURN NEW;
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER order_items_inventory_trigger
    BEFORE INSERT OR UPDATE ON order_items
    FOR EACH ROW EXECUTE FUNCTION manage_product_inventory();
```

## Document Database Modeling

### MongoDB Schema Design Patterns

**Embedded vs. Referenced Data:**
```javascript
// Product catalog with embedded reviews (one-to-few pattern)
{
  "_id": ObjectId("..."),
  "sku": "LAPTOP-001",
  "name": "Professional Laptop",
  "description": "High-performance laptop for professionals",
  "category": {
    "id": ObjectId("..."),
    "name": "Electronics",
    "path": ["electronics", "computers", "laptops"]
  },
  "pricing": {
    "currency": "USD",
    "listPrice": 1299.99,
    "salePrice": 1199.99,
    "costPrice": 800.00,
    "priceHistory": [
      {
        "price": 1299.99,
        "effectiveDate": ISODate("2024-01-01"),
        "reason": "initial_price"
      },
      {
        "price": 1199.99,
        "effectiveDate": ISODate("2024-03-01"),
        "reason": "promotion"
      }
    ]
  },
  "inventory": {
    "quantity": 45,
    "reserved": 5,
    "available": 40,
    "reorderLevel": 10,
    "locations": [
      {
        "warehouse": "main",
        "quantity": 30,
        "reserved": 3
      },
      {
        "warehouse": "west",
        "quantity": 15,
        "reserved": 2
      }
    ]
  },
  "specifications": {
    "processor": "Intel i7-12700H",
    "memory": "16GB DDR4",
    "storage": "512GB SSD",
    "display": "15.6\" FHD",
    "weight": "2.1kg",
    "dimensions": {
      "length": 357,
      "width": 234,
      "height": 19.9,
      "unit": "mm"
    }
  },
  "reviews": {
    "summary": {
      "averageRating": 4.5,
      "totalReviews": 127,
      "distribution": {
        "5": 78,
        "4": 32,
        "3": 12,
        "2": 3,
        "1": 2
      }
    },
    "featured": [
      {
        "id": ObjectId("..."),
        "rating": 5,
        "title": "Excellent performance",
        "content": "Great laptop for development work...",
        "author": {
          "id": ObjectId("..."),
          "name": "John D.",
          "verified": true
        },
        "createdAt": ISODate("2024-01-15"),
        "helpful": 23
      }
    ]
  },
  "seo": {
    "slug": "professional-laptop-i7",
    "metaTitle": "Professional Laptop - High Performance Computing",
    "metaDescription": "Discover our professional laptop with Intel i7 processor...",
    "keywords": ["laptop", "professional", "intel", "i7", "development"]
  },
  "isActive": true,
  "isFeatured": false,
  "createdAt": ISODate("2024-01-01T00:00:00Z"),
  "updatedAt": ISODate("2024-03-01T10:30:00Z")
}

// Customer profile with references to orders (one-to-many pattern)
{
  "_id": ObjectId("..."),
  "email": "john.doe@example.com",
  "profile": {
    "firstName": "John",
    "lastName": "Doe",
    "dateOfBirth": ISODate("1985-06-15"),
    "phone": "+1-555-123-4567",
    "avatar": {
      "url": "https://cdn.example.com/avatars/john.jpg",
      "thumbnails": {
        "small": "https://cdn.example.com/avatars/john_sm.jpg",
        "medium": "https://cdn.example.com/avatars/john_md.jpg"
      }
    }
  },
  "preferences": {
    "notifications": {
      "email": true,
      "sms": false,
      "push": true,
      "categories": ["orders", "promotions", "newsletters"]
    },
    "privacy": {
      "profileVisible": true,
      "showOnlineStatus": false,
      "allowMarketing": true
    },
    "shopping": {
      "preferredCategories": ["electronics", "books"],
      "priceAlerts": true,
      "wishlistPublic": false
    }
  },
  "addresses": [
    {
      "type": "billing",
      "isDefault": true,
      "recipient": "John Doe",
      "street": "123 Main St",
      "city": "Anytown",
      "state": "CA",
      "postalCode": "12345",
      "country": "US",
      "instructions": "Leave at front door"
    },
    {
      "type": "shipping",
      "isDefault": false,
      "recipient": "John Doe",
      "company": "Tech Corp",
      "street": "456 Business Ave",
      "city": "Anytown",
      "state": "CA",
      "postalCode": "12346",
      "country": "US"
    }
  ],
  "loyaltyProgram": {
    "tier": "gold",
    "points": 15420,
    "joinDate": ISODate("2023-01-15"),
    "benefits": ["free_shipping", "early_access", "birthday_discount"]
  },
  "statistics": {
    "totalOrders": 24,
    "totalSpent": 5684.32,
    "averageOrderValue": 236.85,
    "lastOrderDate": ISODate("2024-02-15"),
    "favoriteCategory": "electronics"
  },
  "authentication": {
    "passwordHash": "$2b$12$...", // Handled securely
    "lastLogin": ISODate("2024-03-01T15:30:00Z"),
    "loginCount": 156,
    "twoFactorEnabled": true
  },
  "isActive": true,
  "emailVerified": true,
  "phoneVerified": true,
  "createdAt": ISODate("2023-01-15T00:00:00Z"),
  "updatedAt": ISODate("2024-03-01T15:30:00Z")
}
```

**Schema Validation in MongoDB:**
```javascript
// Comprehensive schema validation
db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["sku", "name", "category", "pricing", "inventory"],
      properties: {
        sku: {
          bsonType: "string",
          pattern: "^[A-Z0-9-]{3,50}$",
          description: "SKU must be 3-50 alphanumeric characters with dashes"
        },
        name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 255,
          description: "Product name is required and must be 1-255 characters"
        },
        category: {
          bsonType: "object",
          required: ["id", "name", "path"],
          properties: {
            id: { bsonType: "objectId" },
            name: { bsonType: "string" },
            path: {
              bsonType: "array",
              items: { bsonType: "string" }
            }
          }
        },
        pricing: {
          bsonType: "object",
          required: ["currency", "listPrice"],
          properties: {
            currency: {
              enum: ["USD", "EUR", "GBP", "JPY"],
              description: "Currency must be a supported currency code"
            },
            listPrice: {
              bsonType: "double",
              minimum: 0,
              description: "List price must be a non-negative number"
            },
            salePrice: {
              bsonType: "double",
              minimum: 0,
              description: "Sale price must be a non-negative number"
            }
          }
        },
        inventory: {
          bsonType: "object",
          required: ["quantity", "available"],
          properties: {
            quantity: {
              bsonType: "int",
              minimum: 0,
              description: "Quantity must be a non-negative integer"
            },
            available: {
              bsonType: "int",
              minimum: 0,
              description: "Available quantity must be non-negative"
            }
          }
        },
        isActive: {
          bsonType: "bool",
          description: "Active status must be a boolean"
        },
        createdAt: {
          bsonType: "date",
          description: "Created date must be a valid date"
        }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// Index creation for optimal query performance
db.products.createIndex({ "sku": 1 }, { unique: true });
db.products.createIndex({ "category.id": 1, "isActive": 1, "pricing.listPrice": 1 });
db.products.createIndex({ "name": "text", "description": "text" }, { 
  weights: { "name": 10, "description": 1 },
  name: "product_search_index"
});
db.products.createIndex({ "inventory.available": 1 });
db.products.createIndex({ "createdAt": -1 });
```

## Graph Database Modeling

### Neo4j Relationship Modeling

**Social Commerce Graph Model:**
```cypher
// Create node types with properties
CREATE CONSTRAINT customer_email IF NOT EXISTS FOR (c:Customer) REQUIRE c.email IS UNIQUE;
CREATE CONSTRAINT product_sku IF NOT EXISTS FOR (p:Product) REQUIRE p.sku IS UNIQUE;
CREATE CONSTRAINT category_slug IF NOT EXISTS FOR (cat:Category) REQUIRE cat.slug IS UNIQUE;

// Customer nodes
CREATE (c:Customer {
  customerId: 'cust_001',
  email: 'john.doe@example.com',
  firstName: 'John',
  lastName: 'Doe',
  dateOfBirth: date('1985-06-15'),
  createdAt: datetime(),
  isActive: true
});

// Product nodes with rich attributes
CREATE (p:Product {
  productId: 'prod_001',
  sku: 'LAPTOP-001',
  name: 'Professional Laptop',
  description: 'High-performance laptop for professionals',
  price: 1299.99,
  category: 'Electronics',
  brand: 'TechBrand',
  model: 'Pro 15',
  specifications: {
    processor: 'Intel i7',
    memory: '16GB',
    storage: '512GB SSD'
  },
  createdAt: datetime(),
  isActive: true
});

// Category hierarchy
CREATE (cat:Category {
  categoryId: 'cat_001',
  name: 'Electronics',
  slug: 'electronics',
  description: 'Electronic devices and accessories'
});

// Relationships with properties
CREATE (c)-[:PURCHASED {
  orderId: 'order_001',
  quantity: 1,
  unitPrice: 1299.99,
  totalPrice: 1299.99,
  purchaseDate: datetime(),
  orderStatus: 'completed'
}]->(p);

CREATE (c)-[:REVIEWED {
  reviewId: 'review_001',
  rating: 5,
  title: 'Excellent laptop',
  content: 'Great performance and build quality',
  reviewDate: datetime(),
  verified: true,
  helpful: 23
}]->(p);

// Social relationships
CREATE (c1:Customer)-[:FOLLOWS {
  followDate: datetime(),
  notifications: true
}]->(c2:Customer);

CREATE (c)-[:ADDED_TO_WISHLIST {
  addedDate: datetime(),
  priority: 'high'
}]->(p);

// Complex queries leveraging graph structure
// Find customers who bought similar products
MATCH (c:Customer)-[:PURCHASED]->(p:Product)<-[:PURCHASED]-(similar:Customer)
WHERE c.customerId = 'cust_001' AND c <> similar
WITH similar, count(p) as commonPurchases
ORDER BY commonPurchases DESC
LIMIT 10
RETURN similar.firstName, similar.lastName, commonPurchases;

// Product recommendation based on purchase patterns
MATCH (c:Customer {customerId: 'cust_001'})-[:PURCHASED]->(p:Product),
      (p)<-[:PURCHASED]-(other:Customer)-[:PURCHASED]->(rec:Product)
WHERE NOT (c)-[:PURCHASED]->(rec)
WITH rec, count(other) as purchaseCount
ORDER BY purchaseCount DESC
LIMIT 5
RETURN rec.name, rec.price, rec.category, purchaseCount;
```

This comprehensive data modeling framework provides systematic approaches to designing data structures across different database paradigms while ensuring optimal performance, maintainability, and business rule compliance.