# auto-reporting-fake-channels

І так це спеціальний скріпт, який підключається до вашого телеграма і дивитися повідомлення з згадкою - фейк каналів, каналів де за мітки платять і автоматично відправляє репорт на ці канали. Ви просто запускаєте і воно в фоновому режимі дудосить СЕПАРАВСЬКІ канали.

## Також хочу повідомити що ваші данні нікуди не відправляються, ні номер телефону, ні пароль, нічого. Все локально і ви все можете відслідкувати в файлі або в консолі. Також ті хто шарять код можуть побачити що в коді не використовується жодне підключення до Баз Даних. Бібліотека `telethon` повністю провірена і верефіцірована самим Telegram'ом.

#### Подивитися слова трігери можна в файлі `main.py з 11 по 29 строку`

## В вас можуть попросити пароль від Telegram, якщо у вас стоїть двухфакторная авторизація. Не переживайте, він також ні куди не записується і не відсилається !!! Його попросять лише один раз!

# Installing
Для цього просто потратьте 2 хвилини на налаштування.

### Створення додатку в Telegram:
1. Спочатку перейдіть на сайт https://my.telegram.org/auth
2. Пройдіть авторизацію.
3. Далі перейдіть на вкладку `API development tools`
![image](https://user-images.githubusercontent.com/68950796/155895319-835ce948-6070-4835-bb05-5d13a9e62727.png)
4. Створіть новий додаток. (офф документація - https://core.telegram.org/api/obtaining_api_id)
5. Після того як ви створили вам буде потрібно взяти звідти вот ці данні: 
![image](https://user-images.githubusercontent.com/68950796/155895646-f90c0f15-b598-426a-8ae4-a7db7bc56043.png)<br>
Їх нікому не показуйте!!!
6. Далі ці данні вам потрібно буде використати при запуску программи.

### Запуск програми для тих хто шарить код ^^ :
```
git clone https://github.com/zakharfsk/auto-reporting-fake-channels.git
cd auto-reporting-fake-channels
pip install -r requirements.txt
python main.py
```
Далі по підсказках в консолі.

### Запуск програми для тих не хто шарить код ^^:
Comming soon... ( В процесі розробки.

## Допомога
Якщо ви хочете допомогти з кодом можете написати в [Offer help](https://github.com/zakharfsk/auto-reporting-fake-channels/issues/1)<br>
Якщо ви хочете запропонувати нові trigger слова пишіть в [Add new triggre letters](https://github.com/zakharfsk/auto-reporting-fake-channels/issues/2)
