import json
import os
import re
from getpass import getpass

import telethon
from telethon import functions, types
from telethon.errors.rpcerrorlist import SessionPasswordNeededError
from telethon.sync import TelegramClient, events

triggers = [
    'забанити',
    'бан',
    'Канали, які зазнечені нижче постять інфу про наші війська',
    'постять інфу про наші війська',
    'На цих Telegram-каналах зливають розташування наших війск',
    'Будь ласка, блокуйте їх скаргами',
    'Як блокувати?',
    'канал, що зливає інфу',
    'канал що зливає інфу',
    'Крупный новостной канал, сливают кучу инфы о местоположении наших военных и не только.'
    'Кто может, добавьте в общий список целей',
    'Канал платить за мітки на дорогах',
    'платить за мітки',
    'платить за мітки на дорогах',
    'Канали Росії, з пропагандою',
    'тг канал з мітками',
    'канал з мітками',
    'тг канал з метками',
    'Репорт загарбникам',
    'Репорт'
] # Слова тріги, тобто на які спрацьовує репорт каналів


try:
    if not os.path.exists(r'settings.json'): # налаштування

        PHONE_NUMBER = input('Input your telephone number: ')
        API_ID = int(input('Input API_ID (datails in documentation): '))
        API_HASH = input('Input API_HASH (datails in documentation): ')

        with open('settings.json', 'w+', encoding='UTF-8') as st:
            json.dump({
                'phone_number': PHONE_NUMBER,
                'api_id': API_ID,
                'api_hash': API_HASH
            }, st)
            st.close()
        print('Your data succsesfull write to settings.json. You can open and see.')
    else:
        with open('settings.json', 'r+', encoding='UTF-8') as st:
            data = json.load(st)

        PHONE_NUMBER = data['phone_number']
        API_ID = data['api_id']
        API_HASH = data['api_hash']
        st.close()
        print('Your data succsesfull get from settings.json. You can open and see.')
        
except ValueError:
    print('API_ID must be integer')

client = TelegramClient(PHONE_NUMBER, API_ID, API_HASH) # створення підключення до вашого ТГ
client.connect()

try:
    if not client.is_user_authorized():
        client.send_code_request(PHONE_NUMBER)
        client.sign_in(PHONE_NUMBER, getpass(
            'Еnter the code sent to you in the telegram: ')) 
except SessionPasswordNeededError as err: # якщо у вас підключеня двухфакторная авторизація то спрацює код нижче, якщо ні то пароль не попросять
    client.sign_in(password=getpass('Enter the password from your telegram: '))


@client.on(events.NewMessage)
async def check(event: events.NewMessage.Event): # функція для проглядання каналів в Тг і виявлення феків
    for i in range(len(triggers)):
        if triggers[i].lower() in event.text.lower():
            urls = re.findall(r'(?P<url>https?://[^\s]+)', event.text)
            usernames = re.findall(r'(@[^\s],+)', event.text)

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
                except ValueError:
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
                except ValueError:
                    pass
            break

client.start() # запуск програми
client.run_until_disconnected() # програма буде працювати поки ви самі не відключете
