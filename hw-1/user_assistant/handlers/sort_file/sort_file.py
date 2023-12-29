from pathlib import Path
from user_assistant.sort_file.file_sorter import FileSorter
from user_assistant.console.console import Console

from user_assistant.handlers.abstract_handler import AbstractHandler


class SortFileHandler(AbstractHandler):

    def execute(self):
        try:
            folder_for_scan = Console.input('Enter folder for scan: ')
            sorter = FileSorter(Path(folder_for_scan))
            sorter.sort_files()

            Console.print_error('The directory was sorted.')
        except (FileNotFoundError, OSError) as e:
            Console.print_error(f'Error: {e}')