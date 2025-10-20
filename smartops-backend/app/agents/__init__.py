"""
Base Agent class and individual agent implementations.
Each agent has a clear interface with Pydantic I/O contracts.
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pydantic import BaseModel
import time

# Type variables for input/output
InputType = TypeVar('InputType', bound=BaseModel)
OutputType = TypeVar('OutputType', bound=BaseModel)


class BaseAgent(ABC, Generic[InputType, OutputType]):
    """
    Abstract base class for all agents.
    Enforces Pydantic I/O contracts and provides timing metrics.
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def process(self, input_data: InputType) -> OutputType:
        """
        Process input and return output.
        Must be implemented by subclasses.
        """
        pass
    
    def run(self, input_data: InputType) -> tuple[OutputType, float]:
        """
        Run the agent and track execution time.
        Returns (output, duration_ms)
        """
        start_time = time.time()
        output = self.process(input_data)
        duration_ms = (time.time() - start_time) * 1000
        return output, duration_ms
