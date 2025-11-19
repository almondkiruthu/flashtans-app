import uuid
from decimal import Decimal
from config.database import get_connection

class Product:
    @staticmethod
    def get_all():
        """Get all products"""
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM products ORDER BY created_at DESC')
            rows = cursor.fetchall()
            cursor.close()
            connection.close()

            # Convert Decimal to float for JSON serialization
            for row in rows:
                if 'price' in row and isinstance(row['price'], Decimal):
                    row['price'] = float(row['price'])

            return rows
        except Exception as error:
            raise error

    @staticmethod
    def get_by_id(product_id):
        """Get a product by ID"""
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM products WHERE id = %s', (product_id,))
            row = cursor.fetchone()
            cursor.close()
            connection.close()

            if row and 'price' in row and isinstance(row['price'], Decimal):
                row['price'] = float(row['price'])

            return row
        except Exception as error:
            raise error

    @staticmethod
    def create(product_data):
        """Create a new product"""
        try:
            product_id = str(uuid.uuid4())
            name = product_data['name']
            price = float(product_data['price'])
            description = product_data['description']
            stock = int(product_data['stock'])

            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO products (id, name, price, description, stock) VALUES (%s, %s, %s, %s, %s)',
                (product_id, name, price, description, stock)
            )
            connection.commit()
            cursor.close()
            connection.close()

            return Product.get_by_id(product_id)
        except Exception as error:
            raise error

    @staticmethod
    def update(product_id, product_data):
        """Update a product"""
        try:
            name = product_data['name']
            price = float(product_data['price'])
            description = product_data['description']
            stock = int(product_data['stock'])

            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                'UPDATE products SET name = %s, price = %s, description = %s, stock = %s WHERE id = %s',
                (name, price, description, stock, product_id)
            )
            connection.commit()
            cursor.close()
            connection.close()

            return Product.get_by_id(product_id)
        except Exception as error:
            raise error

    @staticmethod
    def delete(product_id):
        """Delete a product"""
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
            affected_rows = cursor.rowcount
            connection.commit()
            cursor.close()
            connection.close()

            return affected_rows > 0
        except Exception as error:
            raise error

    @staticmethod
    def update_stock(product_id, quantity):
        """Update product stock"""
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                'UPDATE products SET stock = stock - %s WHERE id = %s',
                (quantity, product_id)
            )
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as error:
            raise error
