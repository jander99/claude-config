# Database Migrations and Version Control

## Overview

Database migrations provide systematic version control for database schema changes, enabling safe, reproducible, and reversible database evolution across development, staging, and production environments while maintaining data integrity and minimizing downtime.

## Migration Strategy and Planning

### Migration Design Principles

**Safe Migration Patterns:**
```python
class MigrationPlanningFramework:
    def __init__(self):
        self.migration_types = {
            'SAFE': 'No data loss or downtime risk',
            'CAUTION': 'Potential performance impact during migration',
            'DANGEROUS': 'Potential data loss or extended downtime'
        }
        self.rollback_strategies = {}
        self.impact_assessment = {}
    
    def assess_migration_impact(self, migration_plan):
        """
        Analyze migration for potential risks and impacts
        """
        impact_analysis = {
            'risk_level': 'SAFE',
            'estimated_downtime': 0,
            'data_loss_risk': False,
            'performance_impact': 'LOW',
            'rollback_complexity': 'SIMPLE',
            'dependencies': [],
            'prerequisites': []
        }
        
        # Analyze each migration operation
        for operation in migration_plan['operations']:
            operation_risk = self.analyze_operation_risk(operation)
            
            # Escalate overall risk to highest individual risk
            if operation_risk['risk_level'] == 'DANGEROUS':
                impact_analysis['risk_level'] = 'DANGEROUS'
            elif operation_risk['risk_level'] == 'CAUTION' and impact_analysis['risk_level'] == 'SAFE':
                impact_analysis['risk_level'] = 'CAUTION'
            
            # Accumulate downtime estimates
            impact_analysis['estimated_downtime'] += operation_risk['downtime_estimate']
            
            # Flag data loss risks
            if operation_risk['data_loss_risk']:
                impact_analysis['data_loss_risk'] = True
        
        return impact_analysis
    
    def analyze_operation_risk(self, operation):
        """
        Assess individual migration operation risks
        """
        risk_profiles = {
            'ADD_COLUMN_NULLABLE': {
                'risk_level': 'SAFE',
                'downtime_estimate': 0,
                'data_loss_risk': False,
                'performance_impact': 'LOW'
            },
            'ADD_COLUMN_NOT_NULL': {
                'risk_level': 'CAUTION',
                'downtime_estimate': 5,  # seconds
                'data_loss_risk': False,
                'performance_impact': 'MEDIUM'
            },
            'DROP_COLUMN': {
                'risk_level': 'DANGEROUS',
                'downtime_estimate': 0,
                'data_loss_risk': True,
                'performance_impact': 'LOW'
            },
            'ALTER_COLUMN_TYPE': {
                'risk_level': 'DANGEROUS',
                'downtime_estimate': 300,  # 5 minutes estimated
                'data_loss_risk': True,
                'performance_impact': 'HIGH'
            },
            'CREATE_INDEX': {
                'risk_level': 'CAUTION',
                'downtime_estimate': 0,  # Can be done online
                'data_loss_risk': False,
                'performance_impact': 'MEDIUM'
            },
            'DROP_INDEX': {
                'risk_level': 'SAFE',
                'downtime_estimate': 0,
                'data_loss_risk': False,
                'performance_impact': 'LOW'
            }
        }
        
        return risk_profiles.get(operation['type'], {
            'risk_level': 'DANGEROUS',
            'downtime_estimate': 60,
            'data_loss_risk': True,
            'performance_impact': 'HIGH'
        })
    
    def generate_safe_migration_plan(self, target_changes):
        """
        Generate a safe migration plan that minimizes risk
        """
        safe_plan = {
            'phases': [],
            'rollback_plan': [],
            'validation_steps': [],
            'deployment_strategy': 'blue_green'
        }
        
        # Phase 1: Additive changes (safe)
        additive_changes = [
            change for change in target_changes 
            if change['type'] in ['ADD_COLUMN_NULLABLE', 'CREATE_INDEX', 'ADD_TABLE']
        ]
        
        if additive_changes:
            safe_plan['phases'].append({
                'name': 'additive_changes',
                'operations': additive_changes,
                'rollback_strategy': 'simple_reverse',
                'validation': 'schema_verification'
            })
        
        # Phase 2: Data transformations (caution)
        transformation_changes = [
            change for change in target_changes
            if change['type'] in ['DATA_MIGRATION', 'UPDATE_VALUES']
        ]
        
        if transformation_changes:
            safe_plan['phases'].append({
                'name': 'data_transformations',
                'operations': transformation_changes,
                'rollback_strategy': 'data_backup_restore',
                'validation': 'data_integrity_check'
            })
        
        # Phase 3: Destructive changes (dangerous - separate deployment)
        destructive_changes = [
            change for change in target_changes
            if change['type'] in ['DROP_COLUMN', 'DROP_TABLE', 'ALTER_COLUMN_TYPE']
        ]
        
        if destructive_changes:
            safe_plan['phases'].append({
                'name': 'destructive_changes',
                'operations': destructive_changes,
                'rollback_strategy': 'full_database_restore',
                'validation': 'comprehensive_testing',
                'requires_maintenance_window': True
            })
        
        return safe_plan
```

### Zero-Downtime Migration Strategies

**Progressive Migration Patterns:**
```sql
-- Example: Adding a NOT NULL column with default value
-- Phase 1: Add nullable column with default
ALTER TABLE customers 
ADD COLUMN customer_tier VARCHAR(20) DEFAULT 'standard';

-- Phase 2: Backfill existing data (can be done in batches)
DO $$
DECLARE
    batch_size INTEGER := 1000;
    processed INTEGER := 0;
    total_rows INTEGER;
BEGIN
    SELECT COUNT(*) INTO total_rows FROM customers WHERE customer_tier IS NULL;
    
    WHILE processed < total_rows LOOP
        UPDATE customers 
        SET customer_tier = CASE 
            WHEN (SELECT SUM(total_amount) FROM orders WHERE orders.customer_id = customers.customer_id) > 10000 THEN 'premium'
            WHEN (SELECT SUM(total_amount) FROM orders WHERE orders.customer_id = customers.customer_id) > 1000 THEN 'gold'
            ELSE 'standard'
        END
        WHERE customer_id IN (
            SELECT customer_id FROM customers 
            WHERE customer_tier IS NULL 
            LIMIT batch_size
        );
        
        processed := processed + batch_size;
        
        -- Commit in batches to avoid long transactions
        COMMIT;
        
        -- Brief pause to reduce load
        PERFORM pg_sleep(0.1);
    END LOOP;
END $$;

-- Phase 3: Add NOT NULL constraint (after all data is populated)
ALTER TABLE customers 
ALTER COLUMN customer_tier SET NOT NULL;

-- Phase 4: Add check constraint for valid values
ALTER TABLE customers 
ADD CONSTRAINT customer_tier_check 
CHECK (customer_tier IN ('standard', 'gold', 'premium'));
```

**Blue-Green Deployment Migration:**
```python
class BlueGreenMigrationManager:
    def __init__(self, blue_db_config, green_db_config):
        self.blue_db = DatabaseConnection(blue_db_config)
        self.green_db = DatabaseConnection(green_db_config)
        self.migration_state = 'blue_active'
        self.sync_manager = DatabaseSyncManager()
    
    def execute_blue_green_migration(self, migration_scripts):
        """
        Execute migration using blue-green strategy
        """
        try:
            # Step 1: Ensure green database is in sync with blue
            self.sync_databases()
            
            # Step 2: Apply migrations to green database
            self.apply_migrations_to_green(migration_scripts)
            
            # Step 3: Validate green database
            validation_results = self.validate_green_database()
            if not validation_results['success']:
                raise MigrationValidationError(validation_results['errors'])
            
            # Step 4: Perform final sync (minimal downtime)
            self.perform_final_sync()
            
            # Step 5: Switch traffic to green
            self.switch_to_green()
            
            # Step 6: Monitor for issues
            self.monitor_post_migration()
            
            return {'success': True, 'migration_completed': True}
            
        except Exception as e:
            # Rollback to blue if any issues
            self.rollback_to_blue()
            raise MigrationError(f"Blue-green migration failed: {str(e)}")
    
    def sync_databases(self):
        """
        Synchronize green database with blue database
        """
        # Use logical replication or dump/restore
        sync_start_time = time.time()
        
        # Create replication slot on blue database
        with self.blue_db.get_connection() as blue_conn:
            blue_conn.execute("""
                SELECT pg_create_logical_replication_slot(
                    'migration_sync_slot', 
                    'pgoutput'
                );
            """)
        
        # Set up subscription on green database
        with self.green_db.get_connection() as green_conn:
            green_conn.execute(f"""
                CREATE SUBSCRIPTION migration_sync
                CONNECTION '{self.blue_db.get_connection_string()}'
                PUBLICATION migration_publication
                WITH (copy_data = true, create_slot = false, slot_name = 'migration_sync_slot');
            """)
        
        # Wait for initial sync to complete
        self.wait_for_sync_completion()
        
        sync_duration = time.time() - sync_start_time
        logger.info(f"Database sync completed in {sync_duration:.2f} seconds")
    
    def apply_migrations_to_green(self, migration_scripts):
        """
        Apply migration scripts to green database
        """
        with self.green_db.get_connection() as conn:
            for script in migration_scripts:
                try:
                    conn.execute(script['sql'])
                    self.log_migration_applied(script['version'], 'green')
                except Exception as e:
                    raise MigrationError(f"Failed to apply migration {script['version']}: {str(e)}")
    
    def validate_green_database(self):
        """
        Comprehensive validation of green database after migration
        """
        validation_results = {
            'success': True,
            'errors': [],
            'warnings': [],
            'performance_metrics': {}
        }
        
        # Schema validation
        schema_diff = self.compare_schemas(self.blue_db, self.green_db)
        if schema_diff:
            validation_results['warnings'].append(f"Schema differences detected: {schema_diff}")
        
        # Data validation
        data_validation = self.validate_data_integrity()
        if not data_validation['success']:
            validation_results['success'] = False
            validation_results['errors'].extend(data_validation['errors'])
        
        # Performance validation
        performance_results = self.run_performance_tests()
        validation_results['performance_metrics'] = performance_results
        
        if performance_results['response_time_degradation'] > 20:  # 20% threshold
            validation_results['success'] = False
            validation_results['errors'].append(
                f"Performance degradation exceeds threshold: {performance_results['response_time_degradation']}%"
            )
        
        return validation_results
```

## Migration Implementation

### Forward Migration Scripts

**Comprehensive Migration Script Structure:**
```sql
-- Migration: 20240301_001_add_customer_loyalty_program.sql
-- Description: Add loyalty program features to customer management
-- Author: database-engineer
-- Risk Level: CAUTION (adds new functionality, minimal data risk)

BEGIN;

-- Set migration metadata
INSERT INTO schema_migrations (
    version, 
    description, 
    applied_at, 
    applied_by,
    risk_level
) VALUES (
    '20240301_001',
    'Add customer loyalty program features',
    CURRENT_TIMESTAMP,
    USER,
    'CAUTION'
);

-- Create loyalty tiers lookup table
CREATE TABLE loyalty_tiers (
    tier_id SERIAL PRIMARY KEY,
    tier_name VARCHAR(50) UNIQUE NOT NULL,
    tier_code VARCHAR(20) UNIQUE NOT NULL,
    min_points INTEGER NOT NULL DEFAULT 0,
    max_points INTEGER,
    benefits JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT loyalty_tier_points_check CHECK (
        max_points IS NULL OR max_points > min_points
    )
);

-- Insert default loyalty tiers
INSERT INTO loyalty_tiers (tier_name, tier_code, min_points, max_points, benefits) VALUES
('Bronze', 'BRONZE', 0, 999, '{"discount_percentage": 5, "free_shipping": false}'),
('Silver', 'SILVER', 1000, 4999, '{"discount_percentage": 10, "free_shipping": true, "early_access": true}'),
('Gold', 'GOLD', 5000, 19999, '{"discount_percentage": 15, "free_shipping": true, "early_access": true, "priority_support": true}'),
('Platinum', 'PLATINUM', 20000, NULL, '{"discount_percentage": 20, "free_shipping": true, "early_access": true, "priority_support": true, "personal_shopper": true}');

-- Add loyalty program columns to customers table
ALTER TABLE customers 
ADD COLUMN loyalty_points INTEGER DEFAULT 0 CHECK (loyalty_points >= 0),
ADD COLUMN loyalty_tier_id INTEGER REFERENCES loyalty_tiers(tier_id) DEFAULT 1,
ADD COLUMN loyalty_joined_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN loyalty_last_activity TIMESTAMP WITH TIME ZONE;

-- Create loyalty transactions table for point tracking
CREATE TABLE loyalty_transactions (
    transaction_id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    transaction_type VARCHAR(20) NOT NULL CHECK (
        transaction_type IN ('EARNED', 'REDEEMED', 'EXPIRED', 'ADJUSTED')
    ),
    points INTEGER NOT NULL,
    description TEXT NOT NULL,
    reference_id BIGINT, -- Links to orders, returns, etc.
    reference_type VARCHAR(20), -- 'order', 'return', 'manual', etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100) DEFAULT USER,
    
    -- Ensure points are appropriate for transaction type
    CONSTRAINT loyalty_points_sign_check CHECK (
        (transaction_type IN ('EARNED', 'ADJUSTED') AND points != 0) OR
        (transaction_type IN ('REDEEMED', 'EXPIRED') AND points <= 0)
    )
);

-- Create indexes for performance
CREATE INDEX idx_customers_loyalty_tier ON customers(loyalty_tier_id);
CREATE INDEX idx_customers_loyalty_points ON customers(loyalty_points DESC);
CREATE INDEX idx_loyalty_transactions_customer_date ON loyalty_transactions(customer_id, created_at DESC);
CREATE INDEX idx_loyalty_transactions_reference ON loyalty_transactions(reference_type, reference_id);

-- Create function to update customer loyalty tier based on points
CREATE OR REPLACE FUNCTION update_customer_loyalty_tier(p_customer_id BIGINT)
RETURNS VOID AS $$
DECLARE
    current_points INTEGER;
    new_tier_id INTEGER;
BEGIN
    -- Get current points for customer
    SELECT loyalty_points INTO current_points
    FROM customers
    WHERE customer_id = p_customer_id;
    
    -- Determine appropriate tier
    SELECT tier_id INTO new_tier_id
    FROM loyalty_tiers
    WHERE min_points <= current_points
    AND (max_points IS NULL OR current_points <= max_points)
    ORDER BY min_points DESC
    LIMIT 1;
    
    -- Update customer tier if changed
    UPDATE customers
    SET 
        loyalty_tier_id = new_tier_id,
        loyalty_last_activity = CURRENT_TIMESTAMP
    WHERE customer_id = p_customer_id
    AND loyalty_tier_id != new_tier_id;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to update loyalty points and tier when loyalty transactions are added
CREATE OR REPLACE FUNCTION process_loyalty_transaction()
RETURNS TRIGGER AS $$
BEGIN
    -- Update customer's total points
    UPDATE customers 
    SET loyalty_points = loyalty_points + NEW.points
    WHERE customer_id = NEW.customer_id;
    
    -- Update customer's loyalty tier
    PERFORM update_customer_loyalty_tier(NEW.customer_id);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER loyalty_transaction_trigger
    AFTER INSERT ON loyalty_transactions
    FOR EACH ROW EXECUTE FUNCTION process_loyalty_transaction();

-- Backfill existing customers with default loyalty tier
UPDATE customers 
SET 
    loyalty_tier_id = 1, -- Bronze tier
    loyalty_joined_date = created_at
WHERE loyalty_tier_id IS NULL;

-- Create view for customer loyalty summary
CREATE VIEW customer_loyalty_summary AS
SELECT 
    c.customer_id,
    c.email,
    c.first_name,
    c.last_name,
    c.loyalty_points,
    lt.tier_name,
    lt.tier_code,
    lt.benefits,
    c.loyalty_joined_date,
    c.loyalty_last_activity,
    COALESCE(stats.total_earned, 0) as total_points_earned,
    COALESCE(stats.total_redeemed, 0) as total_points_redeemed
FROM customers c
JOIN loyalty_tiers lt ON c.loyalty_tier_id = lt.tier_id
LEFT JOIN (
    SELECT 
        customer_id,
        SUM(CASE WHEN points > 0 THEN points ELSE 0 END) as total_earned,
        SUM(CASE WHEN points < 0 THEN ABS(points) ELSE 0 END) as total_redeemed
    FROM loyalty_transactions
    GROUP BY customer_id
) stats ON c.customer_id = stats.customer_id;

-- Add comments for documentation
COMMENT ON TABLE loyalty_tiers IS 'Defines customer loyalty program tiers and their benefits';
COMMENT ON TABLE loyalty_transactions IS 'Tracks all loyalty point transactions for customers';
COMMENT ON COLUMN customers.loyalty_points IS 'Current loyalty points balance for customer';
COMMENT ON COLUMN customers.loyalty_tier_id IS 'Current loyalty tier based on points balance';

COMMIT;

-- Post-migration validation
DO $$
DECLARE
    tier_count INTEGER;
    customer_count INTEGER;
    transaction_count INTEGER;
BEGIN
    -- Validate loyalty tiers were created
    SELECT COUNT(*) INTO tier_count FROM loyalty_tiers;
    IF tier_count != 4 THEN
        RAISE EXCEPTION 'Migration validation failed: Expected 4 loyalty tiers, found %', tier_count;
    END IF;
    
    -- Validate all customers have loyalty tier assigned
    SELECT COUNT(*) INTO customer_count 
    FROM customers 
    WHERE loyalty_tier_id IS NULL OR loyalty_points IS NULL;
    
    IF customer_count > 0 THEN
        RAISE EXCEPTION 'Migration validation failed: % customers without loyalty data', customer_count;
    END IF;
    
    RAISE NOTICE 'Migration 20240301_001 validation passed: % loyalty tiers, % customers updated', 
        tier_count, (SELECT COUNT(*) FROM customers);
END $$;
```

### Rollback Procedures

**Comprehensive Rollback Strategy:**
```sql
-- Rollback: 20240301_001_add_customer_loyalty_program_rollback.sql
-- Description: Rollback loyalty program features migration
-- Risk Level: DANGEROUS (drops tables and data)

BEGIN;

-- Validate rollback preconditions
DO $$
DECLARE
    active_transactions INTEGER;
BEGIN
    -- Check for recent loyalty transactions that would be lost
    SELECT COUNT(*) INTO active_transactions
    FROM loyalty_transactions
    WHERE created_at > CURRENT_TIMESTAMP - INTERVAL '24 hours';
    
    IF active_transactions > 0 THEN
        RAISE EXCEPTION 'Cannot rollback: % recent loyalty transactions would be lost. Manual data preservation required.', active_transactions;
    END IF;
END $$;

-- Drop triggers and functions first
DROP TRIGGER IF EXISTS loyalty_transaction_trigger ON loyalty_transactions;
DROP FUNCTION IF EXISTS process_loyalty_transaction();
DROP FUNCTION IF EXISTS update_customer_loyalty_tier(BIGINT);

-- Drop views
DROP VIEW IF EXISTS customer_loyalty_summary;

-- Remove loyalty columns from customers table
ALTER TABLE customers 
DROP COLUMN IF EXISTS loyalty_points,
DROP COLUMN IF EXISTS loyalty_tier_id,
DROP COLUMN IF EXISTS loyalty_joined_date,
DROP COLUMN IF EXISTS loyalty_last_activity;

-- Drop loyalty tables (in reverse dependency order)
DROP TABLE IF EXISTS loyalty_transactions;
DROP TABLE IF EXISTS loyalty_tiers;

-- Remove migration record
DELETE FROM schema_migrations WHERE version = '20240301_001';

-- Validate rollback completion
DO $$
DECLARE
    loyalty_tables INTEGER;
BEGIN
    SELECT COUNT(*) INTO loyalty_tables
    FROM information_schema.tables
    WHERE table_name IN ('loyalty_tiers', 'loyalty_transactions')
    AND table_schema = 'public';
    
    IF loyalty_tables > 0 THEN
        RAISE EXCEPTION 'Rollback validation failed: Loyalty tables still exist';
    END IF;
    
    RAISE NOTICE 'Rollback 20240301_001 completed successfully';
END $$;

COMMIT;
```

### Data Migration Patterns

**Safe Data Transformation:**
```python
class DataMigrationManager:
    def __init__(self, db_connection):
        self.db = db_connection
        self.batch_size = 1000
        self.max_retry_attempts = 3
        
    def migrate_customer_data_with_validation(self):
        """
        Migrate customer data with comprehensive validation and rollback capability
        """
        migration_id = self.start_migration_tracking('customer_data_normalization')
        
        try:
            # Phase 1: Create backup table
            self.create_backup_table('customers', 'customers_backup_20240301')
            
            # Phase 2: Add new normalized columns
            self.add_migration_columns()
            
            # Phase 3: Migrate data in batches
            total_customers = self.get_total_customer_count()
            migrated_count = 0
            
            while migrated_count < total_customers:
                batch_result = self.migrate_customer_batch(
                    offset=migrated_count,
                    limit=self.batch_size
                )
                
                migrated_count += batch_result['processed']
                
                # Log progress
                progress_pct = (migrated_count / total_customers) * 100
                logger.info(f"Customer migration progress: {progress_pct:.1f}% ({migrated_count}/{total_customers})")
                
                # Validate batch results
                if not batch_result['success']:
                    raise DataMigrationError(f"Batch migration failed: {batch_result['error']}")
            
            # Phase 4: Validate migration results
            validation_results = self.validate_migration_results()
            if not validation_results['success']:
                raise DataMigrationError(f"Migration validation failed: {validation_results['errors']}")
            
            # Phase 5: Update constraints and indexes
            self.finalize_migration()
            
            self.complete_migration_tracking(migration_id, 'SUCCESS')
            return {'success': True, 'migrated_records': migrated_count}
            
        except Exception as e:
            # Rollback migration
            self.rollback_migration('customers_backup_20240301')
            self.complete_migration_tracking(migration_id, 'FAILED', str(e))
            raise e
    
    def migrate_customer_batch(self, offset, limit):
        """
        Migrate a batch of customer records with error handling
        """
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                
                # Select batch of customers to migrate
                cursor.execute("""
                    SELECT customer_id, full_name, address_text
                    FROM customers
                    WHERE migration_status IS NULL
                    ORDER BY customer_id
                    LIMIT %s OFFSET %s
                """, (limit, offset))
                
                customers = cursor.fetchall()
                
                for customer in customers:
                    try:
                        # Parse and normalize data
                        normalized_data = self.normalize_customer_data(customer)
                        
                        # Update customer record
                        cursor.execute("""
                            UPDATE customers
                            SET
                                first_name = %s,
                                last_name = %s,
                                street_address = %s,
                                city = %s,
                                state = %s,
                                postal_code = %s,
                                country = %s,
                                migration_status = 'COMPLETED',
                                migration_timestamp = CURRENT_TIMESTAMP
                            WHERE customer_id = %s
                        """, (
                            normalized_data['first_name'],
                            normalized_data['last_name'],
                            normalized_data['street_address'],
                            normalized_data['city'],
                            normalized_data['state'],
                            normalized_data['postal_code'],
                            normalized_data['country'],
                            customer['customer_id']
                        ))
                        
                    except Exception as e:
                        # Log individual record error but continue with batch
                        logger.error(f"Failed to migrate customer {customer['customer_id']}: {str(e)}")
                        
                        cursor.execute("""
                            UPDATE customers
                            SET
                                migration_status = 'FAILED',
                                migration_error = %s,
                                migration_timestamp = CURRENT_TIMESTAMP
                            WHERE customer_id = %s
                        """, (str(e), customer['customer_id']))
                
                conn.commit()
                return {'success': True, 'processed': len(customers)}
                
        except Exception as e:
            return {'success': False, 'error': str(e), 'processed': 0}
    
    def validate_migration_results(self):
        """
        Comprehensive validation of migration results
        """
        validation_results = {
            'success': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check for failed migrations
            cursor.execute("SELECT COUNT(*) FROM customers WHERE migration_status = 'FAILED'")
            failed_count = cursor.fetchone()[0]
            
            if failed_count > 0:
                validation_results['errors'].append(f"{failed_count} customers failed migration")
                validation_results['success'] = False
            
            # Check for incomplete migrations
            cursor.execute("SELECT COUNT(*) FROM customers WHERE migration_status IS NULL")
            incomplete_count = cursor.fetchone()[0]
            
            if incomplete_count > 0:
                validation_results['errors'].append(f"{incomplete_count} customers not migrated")
                validation_results['success'] = False
            
            # Validate data integrity
            cursor.execute("""
                SELECT COUNT(*) FROM customers 
                WHERE migration_status = 'COMPLETED' 
                AND (first_name IS NULL OR last_name IS NULL)
            """)
            invalid_data_count = cursor.fetchone()[0]
            
            if invalid_data_count > 0:
                validation_results['errors'].append(f"{invalid_data_count} customers have invalid normalized data")
                validation_results['success'] = False
            
            # Collect statistics
            cursor.execute("""
                SELECT 
                    migration_status,
                    COUNT(*) as count
                FROM customers
                GROUP BY migration_status
            """)
            
            validation_results['statistics'] = {
                row[0]: row[1] for row in cursor.fetchall()
            }
        
        return validation_results
```

This comprehensive migration framework provides systematic approaches to database schema evolution, ensuring safe, reproducible, and reversible changes while maintaining data integrity and minimizing operational risks.