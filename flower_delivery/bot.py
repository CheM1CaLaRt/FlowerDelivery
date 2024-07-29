import telebot
import requests


# Инициализация бота
bot = telebot.TeleBot('7352605219:AAFZyO9u6Ren-oI1vn8w_KGlZg3JzxvA5iU')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Flower Delivery Bot! Use /order to place an order.")

@bot.message_handler(commands=['order'])
def show_products(message):
    response = requests.get('http://127.0.0.1:8000/products/')
    products = response.json()
    product_list = "\n".join([f"{product['id']}: {product['name']} - ${product['price']}" for product in products])
    bot.reply_to(message, f"Available products:\n{product_list}\n\nReply with product IDs separated by commas to place an order.")
    bot.register_next_step_handler(message, process_order)

def process_order(message):
    product_ids = [int(pid) for pid in message.text.split(',')]
    response = requests.post('http://127.0.0.1:8000/create_order/', json={'user_id': message.from_user.id, 'product_ids': product_ids})
    if response.status_code == 201:
        bot.reply_to(message, "Order placed successfully!")
    else:
        bot.reply_to(message, "Failed to place order.")

bot.polling()