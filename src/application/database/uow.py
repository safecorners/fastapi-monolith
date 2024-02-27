from __future__ import annotations

import abc
from typing import ContextManager, Iterable, Optional, TracebackType, Type


class AbstractUnitOfWork(ContextManager[AbstractUnitOfWork], metaclass=abc.ABCMeta):
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.rollback()

    def commit(self) -> None:
        self._commit()

    def collect_new_events(self) -> Iterable[...]:
        raise NotImplementedError

    @abc.abstractmethod
    def _commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
