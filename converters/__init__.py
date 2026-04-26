from typing import Callable
from converters import temperature

REGISTRY: dict[str, Callable] = {}


def register(name: str, handler: Callable) -> None:
    REGISTRY[name] = handler


register("Temperature", temperature.run)
