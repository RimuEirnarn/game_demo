# pylint: disable=all
from typing import Callable, TypeVar
from contextlib import contextmanager
from functools import wraps
from enum import IntEnum, auto
from atexit import register
import pyray as pr

TCallable = TypeVar("TCallable")
class ModuleFlag(IntEnum):
    audio = auto()
    physics = auto()

@contextmanager
def draw():
    try:
        yield pr.begin_drawing()
    finally:
        pr.end_drawing()

def mainloop(fn: Callable[[], None]):
    while not pr.window_should_close():
        with draw():
            fn()
    pr.close_window()

def setup(width: int, height: int, title: str, modules: tuple[ModuleFlag]):
    """Setup Raylib window"""
    def inner(fn: Callable[[], None]):
        for module in modules:
            if module == ModuleFlag.audio:
                pr.init_audio_device()
                register(lambda: pr.close_audio_device)
            if module == ModuleFlag.physics:
                pr.init_physics()
        pr.init_window(width, height, title)
        return fn
    return inner

@contextmanager
def initialize(width: int, height: int, title: str, modules: tuple[ModuleFlag]):
    for module in modules:
        if module == ModuleFlag.audio:
            pr.init_audio_device()
            register(lambda: pr.close_audio_device)
    pr.init_window(width, height, title)
    try:
        yield []
    finally:
        pass
