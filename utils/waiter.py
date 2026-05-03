import asyncio
from functools import wraps
from typing import Callable, Any


def async_sleep_after(seconds: float = 5) -> Callable:
    """
    Декоратор, який додає асинхронну паузу після виконання функції.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await func(*args, **kwargs)
            await asyncio.sleep(seconds)
            return result
        return wrapper
    return decorator
