
import re

from sweet_cash.settings import Settings


def check_email_format(email: str):
    regex = Settings.EMAIL_REGEX
    result = re.fullmatch(regex, email)
    return result


def check_phone_format(phone: str):
    regex = Settings.PHONE_REGEX
    result = re.fullmatch(regex, phone)
    return result


def check_password_format(password: str):
    regex = Settings.PASSWORD_REGEX
    result = re.fullmatch(regex, password)
    return result


def ids2list(ids):
    if type(ids) is list:
        return ids

    ids_list = []

    if ids is None:
        return ids_list

    split_list = ids.split(',')

    for elem in split_list:
        try:
            ids_list.append(int(elem))
        except ValueError:
            continue

    return ids_list
