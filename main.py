import telebot
from telebot import types

from PIL import Image, ImageDraw, ImageFont


def textfunc(text, place):
    img = Image.open('1.jpeg')
    d = ImageDraw.Draw(img)

    imgWidth, imgHeight = img.size
    font = ImageFont.truetype("impact.ttf", imgHeight // 16)

    offset = imgWidth // 256 + 1
    shadowColor = 'black'

    l = (len(text) * (imgHeight // 16)) // 2.4

    x = imgWidth // 2
    if place == 'top':
        y = (imgHeight // 32) * 4
    elif place == 'bottom':
        y = (imgHeight // 32) * 29
    elif place == 'dtop':
        y = 50
    if l > imgHeight:
        s1 = text[:len(text) // 2]
        s2 = text[len(text) // 2:]
        text = s1 + '\n' + s2
    # Обводка текста
    for off in range(offset):
        d.text((x - off, y), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x + off, y), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x, y + off), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x, y - off), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x - off, y + off), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x + off, y + off), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x - off, y - off), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x + off, y - off), text, anchor="mm", font=font, fill=shadowColor)
    d.text((x, y), text, anchor="mm", font=font, fill="#fff")
    img.save('1.jpeg')
    return None


def demot(text):
    width = 600
    img = Image.open('1.jpeg')
    imgWidth, imgHeight = img.size
    ratio = width / imgWidth
    height = int((float(imgHeight) * float(ratio)))
    img = img.resize((width, height), Image.ANTIALIAS)
    ram = Image.new(mode="RGB", size=(650, (height * 12)//10))
    ram.paste(img, (25, 10))
    imgWidth, imgHeight = ram.size
    d = ImageDraw.Draw(ram)
    font = ImageFont.truetype("impact.ttf", imgHeight // 16)
    offset = imgWidth // 256 + 1
    shadowColor = 'black'
    l = (len(text) * (imgHeight // 16)) // 2.4
    x = imgWidth // 2
    y = (imgHeight // 12) * 11
    if l > imgHeight:
        s1 = text[:len(text) // 2]
        s2 = text[len(text) // 2:]
        text = s1 + '\n' + s2
    # Обводка текста
    for off in range(offset):
        d.text((x - off, y), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x + off, y), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x, y + off), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x, y - off), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x - off, y + off), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x + off, y + off), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x - off, y - off), text, anchor="mm", font=font, fill=shadowColor)
        d.text((x + off, y - off), text, anchor="mm", font=font, fill=shadowColor)
    d.text((x, y), text, anchor="mm", font=font, fill="#fff")
    ram.save('1.jpeg')
    return None


bot = telebot.TeleBot('6851269224:AAEEZnqV5HKbp8qQ5bA1WojPSZVdKqTyNQY')
text_up = ''
text_low = ''
text_d = ''


@bot.message_handler(content_types=['text', 'photo'])
def start(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Чтобы создать мем загрузите изображение")
    elif message.content_type == 'photo':
        raw = message.photo[2].file_id
        name = "1" + ".jpeg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name, 'wb') as new_file:
            new_file.write(downloaded_file)
        image = open(name, 'rb')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Мем")
        btn2 = types.KeyboardButton("Демoтиватор")
        markup.add(btn1, btn2)
        msg = bot.send_message(message.from_user.id, "Создать демотиватор или мем?", reply_markup=markup)
        bot.register_next_step_handler(msg, meme)


@bot.message_handler(content_types=['text'])
def meme(message):
    if message.text.lower() == 'мем':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton("Пропустить")
        markup.add(btn)
        msg = bot.send_message(message.from_user.id, "Напишите текст, находящийся сверху(чтобы оставить поле "
                                                     "пустым напишите 'Пропустить')", reply_markup=markup)
        bot.register_next_step_handler(msg, up)
    else:
        msg = bot.send_message(message.from_user.id, "Напишите текст, находящийся снизу", reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, demo)


@bot.message_handler(commands=['up'])
def up(message):
    if message.text.lower() != 'пропустить':
        text_up = message.text
        textfunc(text_up, 'top')
    msg = bot.send_message(message.from_user.id, "Напишите текст, находящийся снизу(чтобы оставить поле "
                                                 "пустым напишите 'Пропустить'):")
    bot.register_next_step_handler(msg, low)


@bot.message_handler(content_types=['text'])
def low(message):
    if message.text.lower() != 'пропустить':
        text_low = message.text
        textfunc(text_low, 'bottom')
    photo = open('1.jpeg', 'rb')
    bot.send_photo(message.from_user.id, photo, reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def demo(message):
    text_d = message.text
    demot(text_d)
    photo = open('1.jpeg', 'rb')
    bot.send_photo(message.from_user.id, photo, reply_markup=telebot.types.ReplyKeyboardRemove())


bot.polling(none_stop=True, interval=0)
