from user_assistant.console.console import Console
from user_assistant.handlers.abstract_handler import AbstractHandler


class ExitHandler(AbstractHandler):
    def execute(self):
        Console.print(":waving_hand:[plum3] Good luck. Hope we will see you soon[/]")
