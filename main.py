import json
import os
import re
from getpass import getpass

from telethon import functions, types
from telethon.errors.rpcerrorlist import (PasswordHashInvalidError,
                                          PhoneNumberInvalidError,
                                          SessionPasswordNeededError)
from telethon.sync import TelegramClient, events

triggers = []

with open(r'triggres_word.txt', 'r', encoding='UTF-8') as file: # Слова тріги, тобто на які спрацьовує репорт каналів
    words = file.readlines()

for trigger in words:
    triggers.append(trigger.rstrip('\n'))

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

if not os.path.exists(r'settings.json'): # налаштування
    try:
        data_for_connect = get_data_for_connect()
        
        client = TelegramClient(data_for_connect[0], data_for_connect[1], data_for_connect[2]) # створення підключення до вашого ТГ
        client.connect()

        try:
            if not client.is_user_authorized():
                client.send_code_request(data_for_connect[0])
                client.sign_in(data_for_connect[0], getpass(
                    'Еnter the code sent to you in the telegram: ')) 
        except SessionPasswordNeededError as err: # якщо у вас підключеня двухфакторная авторизація то спрацює код нижче, якщо ні то пароль не попросять
            try:
                client.sign_in(password=getpass('Enter the password from your telegram: '))
            except PasswordHashInvalidError:
                client.sign_in(password=getpass('Invalid password. Please try again: '))
        print('Program start...')
    except ValueError:
        print('API_ID must be integer.')
        data_for_connect = get_data_for_connect()
        
        client = TelegramClient(data_for_connect[0], data_for_connect[1], data_for_connect[2]) # створення підключення до вашого ТГ
        client.connect()

        try:
            if not client.is_user_authorized():
                client.send_code_request(data_for_connect[0])
                client.sign_in(data_for_connect[0], getpass(
                    'Еnter the code sent to you in the telegram: ')) 
        except SessionPasswordNeededError as err: # якщо у вас підключеня двухфакторная авторизація то спрацює код нижче, якщо ні то пароль не попросять
            try:
                client.sign_in(password=getpass('Enter the password from your telegram: '))
            except PasswordHashInvalidError:
                client.sign_in(password=getpass('Invalid password. Please try again: '))

        print('Program start...')
    
    except PhoneNumberInvalidError:
        print('You enter invalid telephon number. Pleas enter again.')
        data_for_connect = get_data_for_connect()
        
        client = TelegramClient(data_for_connect[0], data_for_connect[1], data_for_connect[2]) # створення підключення до вашого ТГ
        client.connect()

        try:
            if not client.is_user_authorized():
                client.send_code_request(data_for_connect[0])
                client.sign_in(data_for_connect[0], getpass(
                    'Еnter the code sent to you in the telegram: ')) 
        except SessionPasswordNeededError as err: # якщо у вас підключеня двухфакторная авторизація то спрацює код нижче, якщо ні то пароль не попросять
            try:
                client.sign_in(password=getpass('Enter the password from your telegram: '))
            except PasswordHashInvalidError:
                client.sign_in(password=getpass('Invalid password. Please try again: '))

        print('Program start...')
else:
    with open('settings.json', 'r+', encoding='UTF-8') as st:
        data = json.load(st)

    PHONE_NUMBER = data['phone_number']
    API_ID = data['api_id']
    API_HASH = data['api_hash']
    
    print('Your data succsesfull get from settings.json. You can open and see.')

    client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH) # створення підключення до вашого ТГ
    client.connect()

    print('Program start...')


@client.on(events.NewMessage)
async def check(event): # функція для проглядання каналів в Тг і виявлення феків
    for i in range(len(triggers)):
        if triggers[i].lower() in event.text.lower():
            urls = re.findall(r'(?P<url>https?://[^\s]+)', event.text)
            usernames = re.findall(r'(@[^\s]+)', event.text)

            for username in usernames: 
                try:
                    channel_info_by_username = await client.get_entity(username)

                    result = await client(functions.messages.ReportRequest( # відправка репорта на канал
                        peer=channel_info_by_username,
                        id=[1],
                        reason=types.InputReportReasonOther(),
                        message='Неправдива інформація про війну Росії з Україною\n'
                        'Неправдивая информация о войне России с Украиной\n'
                        'False information about Russia\'s war with Ukraine\n'
                        'Propaganda of the war in Ukraine. Propaganda of the murder of Ukrainians and Ukrainian soldiers.\n'
                        'Пропаганда війни в Україні. Пропаганда вбивства українців та українських солдат.'))
                    print(f'Channel {channel_info_by_username.title} reported. Status: ' + str(result)) # якщо статус True то канал успішно зарепорчений
                except Exception as err:
                    pass
            
            for url in urls:
                try:
                    channel_info_by_url = await client.get_entity(url)

                    result = await client(functions.messages.ReportRequest( # відправка репорта на канал
                        peer=channel_info_by_url,
                        id=[1],
                        reason=types.InputReportReasonOther(),
                        message='Неправдива інформація про війну Росії з Україною\n'
                        'Неправдивая информация о войне России с Украиной\n'
                        'False information about Russia\'s war with Ukraine\n'
                        'Propaganda of the war in Ukraine. Propaganda of the murder of Ukrainians and Ukrainian soldiers.\n'
                        'Пропаганда війни в Україні. Пропаганда вбивства українців та українських солдат.'))
                    print(f'Channel {channel_info_by_url.title} is reported. Status: ' + str(result)) # якщо статус True то канал успішно зарепорчений
                except Exception as err:
                    pass
            break

client.start() # запуск програми
client.run_until_disconnected() # програма буде працювати поки ви самі не відключете
