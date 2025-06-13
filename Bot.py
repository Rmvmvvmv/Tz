import telebot
import random
import pandas as pd

API_TOKEN = '8107698493:AAHGt3kXXYUBwfjrCr4NekbZiGN6imZsVBA'
COOKING_METHOD = 'Cooking_Method'
NAME = 'Name'
INGREDIENTS = 'Ingredients'
RECIPE = 'Recipe'

bot = telebot.TeleBot(API_TOKEN)
df_recipes = pd.read_excel('rtp.xlsx', engine="openpyxl")
cooking_methods_column = df_recipes[COOKING_METHOD]
cooking_methods = cooking_methods_column.drop_duplicates().tolist()

def get_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    for cooking_method in cooking_methods:
        button = telebot.types.InlineKeyboardButton(text=cooking_method, callback_data=cooking_method)
        keyboard.add(button)
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = get_keyboard()
    bot.send_message(message.chat.id, "Привет! Я твой кулинарный помощник. Выбери как будем готовить: ", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in cooking_methods)
def show_recipe(call):
    chat_id = call.message.chat.id
    cooking_method = call.data
    filtered_recipes = df_recipes[df_recipes[COOKING_METHOD] == cooking_method]
    recipes_dict = filtered_recipes.to_dict('records')
    random_recipe = random.choice(recipes_dict)
    recipe_message = f"*{random_recipe[NAME]}*\n\n"
    recipe_message += f"*Метод приготовления:*\n{random_recipe[COOKING_METHOD]}\n\n"
    recipe_message += f"*Ингредиенты:*\n{random_recipe[INGREDIENTS]}\n\n"
    recipe_message += f"*Рецепт:*\n{random_recipe[RECIPE]}"
    bot.send_message(chat_id, recipe_message, parse_mode="Markdown")
    bot.answer_callback_query(call.id)
    keyboard = get_keyboard()
    bot.send_message(chat_id, "Хочешь попробовать что-то другое?", reply_markup=keyboard)

@bot.message_handler(commands=['info'])
def send_welcome(message):
    bot.reply_to(message, "Я могу предоставить тебе рецепты для приготовление блюд.\nЖми /start для начала.")

bot.infinity_polling()