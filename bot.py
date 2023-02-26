import config 
import logging
from orders import get_new_orders, orders_formatter
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType

# logging
logging.basicConfig(level=logging.INFO)

# INITIALIZATION
bot = Bot(config.bot_token)
dp = Dispatcher(bot)

# PRICES
PRICE = [types.LabeledPrice(label="Курс по варению красиваого, целебного мыло.", amount=500*100)]

# BUTTONS AND KEYBOARDS
wanna2buy_button = KeyboardButton('Купить курс')
get_orders_button = KeyboardButton('Новые заказы')
buttons_for_boss = [[wanna2buy_button, get_orders_button]]

keyboard_for_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(wanna2buy_button)
keyboard_for_boss = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard = buttons_for_boss)

def user_is_boss(user_id):
    return user_id in (704339275, 941095113, 5093633989, 407594558)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if user_is_boss(message.from_user.id):
        await message.reply("Привет!", reply_markup=keyboard_for_boss)
    else:   
        await message.reply("Привет!", reply_markup=keyboard_for_user)


@dp.message_handler()
async def buy(message: types.Message):
    if message.text == "Новые заказы" and user_is_boss(message.from_user.id):
        orders = orders_formatter(get_new_orders())
        if orders:
            for order in orders:
                await bot.send_message(message.chat.id, order)
        else:
            await bot.send_message(message.chat.id, 'Новых заказов ещё нет')
    else:
        await bot.send_invoice(message.chat.id, title="Курс по мыловарению", description='Мыловарение с нуля для начинающих с полезными добавками холодным способом.', provider_token=config.payments_token, currency='rub', photo_width=1183, photo_height=1183, photo_url="https://sun9-56.userapi.com/impg/ZnMiQGk3EtfduLoaxh692l5kE-VB3MBb08uMZw/41dJ9SosqKM.jpg?size=1183x1183&quality=95&sign=fcc9a774e7ea8e74c9ffb2655f955f79&type=album", is_flexible=False, prices=PRICE, start_parameter='dasdfasdf', payload='test-invoice-payload',)

# pre checkout 
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

async def send_order_data2boss(message):
    await bot.send_message(704339275, message)

# successfully payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def adding2channel(message: types.Message):
    link_for_course = await bot.create_chat_invite_link(-1001873710732, member_limit=1)
    link_for_support = await bot.create_chat_invite_link(-1001502001720, member_limit=1)
    await bot.send_message(message["chat"]["id"], 'Канал курса:' + link_for_course.invite_link)    
    await bot.send_message(message["chat"]["id"], "Чат поддержки:" + link_for_support.invite_link)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)