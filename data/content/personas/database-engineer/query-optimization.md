# Database Performance Optimization

## Overview

Database performance optimization encompasses systematic approaches to improving database response times, throughput, and resource utilization through query optimization, indexing strategies, connection management, and monitoring techniques that ensure optimal performance under varying load conditions.

## Query Performance Analysis

### Query Execution Plan Analysis

**PostgreSQL Query Analysis:**
```sql
-- Comprehensive query analysis with timing and resource usage
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, WAL, SETTINGS) 
SELECT 
    c.customer_id,
    c.email,
    c.first_name || ' ' || c.last_name AS full_name,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value,
    MAX(o.created_at) AS last_order_date,
    EXTRACT(DAYS FROM (CURRENT_DATE - MAX(o.created_at))) AS days_since_last_order
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id 
    AND o.order_status IN ('completed', 'shipped')
    AND o.created_at >= CURRENT_DATE - INTERVAL '1 year'
WHERE c.is_active = true
    AND c.created_at >= '2023-01-01'
GROUP BY c.customer_id, c.email, c.first_name, c.last_name
HAVING COUNT(o.order_id) >= 3
ORDER BY total_revenue DESC NULLS LAST, order_count DESC
LIMIT 1000;

-- Query optimization analysis function
CREATE OR REPLACE FUNCTION analyze_query_performance(query_text TEXT)
RETURNS TABLE (
    execution_time_ms NUMERIC,
    planning_time_ms NUMERIC,
    shared_buffers_hit BIGINT,
    shared_buffers_read BIGINT,
    temp_buffers_read BIGINT,
    rows_examined BIGINT,
    rows_returned BIGINT
) AS $$
DECLARE
    plan_result JSONB;
    execution_stats RECORD;
BEGIN
    -- Execute query with detailed analysis
    EXECUTE 'EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) ' || query_text INTO plan_result;
    
    -- Extract performance metrics from execution plan
    SELECT 
        (plan_result->0->'Execution Time')::NUMERIC,
        (plan_result->0->'Planning Time')::NUMERIC,
        COALESCE((plan_result->0->'Shared Hit Blocks')::BIGINT, 0),
        COALESCE((plan_result->0->'Shared Read Blocks')::BIGINT, 0),
        COALESCE((plan_result->0->'Temp Read Blocks')::BIGINT, 0),
        (plan_result->0->'Plan'->'Actual Rows')::BIGINT,
        (plan_result->0->'Plan'->'Plan Rows')::BIGINT
    INTO execution_stats;
    
    RETURN QUERY SELECT 
        execution_stats.execution_time_ms,
        execution_stats.planning_time_ms,
        execution_stats.shared_buffers_hit,
        execution_stats.shared_buffers_read,
        execution_stats.temp_buffers_read,
        execution_stats.rows_examined,
        execution_stats.rows_returned;
END;
$$ LANGUAGE plpgsql;
```

**MySQL Query Performance Analysis:**
```sql
-- MySQL query performance analysis with profiling
SET profiling = 1;

SELECT 
    c.customer_id,
    c.email,
    CONCAT(c.first_name, ' ', c.last_name) AS full_name,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id 
    AND o.order_status IN ('completed', 'shipped')
    AND o.created_at >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
WHERE c.is_active = 1
GROUP BY c.customer_id, c.email, c.first_name, c.last_name
HAVING COUNT(o.order_id) >= 3
ORDER BY total_revenue DESC
LIMIT 1000;

-- Analyze query performance
SHOW PROFILE FOR QUERY 1;
SHOW PROFILE CPU, MEMORY, SWAPS FOR QUERY 1;

-- Query execution plan analysis
EXPLAIN FORMAT=JSON
SELECT /* ... query ... */;
```

### Query Optimization Techniques

**Optimized Query Patterns:**
```sql
-- Subquery optimization using EXISTS instead of IN
-- Inefficient version
SELECT * FROM customers c
WHERE c.customer_id IN (
    SELECT DISTINCT o.customer_id 
    FROM orders o 
    WHERE o.order_status = 'completed'
    AND o.created_at >= '2024-01-01'
);

-- Optimized version using EXISTS
SELECT * FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id 
    AND o.order_status = 'completed'
    AND o.created_at >= '2024-01-01'
);

-- Window function optimization for ranking
-- Efficient pagination with window functions
SELECT 
    customer_id,
    email,
    order_count,
    total_revenue,
    revenue_rank
FROM (
    SELECT 
        c.customer_id,
        c.email,
        COUNT(o.order_id) AS order_count,
        SUM(o.total_amount) AS total_revenue,
        ROW_NUMBER() OVER (ORDER BY SUM(o.total_amount) DESC) AS revenue_rank
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.is_active = true
    GROUP BY c.customer_id, c.email
) ranked_customers
WHERE revenue_rank BETWEEN 101 AND 200;

-- Efficient bulk operations using CASE statements
UPDATE products 
SET 
    price = CASE 
        WHEN category_id = 1 THEN price * 1.10  -- Electronics +10%
        WHEN category_id = 2 THEN price * 1.05  -- Books +5%
        WHEN category_id = 3 THEN price * 1.15  -- Clothing +15%
        ELSE price
    END,
    updated_at = CURRENT_TIMESTAMP
WHERE category_id IN (1, 2, 3) AND is_active = true;
```

**Advanced Optimization Strategies:**
```python
class QueryOptimizer:
    def __init__(self, db_connection):
        self.db = db_connection
        self.query_cache = {}
        self.execution_stats = {}
    
    def optimize_pagination_query(self, base_query, page_size, offset):
        """
        Optimize pagination using cursor-based pagination for better performance
        """
        # Use cursor-based pagination instead of OFFSET
        cursor_query = f"""
        WITH ordered_results AS ({base_query})
        SELECT * FROM ordered_results
        WHERE id > %(cursor_id)s
        ORDER BY id
        LIMIT %(limit)s
        """
        
        return cursor_query
    
    def batch_insert_optimization(self, table_name, records, batch_size=1000):
        """
        Optimized batch insert with transaction management
        """
        total_records = len(records)
        
        try:
            self.db.begin()
            
            for i in range(0, total_records, batch_size):
                batch = records[i:i + batch_size]
                
                # Use prepared statements for better performance
                placeholders = ', '.join(['%s'] * len(batch))
                query = f"""
                INSERT INTO {table_name} 
                VALUES {placeholders}
                ON CONFLICT (unique_column) DO UPDATE SET
                updated_at = CURRENT_TIMESTAMP
                """
                
                self.db.execute(query, batch)
                
                # Commit in batches to avoid long transactions
                if i % (batch_size * 10) == 0:
                    self.db.commit()
                    self.db.begin()
            
            self.db.commit()
            
        except Exception as e:
            self.db.rollback()
            raise e
    
    def generate_query_statistics(self, query_id, execution_time, rows_affected):
        """
        Track query performance statistics for optimization analysis
        """
        if query_id not in self.execution_stats:
            self.execution_stats[query_id] = {
                'executions': 0,
                'total_time': 0,
                'avg_time': 0,
                'max_time': 0,
                'min_time': float('inf')
            }
        
        stats = self.execution_stats[query_id]
        stats['executions'] += 1
        stats['total_time'] += execution_time
        stats['avg_time'] = stats['total_time'] / stats['executions']
        stats['max_time'] = max(stats['max_time'], execution_time)
        stats['min_time'] = min(stats['min_time'], execution_time)
        
        # Alert on performance degradation
        if execution_time > stats['avg_time'] * 2:
            self.alert_performance_degradation(query_id, execution_time, stats['avg_time'])
```

## Index Optimization

### Strategic Indexing

**Index Design Patterns:**
```sql
-- Multi-column index ordering by selectivity
-- High to low selectivity ordering
CREATE INDEX idx_orders_status_date_customer ON orders(
    order_status,     -- High selectivity (few distinct values)
    created_at DESC,  -- Medium selectivity (time-based)
    customer_id       -- High selectivity (many distinct values)
);

-- Covering indexes to avoid table lookups
CREATE INDEX idx_products_category_covering ON products(
    category_id, 
    is_active
) INCLUDE (
    name, 
    price, 
    description
) WHERE is_active = true;

-- Functional indexes for computed values
CREATE INDEX idx_customers_search_name ON customers(
    LOWER(first_name || ' ' || last_name)
);

-- Partial indexes for specific conditions
CREATE INDEX idx_orders_recent_active ON orders(
    customer_id, 
    created_at DESC
) WHERE 
    order_status IN ('pending', 'processing')
    AND created_at >= CURRENT_DATE - INTERVAL '30 days';
```

**Index Monitoring and Maintenance:**
```sql
-- Index usage analysis
CREATE OR REPLACE VIEW index_usage_stats AS
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    ROUND(
        100.0 * idx_scan / GREATEST(
            (SELECT SUM(idx_scan + seq_scan) FROM pg_stat_user_tables WHERE relname = tablename), 
            1
        ), 2
    ) AS index_usage_pct
FROM pg_stat_user_indexes 
ORDER BY pg_relation_size(indexrelid) DESC;

-- Duplicate index detection
WITH index_columns AS (
    SELECT 
        schemaname,
        tablename,
        indexname,
        array_agg(attname ORDER BY attnum) as columns
    FROM pg_indexes 
    JOIN pg_index ON pg_indexes.indexname = pg_class.relname
    JOIN pg_attribute ON pg_attribute.attrelid = pg_index.indrelid 
        AND pg_attribute.attnum = ANY(pg_index.indkey)
    JOIN pg_class ON pg_class.oid = pg_index.indexrelid
    WHERE schemaname = 'public'
    GROUP BY schemaname, tablename, indexname
)
SELECT 
    i1.schemaname,
    i1.tablename,
    i1.indexname as index1,
    i2.indexname as index2,
    i1.columns
FROM index_columns i1
JOIN index_columns i2 ON i1.tablename = i2.tablename 
    AND i1.columns = i2.columns 
    AND i1.indexname < i2.indexname;
```

### NoSQL Indexing Optimization

**MongoDB Index Strategies:**
```javascript
// Compound index optimization for query patterns
db.orders.createIndex(
  { customerId: 1, status: 1, createdAt: -1 },
  { 
    name: "idx_orders_customer_status_date",
    partialFilterExpression: { 
      status: { $in: ["pending", "processing", "completed"] }
    }
  }
);

// Text index with weights for search relevance
db.products.createIndex(
  {
    name: "text",
    description: "text",
    "category.name": "text"
  },
  {
    name: "idx_product_search",
    weights: {
      name: 10,
      "category.name": 5,
      description: 1
    },
    default_language: "english",
    language_override: "language"
  }
);

// Geospatial index for location queries
db.stores.createIndex(
  { location: "2dsphere" },
  {
    name: "idx_store_location",
    "2dsphereIndexVersion": 3
  }
);

// Wildcard index for dynamic schemas
db.products.createIndex(
  { "attributes.$**": 1 },
  { name: "idx_product_attributes_wildcard" }
);

// Index usage analysis
db.runCommand({
  aggregate: "orders",
  pipeline: [
    { $indexStats: {} }
  ]
});
```

## Connection Optimization

### Connection Pooling Strategies

**PostgreSQL Connection Pooling:**
```python
import psycopg2
from psycopg2 import pool
import threading
import time

class OptimizedConnectionPool:
    def __init__(self, connection_config, min_connections=5, max_connections=20):
        self.config = connection_config
        self.min_connections = min_connections
        self.max_connections = max_connections
        
        # Create connection pool
        self.pool = psycopg2.pool.ThreadedConnectionPool(
            minconn=min_connections,
            maxconn=max_connections,
            **connection_config
        )
        
        self.connection_stats = {
            'active_connections': 0,
            'total_connections_created': 0,
            'connection_errors': 0,
            'avg_connection_time': 0
        }
        
        self.lock = threading.Lock()
    
    def get_connection(self, timeout=30):
        start_time = time.time()
        
        try:
            connection = self.pool.getconn()
            
            if connection:
                with self.lock:
                    self.connection_stats['active_connections'] += 1
                    self.connection_stats['total_connections_created'] += 1
                    
                    # Update average connection time
                    connection_time = time.time() - start_time
                    self.connection_stats['avg_connection_time'] = (
                        (self.connection_stats['avg_connection_time'] * 
                         (self.connection_stats['total_connections_created'] - 1) +
                         connection_time) / 
                        self.connection_stats['total_connections_created']
                    )
                
                return ConnectionWrapper(connection, self)
            
        except psycopg2.pool.PoolError as e:
            with self.lock:
                self.connection_stats['connection_errors'] += 1
            
            raise ConnectionPoolExhausted(f"Connection pool exhausted: {str(e)}")
    
    def return_connection(self, connection):
        try:
            self.pool.putconn(connection)
            
            with self.lock:
                self.connection_stats['active_connections'] -= 1
                
        except Exception as e:
            # Log error but don't raise to avoid cascading failures
            logger.error(f"Error returning connection to pool: {str(e)}")
    
    def get_pool_status(self):
        return {
            'active_connections': self.connection_stats['active_connections'],
            'total_created': self.connection_stats['total_connections_created'],
            'errors': self.connection_stats['connection_errors'],
            'avg_connection_time': self.connection_stats['avg_connection_time'],
            'pool_size': len(self.pool._pool),
            'available_connections': len(self.pool._pool) - self.connection_stats['active_connections']
        }

class ConnectionWrapper:
    def __init__(self, connection, pool):
        self.connection = connection
        self.pool = pool
        self.start_time = time.time()
    
    def __enter__(self):
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Log long-running connections
        connection_duration = time.time() - self.start_time
        if connection_duration > 300:  # 5 minutes
            logger.warning(f"Long-running connection detected: {connection_duration:.2f}s")
        
        self.pool.return_connection(self.connection)
    
    def execute(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
```

### Read Replica Configuration

**Multi-Database Connection Management:**
```python
class ReadWriteConnectionManager:
    def __init__(self, write_config, read_configs):
        self.write_pool = OptimizedConnectionPool(write_config, min_connections=5, max_connections=15)
        self.read_pools = [
            OptimizedConnectionPool(config, min_connections=3, max_connections=10)
            for config in read_configs
        ]
        self.read_pool_index = 0
        self.read_pool_lock = threading.Lock()
        
        # Health checking for read replicas
        self.replica_health = [True] * len(self.read_pools)
        self.start_health_monitoring()
    
    def get_write_connection(self):
        return self.write_pool.get_connection()
    
    def get_read_connection(self):
        # Round-robin load balancing across healthy read replicas
        healthy_pools = [
            (i, pool) for i, pool in enumerate(self.read_pools)
            if self.replica_health[i]
        ]
        
        if not healthy_pools:
            # Fallback to write connection if no read replicas available
            logger.warning("No healthy read replicas available, using write connection")
            return self.write_pool.get_connection()
        
        with self.read_pool_lock:
            pool_index = self.read_pool_index % len(healthy_pools)
            self.read_pool_index += 1
        
        selected_pool_index, selected_pool = healthy_pools[pool_index]
        return selected_pool.get_connection()
    
    def start_health_monitoring(self):
        def monitor_replica_health():
            while True:
                for i, pool in enumerate(self.read_pools):
                    try:
                        with pool.get_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT 1")
                            cursor.fetchone()
                        
                        self.replica_health[i] = True
                        
                    except Exception as e:
                        logger.error(f"Read replica {i} health check failed: {str(e)}")
                        self.replica_health[i] = False
                
                time.sleep(30)  # Check every 30 seconds
        
        health_thread = threading.Thread(target=monitor_replica_health, daemon=True)
        health_thread.start()
```

## Monitoring and Performance Metrics

### Real-time Performance Monitoring

**Database Performance Dashboard:**
```python
class DatabasePerformanceMonitor:
    def __init__(self, db_connections):
        self.connections = db_connections
        self.metrics_collector = MetricsCollector()
        self.alerting_system = AlertingSystem()
        self.performance_history = {}
    
    def collect_performance_metrics(self):
        metrics = {}
        
        # Connection pool metrics
        for db_name, connection_pool in self.connections.items():
            pool_stats = connection_pool.get_pool_status()
            metrics[f"{db_name}_pool"] = pool_stats
            
            # Alert on connection pool exhaustion
            if pool_stats['available_connections'] < 2:
                self.alerting_system.send_alert(
                    f"Connection pool nearly exhausted for {db_name}",
                    severity="HIGH"
                )
        
        # Database-specific metrics
        for db_name, connection_pool in self.connections.items():
            with connection_pool.get_connection() as conn:
                db_metrics = self.collect_database_metrics(conn, db_name)
                metrics[f"{db_name}_db"] = db_metrics
        
        # Store metrics for trend analysis
        timestamp = time.time()
        self.performance_history[timestamp] = metrics
        
        # Clean old metrics (keep last 24 hours)
        cutoff_time = timestamp - 86400
        self.performance_history = {
            t: m for t, m in self.performance_history.items() 
            if t > cutoff_time
        }
        
        return metrics
    
    def collect_database_metrics(self, connection, db_name):
        cursor = connection.cursor()
        
        # PostgreSQL-specific metrics
        if db_name.startswith('postgres'):
            metrics = {}
            
            # Active connections
            cursor.execute("""
                SELECT count(*) as active_connections
                FROM pg_stat_activity 
                WHERE state = 'active'
            """)
            metrics['active_connections'] = cursor.fetchone()[0]
            
            # Long-running queries
            cursor.execute("""
                SELECT count(*) as long_queries
                FROM pg_stat_activity 
                WHERE state = 'active' 
                AND now() - query_start > interval '5 minutes'
            """)
            metrics['long_running_queries'] = cursor.fetchone()[0]
            
            # Cache hit ratio
            cursor.execute("""
                SELECT 
                    round(
                        100.0 * sum(blks_hit) / (sum(blks_hit) + sum(blks_read)), 2
                    ) as cache_hit_ratio
                FROM pg_stat_database
            """)
            result = cursor.fetchone()
            metrics['cache_hit_ratio'] = result[0] if result[0] else 0
            
            # Table and index sizes
            cursor.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
                LIMIT 10
            """)
            metrics['largest_tables'] = cursor.fetchall()
            
            return metrics
        
        cursor.close()
        return {}
    
    def analyze_performance_trends(self):
        if len(self.performance_history) < 10:
            return {}
        
        # Analyze trends over time
        timestamps = sorted(self.performance_history.keys())
        
        trends = {}
        for metric_category in ['pool', 'db']:
            category_trends = {}
            
            # Analyze key metrics
            for key_metric in ['active_connections', 'cache_hit_ratio', 'long_running_queries']:
                values = []
                for ts in timestamps:
                    for db_key, metrics in self.performance_history[ts].items():
                        if metric_category in db_key and key_metric in metrics:
                            values.append(metrics[key_metric])
                
                if len(values) > 5:
                    # Calculate trend (simple linear regression slope)
                    n = len(values)
                    x_sum = sum(range(n))
                    y_sum = sum(values)
                    xy_sum = sum(i * values[i] for i in range(n))
                    x2_sum = sum(i * i for i in range(n))
                    
                    slope = (n * xy_sum - x_sum * y_sum) / (n * x2_sum - x_sum * x_sum)
                    category_trends[key_metric] = {
                        'trend_slope': slope,
                        'current_value': values[-1],
                        'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
                    }
            
            trends[metric_category] = category_trends
        
        return trends
```

This comprehensive performance optimization framework provides systematic approaches to query optimization, indexing strategies, connection management, and monitoring that ensure optimal database performance under varying load conditions.