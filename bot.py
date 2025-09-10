from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла .env
load_dotenv()
# Получаем токен из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверяем, что токен загружен
if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN не определен в .env файле")

print(f"Ваш токен бота: {BOT_TOKEN}")

"""Обработчики"""
#Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = []
    await update.message.reply_text("🧑🏻‍🎨 Приветствую Вас! \nДобро пожаловать в мое портфолио! ✅")
    await show_main_menu(update, context)

# Функция-обработчик команды /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Вот чем я могу быть полезен:\n"
        "⚜️ /start - запуск программы\n"
        "‼️ /help - помощь по командам управления\n"
        "⚛️ /menu - меню моих возможностей\n\n"
        "📌 В скором времени количество команд будет существенно больше! 📌"
    )
    await update.message.reply_text(text)

#Главное меню с кнопками
async def show_main_menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("🏞️ Дизайн БАННЕРОВ", url="https://t.me/richter_design1")],
        [InlineKeyboardButton("🌇 Дизайн СОЦСЕТЕЙ", url="https://t.me/richter_design2")],
        [InlineKeyboardButton("🌠 Дизайн МАРКЕТПЛЕЙСОВ", url="https://t.me/richter_design4")],
        [InlineKeyboardButton("💻 Дизайн ТАПЛИНК и САЙТОВ", url="https://t.me/richter_design3")],
        [InlineKeyboardButton("🎨 Прочие направления дизайна", url="https://t.me/+eL3QkEuRoMo5ZTYy")],
        [InlineKeyboardButton("🏆 Сертификаты", url="https://t.me/+BRNKxgphQLcwOGRi")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите интересующее Вас направление:", reply_markup=reply_markup)


#Команда /menu
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Чтобы просмотреть портфолио, выберите интересующее Вас направление:", reply_markup=menu)

#Обработка нажатий на кнопки
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query #Получаем информацию о нажатии
    await query.answer() #Обязательно подтверждаем нажатие (иначе Телеграм может "висеть")
    data = query.data #достаем то самое callback_data с кнопок

    if data == "random_meme":
        await query.edit_message_text("📸 Здесь будет случайный мем!")
    elif data == "create_meme":
        await query.edit_message_text("🏞️ Отправь мне картинку для мема!")
        context.user_data["wait_for_photo"] = True #Если картинку отправили, бот в состоянии загрузки
    elif data == "quiz":
        await query.edit_message_text("🔥 Викторина скоро начнется!")
    elif data == "top":
        await query.edit_message_text("🏆 Топ игроков появится здесь!")

"""Приложения"""



# Создание приложения бота
app = ApplicationBuilder().token(BOT_TOKEN).build()
# Подключение обработчика команды /start
app.add_handler(CommandHandler("start", start))
# Подключение обработчика команды /help
app.add_handler(CommandHandler("help", help))
# Подключаем меню
app.add_handler(CommandHandler("menu", menu_handler))
#Подключение нажатие кнопок
app.add_handler(CallbackQueryHandler(handle_buttons))

# Запускаем бота
app.run_polling()