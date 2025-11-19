import uuid
from config.database import get_connection

class Customer:
    @staticmethod
    def create(customer_data):
        """Create a new customer"""
        try:
            customer_id = str(uuid.uuid4())
            name = customer_data['name']
            email = customer_data['email']
            address = customer_data['address']

            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO customers (id, name, email, address) VALUES (%s, %s, %s, %s)',
                (customer_id, name, email, address)
            )
            connection.commit()
            cursor.close()
            connection.close()

            return customer_id
        except Exception as error:
            raise error

    @staticmethod
    def get_by_id(customer_id):
        """Get a customer by ID"""
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM customers WHERE id = %s', (customer_id,))
            row = cursor.fetchone()
            cursor.close()
            connection.close()

            return row
        except Exception as error:
            raise error
