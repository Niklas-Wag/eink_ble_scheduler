from abc import ABC, abstractmethod

class BaseJob(ABC):
    def __init__(self, device_name):
        self.device_name = device_name

    @abstractmethod
    def execute(self):
        pass