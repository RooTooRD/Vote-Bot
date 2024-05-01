import telebot
import config  # Import your bot token and channel ID from a separate configuration file
import json
import flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# Initialize the bot



api_key = config.TOKEN
bot = telebot.TeleBot(api_key)
# secret = '1ff5b502-e35f-46a7-a626-de55336cf9e3'

#bot = telebot.TeleBot(api_key, threaded=False)
bot.remove_webhook()
# bot.set_webhook(f'abderrahmane2005.pythonanywhere.com/{secret}')

# app = flask.Flask(__name__)

# @app.route(f'/{secret}', methods=['POST'])
# def webhook():
#     if flask.request.headers.get('content-type') == 'application/json':
#         json_string = flask.request.get_data().decode('utf-8')
#         update = telebot.types.Update.de_json(json_string)
#         bot.process_new_updates([update])
#         return ''
#     else:
#         flask.abort(403)


def hasVoted(name):
    with open(r'./data.json', 'r') as file:
        data = json.load(file)

    for obj in data['names'] :
        if str(name) == str(obj):
            return True
    return False


def writeData(text, user_id):
    with open(r'./data.json', 'r') as file:
        data = json.load(file)
        data['names'][user_id] = text
        
    with open(r'./data.json', 'w') as json_file:
    # Write the updated JSON data back to the file
        json.dump(data, json_file, indent=2)

    with open(r'./data.json', 'r') as file:
        data = json.load(file)

        data['counters'][text]+=1


    with open(r'./data.json', 'w') as json_file:
        # Write the updated JSON data back to the file
        json.dump(data, json_file, indent=2)


def getResult():
    with open(r'./data.json', 'r') as file:
        data = json.load(file)
        return {
            'before': data['counters']['before'],
            'after': data['counters']['after']
        }


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('قبل', callback_data="before"),
                InlineKeyboardButton('بعد', callback_data="after"))
    return markup



# Handler for handling user messages
@bot.message_handler(commands=['start'])
def handle_message(message):

    # Check if the user is a member of the specified channel
    member_info = bot.get_chat_member(config.CHANNEL_ID1, message.from_user.id)
    if not is_member(message.from_user.id):
        # If the user is not a member, prompt them to join the channel
        bot.reply_to(message,  
        ''' 
يبدو أنك لست أحد الطلاب 😑
        ''')
        return
    else:
        if hasVoted(message.from_user.id):
            bot.send_message(message.chat.id, 
            '''
لقد قدمت بالتصويت من قبل 😊
            ''')
        else:
            bot.send_message(message.chat.id, 
            ''' 
السلام عليكم
أنت حاليا  أمام صندوق الإقتراع لتحديد موعد إجتياز إمتحانات السداسي الثاني لدفعة 2024/2023 طب جامعة باتنة 2
ليكن في علمك أنك تملك الحق في التصويت لمرة واحدة فقط مع عدم إمكانيات تغيير التصويت
وليكن في علمك أيضا أنك أمام احتمالين:
	📍إحتمال إجتياز الإمتحانات قبل العيد
	📍إحتمال إجتياز الإمتحانات بعد العيد
كما أن لكل إحتمال تبعات وجب أخذها بعين الإعتبار قبل إبداء 

🔴 تبعات إحتمال إجتياز الإمتحانات قبل العيد :
	📌 إحتمالية إجراء الإمتحانات سيكون في مدة أسبوعين (ليست أكيدة لأن اخر حصة تيبي شيمي ستكون يوم 7 جوان)
	📌 تعويض بعض المحاضرات و الأعمال التوجيهية لإستكمال المقرر
	📌 لن يكون هناك semaine blockée

🔴 تبعات إحتمال إجتياز الإمتحانات بعد العيد :
	📌 إجراء الإمتحانات سيكون في مدة أسبوع واحد
	📌 وجود semaine blockée (نفس أسبوع العيد)
	📌 إستكمال الدروس بوتيرة عادية 

❗تنبيه : فترة الإمتحانات لن تتداخل مع أسبوع البكالوريا سواءا كانت قبل أو بعد العيد
            '''
            , reply_markup=gen_markup())
            

    # If the user is a member, proceed with handling the message
    # Your logic for handling user messages goes here


@bot.message_handler(commands=['res'])
def result(message):
    result = getResult()
    bot.send_message(message.chat.id, 
    f'''
    before -- {result['before']}
after -- {result['after']}
    ''')


@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    if hasVoted(call.message.from_user.id):
        bot.send_message(call.message.chat.id, 
            '''
لقد قدمت بالتصويت من قبل 😊
            ''')
    else:
        writeData(call.data, call.from_user.id)
        bot.send_message(call.message.chat.id, 
        ''' 
    📍سيتم الإعلان عن النتائج بعد إنتهاء عملية التصويت
        ''')
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
# Function to check if a user is a member of a channel
def is_member(user_id):
    try:
        # Retrieve information about the user's membership status in the channel
        member_info1 = bot.get_chat_member(config.CHANNEL_ID1, user_id)
        member_info2 = bot.get_chat_member(config.CHANNEL_ID2, user_id)
        member_info3 = bot.get_chat_member(config.CHANNEL_ID3, user_id)
        # Check if the user is a member of the channel
        return member_info1.status in ('member', 'creator', 'administrator') or member_info2.status in ('member', 'creator', 'administrator') or member_info3.status in ('member', 'creator', 'administrator') 
        #return member_info1.status in ('member', 'creator', 'administrator')
    except Exception as e:
        print("Error:", e)
        return False

# Start the bot
bot.polling()
