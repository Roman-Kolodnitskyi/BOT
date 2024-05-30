import telebot
from telebot import types
import random
import time
from datetime import datetime

API_TOKEN = '6664347044:AAHKKe9iidRhRr-ldoRxSMWged_lA81sUgg'
bot = telebot.TeleBot(API_TOKEN)

questions = [
    {
        "question": "Як відкрити файл для читання в Python?",
        "options": ["open('file.txt')", "open('file.txt', 'r')", "open('file.txt', 'w')", "open('file.txt', 'a')"],
        "answer": "open('file.txt', 'r')"
    },
    {
        "question": "Як записати рядок у файл в Python?",
        "options": ["write('file.txt', 'Hello')", "file.write('Hello')", "file.append('Hello')", "write('Hello')"],
        "answer": "file.write('Hello')"
    },
    {
        "question": "Як закрити файл в Python?",
        "options": ["close('file.txt')", "file.close()", "file.end()", "close.file()"],
        "answer": "file.close()"
    },
    {
        "question": "Як прочитати всі рядки з файлу в Python?",
        "options": ["file.readlines()", "file.read()", "file.readline()", "read.file()"],
        "answer": "file.readlines()"
    },
    {
        "question": "Як відкрити файл для запису в Python?",
        "options": ["open('file.txt', 'r')", "open('file.txt', 'w')", "open('file.txt', 'a')", "open('file.txt')"],
        "answer": "open('file.txt', 'w')"
    },
    {
        "question": "Як перевірити, чи файл існує в Python?",
        "options": ["os.path.isfile('file.txt')", "file.exists('file.txt')", "os.exists('file.txt')", "path.isfile('file.txt')"],
        "answer": "os.path.isfile('file.txt')"
    },
    {
        "question": "Як додати текст у кінець файлу в Python?",
        "options": ["open('file.txt', 'a')", "open('file.txt', 'w')", "open('file.txt', 'r')", "open('file.txt', 'x')"],
        "answer": "open('file.txt', 'a')"
    },
    {
        "question": "Як створити новий файл в Python?",
        "options": ["open('file.txt', 'x')", "open('file.txt', 'w')", "open('file.txt', 'a')", "open('file.txt')"],
        "answer": "open('file.txt', 'x')"
    },
    {
        "question": "Як прочитати один рядок з файлу в Python?",
        "options": ["file.readline()", "file.readlines()", "file.read()", "read.file()"],
        "answer": "file.readline()"
    },
    {
        "question": "Який модуль використовують для роботи з файлами та директоріями в Python?",
        "options": ["os", "sys", "file", "dir"],
        "answer": "os"
    }
]

user_data = {}

@bot.message_handler(commands=['start'])
def start_test(message):
    user_id = message.chat.id
    random.shuffle(questions)
    user_data[user_id] = {
        'questions': questions.copy(),
        'score': 0,
        'start_time': time.time(),
        'answers': []
    }
    send_question(message)

def send_question(message):
    user_id = message.chat.id
    if user_data[user_id]['questions']:
        current_question = user_data[user_id]['questions'].pop()
        markup = types.InlineKeyboardMarkup()
        for option in current_question['options']:
            markup.add(types.InlineKeyboardButton(option, callback_data=option))
        user_data[user_id]['current_question'] = current_question
        bot.send_message(user_id, current_question['question'], reply_markup=markup)
    else:
        end_test(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.message.chat.id
    answer = call.data
    current_question = user_data[user_id]['current_question']
    user_data[user_id]['answers'].append((current_question['question'], answer))
    if answer == current_question['answer']:
        user_data[user_id]['score'] += 1
    
    markup = types.InlineKeyboardMarkup()
    for option in current_question['options']:
        if option == answer:
            markup.add(types.InlineKeyboardButton(f"✔️ {option}", callback_data=option))
        else:
            markup.add(types.InlineKeyboardButton(option, callback_data=option))

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
    time.sleep(1)
    send_question(call.message)

def end_test(message):
    user_id = message.chat.id
    end_time = time.time()
    duration = end_time - user_data[user_id]['start_time']
    minutes, seconds = divmod(duration, 60)
    result_message = (
        f"Тест завершено!\n"
        f"Кількість набраних балів: {user_data[user_id]['score']}\n"
        f"Дата проходження: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Тривалість проходження: {int(minutes)} хвилин {int(seconds)} секунд\n\n"
    )
    bot.send_message(user_id, result_message)
    del user_data[user_id]

bot.polling()
