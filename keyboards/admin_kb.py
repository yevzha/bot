from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки головного меню
b_weather = KeyboardButton(text='/Weather')
b_download = KeyboardButton(text='/Download')
b_show = KeyboardButton(text='/Show')
b_poem = KeyboardButton(text='/Poem')

# Кнопки для клавіатури підтвердження завантаження
b_cancel = KeyboardButton(text='Cancel')

# Головна клавіатура
main_keyboard = ReplyKeyboardMarkup(keyboard=[[b_weather, b_download, b_poem, b_show]], resize_keyboard=True)

# Клавіатура для підтвердження завантаження
download_keyboard = ReplyKeyboardMarkup(keyboard=[[b_cancel]], resize_keyboard=True)
