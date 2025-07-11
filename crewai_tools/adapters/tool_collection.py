from typing import List, Optional, Union, TypeVar, Generic, Dict
from crewai.tools import BaseTool

T = TypeVar('T', bound=BaseTool)

class ToolCollection(list, Generic[T]):
    """
    A collection of tools that can be accessed by index or name

    This class extends the built-in list to provide dictionary-like
    access to tools based on their name property.

    Usage:
        tools = ToolCollection(list_of_tools)
        # Access by index (regular list behavior)
        first_tool = tools[0]
        # Access by name (new functionality)
        search_tool = tools["search"]
    """

    def __init__(self, tools: Optional[List[T]] = None):
        super().__init__(tools or [])
        self._name_cache: Dict[str, T] = {}
        self._build_name_cache()

    def _build_name_cache(self) -> None:
        self._name_cache = {tool.name: tool for tool in self}

    def __getitem__(self, key: Union[int, str]) -> T:
        if isinstance(key, str):
            return self._name_cache[key]
        return super().__getitem__(key)

    def append(self, tool: T) -> None:
        super().append(tool)
        self._name_cache[tool.name] = tool

    def extend(self, tools: List[T]) -> None:
        super().extend(tools)
        self._build_name_cache()

    def insert(self, index: int, tool: T) -> None:
        super().insert(index, tool)
        self._name_cache[tool.name] = tool

    def remove(self, tool: T) -> None:
        super().remove(tool)
        if tool.name in self._name_cache:
            del self._name_cache[tool.name]

    def pop(self, index: int = -1) -> T:
        tool = super().pop(index)
        if tool.name in self._name_cache:
            del self._name_cache[tool.name]
        return tool

    def clear(self) -> None:
        super().clear()
        self._name_cache.clear()
