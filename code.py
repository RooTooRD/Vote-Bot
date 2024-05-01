
import json
import telebot
import requests
import config
# json_data = '''
# {
#     "counters": {
#         "after": 0,
#         "before": 0
#     },

#     "names": {
#         "Abderrahmane" : "after",
#         "oussama" : "before"
#     }
# }
# '''

# data = json.loads(json_data)

#data['names']['Abderrahmane'] = 'af'
#data["names"]["abdou"] = data['names'].pop("Abderrahmane")

# add new key-value to the object 'names'
#data['names']['hichem'] = 'before'

#data['counters']['after'] +=1

# for obj in data:
#     for k in data[obj]:
        
#         print(f'{k} --- > {data[obj][k]}')
#         print('-'*10)


TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN)

target_chat_id1 = '-1001825264285'
target_chat_id2 = 'TARGET_CHAT_ID'
target_chat_id3 = 'TARGET_CHAT_ID'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'hello')
    user_id = message.from_user.id

    api_url1 = fr'https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={target_chat_id1}&user_id={user_id}'
    #api_url2 = fr'https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={target_chat_id2}&user_id={user_id}'
    #api_url3 = fr'https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={target_chat_id3}&user_id={user_id}'

    response1 = requests.get(api_url1)
   # response2 = requests.get(api_url2)
   # response3 = requests.get(api_url3)
    
    #if response1.ok or response2.ok or response3.ok :
    
   
    if response1.ok:
        result1 = response1.json()
        # result2 = response2.json()
        #  result3 = response3.json()
        #if result1['ok'] and result1['result']['status'] in ('member', 'administrator', 'creator') or result2['ok'] and result2['result']['status'] in ('member', 'administrator', 'creator' or result3['ok'] and result3['result']['status'] in ('member', 'administrator', 'creator')):
        bot.send_message(message.chat.id, 'above')
        if result1['ok'] and result1['result']['status'] in ('member', 'administrator', 'creator'):
            bot.send_message(message.chat.id, 'below')
            bot.send_message(message.chat.id, 'you are welocme')
        else:
            bot.send_message(message.chat.id, 'no')

# @bot.message_handler(commands=['get_id'])
# def get_chat_id(message):
#     user_id = message.from_user.id
#     chat_id = message.chat.id
    
#     bot.reply_to(message, f"The ID of this User is: {chat_id}")






bot.polling()

    

