from pathlib import Path


def get_sql_script(file: str):
    with open(Path("sql_scripts", file), "r") as f:
        return f.read()
