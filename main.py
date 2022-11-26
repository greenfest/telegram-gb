import os
import telebot
import random

#main variables
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
isRunning = False
countGuess = 1

@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    global isRunning
    if not isRunning:
        bot.send_message(message.chat.id, 'Привет! Я умею решать несложные математические примеры и играть в игру "Угадай число". Открой меню, чтобы увидеть команды')
        isRunning = True

@bot.message_handler(commands=['guess'])
def guess_handler(message):
    chat_id = message.chat.id
    text = message.text    
    randomNum = random.randint(0,1000)
    guess = bot.send_message(chat_id, 'Давай поиграем в игру! Я загадываю число от 1 до 1000, а тебе нужно отгадать. Как ты думаешь, какое число я загадал?')
    bot.register_next_step_handler(guess, checkNum, randomNum)

def checkNum(message, randomNum):
    chat_id = message.chat.id
    text = message.text
    global countGuess, isRunning

    if not text.isdigit():
        msg = bot.send_message(chat_id, 'Введите число')
        bot.register_next_step_handler(msg, checkNum) 
        return
    if int(text) != randomNum:
        if int(text) > randomNum:
            msg = bot.send_message(chat_id, f'Нет, я загадал число поменьше, попробуй еще раз! Попытка № {countGuess}')
        else:     
            msg = bot.send_message(chat_id, f'Нет, я загадал число побольше, попробуй еще раз! Попытка № {countGuess}')
        countGuess += 1
        bot.register_next_step_handler(msg, checkNum, randomNum) 
        return
    
    msg = bot.send_message(chat_id, f'Молодец! Ты угадал число с {countGuess} попытки!')
    countGuess = 1
    isRunning = False


@bot.message_handler(commands=['calc'])
def guess_handler(message):
    chat_id = message.chat.id
    text = message.text    
    expression = bot.send_message(chat_id, 'Сейчас я попробую вычислить значение выражения, которое ты мне напишешь! Напиши мне, например: 2 + 2 * 2')
    bot.register_next_step_handler(expression, getResultExpression)

def getResultExpression(message):
    chat_id = message.chat.id
    text = message.text

    try:
        result = eval(text)
        bot.send_message(chat_id, f'Значение выражения {text} = {result}')
    except:
        msg = bot.send_message(chat_id, f'Что то здесь не так! Попробуй снова')
        bot.register_next_step_handler(msg, getResultExpression) 



bot.polling()


    