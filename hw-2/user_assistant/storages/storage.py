from abc import ABC, abstractmethod
from user_assistant.serializers.serializer import Serializer


class Storage(ABC):
    @abstractmethod
    def __init__(self, path: str, serializer: Serializer):
        pass

    @abstractmethod
    def get(self):
        return []

    @abstractmethod
    def update(self, records: []):
        pass
