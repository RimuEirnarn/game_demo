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
    headless = auto()
    transparent = auto()
    msaa_4x = auto()
    always_run = auto()

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

@contextmanager
def initialize(width: int, height: int, title: str, modules: tuple[ModuleFlag, ...]):
    window_flags: list[int] = []
    for module in modules:
        if module == ModuleFlag.audio:
            pr.init_audio_device()
            register(lambda: pr.close_audio_device)
        if module == ModuleFlag.headless:
            headless = pr.ConfigFlags.FLAG_WINDOW_UNDECORATED
            window_flags.append(headless)
        if module == ModuleFlag.transparent:
            transparent = pr.ConfigFlags.FLAG_WINDOW_TRANSPARENT
            window_flags.append(transparent)
        if module == ModuleFlag.msaa_4x:
            msaa_4x = pr.ConfigFlags.FLAG_MSAA_4X_HINT
            window_flags.append(msaa_4x)
        if module == ModuleFlag.always_run:
            always_run = pr.ConfigFlags.FLAG_WINDOW_ALWAYS_RUN
            window_flags.append(always_run)

    if len(window_flags) >= 1:
        flag = window_flags[0]
        for fx in window_flags[1:]:
            flag |= fx
        pr.set_config_flags(flag)
    pr.init_window(width, height, title)
    try:
        yield []
    finally:
        pr.close_window()
