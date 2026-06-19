from abc import ABC, abstractmethod

class DatabaseConnection(ABC):
    @classmethod
    @abstractmethod
    def connect(self):
        pass

    @classmethod
    @abstractmethod
    def close(self):
        pass