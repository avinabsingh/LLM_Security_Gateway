from abc import ABC, abstractmethod


class BaseAdapter(ABC):

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def convert(self):
        pass

    @abstractmethod
    def save(self):
        pass