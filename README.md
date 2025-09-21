# ☕ Cafe Warehouse Management System v2.0

A secure, role-based web application for managing cafe inventory across multiple departments with user authentication and profit tracking.

## 🔐 **NEW: Role-Based Access Control**

The system now supports **three user roles** with different access levels:

### **👑 Manager Role**
- **Full Access**: Can view and manage all departments
- **User Management**: Create and manage staff accounts
- **Complete Dashboard**: See profits and inventory across all departments
- **All Permissions**: Can add stock and record sales for any department

### **👥 Department Staff Roles**
- **Beverages Staff**: Limited access to Beverages & Snacks department only
- **Kitchen Staff**: Limited access to Kitchen department only
- **Restricted View**: Can only see their department's data
- **Department Operations**: Can only add stock and record sales for their assigned department

## 🎯 Features

- **🔐 Secure Authentication**: Login system with role-based access control
- **Multi-Department Inventory**: Separate tracking for Beverages & Snacks and Kitchen departments
- **Real-Time Stock Management**: Add stock imports and record sales instantly
- **Profit Tracking**: Automatic calculation of profit margins per product and department
- **Mobile-First Design**: Clean, responsive interface optimized for mobile devices
- **User-Friendly Interface**: No technical knowledge required - designed for cafe staff
- **Live Dashboard**: Real-time updates with stock levels and profit figures
- **Low Stock Alerts**: Visual warnings when inventory runs low (< 5 units)
- **Session Management**: 30-minute sessions with persistent login capability
- **User Management**: Manager can create and manage staff accounts

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Internet connection (for Tailwind CSS and Font Awesome)

### Installation & Setup

1. **Clone or Download** this project to your computer
2. **Open Command Prompt/Terminal** and navigate to the project folder
3. **Run the setup commands** (copy and paste these one by one):

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install Flask
pip install Flask

# Set up the database with sample data
python database.py

# Start the application
python app.py
```

4. **Open your browser** and go to: `http://localhost:5000`

## � Login Credentials

The system comes with three default accounts for immediate testing:

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| **Manager** | `manager` | `manager123` | Full access to all departments |
| **Beverages Staff** | `beverages` | `bev123` | Beverages & Snacks department only |
| **Kitchen Staff** | `kitchen` | `kit123` | Kitchen department only |

## �📱 How to Use

### First Time Access
1. **Navigate to** `http://localhost:5000`
2. **You'll be redirected** to the login page
3. **Choose your role** and use the credentials above
4. **Click "Sign In"** to access the dashboard

### Manager Dashboard
- **Full Control**: View all departments and their inventory
- **User Management**: Click the user icon → "Manage Users" to create new staff accounts
- **Complete Access**: Add stock and record sales for any department
- **Financial Overview**: See total profits across all departments

### Department Staff Dashboard
- **Department-Specific**: Only see your assigned department
- **Limited Operations**: Can only manage inventory for your department
- **Focused Interface**: Simplified view showing only relevant products
- View current stock levels for all products
- See total profit for each department
- Monitor overall cafe profit
- Get low stock alerts (red warning for items < 5 units)

### Adding New Stock
1. Click **"Add Stock"** button on any department card
2. Select the product from the dropdown
3. Enter the quantity you're adding to inventory
4. Click **"Add Stock"** to confirm

### Recording Sales
1. Click **"Record Sale"** button on any department card
2. Select the product you sold
3. Enter the quantity sold
4. Enter the selling price per unit
5. See the expected profit calculation
6. Click **"Record Sale"** to confirm

### Understanding the Interface
- **Green numbers**: Healthy stock levels
- **Red numbers**: Low stock warnings (< 5 units)
- **Blue numbers**: Profit figures
- **Department cards**: Show products, stock, and department totals
- **Header**: Displays total profit across all departments

## 🛠️ Technical Details

### Project Structure
```
warehouse/
├── app.py                 # Main Flask application
├── database.py           # Database setup and initialization
├── warehouse.db          # SQLite database (created automatically)
├── templates/
│   └── index.html        # Frontend interface
├── venv/                 # Python virtual environment
└── README.md            # This documentation
```

### Database Schema
- **Departments**: Store department information (Beverages & Snacks, Kitchen)
- **Products**: Store product details with cost prices
- **InventoryTransactions**: Log all stock movements and sales

### API Endpoints
- `GET /login` - Login page
- `POST /login` - Handle login authentication
- `GET /logout` - Logout and clear session
- `GET /` - Main dashboard page (requires authentication)
- `GET /dashboard` - Get all inventory and profit data (JSON, role-filtered)
- `POST /log_transaction` - Log stock imports or sales (JSON, role-protected)
- `GET /products/<department_id>` - Get products for department (JSON, role-protected)
- `GET /users` - Get all users (JSON, manager only)
- `POST /users` - Create new user (JSON, manager only)
- `GET /user-info` - Get current user information (JSON)

## � User Management (Manager Only)

### Creating New Staff Accounts
1. **Login as Manager** using the manager credentials
2. **Click the user icon** in the top-right corner
3. **Select "Manage Users"** from the dropdown menu
4. **Fill out the form** with the new user's details:
   - Username (must be unique)
   - Full Name
   - Password
   - Role (Manager, Beverages Staff, or Kitchen Staff)
   - Department (auto-selected for staff roles)
5. **Click "Add User"** to create the account

### User Roles Explained
- **Manager**: Can access everything, manage users, see all financial data
- **Beverages Staff**: Can only work with Beverages & Snacks department
- **Kitchen Staff**: Can only work with Kitchen department

### Session Management
- **Session Duration**: 30 minutes of inactivity before auto-logout
- **Persistent Login**: Users can stay logged in on their devices
- **Secure Logout**: Click user icon → "Logout" to end session safely

## �🔧 Customization

### Adding New Products
1. Stop the application (Ctrl+C)
2. Edit `database.py`
3. Add your products to the `products` list with format: `('Product Name', cost_price)`
4. Run `python database.py` again
5. Restart the application

### Adding New Departments
1. Edit `database.py`
2. Add departments to the `departments` list
3. Assign products to the new department in `initial_transactions`
4. Run `python database.py` again

## 🌐 Making it Accessible Online (Demo)

To share your application with others:

1. **Install ngrok** (free tunneling service):
   - Download from: https://ngrok.com/download
   - Extract and run: `ngrok http 5000`

2. **Share the link**: ngrok will provide a public URL like `https://xyz123.ngrok.io`

3. **Send this link** to anyone - they can access your cafe management system from their phone or computer!

## 📊 Sample Data Included

The system comes pre-loaded with realistic cafe inventory:

**Beverages & Snacks Department:**
- Coffee Beans, Tea Leaves, Sugar, Milk
- Biscuits, Chips, Cold Drink Bottles

**Kitchen Department:**
- Rice, Dosa Batter, Idli Batter, Oil
- Onions, Tomatoes, Bread, Eggs

Each item includes initial stock quantities to demonstrate the system immediately.

## 🆘 Troubleshooting

### Common Issues

**"Database not found" error:**
- Run `python database.py` first to create the database

**"Port already in use" error:**
- Change the port in `app.py`: `app.run(port=5001)`
- Or kill the existing process and restart

**Page doesn't load:**
- Make sure Flask is running (you should see "Running on http://127.0.0.1:5000")
- Check that you're visiting the correct URL: `http://localhost:5000`

**Database changes not showing:**
- Restart the Flask application
- Refresh your browser page

### Getting Help

If you encounter any issues:
1. Check that all commands ran without errors
2. Ensure Python 3.7+ is installed
3. Make sure you're in the correct project folder
4. Try restarting the application

## 🔒 Security Features

**✅ Already Implemented:**
- ✅ **User Authentication**: Secure login system with hashed passwords
- ✅ **Role-Based Access Control**: Different permissions for different user types
- ✅ **Session Management**: 30-minute timeout with secure session handling
- ✅ **API Protection**: All endpoints require authentication and proper permissions
- ✅ **Input Validation**: Form validation and data sanitization

**🔧 For Production Use:**
- Use environment variables for secret keys
- Use a production database (PostgreSQL, MySQL)
- Deploy with a production WSGI server (Gunicorn, uWSGI)
- Enable HTTPS with SSL certificates
- Add rate limiting and additional security headers
- Implement password complexity requirements
- Add audit logging for user actions

## 📝 License

This project is created for educational and demonstration purposes. Feel free to modify and use as needed.

---

**Built with:** Python Flask, Flask-Login, SQLite, HTML5, Tailwind CSS, JavaScript  
**Version:** 2.0 (with Authentication & Role-Based Access Control)  
**Author:** Cafe Warehouse Management System  
**Date:** September 2025

---

## 🎉 **What's New in v2.0**

### 🔐 **Complete Authentication System**
- **Secure Login**: SHA-256 password hashing
- **Role-Based Access**: Manager, Beverages Staff, Kitchen Staff
- **Session Management**: 30-minute sessions with persistent login
- **Mobile-Optimized**: Touch-friendly login interface

### 👑 **Manager Features**
- **User Management**: Create and manage staff accounts through web interface
- **Full Dashboard Access**: View all departments and complete financial data
- **Complete Control**: Manage inventory across all departments

### 👥 **Staff Features** 
- **Department-Specific Access**: Staff can only access their assigned department
- **Simplified Interface**: Clean, focused view of relevant products only
- **Role-Based Restrictions**: Cannot access other departments' data

### 🛡️ **Security Enhancements**
- **API Protection**: All endpoints require proper authentication
- **Permission Checks**: Users can only access their authorized data
- **Secure Sessions**: Automatic timeout and logout functionality
