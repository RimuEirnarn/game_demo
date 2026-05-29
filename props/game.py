# pylint: disable=no-member
"""Game instance"""
import pyray as pr

from props.audio import (
    AudioManager,
    MusicHandler
)
from props.runner import draw


class Game:
    """Game instance"""
    def __init__(self):
        self.soundmgr = AudioManager({
            "newpage": MusicHandler("external/NewPage.mp3", 1)
        })

    def load(self):
        """load"""
        self.soundmgr.load()

        bgm = self.soundmgr.get("newpage", MusicHandler)
        bgm.play()

    def update(self):
        """Update"""
        self.soundmgr.update()

    def draw(self):
        """Draw"""
        pr.clear_background(pr.BLACK)

        pr.draw_text(
            "Hello, Cyrene~",
            300,
            225,
            20,
            pr.LIGHTGRAY
        )

    def run(self):
        """Run"""
        try:
            while not pr.window_should_close():
                self.update()
                with draw():
                    self.draw()
        finally:
            self.unload()
            pr.close_window()

    def unload(self):
        """Unload"""
        self.soundmgr.unload()
