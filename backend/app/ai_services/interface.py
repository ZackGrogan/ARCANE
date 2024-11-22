from ..ai_services.interface import AIServiceInterface
from .. import logging

logger = logging.getLogger(__name__)

class AIServiceError(Exception):
    pass

# class AIServiceInterface(ABC):
#
#     @abstractmethod
#     def generate_name(self, prompt: str) -> str:
#         pass
#
#     @abstractmethod
#     def generate_backstory(self, prompt: str) -> str:
#         pass
#
#     @abstractmethod
#     def generate_profile_picture(self, prompt: str) -> str:
#         pass
#
#     def handle_error(self, error):
#         logger.error(f"AI Service error: {error}")
#         raise AIServiceError("An error occurred while processing your request.")
