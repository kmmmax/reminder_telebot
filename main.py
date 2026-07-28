from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
import asyncio
import sqlite3
import datetime

TOKEN = 
PROXY = "socks5://127.0.0.1:10808"

session = AiohttpSession(proxy=PROXY)
conn = sqlite3.connect("main.db")
cursor = conn.cursor()

allowed_hours = []
for i in range(0, 24):
    i_str = str(i)
    if len(i_str) == 1:
        i_str = "0" + i_str
    allowed_hours.append(i_str)

allowed_minutes = []
for i in range(0, 60):
    i_str = str(i)
    if len(i_str) == 1:
        i_str = "0" + i_str
    allowed_minutes.append(i_str)

allowed_days = []
for i in range(1, 32):
    i_str = str(i)
    if len(i_str) == 1:
        i_str = "0" + i_str
    allowed_days.append(i_str)

allowed_months = []
for i in range(1, 13):
    i_str = str(i)
    if len(i_str) == 1:
        i_str = "0" + i_str
    allowed_months.append(i_str)

allowed_years = []
for i in range(int(str(datetime.datetime.now().year)[2:4]), 41):
    i_str = str(i)
    allowed_years.append(i_str)

def check_compatability(day: str, month: str, year: str) -> int:
    if month == "01" or month == "03" or month == "05" or month == "07" or month == "08" or month == "10" or month == "12":
        if day in allowed_days:
            return 1
        else:
            return 0
    if month == "04" or month == "06" or month == "09" or month == "11":
        if day in allowed_days[:30]:
            return 1
        else:
            return 0
    if month == "02":
        if int("20"+str(year)) % 4 == 0 and ((int("20"+str(year)) % 100 != 0) or (int("20"+str(year)) % 400 == 0)):
            if day in allowed_days[:29]:
                return 1
            else:
                return 0
        else:
            if day in allowed_days[:28]:
                return 1
            else:
                return 0
    return 0

def check_time(source: str) -> int:
    minute = ""
    hour = ""
    day = ""
    month = ""
    year = ""
    score = 0
    score_2 = 0
    final_score = 0

    if len(source) == 14 and " " in source:
        source_splited = source.split()
        for el in source_splited:

            if el == source_splited[0]:
                if len(el) == 5:
                    part_one_splited = el.split(":")
                    for i in part_one_splited:
                        if len(i) == 2:
                            score += 1
                    if score == 2:
                        for i in part_one_splited:
                            if i == part_one_splited[0]:
                                if i in allowed_hours:
                                    final_score += 1
                                hour = i
                            if i == part_one_splited[1]:
                                if i in allowed_minutes:
                                    final_score += 1
                                minute = i

            if el == source_splited[1]:
                if len(el) == 8:
                    part_two_splited = el.split(".")
                    for x in part_two_splited:
                        if len(x) == 2:
                            score_2 += 1
                    if score_2 == 3:
                        for x in part_two_splited:
                            if x == part_two_splited[0]:
                                if x in allowed_days:
                                    final_score += 1
                                day = x
                            if x == part_two_splited[1]:
                                if x in allowed_months:
                                    final_score += 1
                                month = x
                            if x == part_two_splited[2]:
                                if x in allowed_years:
                                    final_score += 1
                                year = x
        if final_score == 5:
            final_score += check_compatability(day, month, year)
            if final_score == 6:
                input_datetime = datetime.datetime(2000 + int(year), int(month), int(day), int(hour), int(minute))
                now = datetime.datetime.now()
                if input_datetime - now >= datetime.timedelta(minutes=2):
                    return 1
                else:
                    return 0
    return 0

def get_all_time(source: str) -> str:
    list = source.split()
    if len(list) == 3:
        if len(list[0]) == 5 and len(list[1]) == 8:
            return (f"{list[0]} {list[1]}")
    return ""

def get_name(source: str) -> str:
    list = source.split()
    if len(list) == 3:
        if len(list[0]) == 5 and len(list[1]) == 8:
            if len(list[2]) > 2 and len(list[2]) < 41:
                return list[2]
    return ""

waiting = {}
another_waiting = {}

bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()


@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Привет 👋! Это бот для напоминаний, написанный по фану\n\
за 2 дня. Полностью в рабочем состоянии. Команды для использования:\n\
/start = увидеть этот бессмысленный текст еще раз\n\
/set_reminder = самая важная команда для создания напоминаний\n\
/del_reminder = удалить существующее напоминание\n\
/show_all = показать все твои напоминания")


@dp.message(Command("set_reminder"))
async def set_reminder(message: Message):
    await message.answer(' Укажите время вашего напоминания. ⏰\n\
Формат "ЧЧ:ММ ДД.ММ.ГГ ИМЯ_НАПОМИНАНИЯ"\n\
Пример: "23:38 23.07.26 Поиграть_в_майнкрафт"\n\
'' \n\
Правила создания: \n\
❌ Напоминания с прошедшим временем не будут зачтены.\n\
❌ Напоминания с годом позже чем 2040 не будут зачтены.\n\
❌ В именах запрещены пробелы.\n\
✅ Длина имени от 3 до 40 символов.\n\
✅ Минимальный срок - 5 минут от текущего времени.\n\
Например: сейчас 13:40 -> можно указать только 13:45 и позже.\n\
'' \n\
Ввод: ')
    
    tg_id = message.from_user.id

    waiting[tg_id] = True


@dp.message(Command("del_reminder"))
async def del_reminder(message: Message):
    await message.answer('🗑️ Укажите ID (!) напоминания, которое хотите удалить\n\
''\n\
Ввод:')
    
    tg_id = message.from_user.id
    another_waiting[tg_id] = True


@dp.message(Command("show_all"))
async def show_all(message: Message):
    tg_id = message.from_user.id
    sum = cursor.execute("SELECT COUNT(id) FROM reminders WHERE tg_id = (?)", (tg_id,)).fetchone()[0]
    if sum == 0:
        await message.answer("😟 Напоминаний нет")
    else:
        names = cursor.execute("SELECT name FROM reminders WHERE tg_id = (?)", (tg_id,)).fetchall()
        times = cursor.execute("SELECT time FROM reminders WHERE tg_id = (?)", (tg_id,)).fetchall()
        dates = cursor.execute("SELECT date FROM reminders WHERE tg_id = (?)", (tg_id,)).fetchall()
        ids = cursor.execute("SELECT id FROM reminders WHERE tg_id = (?)", (tg_id,)).fetchall()
        text = "📌 Список напоминаний\n"
        for i in range(0, sum):
            name_for_answer = names[i][0]
            time_for_answer = times[i][0]
            date_for_answer = dates[i][0]
            id_for_answer = ids[i][0]
            text += (f"{i+1}. Имя: {name_for_answer} | ID: {id_for_answer} | Время: {time_for_answer} | Дата: {date_for_answer}\n")
        await message.answer(f"{text}")

    
@dp.message()
async def check(message: Message):
    tg_id = message.from_user.id
    if waiting.get(tg_id) == True:
        waiting[tg_id] = False
        answer = message.text
        all_time = get_all_time(answer)
        name_of_reminder = get_name(answer)
        if len(all_time) == 0 or len(name_of_reminder) == 0:
            await message.answer("🚫 Вы что-то указали не так (см. правила)")
            return
        result = check_time(all_time)
        if result == 1:
            try:
                data = cursor.execute("SELECT * FROM reminders WHERE tg_id = (?) AND time = (?) AND date = (?) AND name = (?)", (tg_id, all_time[0:5], all_time[6:14], name_of_reminder)).fetchone()
                if data is None:
                    cursor.execute("INSERT INTO reminders (tg_id, time, date, name) VALUES (?, ?, ?, ?)", (tg_id, all_time[0:5], all_time[6:14], name_of_reminder))
                    id = cursor.lastrowid
                    await message.answer("✅ " + f"Напоминание успешно сохранено. Его ID - {id}")
                    conn.commit()
                else:
                    await message.answer("🚫 Не удалось создать: точно такое же напоминание уже находится в базе!")
            except:
                    await message.answer("🚫 Проблема с базой данных")
        elif result == 0:   
            await message.answer("🚫 Вы что-то указали не так (см. правила)")
    elif another_waiting.get(tg_id) == True:
        another_waiting[tg_id] = False
        answer = message.text
        try:
            answer = int(answer)
        except:
            await message.answer("🚫 Вы ввели не цифры. Для удаления необходим ID напоминания")
            return
        try:
            test_data = cursor.execute("SELECT * FROM reminders WHERE id = (?)", (int(answer),)).fetchone()
            if test_data is not None:
                tg_id_from_base = cursor.execute("SELECT tg_id FROM reminders WHERE id = (?)", (int(answer),)).fetchone()[0]
                if (tg_id == tg_id_from_base):
                    cursor.execute("DELETE FROM reminders WHERE id = (?)", (int(answer),))
                    conn.commit()
                    await message.answer("✅ Напоминание успешно удалено")                   
                else:
                    await message.answer("🚫 Данное напоминание не ваше")
            else:
                await message.answer("🚫 По такому ID нет напоминаний!")
        except:
            await message.answer("🚫 Проблема с базой данных")
    else:
        await message.answer("🚫 Неизвестная команда")


async def scaner() -> None:
    while True:
        all_table = cursor.execute("SELECT * FROM reminders").fetchall()

        now_time = datetime.datetime.now().strftime("%H:%M")
        now_date = datetime.datetime.now().strftime("%d.%m.%y")

        for i in all_table:
            if (i[2] == now_time) and (i[3] == now_date):
                current_id = cursor.execute("SELECT id FROM reminders WHERE time = (?) AND date = (?)", (now_time, now_date)).fetchone()[0]
                current_tg_id = cursor.execute("SELECT tg_id FROM reminders WHERE id = (?)", (current_id,)).fetchone()[0]
                current_name = cursor.execute("SELECT name from reminders WHERE id = (?)", (current_id,)).fetchone()[0]
                cursor.execute("DELETE FROM reminders WHERE id = (?)", (current_id,))
                conn.commit()
                await bot.send_message(current_tg_id, "🔔 " + f'Напоминание с именем "{current_name}"!!! (ID - {current_id})')
        await asyncio.sleep(30)


async def main():
    asyncio.create_task(scaner())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
