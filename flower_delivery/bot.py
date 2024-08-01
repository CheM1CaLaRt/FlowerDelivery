import telebot
import requests
import time
from threading import Thread
from config import TOKEN_TG

API_URL = 'http://127.0.0.1:8000/api/get_order_status/'
API_TOKEN = TOKEN_TG
bot = telebot.TeleBot(API_TOKEN)

# Хранилище для статусов заказов и идентификаторов чатов
user_data = {}


# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {'username': None, 'orders': {}}
    bot.reply_to(message, "Привет! Пожалуйста, введите ваш логин для отслеживания заказов.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    username = message.text.strip()

    if user_id not in user_data:
        user_data[user_id] = {'username': username, 'orders': {}}
    else:
        user_data[user_id]['username'] = username

    response = requests.post(API_URL, json={'username': username})

    if response.status_code == 200:
        orders = response.json().get('orders', [])
        if not orders:
            bot.reply_to(message, "У вас нет заказов.")
        else:
            orders.sort(key=lambda x: x['created_at'], reverse=True)
            # Сохраняем текущие статусы заказов для пользователя
            if username not in user_data[user_id]['orders']:
                user_data[user_id]['orders'] = {}

            # Формируем текст для ответа
            response_text = "Ваши заказы:\n\n"
            for order in orders:
                order_id = order['order_id']
                current_status = order['status']

                # Проверка изменений статуса
                if order_id in user_data[user_id]['orders']:
                    if user_data[user_id]['orders'][order_id] != current_status:
                        bot.send_message(
                            user_id,
                            f"Обновление статуса заказа #{order_id}: {current_status}"
                        )

                # Обновляем статус
                user_data[user_id]['orders'][order_id] = current_status

                # Формирование текста ответа
                response_text += (
                    f"Заказ #{order_id}\n"
                    f"Статус: {current_status}\n"
                    f"Адрес доставки: {order['delivery_address']}\n"
                    f"Создан: {order['created_at']}\n"
                    f"Общая сумма: {order['total_price']} руб.\n"
                    f"Содержимое заказа:\n"
                )
                for item in order['items']:
                    response_text += f"- {item['product_name']} (x{item['quantity']})\n"
                response_text += "\n"
            bot.reply_to(message, response_text)
    else:
        bot.reply_to(message, "Ошибка при получении данных. Попробуйте снова позже.")


def check_status_updates():
    while True:
        time.sleep(60)  # Проверяем каждые 60 секунд
        for user_id, data in user_data.items():
            username = data['username']
            if username:
                response = requests.post(API_URL, json={'username': username})
                if response.status_code == 200:
                    orders = response.json().get('orders', [])
                    current_statuses = {order['order_id']: order['status'] for order in orders}

                    for order_id, status in current_statuses.items():
                        if order_id in data['orders']:
                            if data['orders'][order_id] != status:
                                # Отправляем уведомление об изменении статуса
                                bot.send_message(
                                    user_id,
                                    f"Обновление статуса заказа #{order_id}: {status}"
                                )

                        # Обновляем статус
                        data['orders'][order_id] = status


if __name__ == '__main__':
    # Запускаем фоновую задачу для проверки статусов
    status_check_thread = Thread(target=check_status_updates)
    status_check_thread.daemon = True
    status_check_thread.start()

    bot.polling()
