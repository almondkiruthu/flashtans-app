import uuid
from decimal import Decimal
from config.database import get_connection

class Order:
    @staticmethod
    def create(order_data):
        """Create a new order with transaction support"""
        connection = get_connection()
        cursor = connection.cursor()

        try:
            # Start transaction
            connection.start_transaction()

            order_id = str(uuid.uuid4())
            customer_id = order_data['customerId']
            total = order_data['total']
            items = order_data['items']

            # Create order
            cursor.execute(
                'INSERT INTO orders (id, customer_id, total) VALUES (%s, %s, %s)',
                (order_id, customer_id, total)
            )

            # Create order items and update stock
            for item in items:
                item_id = str(uuid.uuid4())
                cursor.execute(
                    'INSERT INTO order_items (id, order_id, product_id, product_name, price, quantity, subtotal) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (item_id, order_id, item['productId'], item['productName'], item['price'], item['quantity'], item['subtotal'])
                )

                # Update product stock
                cursor.execute(
                    'UPDATE products SET stock = stock - %s WHERE id = %s',
                    (item['quantity'], item['productId'])
                )

            # Commit transaction
            connection.commit()
            cursor.close()
            connection.close()

            return Order.get_by_id(order_id)
        except Exception as error:
            # Rollback on error
            connection.rollback()
            cursor.close()
            connection.close()
            raise error

    @staticmethod
    def get_by_id(order_id):
        """Get an order by ID with its items"""
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            # Get order with customer info
            cursor.execute("""
                SELECT o.*, c.name as customer_name, c.email as customer_email, c.address as customer_address
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
                WHERE o.id = %s
            """, (order_id,))

            order = cursor.fetchone()

            if not order:
                cursor.close()
                connection.close()
                return None

            # Convert Decimal to float
            if 'total' in order and isinstance(order['total'], Decimal):
                order['total'] = float(order['total'])

            # Get order items
            cursor.execute('SELECT * FROM order_items WHERE order_id = %s', (order_id,))
            items = cursor.fetchall()

            # Convert Decimals to float in items
            for item in items:
                if 'price' in item and isinstance(item['price'], Decimal):
                    item['price'] = float(item['price'])
                if 'subtotal' in item and isinstance(item['subtotal'], Decimal):
                    item['subtotal'] = float(item['subtotal'])

            order['items'] = items

            cursor.close()
            connection.close()

            return order
        except Exception as error:
            raise error

    @staticmethod
    def get_all():
        """Get all orders with customer info"""
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT o.*, c.name as customer_name, c.email as customer_email
                FROM orders o
                LEFT JOIN customers c ON o.customer_id = c.id
                ORDER BY o.created_at DESC
            """)

            rows = cursor.fetchall()
            cursor.close()
            connection.close()

            # Convert Decimal to float
            for row in rows:
                if 'total' in row and isinstance(row['total'], Decimal):
                    row['total'] = float(row['total'])

            return rows
        except Exception as error:
            raise error
