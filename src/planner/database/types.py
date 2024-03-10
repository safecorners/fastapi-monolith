from typing import Callable
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session

SessionFactory = Callable[..., AbstractContextManager[Session]]
