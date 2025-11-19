import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'flash_tans_db'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Create connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="flash_tans_pool",
    pool_size=10,
    pool_reset_session=True,
    **db_config
)

def get_connection():
    """Get a connection from the pool"""
    return connection_pool.get_connection()

def init_database():
    """Initialize database and tables"""
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                description TEXT,
                image VARCHAR(255) DEFAULT '/images/placeholder.jpg',
                stock INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        # Create customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id VARCHAR(36) PRIMARY KEY,
                customer_id VARCHAR(36),
                total DECIMAL(10, 2) NOT NULL,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            )
        """)

        # Create order_items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id VARCHAR(36) PRIMARY KEY,
                order_id VARCHAR(36),
                product_id VARCHAR(36),
                product_name VARCHAR(255),
                price DECIMAL(10, 2),
                quantity INT,
                subtotal DECIMAL(10, 2),
                FOREIGN KEY (order_id) REFERENCES orders(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        # Insert sample products if table is empty
        cursor.execute('SELECT COUNT(*) as count FROM products')
        result = cursor.fetchone()

        if result[0] == 0:
            sample_products = [
                {
                    'id': '1',
                    'name': 'Buckets',
                    'price': 29.99,
                    'description': 'Amazon S3 Buckets for scalable storage',
                    'stock': 50
                },
                {
                    'id': '2',
                    'name': 'Load Balancers',
                    'price': 34.99,
                    'description': 'Customizable load balancers for your applications',
                    'stock': 30
                },
                {
                    'id': '3',
                    'name': 'Microsoft Azure',
                    'price': 24.99,
                    'description': 'Cloud computing services for building, testing, and deploying applications',
                    'stock': 25
                }
            ]

            for product in sample_products:
                cursor.execute(
                    'INSERT INTO products (id, name, price, description, stock) VALUES (%s, %s, %s, %s, %s)',
                    (product['id'], product['name'], product['price'], product['description'], product['stock'])
                )

        connection.commit()
        cursor.close()
        connection.close()
        print('Database initialized successfully')
    except Exception as error:
        print(f'Database initialization error: {error}')
