import re


def password_check(password):
    return False if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password) else True

