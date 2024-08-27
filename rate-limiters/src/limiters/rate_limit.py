from abc import ABC, abstractmethod

class RateLimit(ABC):
    @abstractmethod
    def allow_request(self) -> bool:
        pass