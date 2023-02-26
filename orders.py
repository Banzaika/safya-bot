from config import secret_token
import requests
def get_new_orders():
    url = 'http://127.0.0.1:8000/new_orders'
    token = {'token': secret_token}
    response = requests.post(url , json = token)
    if response.status_code == 200:
        return response.json()
    else:
        return []

def orders_formatter(orders_list):
    orders = []
    for order in orders_list:
        str = ''
        str += f"{order['lastname']} {order['name']} {order['patronymic']}\n"
        str += f"Телефон - {order['phone']}\n"
        str += f"Индекс - {order['postcode']}\n"
        str += f"Адрес - {order['street_address']}\n"
        str += 'Товары:\n'
        for relation in order['order_relations']:
            str += f" {relation['product_category']}, {relation['product_name']} - {relation['amount']}шт.\n"

        str += f"Итоговая цена - {order['common_price']}₽"
        orders.append(str)
    return orders