import telebot
import requests
from config import TOKEN_TG

API_URL = ' http://127.0.0.1:8000/api/get_order_status/'
API_TOKEN = TOKEN_TG
bot = telebot.TeleBot(API_TOKEN)


# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пожалуйста, введите ваш логин для отслеживания заказов.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    username = message.text.strip()
    response = requests.post(API_URL, json={'username': username})

    if response.status_code == 200:
        orders = response.json().get('orders', [])
        if not orders:
            bot.reply_to(message, "У вас нет заказов.")
        else:
            response_text = "Ваши заказы:\n\n"
            for order in orders:
                response_text += (
                    f"Заказ #{order['order_id']}\n"
                    f"Статус: {order['status']}\n"
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


if __name__ == '__main__':
    bot.polling()
