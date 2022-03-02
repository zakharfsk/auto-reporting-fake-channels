from ast import While
import asyncio
import json
import logging
import os
import re
import time
from colorama import Fore, Back, init

from telethon import functions, types
from telethon.errors.rpcerrorlist import (PasswordHashInvalidError,
                                          PhoneNumberInvalidError,
                                          SessionPasswordNeededError,
                                          FloodWaitError)
from telethon.sync import TelegramClient, events

triggers = []
fake_channels = []

init(autoreset=True)

# Слова тріги, тобто на які спрацьовує репорт каналів
try:
    with open(r'triggres_word.txt', 'r', encoding='UTF-8') as file:
        words = file.readlines()

    with open(r'fake_channels.txt', 'r', encoding='UTF-8') as file:
        channels = file.readlines()
except FileNotFoundError:
    print(Fore.RED + 'File not found in derectory. Pleas restart program.')

for trigger in words:
    triggers.append(trigger.rstrip('\n'))

for channel in channels:
    fake_channels.append(channel.rstrip('\n'))


def get_data_for_connect():
    PHONE_NUMBER = input('Input your telephone number: ')
    API_ID = int(input('Input API_ID (datails in documentation): '))
    API_HASH = input('Input API_HASH (datails in documentation): ')

    with open('settings.json', 'w+', encoding='UTF-8') as st:
        json.dump({
            'phone_number': PHONE_NUMBER,
            'api_id': API_ID,
            'api_hash': API_HASH
        }, st)

    print('Your data succsesfull write to settings.json. You can open and see.')

    return PHONE_NUMBER, API_ID, API_HASH


if not os.path.exists(r'settings.json'):  # налаштування
    try:
        data_for_connect = get_data_for_connect()

        # створення підключення до вашого ТГ
        client = TelegramClient(data_for_connect[0], data_for_connect[1], data_for_connect[2])
        client.connect()

        try:
            if not client.is_user_authorized():
                client.send_code_request(data_for_connect[0])
                client.sign_in(data_for_connect[0], input(
                    Fore.BLUE + 'Еnter the code sent to you in the telegram: '))
        # якщо у вас підключеня двухфакторная авторизація то спрацює код нижче, якщо ні то пароль не попросять
        except SessionPasswordNeededError as err:
            try:
                client.sign_in(password=input(
                    'Enter the password from your telegram: '))
            except PasswordHashInvalidError:
                client.sign_in(password=input(
                    Fore.RED + 'Invalid password. Please try again: '))
        print(Fore.GREEN + 'Program start...')
    except ValueError:
        print(Fore.RED + 'API_ID must be integer.')
        data_for_connect = get_data_for_connect()

        # створення підключення до вашого ТГ
        client = TelegramClient(data_for_connect[0], data_for_connect[1], data_for_connect[2])
        client.connect()

        try:
            if not client.is_user_authorized():
                client.send_code_request(data_for_connect[0])
                client.sign_in(data_for_connect[0], input(
                    Fore.BLUE + 'Еnter the code sent to you in the telegram: '))
        # якщо у вас підключеня двухфакторная авторизація то спрацює код нижче, якщо ні то пароль не попросять
        except SessionPasswordNeededError as err:
            try:
                client.sign_in(password=input(
                    'Enter the password from your telegram: '))
            except PasswordHashInvalidError:
                client.sign_in(password=input(
                    Fore.RED + 'Invalid password. Please try again: '))

        print(Fore.GREEN + 'Program start...')

    except PhoneNumberInvalidError:
        print(Fore.RED + 'You enter invalid telephon number. Pleas enter again.')
        data_for_connect = get_data_for_connect()

        # створення підключення до вашого ТГ
        client = TelegramClient(data_for_connect[0], data_for_connect[1], data_for_connect[2])
        client.connect()

        try:
            if not client.is_user_authorized():
                client.send_code_request(data_for_connect[0])
                client.sign_in(data_for_connect[0], input(
                    Fore.BLUE + 'Еnter the code sent to you in the telegram: '))
        # якщо у вас підключеня двухфакторная авторизація то спрацює код нижче, якщо ні то пароль не попросять
        except SessionPasswordNeededError as err:
            try:
                client.sign_in(password=input(
                    'Enter the password from your telegram: '))
            except PasswordHashInvalidError:
                client.sign_in(password=input(
                    Fore.RED + 'Invalid password. Please try again: '))

        print(Fore.GREEN + 'Program start...')
else:
    with open('settings.json', 'r+', encoding='UTF-8') as st:
        data = json.load(st)

    PHONE_NUMBER = data['phone_number']
    API_ID = data['api_id']
    API_HASH = data['api_hash']

    print(Fore.GREEN + 'Your data succsesfull get from settings.json. You can open and see.')

    # створення підключення до вашого ТГ
    client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH)
    client.connect()

    print(Fore.GREEN + 'Program start...')

status = True

@client.on(events.NewMessage)
# функція для проглядання каналів в Тг і виявлення феків
async def check(event: events.NewMessage.Event):
    for i in range(len(triggers)):
        if triggers[i].lower() in event.text.lower():
            status = False

            urls = re.findall(r'(?P<url>https?://[^\s]+)', event.text)
            usernames = re.findall(r'(@[^\s|()]+)', event.text)

            print(
                Fore.YELLOW +
                f'In channel: {event.chat.title}\n\n'
                f'Urls find: {urls}\n'
                f'Username find: {usernames}\n\n'
            )

            print(Fore.GREEN + 'Start reporting')

            for username in usernames:
                try:
                    channel_info_by_username = await client.get_entity(username)

                    result = await client(functions.messages.ReportRequest(  # відправка репорта на канал
                        peer=channel_info_by_username,
                        id=[1],
                        reason=types.InputReportReasonOther(),
                        message='Неправдива інформація про війну Росії з Україною\n'
                        'Неправдивая информация о войне России с Украиной\n'
                        'False information about Russia\'s war with Ukraine\n'
                        'Propaganda of the war in Ukraine. Propaganda of the murder of Ukrainians and Ukrainian soldiers.\n'
                        'Пропаганда війни в Україні. Пропаганда вбивства українців та українських солдат.'))
                    # якщо статус True то канал успішно зарепорчений
                    print(Fore.YELLOW + f'Channel {channel_info_by_username.title} reported.' 'Status: ' + str(result))
                    await asyncio.sleep(5)
                except FloodWaitError as err:
                    print(Back.RED + f'You send reports very often, please wait {err.seconds}')
                    print(Fore.BLUE + f'Set pause 60 second')
                    await asyncio.sleep(60)

                except Exception as err:
                    pass

            for url in urls:
                try:
                    channel_info_by_url = await client.get_entity(url)

                    result = await client(functions.messages.ReportRequest(  # відправка репорта на канал
                        peer=channel_info_by_url,
                        id=[1],
                        reason=types.InputReportReasonOther(),
                        message='Неправдива інформація про війну Росії з Україною\n'
                        'Неправдивая информация о войне России с Украиной\n'
                        'False information about Russia\'s war with Ukraine\n'
                        'Propaganda of the war in Ukraine. Propaganda of the murder of Ukrainians and Ukrainian soldiers.\n'
                        'Пропаганда війни в Україні. Пропаганда вбивства українців та українських солдат.'))
                    # якщо статус True то канал успішно зарепорчений
                    print(Fore.GREEN + f'Channel {channel_info_by_url.title} is reported. Status: ' + str(result))
                    await asyncio.sleep(5)
                except FloodWaitError as err:
                    print(Back.RED + f'You send reports very often, please wait {err.seconds}')
                    print(Fore.BLUE + f'Set pause 60 second')
                    await asyncio.sleep(60)

                except Exception as err:
                    pass
            break
    try:
        urls = re.findall(r'(?P<url>https?://[^\s]+)', event.text)
        usernames = re.findall(r'(@[^\s]+)', event.text)

        print(
            Fore.YELLOW +
            f'\nIn channel: {event.chat.title}\n'
            f'Urls find: {urls}\n'
            f'Username find: {usernames}\n'
        )
    except Exception as err:
        pass
    finally:
        status = True

async def task_report():
    while status:
        for channel in fake_channels:
            try:
                channel_info_by_url = await client.get_entity(channel)

                result = await client(functions.messages.ReportRequest(  # відправка репорта на канал
                    peer=channel_info_by_url,
                    id=[1],
                    reason=types.InputReportReasonOther(),
                    message='Неправдива інформація про війну Росії з Україною\n'
                    'Неправдивая информация о войне России с Украиной\n'
                    'False information about Russia\'s war with Ukraine\n'
                    'Propaganda of the war in Ukraine. Propaganda of the murder of Ukrainians and Ukrainian soldiers.\n'
                    'Пропаганда війни в Україні. Пропаганда вбивства українців та українських солдат.')) # якщо статус True то канал успішно зарепорчений
                print(Fore.GREEN + f'Channel {channel_info_by_url.title} is reported. Status: ' + str(result))
                await asyncio.sleep(5)

            except FloodWaitError as err:
                print(Back.RED + f'You send reports very often, please wait {err.seconds}')
                print(Fore.BLUE + f'Set pause 60 second')
                await asyncio.sleep(60)

            except Exception as err:
                pass

if __name__ == '__main__':
    asyncio.get_event_loop().create_task(task_report())

    client.start()  # запуск програми
    # програма буде працювати поки ви самі не відключете
    client.run_until_disconnected()
