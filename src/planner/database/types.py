from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

SessionFactory = Callable[..., AbstractAsyncContextManager[AsyncSession]]
