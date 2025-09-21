from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
from datetime import datetime, timedelta
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'cafe-warehouse-secret-key-2025'  # Change this in production
app.permanent_session_lifetime = timedelta(minutes=30)  # 30 minute sessions

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

class User(UserMixin):
    def __init__(self, id, username, role, department_id, full_name):
        self.id = id
        self.username = username
        self.role = role
        self.department_id = department_id
        self.full_name = full_name
    
    def is_manager(self):
        return self.role == 'manager'
    
    def can_access_department(self, dept_id):
        if self.is_manager():
            return True
        return self.department_id == dept_id

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, role, department_id, full_name FROM users WHERE id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['role'], 
                   user_data['department_id'], user_data['full_name'])
    return None

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('warehouse.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, role, department_id, full_name 
            FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        user_data = cursor.fetchone()
        
        if user_data:
            # Update last login
            cursor.execute('UPDATE users SET last_login = ? WHERE id = ?', 
                         (datetime.now().isoformat(), user_data['id']))
            conn.commit()
            
            user = User(user_data['id'], user_data['username'], user_data['role'], 
                       user_data['department_id'], user_data['full_name'])
            login_user(user, remember=True)
            session.permanent = True
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
        
        conn.close()
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')

@app.route('/log_transaction', methods=['POST'])
@login_required
def log_transaction():
    """
    Log a transaction (either import or sale)
    Expected JSON payload:
    {
        "product_id": 1,
        "department_id": 1,
        "quantity_change": -2,  # negative for sales, positive for imports
        "type": "sale",  # or "import"
        "selling_price": 50.0  # price per unit for sales, 0 for imports
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['product_id', 'department_id', 'quantity_change', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        product_id = data['product_id']
        department_id = data['department_id']
        quantity_change = data['quantity_change']
        transaction_type = data['type']
        selling_price = data.get('selling_price', 0.0)
        
        # Check if user can access this department
        if not current_user.can_access_department(department_id):
            return jsonify({'error': 'Access denied to this department'}), 403
        
        # Validate transaction type
        if transaction_type not in ['import', 'sale']:
            return jsonify({'error': 'Transaction type must be "import" or "sale"'}), 400
        
        # For sales, quantity_change should be negative
        if transaction_type == 'sale' and quantity_change > 0:
            quantity_change = -abs(quantity_change)
        
        # For imports, quantity_change should be positive
        if transaction_type == 'import' and quantity_change < 0:
            quantity_change = abs(quantity_change)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if product and department exist
        cursor.execute('SELECT name FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        if not product:
            conn.close()
            return jsonify({'error': 'Product not found'}), 404
        
        cursor.execute('SELECT name FROM departments WHERE id = ?', (department_id,))
        department = cursor.fetchone()
        if not department:
            conn.close()
            return jsonify({'error': 'Department not found'}), 404
        
        # For sales, check if we have enough stock
        if transaction_type == 'sale':
            cursor.execute('''
                SELECT COALESCE(SUM(quantity_change), 0) as current_stock
                FROM inventory_transactions
                WHERE product_id = ? AND department_id = ?
            ''', (product_id, department_id))
            
            current_stock = cursor.fetchone()['current_stock']
            requested_quantity = abs(quantity_change)
            
            if current_stock < requested_quantity:
                conn.close()
                return jsonify({
                    'error': f'Insufficient stock. Available: {current_stock}, Requested: {requested_quantity}'
                }), 400
        
        # Insert the transaction
        cursor.execute('''
            INSERT INTO inventory_transactions 
            (product_id, department_id, quantity_change, transaction_type, selling_price, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (product_id, department_id, quantity_change, transaction_type, selling_price, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': f'{transaction_type.capitalize()} logged successfully',
            'product': product['name'],
            'department': department['name'],
            'quantity_change': quantity_change,
            'selling_price': selling_price
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    Get dashboard data including current inventory and profit per department
    Returns:
    {
        "departments": [
            {
                "id": 1,
                "name": "Beverages & Snacks",
                "products": [
                    {
                        "id": 1,
                        "name": "Coffee Beans (kg)",
                        "cost_price": 15.0,
                        "current_stock": 8,
                        "total_profit": 45.0
                    }
                ],
                "total_department_profit": 120.0
            }
        ],
        "overall_profit": 245.0
    }
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get departments based on user role
        if current_user.is_manager():
            cursor.execute('SELECT id, name FROM departments ORDER BY name')
            departments = cursor.fetchall()
        else:
            cursor.execute('SELECT id, name FROM departments WHERE id = ? ORDER BY name', 
                         (current_user.department_id,))
            departments = cursor.fetchall()
        
        dashboard_data = {
            'departments': [],
            'overall_profit': 0.0
        }
        
        total_overall_profit = 0.0
        
        for dept in departments:
            dept_id = dept['id']
            dept_name = dept['name']
            
            # Get all products with their current stock and profit for this department
            cursor.execute('''
                SELECT 
                    p.id,
                    p.name,
                    p.cost_price,
                    COALESCE(SUM(it.quantity_change), 0) as current_stock,
                    COALESCE(SUM(
                        CASE 
                            WHEN it.transaction_type = 'sale' 
                            THEN (it.selling_price - p.cost_price) * ABS(it.quantity_change)
                            ELSE 0 
                        END
                    ), 0) as total_profit
                FROM products p
                LEFT JOIN inventory_transactions it ON p.id = it.product_id AND it.department_id = ?
                GROUP BY p.id, p.name, p.cost_price
                HAVING current_stock > 0 OR total_profit > 0
                ORDER BY p.name
            ''', (dept_id,))
            
            products = cursor.fetchall()
            
            dept_products = []
            dept_total_profit = 0.0
            
            for product in products:
                product_data = {
                    'id': product['id'],
                    'name': product['name'],
                    'cost_price': product['cost_price'],
                    'current_stock': product['current_stock'],
                    'total_profit': round(product['total_profit'], 2)
                }
                dept_products.append(product_data)
                dept_total_profit += product['total_profit']
            
            dept_data = {
                'id': dept_id,
                'name': dept_name,
                'products': dept_products,
                'total_department_profit': round(dept_total_profit, 2)
            }
            
            dashboard_data['departments'].append(dept_data)
            total_overall_profit += dept_total_profit
        
        dashboard_data['overall_profit'] = round(total_overall_profit, 2)
        
        conn.close()
        return jsonify(dashboard_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/products/<int:department_id>', methods=['GET'])
@login_required
def get_products_by_department(department_id):
    """Get all products for a specific department with their current stock"""
    # Check if user can access this department
    if not current_user.can_access_department(department_id):
        return jsonify({'error': 'Access denied to this department'}), 403
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                p.id,
                p.name,
                p.cost_price,
                COALESCE(SUM(it.quantity_change), 0) as current_stock
            FROM products p
            LEFT JOIN inventory_transactions it ON p.id = it.product_id AND it.department_id = ?
            GROUP BY p.id, p.name, p.cost_price
            ORDER BY p.name
        ''', (department_id,))
        
        products = cursor.fetchall()
        
        product_list = []
        for product in products:
            product_list.append({
                'id': product['id'],
                'name': product['name'],
                'cost_price': product['cost_price'],
                'current_stock': product['current_stock']
            })
        
        conn.close()
        return jsonify({'products': product_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['GET'])
@login_required
def get_users():
    """Get all users (manager only)"""
    if not current_user.is_manager():
        return jsonify({'error': 'Access denied. Manager role required.'}), 403
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.id, u.username, u.role, u.full_name, u.created_at, u.last_login,
                   d.name as department_name
            FROM users u
            LEFT JOIN departments d ON u.department_id = d.id
            ORDER BY u.role, u.username
        ''')
        
        users = cursor.fetchall()
        
        user_list = []
        for user in users:
            user_list.append({
                'id': user['id'],
                'username': user['username'],
                'role': user['role'],
                'full_name': user['full_name'],
                'department_name': user['department_name'] or 'All Departments',
                'created_at': user['created_at'],
                'last_login': user['last_login']
            })
        
        conn.close()
        return jsonify({'users': user_list})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['POST'])
@login_required
def create_user():
    """Create a new user (manager only)"""
    if not current_user.is_manager():
        return jsonify({'error': 'Access denied. Manager role required.'}), 403
    
    try:
        data = request.get_json()
        
        required_fields = ['username', 'password', 'role', 'full_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        username = data['username']
        password = data['password']
        role = data['role']
        full_name = data['full_name']
        department_id = data.get('department_id')
        
        if role not in ['manager', 'beverages', 'kitchen']:
            return jsonify({'error': 'Invalid role. Must be manager, beverages, or kitchen'}), 400
        
        if role != 'manager' and not department_id:
            return jsonify({'error': 'Department ID required for non-manager roles'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Username already exists'}), 400
        
        # Create the user
        password_hash = hash_password(password)
        current_time = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, department_id, full_name, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password_hash, role, department_id, full_name, current_time))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': f'User {username} created successfully',
            'username': username,
            'role': role,
            'full_name': full_name
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user-info', methods=['GET'])
@login_required
def get_current_user_info():
    """Get current user information"""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'role': current_user.role,
        'full_name': current_user.full_name,
        'department_id': current_user.department_id,
        'is_manager': current_user.is_manager()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists('warehouse.db'):
        print("❌ Database not found! Please run 'python database.py' first.")
        exit(1)
    
    print("🚀 Starting Cafe Warehouse Management System...")
    print("📱 Access the dashboard at: http://localhost:5000")
    print("📊 API endpoints available:")
    print("   - GET  /dashboard (get all inventory and profit data)")
    print("   - POST /log_transaction (log imports/sales)")
    print("   - GET  /products/<department_id> (get products by department)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
