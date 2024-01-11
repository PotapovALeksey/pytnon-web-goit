from rich.console import Console as RichConsole
from rich.table import Table
from random import randint
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

import re

console = RichConsole()

table_colors = [
    "slate_blue1",
    "magenta",
    "chartreuse1",
    "sea_green1",
    "pale_turquoise1",
    "yellow2",
    "dark_sea_green3",
]
input_emojis = ["🤩", "😃", "😂", "🤑", "🤗", "😜", "🤠", "🥸", "🤡", "🥳", "😍"]


class Console:
    @staticmethod
    def print_error(error: Exception | str):
        error_text = str(error)

        try:
            result = re.findall(r"\[.*\]", error_text)

            if result is not None and len(result) > 0:
                updated_format = re.sub("[\[\]]", "", result[0])
                formatted_text = error_text.replace(
                    result[0], f"[bold deep_sky_blue1]{updated_format}[/]"
                )
                return console.print("🤯 ", formatted_text, style="red")
        except:
            return console.print("🤯 ", error_text, style="red")

        return console.print("🤯 ", error_text, style="red")

    @staticmethod
    def print_success(text: str):
        console.print("🥳 ", text, style="chartreuse1")

    @staticmethod
    def print_tip(text: str):
        console.print("🤓", text, style="wheat1")

    @staticmethod
    def input(text: str, prompts: [str] = [], placeholder=None):
        style = Style.from_dict(
            {
                "": "#afffff",
                "text": "#5f87ff",
            }
        )

        message = [
            ("class:emoji", f"{input_emojis[randint(0, len(input_emojis) - 1)]} "),
            ("class:text", f"{text}"),
        ]

        completer = WordCompleter(prompts)

        return prompt(
            message, completer=completer, style=style, placeholder=placeholder
        )

    @staticmethod
    def print(text: str, justify="left", **kwargs):
        console.print(text, justify=justify, **kwargs)

    @staticmethod
    def print_table(title: str, column_titles: [str], rows: []):
        if len(rows) == 0:
            console.print(
                "[i wheat1] There are no data by your request[/]", justify="center"
            )
            return console.print(
                "[i wheat1]The table is empty🤦‍♂️[/]", justify="center"
            )

        table = Table(title=f"[i]{title}[/]")

        for index, title in enumerate(column_titles):
            table.add_column(
                title,
                style=table_colors[index],
                justify="center",
                vertical="top",
                min_width=15,
            )

        for row in rows:
            table.add_row(*row)

        console.print(table, justify="center")
