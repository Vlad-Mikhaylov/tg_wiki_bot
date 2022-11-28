import telebot, wikipedia, re
from telebot import types

bot = telebot.TeleBot('5467142177:AAEpDG53itOlL9DtiHe33yRbk3KjnvisssM') #set telegram bot

def getwiki(s):
    '''work with wiki article`s presentation'''
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        return [ny.title, wikitext2]
        
    #work with excaptions in case of wiki unfound eror
    except Exception as e:
        if wikipedia.languages == "ru":
            return [f'В Wikipedia нет информации связаной с "{s}"', '']
        return [f'There is no such info in Wikipedia connected with "{s}"', '']


@bot.message_handler(commands=["start"])
def start(m):
    '''start and set the language'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🇷🇺 Русский")
    btn2 = types.KeyboardButton('🇬🇧 English')
    markup.add(btn1, btn2)
    bot.send_message(m.from_user.id, "🇷🇺 Выберите язык / 🇬🇧 Choose your language", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    '''accept tha language and make wiki request'''
    if (message.text != "🇷🇺 Русский") & (message.text != '🇬🇧 English'):
        title = getwiki(message.text)
        bot.send_message(message.chat.id, text=f"_*{title[0]}*_", parse_mode= 'Markdown')
        bot.send_message(message.chat.id, title[1])
    else:
        if message.text == "🇷🇺 Русский":
            wikipedia.set_lang("ru") #deffault language is english
            bot.send_message(message.from_user.id, 'Отправьте мне любое слово, и я найду статью, связанную с ним на Wikipedia')
    

        if message.text == '🇬🇧 English':
            bot.send_message(message.from_user.id, 'Send me a word combination and I will find its article in Wikipedia')
    
bot.polling(none_stop=True, interval=0) #making bot