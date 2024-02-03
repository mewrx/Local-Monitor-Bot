import asyncio
import os
import ast
import logging
import delegator

from dotenv import find_dotenv, load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message


load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('TG_TOKEN'))
dp = Dispatcher()


def do_as_sudo():
    logging.info('Starting scanning for all local devices')
    password = os.getenv('PASSWD')
    c = delegator.chain(f'echo "{password}" | sudo -S python3 scaner.py')
    lines = c.out.split('\n')
    lines = lines[1:]
    text = '\n'.join(lines)
    return text


def add_device_names(text):
    load_dotenv(find_dotenv())
    devices = ast.literal_eval(os.getenv('DEVICES'))

    lines = text.splitlines()
    result = []

    for i in range(len(lines)):
        if lines[i].startswith('192'):
            mac = lines[i].split()[-1]
            if mac in devices:
                lines[i] += ' ' + devices[mac]
            else:
                lines[i] += ' ?'
            print(lines[i])
        else:
            print(lines[i])
        result.append(lines[i])
    return '\n'.join(result)


@dp.message(F.text == '/scan')
async def scan_all(message: Message):
    await message.answer(f'{add_device_names(do_as_sudo())}\n')


@dp.message(F.text == '/help')
async def help_msg(message: Message):
    await message.answer('Commands:\n/scan\n/help')


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        logging.info("Bot started")
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
