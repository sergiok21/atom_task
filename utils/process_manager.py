from typing import Callable, Dict, Any

from asgiref.sync import sync_to_async

from core.parser.base import BaseCommand


async def execute_commands(pipeline: dict[str, BaseCommand]) -> dict[str, str | int]:
    result_data = {}
    for key, command in pipeline.items():
        result_data[key] = await command.execute()
    return result_data


async def sync_to_async_func(func: Callable, **fields: Dict[str, Any]) -> Any:
    return await sync_to_async(func)(**fields)
