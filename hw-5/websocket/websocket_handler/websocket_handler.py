from abc import ABC, abstractmethod


class WebsocketHandler(ABC):
    @property
    @abstractmethod
    def name(self):
        ...

    @abstractmethod
    async def handle(self, *args, **kwargs):
        ...
