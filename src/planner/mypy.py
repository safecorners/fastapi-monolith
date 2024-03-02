"""
mypy plugin for dynamic attrs.

see :
https://github.com/python/mypy/blob/master/mypy/plugin.py
https://github.com/pydantic/pydantic/blob/main/pydantic/mypy.py
https://github.com/dry-python/returns/tree/master/returns/contrib/mypy

"""
from typing import Callable, Optional, Type

from mypy.plugin import (
    AnalyzeTypeContext,
    AttributeContext,
    FunctionContext,
    MethodContext,
    Plugin,
)
from mypy.types import Type as MypyType

FQN = "fastapi.applications.FastAPI"


class FastAPIPlugin(Plugin):
    def get_type_analyze_hook(
        self, fullname: str
    ) -> Optional[Callable[[AnalyzeTypeContext], MypyType]]:
        return None

    def get_function_hook(
        self, fullname: str
    ) -> Optional[Callable[[FunctionContext], MypyType]]:
        return None

    def get_method_hook(
        self, fullname: str
    ) -> Optional[Callable[[MethodContext], MypyType]]:
        print(f"fullname={fullname}")
        return None

    def get_attribute_hook(
        self, fullname: str
    ) -> Optional[Callable[[AttributeContext], MypyType]]:
        return None

    def get_class_attribute_hook(
        self, fullname: str
    ) -> Optional[Callable[[AttributeContext], MypyType]]:
        return None


def plugin(version: str) -> Type[Plugin]:
    return FastAPIPlugin
