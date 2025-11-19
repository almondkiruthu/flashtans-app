import uuid
from datetime import datetime
from config.database import get_storage, data_lock

class Customer:
    @staticmethod
    def create(customer_data):
        """Create a new customer"""
        try:
            customer_id = str(uuid.uuid4())

            customer = {
                'id': customer_id,
                'name': customer_data['name'],
                'email': customer_data['email'],
                'address': customer_data['address'],
                'created_at': datetime.now().isoformat()
            }

            with data_lock:
                storage = get_storage()
                storage['customers'][customer_id] = customer

            return customer_id
        except Exception as error:
            raise error

    @staticmethod
    def get_by_id(customer_id):
        """Get a customer by ID"""
        try:
            with data_lock:
                storage = get_storage()
                return storage['customers'].get(customer_id)
        except Exception as error:
            raise error
