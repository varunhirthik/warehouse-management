import sqlite3
from datetime import datetime
import hashlib

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_database():
    """Create the database and tables for the Cafe Warehouse Management System v2.0"""
    
    # Connect to SQLite database (creates if doesn't exist)
    conn = sqlite3.connect('warehouse.db')
    cursor = conn.cursor()
    
    # Create Departments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    
    # Create Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cost_price REAL NOT NULL
        )
    ''')
    
    # Create Users table (NEW in v2.0)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            department_id INTEGER,
            full_name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            last_login TEXT,
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
    ''')
    
    # Create InventoryTransactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            department_id INTEGER NOT NULL,
            quantity_change INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            selling_price REAL DEFAULT 0,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (department_id) REFERENCES departments (id)
        )
    ''')
    
    print("✅ Database tables created successfully!")
    
    # Insert initial departments
    departments = [
        ('Beverages & Snacks',),
        ('Kitchen',)
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO departments (name) VALUES (?)', departments)
    
    # Insert initial products with realistic cafe items
    products = [
        # Beverages & Snacks Department
        ('Coffee Beans (kg)', 15.0),
        ('Tea Leaves (kg)', 12.0),
        ('Sugar (kg)', 3.0),
        ('Milk (L)', 2.5),
        ('Biscuits (packet)', 1.5),
        ('Chips (packet)', 2.0),
        ('Cold Drink Bottles', 1.0),
        
        # Kitchen Department
        ('Rice (kg)', 8.0),
        ('Dosa Batter (L)', 5.0),
        ('Idli Batter (L)', 4.5),
        ('Oil (L)', 6.0),
        ('Onions (kg)', 2.0),
        ('Tomatoes (kg)', 3.0),
        ('Bread (loaf)', 1.5),
        ('Eggs (dozen)', 4.0),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO products (name, cost_price) VALUES (?, ?)', products)
    
    # Create default user accounts (NEW in v2.0)
    current_time = datetime.now().isoformat()
    default_users = [
        ('manager', hash_password('manager123'), 'manager', None, 'System Manager', current_time),
        ('beverages', hash_password('bev123'), 'beverages', 1, 'Beverages Staff', current_time),
        ('kitchen', hash_password('kit123'), 'kitchen', 2, 'Kitchen Staff', current_time),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO users (username, password_hash, role, department_id, full_name, created_at) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', default_users)
    
    # Add some initial inventory to demonstrate the system
    # Get department and product IDs
    cursor.execute('SELECT id FROM departments WHERE name = "Beverages & Snacks"')
    beverages_dept_id = cursor.fetchone()[0]
    
    cursor.execute('SELECT id FROM departments WHERE name = "Kitchen"')
    kitchen_dept_id = cursor.fetchone()[0]
    
    # Initial stock imports
    initial_transactions = [
        # Beverages & Snacks initial stock
        (1, beverages_dept_id, 10, 'import', 0.0, datetime.now().isoformat()),  # Coffee Beans
        (2, beverages_dept_id, 5, 'import', 0.0, datetime.now().isoformat()),   # Tea Leaves
        (3, beverages_dept_id, 20, 'import', 0.0, datetime.now().isoformat()),  # Sugar
        (4, beverages_dept_id, 15, 'import', 0.0, datetime.now().isoformat()),  # Milk
        (5, beverages_dept_id, 50, 'import', 0.0, datetime.now().isoformat()),  # Biscuits
        (6, beverages_dept_id, 30, 'import', 0.0, datetime.now().isoformat()),  # Chips
        (7, beverages_dept_id, 100, 'import', 0.0, datetime.now().isoformat()), # Cold Drinks
        
        # Kitchen initial stock
        (8, kitchen_dept_id, 25, 'import', 0.0, datetime.now().isoformat()),    # Rice
        (9, kitchen_dept_id, 10, 'import', 0.0, datetime.now().isoformat()),    # Dosa Batter
        (10, kitchen_dept_id, 8, 'import', 0.0, datetime.now().isoformat()),    # Idli Batter
        (11, kitchen_dept_id, 5, 'import', 0.0, datetime.now().isoformat()),    # Oil
        (12, kitchen_dept_id, 15, 'import', 0.0, datetime.now().isoformat()),   # Onions
        (13, kitchen_dept_id, 12, 'import', 0.0, datetime.now().isoformat()),   # Tomatoes
        (14, kitchen_dept_id, 20, 'import', 0.0, datetime.now().isoformat()),   # Bread
        (15, kitchen_dept_id, 10, 'import', 0.0, datetime.now().isoformat()),   # Eggs
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO inventory_transactions 
        (product_id, department_id, quantity_change, transaction_type, selling_price, timestamp) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', initial_transactions)
    
    # Commit all changes
    conn.commit()
    
    print("✅ Initial departments and products added successfully!")
    print("✅ Default user accounts created successfully!")
    print("✅ Sample inventory data loaded!")
    
    # Display summary
    cursor.execute('SELECT COUNT(*) FROM departments')
    dept_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM products')
    product_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users')
    user_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM inventory_transactions')
    transaction_count = cursor.fetchone()[0]
    
    print(f"\n📊 Database Summary:")
    print(f"   Departments: {dept_count}")
    print(f"   Products: {product_count}")
    print(f"   Users: {user_count}")
    print(f"   Initial Transactions: {transaction_count}")
    
    print(f"\n🔐 Default Login Credentials:")
    print(f"   Manager: username='manager', password='manager123'")
    print(f"   Beverages Staff: username='beverages', password='bev123'")
    print(f"   Kitchen Staff: username='kitchen', password='kit123'")
    
    conn.close()
    print("\n🎉 Database setup complete! Ready to run the application with authentication.")

if __name__ == '__main__':
    create_database()
