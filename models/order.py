import uuid
from datetime import datetime
from config.database import get_storage, data_lock

class Order:
    @staticmethod
    def create(order_data):
        """Create a new order"""
        try:
            with data_lock:
                storage = get_storage()

                order_id = str(uuid.uuid4())
                customer_id = order_data['customerId']
                total = order_data['total']
                items = order_data['items']

                # Create order
                order = {
                    'id': order_id,
                    'customer_id': customer_id,
                    'total': float(total),
                    'status': 'pending',
                    'created_at': datetime.now().isoformat()
                }
                storage['orders'][order_id] = order

                # Create order items and update stock
                for item in items:
                    item_id = str(uuid.uuid4())
                    order_item = {
                        'id': item_id,
                        'order_id': order_id,
                        'product_id': item['productId'],
                        'product_name': item['productName'],
                        'price': float(item['price']),
                        'quantity': item['quantity'],
                        'subtotal': float(item['subtotal'])
                    }
                    storage['order_items'][item_id] = order_item

                    # Update product stock
                    if item['productId'] in storage['products']:
                        storage['products'][item['productId']]['stock'] -= item['quantity']

            return Order.get_by_id(order_id)
        except Exception as error:
            raise error

    @staticmethod
    def get_by_id(order_id):
        """Get an order by ID with its items"""
        try:
            with data_lock:
                storage = get_storage()

                if order_id not in storage['orders']:
                    return None

                order = storage['orders'][order_id].copy()

                # Get customer info
                customer_id = order.get('customer_id')
                if customer_id and customer_id in storage['customers']:
                    customer = storage['customers'][customer_id]
                    order['customer_name'] = customer['name']
                    order['customer_email'] = customer['email']
                    order['customer_address'] = customer['address']

                # Get order items
                items = []
                for item_id, item in storage['order_items'].items():
                    if item['order_id'] == order_id:
                        items.append(item.copy())

                order['items'] = items

                return order
        except Exception as error:
            raise error

    @staticmethod
    def get_all():
        """Get all orders with customer info"""
        try:
            with data_lock:
                storage = get_storage()

                orders = []
                for order_id, order in storage['orders'].items():
                    order_copy = order.copy()

                    # Get customer info
                    customer_id = order_copy.get('customer_id')
                    if customer_id and customer_id in storage['customers']:
                        customer = storage['customers'][customer_id]
                        order_copy['customer_name'] = customer['name']
                        order_copy['customer_email'] = customer['email']

                    orders.append(order_copy)

                # Sort by created_at descending
                orders.sort(key=lambda x: x.get('created_at', ''), reverse=True)

                return orders
        except Exception as error:
            raise error
