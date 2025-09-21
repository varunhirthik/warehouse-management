# ☕ Cafe Warehouse Management System v1.0

A simple, mobile-first web application for managing cafe inventory across multiple departments and tracking profit margins in real-time.

## 🎯 Features

- **Multi-Department Inventory**: Separate tracking for Beverages & Snacks and Kitchen departments
- **Real-Time Stock Management**: Add stock imports and record sales instantly
- **Profit Tracking**: Automatic calculation of profit margins per product and department
- **Mobile-First Design**: Clean, responsive interface optimized for mobile devices
- **User-Friendly Interface**: No technical knowledge required - designed for cafe managers
- **Live Dashboard**: Real-time updates with stock levels and profit figures
- **Low Stock Alerts**: Visual warnings when inventory runs low (< 5 units)

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

## 📱 How to Use

### Main Dashboard
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
- `GET /` - Main dashboard page
- `GET /dashboard` - Get all inventory and profit data (JSON)
- `POST /log_transaction` - Log stock imports or sales (JSON)
- `GET /products/<department_id>` - Get products for specific department (JSON)

## 🔧 Customization

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

## 🔒 Security Note

This is a prototype application designed for demonstration purposes. For production use:
- Add user authentication
- Use a production database (PostgreSQL, MySQL)
- Deploy with a production WSGI server (Gunicorn, uWSGI)
- Enable HTTPS
- Add input validation and sanitization

## 📝 License

This project is created for educational and demonstration purposes. Feel free to modify and use as needed.

---

**Built with:** Python Flask, SQLite, HTML5, Tailwind CSS, JavaScript  
**Version:** 1.0  
**Author:** Cafe Warehouse Management System  
**Date:** September 2025
