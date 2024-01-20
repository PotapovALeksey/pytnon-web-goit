import re
from regexp import ARCHIVE_REGEXP

symbols = (
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
    "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA",
)

dictionary = {ord(a): ord(b) for a, b in zip(*symbols)}

REGEXP = r"[^\w]"


def transliterate(text: str):
    return text.translate(dictionary)


def clear_name(filename: str):
    if "." in filename:
        name, file_format = filename.rsplit(".", 1)
        cleared_name = re.sub(REGEXP, "", name)

        return ".".join((cleared_name, file_format))
    else:
        return filename


def normalize_name(filename: str):
    return transliterate(clear_name(filename))


def clear_archive_name(archive_name):
    return re.sub(ARCHIVE_REGEXP, "", archive_name)
