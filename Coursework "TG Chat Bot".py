import os
import sqlite3
from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()
bot = TeleBot(os.getenv('BOT_TOKEN'))

def init_db():
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        russian TEXT NOT NULL,
        english TEXT NOT NULL,
        added_by INTEGER DEFAULT 0
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_words (
        user_id INTEGER,
        word_id INTEGER,
        PRIMARY KEY (user_id, word_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (word_id) REFERENCES words(word_id)
    )
    ''')
    
    initial_words = [
        ('красный', 'red'),
        ('синий', 'blue'),
        ('зеленый', 'green'),
        ('я', 'I'),
        ('ты', 'you'),
        ('он', 'he'),
        ('она', 'she'),
        ('дом', 'house'),
        ('кошка', 'cat'),
        ('собака', 'dog')
    ]
    
    cursor.execute('SELECT COUNT(*) FROM words')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO words (russian, english) VALUES (?, ?)', initial_words)
    
    conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)',
                   (user_id, username, first_name, last_name))
    conn.commit()
    conn.close()
    
    welcome_text = """
    Привет! Я бот для изучения английских слов.
    
    Что я умею:
    - /practice - начать тренировку
    - /add_word - добавить новое слово
    - /delete_word - удалить слово
    
    Давай учить английский?!
    """
    bot.reply_to(message, welcome_text)


if __name__ == '__main__':
    init_db()
    bot.polling()
