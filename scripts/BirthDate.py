from helpers.utils import sort_actual, to_up_date, map_month
import datetime
from db.db_impl import get_members_for_chat, get_members_and_chats_id
import logging
from helpers.utils import validate_date

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)


def get_birth_from_db(chat_id):
    data = get_members_for_chat(chat_id)
    list_of_birth = []
    for member in data:
        tmp = str(member[0]).split("\n")
        tmp[1] = validate_date(tmp[1])
        list_of_birth.append(tmp)

    return list_of_birth


def get_birth_and_chat_from_db():
    data = get_members_and_chats_id()
    list_of_birth = []
    for member in data:
        tmp = str(member[0]).split("\n")
        tmp[1] = validate_date(tmp[1])
        list_of_birth.append([tmp, member[1]])

    return list_of_birth


today = datetime.datetime.now()
logger.info(today)

def get_message_birth(chat_id):
    list_of_birth = get_birth_from_db(chat_id)
    message_string = ""
    check_birth_list = []
    for dates in list_of_birth:
        if today.month == dates[1].tm_mon:
            timestamp = dates[1].tm_mday - today.day
            check_birth_list.append([timestamp, dates])

    for actual_birth in sorted(check_birth_list, key=sort_actual, reverse=True):
        if actual_birth[0] == 0:
            message_string += f"\nСегодня день рождения у {actual_birth[1][0]}!!!\nЕму/ей {today.year - actual_birth[1][1].tm_year}!\n\n"
        elif actual_birth[0] in range(1, 31):
            message_string += f"{actual_birth[1][0]} через {actual_birth[0]} дней ({actual_birth[1][1].tm_mday} {map_month(actual_birth[1][1].tm_mon)}) \n"
        elif actual_birth[0] in range(-31, 0):
            message_string += f"{actual_birth[1][0]} был {actual_birth[0] * (-1)} дней назад ({actual_birth[1][1].tm_mday} {map_month(actual_birth[1][1].tm_mon)})\n"
    return message_string


def get_all_birth(chat_id):
    list_of_birth = get_birth_from_db(chat_id)
    message_string = "Все др ваших братишек:\n\n"
    i = 0
    for dates in sorted(list_of_birth, key=to_up_date, reverse=True):
        message_string += f"{dates[0]} - {dates[1].tm_mday} {map_month(dates[1].tm_mon)}\n"
        i += 1

    return message_string


def get_today_birth():
    list_of_actual_birth = []
    for date in get_birth_and_chat_from_db():
        if today.month == date[0][1].tm_mon and today.day + 1 == date[0][1].tm_mday:
            list_of_actual_birth.append(date)

    return list_of_actual_birth
