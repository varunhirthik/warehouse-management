import sqlite3
from datetime import datetime

def create_database():
    """Create the database and tables for the Cafe Warehouse Management System"""
    
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
    print("✅ Sample inventory data loaded!")
    
    # Display summary
    cursor.execute('SELECT COUNT(*) FROM departments')
    dept_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM products')
    product_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM inventory_transactions')
    transaction_count = cursor.fetchone()[0]
    
    print(f"\n📊 Database Summary:")
    print(f"   Departments: {dept_count}")
    print(f"   Products: {product_count}")
    print(f"   Initial Transactions: {transaction_count}")
    
    conn.close()
    print("\n🎉 Database setup complete! Ready to run the application.")

if __name__ == '__main__':
    create_database()
