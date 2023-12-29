from user_assistant.console.console import Console
from user_assistant.handlers.abstract_handler import AbstractHandler


class GreetingHandler(AbstractHandler):
    def execute(self):
        Console.print(
            '[cornflower_blue]Welcome dear friend in [bold deep_sky_blue1]User assistant[/] application![/]:red_heart-emoji:', 'center')
        Console.print('[dark_olive_green1]You will be amazed using it [/]:fire:', 'center')
        Console.print('[dark_olive_green1]We have prepared detail documentation of your assistant[/]:scroll:', 'center')
        Console.print('[dark_olive_green1]Just enter [bold deep_sky_blue1]help[/] to see all possible commands[/]:scroll:', 'center')
        Console.print(
            '[dark_olive_green1]We wish you good luck on your way [/]:money_bag::crown::party_popper:', 'center')