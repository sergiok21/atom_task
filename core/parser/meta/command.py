from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """Abstract base class for the Command pattern implementation."""

    @abstractmethod
    def execute(self):
        """Executes the specific logic encapsulated within the command."""
        pass