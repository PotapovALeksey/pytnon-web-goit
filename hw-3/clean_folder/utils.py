import re
from pathlib import Path
from regexp import (
    ARCHIVE_REGEXP,
    IMAGE_REGEXP,
    VIDEO_REGEXP,
    DOCUMENT_REGEXP,
    AUDIO_REGEXP,
)
from normalize import clear_archive_name

ARCHIVES_DIRECTORY_NAME = "archives"
IMAGES_DIRECTORY_NAME = "images"
VIDEO_DIRECTORY_NAME = "video"
DOCUMENTS_DIRECTORY_NAME = "documents"
AUDIO_DIRECTORY_NAME = "audio"

SYSTEM_DIRECTORY_NAMES = (
    ARCHIVES_DIRECTORY_NAME,
    IMAGES_DIRECTORY_NAME,
    VIDEO_DIRECTORY_NAME,
    DOCUMENTS_DIRECTORY_NAME,
    AUDIO_DIRECTORY_NAME,
)


def is_matched(regexp: str, file_name: str):
    result = re.search(regexp, file_name)

    return bool(result)


def is_file_archive(file_name: str):
    result = re.search(ARCHIVE_REGEXP, file_name)

    return result is not None


def get_directory_name(file_name: str):
    if is_matched(IMAGE_REGEXP, file_name):
        return IMAGES_DIRECTORY_NAME

    if is_matched(VIDEO_REGEXP, file_name):
        return VIDEO_DIRECTORY_NAME

    if is_matched(DOCUMENT_REGEXP, file_name):
        return DOCUMENTS_DIRECTORY_NAME

    if is_matched(AUDIO_REGEXP, file_name):
        return AUDIO_DIRECTORY_NAME

    if is_matched(ARCHIVE_REGEXP, file_name):
        return ARCHIVES_DIRECTORY_NAME

    return ""


def get_archive_directory(file: Path):
    return str(file.absolute()).replace(file.name, clear_archive_name(file.name))
