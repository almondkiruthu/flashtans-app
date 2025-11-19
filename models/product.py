import uuid
from datetime import datetime
from config.database import get_storage, data_lock

class Product:
    @staticmethod
    def get_all():
        """Get all products"""
        try:
            with data_lock:
                storage = get_storage()
                products = list(storage['products'].values())
                # Sort by created_at descending (newest first)
                products.sort(key=lambda x: x.get('created_at', ''), reverse=True)
                return products
        except Exception as error:
            raise error

    @staticmethod
    def get_by_id(product_id):
        """Get a product by ID"""
        try:
            with data_lock:
                storage = get_storage()
                return storage['products'].get(product_id)
        except Exception as error:
            raise error

    @staticmethod
    def create(product_data):
        """Create a new product"""
        try:
            product_id = str(uuid.uuid4())
            now = datetime.now().isoformat()

            product = {
                'id': product_id,
                'name': product_data['name'],
                'price': float(product_data['price']),
                'description': product_data['description'],
                'stock': int(product_data['stock']),
                'image': product_data.get('image', '/images/placeholder.jpg'),
                'created_at': now,
                'updated_at': now
            }

            with data_lock:
                storage = get_storage()
                storage['products'][product_id] = product

            return product
        except Exception as error:
            raise error

    @staticmethod
    def update(product_id, product_data):
        """Update a product"""
        try:
            with data_lock:
                storage = get_storage()
                if product_id not in storage['products']:
                    return None

                product = storage['products'][product_id]
                product['name'] = product_data['name']
                product['price'] = float(product_data['price'])
                product['description'] = product_data['description']
                product['stock'] = int(product_data['stock'])
                product['updated_at'] = datetime.now().isoformat()

                return product
        except Exception as error:
            raise error

    @staticmethod
    def delete(product_id):
        """Delete a product"""
        try:
            with data_lock:
                storage = get_storage()
                if product_id in storage['products']:
                    del storage['products'][product_id]
                    return True
                return False
        except Exception as error:
            raise error

    @staticmethod
    def update_stock(product_id, quantity):
        """Update product stock"""
        try:
            with data_lock:
                storage = get_storage()
                if product_id in storage['products']:
                    storage['products'][product_id]['stock'] -= quantity
        except Exception as error:
            raise error
