import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


# get tokens from the file
import var.config as config
# import functions
from get_voices import get_all_voices, generate_audio_file

bot = telebot.TeleBot(config.telegram_bot_token)

# Словарь для хранения выбранного голоса на пользователя
user_voice = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    voices = get_all_voices()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    buttons = [KeyboardButton(v.name) for v in voices]
    markup.add(*buttons)
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для создания озвучки! Выберите голос, который будет использоваться при создании озвучки.",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, lambda msg: select_voice(msg, voices))

def select_voice(message, voices):
    voice_name = message.text
    voice = next((v for v in voices if v.name == voice_name), None)
    if voice:
        user_voice[message.chat.id] = voice.voice_id
        bot.send_message(message.chat.id,
                         f"Голос '{voice_name}' выбран. Введите текст для озвучки:",
                         reply_markup = ReplyKeyboardRemove()
                        )
        bot.register_next_step_handler(message, generate_and_send_audio)
    else:
        bot.send_message(message.chat.id, "Выбранный голос не найден. Попробуйте снова с /start.")

def generate_and_send_audio(message):
    voice_id = user_voice.get(message.chat.id)
    if not voice_id:
        bot.send_message(message.chat.id, "Сначала выберите голос через команду /start.")
        return
    text = message.text
    # audio_generator = generate_audio_file(text, voice_id, filename=f"audio_{message.chat.id}.mp3")
    mp3_path = f"audio_{message.chat.id}.mp3"
    ogg_path = f"voice_{message.chat.id}.ogg"

    # Генерируем сразу два файла с разными форматами
    generate_audio_file(text, voice_id, filename=mp3_path, output_format="mp3_44100_128")
    generate_audio_file(text, voice_id, filename=ogg_path, output_format="opus_48000_128")

    with open(mp3_path, 'rb') as f_audio:
        bot.send_audio(message.chat.id, f_audio)

    try:
        with open(ogg_path, 'rb') as f_voice:
            bot.send_voice(message.chat.id, f_voice)
    except telebot.apihelper.ApiTelegramException as e:
        if "VOICE_MESSAGES_FORBIDDEN" in str(e):
            bot.send_message(message.chat.id,
                             "⚠️ Невозможно отправить голосовое сообщение. Ваш Telegram запрещает получать голосовые.")
        else:
            raise


bot.polling(none_stop=True)
