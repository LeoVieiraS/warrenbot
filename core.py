"""#from telegram.ext import CommandHandler, Filters, Updater from conf.settings import TELEGRAM_TOKEN from app.controllers.controller_alert import ControllerAlert from threading import Thread from time import sleep from app import pubsub

from app.check_current_price import CurrentPrice
from check_last_price import GetLastPrice

from datetime import datetime


def start_monitoring():
    now = datetime.now()

    while True:
        if 9 < now.hour < 25:
            current_price = CurrentPrice()
            current_price.alerts = current_price.get_alerts()
            current_price.last_price = current_price.get_last_price()
            current_price.verify()
        sleep(10)

def notify_up(updater):
    sub = pubsub.subscribe("alerts")
    print(type(updater))
    while True:
        msgs_list = list(sub.listen(block=False))
        for msg in msgs_list:
            print(msg)
            response_message = msg["data"][1]

            updater.bot.send_message(chat_id=msg["data"][0], text=response_message)
        sleep(2)


def get_last_price():
    last_prices = GetLastPrice()
    now = datetime.now()
    while True:
        if now.hour == 9 and now.minute == 00:
            last_prices.last_price_tickets()
            sleep(60)


def get_alerts(update, context):
    chat_id = update.message.chat_id
    ControllerAlert.get_alerts(chat_id)


def insert(update, context):
    if context.args:
        user_id = update.message.chat_id
        ControllerAlert.insert(context.args, user_id)
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Opa! Parece que vôce esqueceu de informar os parametros. Consulte o manual com /manual",
        )


def excluir(update, context):
    if context.args:
        user_id = update.message.chat_id
        ControllerAlert.delete_alert(context.args[0], user_id)

    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Opa! Parece que vôce esqueceu de informar os parametros. Consulte o manual com /manual",
        )








def main():
    queue = PubSubManager()
    queue.new_queue("alerts")
    connection = Connection()
    users_ids = connection.get_user()

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

    t1 = Thread(target=notify_up, args=[updater])
    t2 = Thread(target=start_monitoring)
    t3 = Thread(target=get_last_price)
    t1.start()
    t2.start()
    t3.start()
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        CommandHandler("listar", get_alerts, Filters.user(user_id=users_ids))
    )
    dispatcher.add_handler(
        CommandHandler(
            "inserir", insert, Filters.user(user_id=users_ids), pass_args=True
        )
    )
    dispatcher.add_handler(
        CommandHandler(
            "excluir", excluir, Filters.user(user_id=users_ids), pass_args=True
        )
    )
    dispatcher.add_handler(
        CommandHandler("help", help, Filters.user(user_id=users_ids))
    )
    updater.start_polling()
    updater.idle()
"""
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from app.manager_queue import PubSubManager
from conf.settings import TELEGRAM_TOKEN


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello {update.effective_user.first_name}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response_message = (
        f"Olá, eu sou seu bot de investimentos, seu ID é {update.message.chat_id}"
    )
    await update.message.reply_text(response_message)


async def help(update: Update, context):
    response_message = "Menu ainda em construção"
    await update.message.reply_text(
        chat_id=update.message.chat_id, text=response_message
    )


def unknown(update, context):
    response_message = (
        "Não entendi. você pode consultar o menu de opções enviando /help"
    )
    context.bot.send_message(chat_id=update.message.chat_id, text=response_message)


if __name__ == "__main__":
    print("press CTRL + C to cancel.")

    queue = PubSubManager()
    queue.new_queue("alerts")
    # connection = Connection()
    # users_ids = connection.get_user()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CommandHandler("hello", hello))

    app.add_handler(CommandHandler("help", help))

    app.run_polling(allowed_updates=Update.ALL_TYPES)
