### Специфікація завдання
Завершіть реалізацію вашої енциклопедії Wiki з урахуванням наступних вимог:

- Сторінка статті: Перехід на /wiki/TITLE, де TITLE - це назва енциклопедичної статті, має відобразити сторінку, що показує вміст цієї статті.
    - Представлення має отримувати вміст статті за допомогою виклику відповідної функції util.
    - Якщо стаття, яку хоче відкрити користувач, не існує, йому має бути показана сторінка помилки, де буде зазначено, що потрібну статтю не знайдено.
    - Якщо стаття існує, користувач має побачити сторінку, що відображає вміст статті. Назва сторінки має містити назву статті.
- Сторінка index: Змініть index.html так, щоб замість того, щоб побачити звичайний перелік назв усіх сторінок в енциклопедії, користувач міг натиснути на назву статті, щоб перейти безпосередньо на сторінку цієї статті.
- Пошук: Дозвольте користувачу набрати запит у полі пошуку на бічній панелі, щоб відшукати статтю в енциклопедії.
    - Якщо запит збігається з назвою статті, користувач має бути направлений на сторінку цієї статті.
    - Якщо запит не збігається з назвою статті, користувач має бути направлений на сторінку результатів пошуку, яка відображає список всіх статей енциклопедії, що містять цей запит в підрядку. Наприклад, якщо пошуковий запит був ytho, в результатах пошуку повинен з'явитися Python.
    - Натискання на будь-яку назву статті в результатах пошуку має переносити користувача на сторінку цієї статті.
- Нова сторінка: Натискання на «Create New Page» на бічній панелі має переносити користувача на сторінку, де він зможе створити нову енциклопедичну статтю.
    - Користувач повинен мати змогу ввести назву сторінки і у textarea ввести Markdown-наповнення для сторінки.
    - Користувач повинен мати змогу натиснути кнопку для збереження своєї нової сторінки.
    - Коли сторінку збережено, у випадку, якщо енциклопедична стаття з наданою назвою вже існує, користувач має отримати повідомлення про помилку.
    - В іншому випадку енциклопедичну статтю має бути збережено на диск, а користувача треба перенести на сторінку цієї нової статті.
- Редагування сторінки: На сторінці кожної статті користувач повинен мати можливість натиснути на посилання, що перенесе його на сторінку, де він зможе змінити Markdown-наповнення у textarea.
    - textarea має бути попередньо заповнена наявним Markdown-наповненням сторінки (іншими словами, наявний вміст має бути початковим значенням value у textarea).
    - Користувач повинен мати змогу натиснути кнопку, щоб зберегти впроваджені до статті зміни.
    - Після збереження статті користувача має бути перенаправлено назад на сторінку цієї статті.
- Випадкова сторінка: Настискання на «Random Page» на бічній панелі має перенести користувача на випадкову статтю енциклопедії.
    - Конвертування Markdown у HTML: На сторінці кожної статті будь-яке Markdown-наповнення має бути конвертоване в HTML перед тим, як відобразити його для користувача. Щоб виконати це конвертування, ви можете використати пакет python-markdown2, який встановлюється за допомогою pip3 install markdown2.
    - Завдання для впевнених: якщо вам це до снаги, спробуйте впровадити конвертування Markdown у HTML без використання зовнішніх бібліотек зі збереженням заголовків, виділеного шрифту, маркованих списків, посилань та параграфів. Вам може допомогти використання регулярних виразів у Python.