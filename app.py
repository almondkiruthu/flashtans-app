from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

from config.database import init_database
from models.product import Product
from models.customer import Customer
from models.order import Order

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database
init_database()

# Routes
@app.route('/')
def index():
    try:
        products = Product.get_all()
        return render_template('index.html', products=products)
    except Exception as error:
        print(f'Error fetching products: {error}')
        return render_template('error.html', message='Failed to load products'), 500

@app.route('/admin')
def admin():
    try:
        products = Product.get_all()
        orders = Order.get_all()
        return render_template('admin.html', products=products, orders=orders)
    except Exception as error:
        print(f'Error loading admin data: {error}')
        return render_template('error.html', message='Failed to load admin data'), 500

@app.route('/cart')
def cart():
    return render_template('cart.html')

# API Routes
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = Product.get_all()
        return jsonify(products)
    except Exception as error:
        print(f'Error fetching products: {error}')
        return jsonify({'error': 'Failed to fetch products'}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        description = data.get('description')
        stock = data.get('stock')

        if not all([name, price, description, stock is not None]):
            return jsonify({'error': 'All fields are required'}), 400

        new_product = Product.create({
            'name': name,
            'price': price,
            'description': description,
            'stock': stock
        })
        return jsonify(new_product), 201
    except Exception as error:
        print(f'Error creating product: {error}')
        return jsonify({'error': 'Failed to create product'}), 500

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        deleted = Product.delete(product_id)

        if not deleted:
            return jsonify({'error': 'Product not found'}), 404

        return jsonify({'message': 'Product deleted successfully'})
    except Exception as error:
        print(f'Error deleting product: {error}')
        return jsonify({'error': 'Failed to delete product'}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        items = data.get('items')
        customer_info = data.get('customerInfo')

        if not items or not len(items) or not customer_info:
            return jsonify({'error': 'Items and customer info are required'}), 400

        # Verify products and calculate total
        total = 0
        order_items = []

        for item in items:
            product = Product.get_by_id(item['productId'])
            if not product:
                return jsonify({'error': f"Product {item['productId']} not found"}), 404

            if product['stock'] < item['quantity']:
                return jsonify({'error': f"Insufficient stock for {product['name']}"}), 400

            item_total = product['price'] * item['quantity']
            total += item_total

            order_items.append({
                'productId': product['id'],
                'productName': product['name'],
                'price': product['price'],
                'quantity': item['quantity'],
                'subtotal': item_total
            })

        # Create customer
        customer_id = Customer.create(customer_info)

        # Create order
        new_order = Order.create({
            'customerId': customer_id,
            'total': total,
            'items': order_items
        })

        return jsonify(new_order), 201
    except Exception as error:
        print(f'Error creating order: {error}')
        return jsonify({'error': 'Failed to create order'}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.get_all()
        return jsonify(orders)
    except Exception as error:
        print(f'Error fetching orders: {error}')
        return jsonify({'error': 'Failed to fetch orders'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', message='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', message='Something went wrong!'), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    # IMPORTANT: Listen on 0.0.0.0 so it can be accessed from outside the VM
    app.run(host='0.0.0.0', port=port, debug=True)
