import abc
from typing import Dict, Any

class BaseAnalyzer(abc.ABC):

    @property
    @abc.abstractmethod
    def system_prompt(self) -> str:
        pass

    @abc.abstractmethod
    def parse_response(self, raw_json: Dict[str, Any]) -> Dict[str, Any]:
        pass