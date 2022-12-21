from aiogram import types,exceptions,Dispatcher,Bot,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN_API
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram.dispatcher import FSMContext
from sqlite import db_start, edit_profile, create_profile

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())

class ProfileStateGroup(StatesGroup):
    photo = State()
    name = State()
    age = State()
    description = State()

async def on_startup(_):
    await db_start()

def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/create'))
    return kb

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    await message.answer("Welcome")
    await create_profile(user_id=message.from_user.id)


@dp.message_handler(commands=['log'])
async def cmd_create(message: types.Message) -> None:
    await message.answer("Let's create your Profile! to begin, send me your name")

@dp.message_handler(state=ProfileStateGroup.name)
async def load_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply("Now, send me your age!")
    await ProfileStateGroup.next()

@dp.message_handler(state=ProfileStateGroup.age)
async def load_age(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['age'] = message.text
    await message.reply("Now, tell me something about you!")
    await ProfileStateGroup.next()

@dp.message_handler(state=ProfileStateGroup.description)
async def load_description(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['description'] = message.text
        await message.reply("Now, send in a profile picture")
        await ProfileStateGroup.next()
        await ProfileStateGroup.photo.set()


@dp.message_handler(content_types=['photo'], state=ProfileStateGroup.photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await bot.send_photo(message.from_user.id, photo=data['photo'],
                             caption=f"{data['name'], data['age'], data['description']}")
    await edit_profile(state, user_id=message.from_user.id)
    await message.reply("Completed!")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup)
