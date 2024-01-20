import argparse
from pathlib import Path
from shutil import copyfile, unpack_archive
import logging
from utils import get_directory_name, get_archive_directory, is_file_archive
from normalize import normalize_name
import concurrent.futures

parser = argparse.ArgumentParser(description="App for sorting folder")
parser.add_argument("-s", "--source", type=str)
parser.add_argument("-o", "--output", type=str, default="dist")
args = vars(parser.parse_args())
source = args.get("source")
output = args.get("output")

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")


def get_folders(path: Path) -> [Path]:
    folders = [path]

    for folder in path.iterdir():
        if folder.is_dir():
            folders.append(folder)
            get_folders(folder)

    return folders


def copy_file(file: Path, normalized_file_name: str) -> Path:
    new_path = output_path / get_directory_name(file.name)

    try:
        new_path.mkdir(exist_ok=True, parents=True)
        copyfile(file, new_path / normalized_file_name)
    except OSError as error:
        logging.error(error)

    return new_path / file.name


def unarchive_file(file: Path):
    unpack_archive(file, extract_dir=get_archive_directory(file))


def worker(path: Path):
    for file in path.iterdir():
        if file.is_file():
            new_file_path = copy_file(file, normalize_name(file.name))

            if is_file_archive(new_file_path.name):
                unarchive_file(new_file_path)


if __name__ == "__main__":
    source_path = Path(source)
    output_path = Path(output)

    folders = get_folders(source_path)
    threads = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(worker, folders)

    logging.info("Operation is finished")
