"""
In-memory data storage for Flash Tans application
No database dependency - perfect for low-resource machines
"""
from datetime import datetime
from threading import Lock

# Thread-safe lock for concurrent access
data_lock = Lock()

# In-memory data storage
_data_storage = {
    'products': {},
    'customers': {},
    'orders': {},
    'order_items': {}
}

def get_storage():
    """Get the in-memory data storage"""
    return _data_storage

def init_database():
    """Initialize in-memory storage with sample data"""
    try:
        with data_lock:
            # Only initialize if products are empty
            if len(_data_storage['products']) == 0:
                sample_products = [
                    {
                        'id': '1',
                        'name': 'Buckets',
                        'price': 29.99,
                        'description': 'Amazon S3 Buckets for scalable storage',
                        'stock': 50,
                        'image': '/images/placeholder.jpg',
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat()
                    },
                    {
                        'id': '2',
                        'name': 'Load Balancers',
                        'price': 34.99,
                        'description': 'Customizable load balancers for your applications',
                        'stock': 30,
                        'image': '/images/placeholder.jpg',
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat()
                    },
                    {
                        'id': '3',
                        'name': 'Microsoft Azure',
                        'price': 24.99,
                        'description': 'Cloud computing services for building, testing, and deploying applications',
                        'stock': 25,
                        'image': '/images/placeholder.jpg',
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat()
                    }
                ]

                for product in sample_products:
                    _data_storage['products'][product['id']] = product

                print('In-memory storage initialized successfully with sample data')
    except Exception as error:
        print(f'Storage initialization error: {error}')
