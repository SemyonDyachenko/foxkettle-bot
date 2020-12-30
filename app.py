import telebot
import sqlite3
 
bot = telebot.TeleBot('1456273579:AAEzzeJPbPESYwRUHEeuTVzW3kqH9_symaY')

conn = sqlite3.connect('dz.db',check_same_thread=False)



def create_table():
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(
   id INT PRIMARY KEY,
   userid INT,
   task TEXT,
   task_date TEXT)
   ''')
    conn.commit()

def add_new_task(user_id,text,date):
    cursor = conn.cursor()
    data = (user_id,text,date)
    cursor.execute("INSERT INTO tasks(userid,task,task_date) VALUES(?,?,?);",data)
    conn.commit()

def get_tasks(user_id):
    cursor = conn.cursor()
    data = user_id
    cursor.execute("""SELECT * FROM tasks WHERE userid=?""",(data,))
    return cursor.fetchall()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Це foxkettle бот!')

@bot.message_handler(commands=['task'])
def send_tasks(message):
    data = get_tasks(message.from_user.id)
    for i in data:
        bot.send_message(message.chat.id, i[2])

@bot.message_handler(commands=['data'])
def send_data(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(content_types=['text'])
def new_task(message):
    if(message.text.lower()[0] == "t" and message.text.lower()[1] == "o" and message.text.lower()[2] == "d" and message.text.lower()[3] == "o"):
        create_table()
        add_new_task(message.from_user.id,message.text,message.date)
        bot.send_message(message.chat.id, "Добавлено")
    elif message.text.lower() == "привет":
        bot.send_message(message.chat.id,"Привет")
    else:
        bot.send_message(message.chat.id, "Непонял")



@bot.message_handler(content_types=['text'])
def send_message(message):
    print(message)
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет ' + message.from_user.first_name)
    elif message.text.lower() == "пока":
        bot.send_message(message.chat.id, 'Пока ' + message.from_user.first_name)


bot.polling()